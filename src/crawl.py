#-*-coding:utf-8-*-

'''
Created on 2013-5-18

@author: chenko
'''

from __future__ import print_function
from contextlib import closing
from BeautifulSoup import BeautifulSoup
import re
import cPickle as pickle
import shelve

from request import Request


error_log = r"./error.log"


class Crawl():
    '''Crawl the friends circle
    '''
    circle = {}

    def __init__(self, root_uid, hops):
        self.depths = hops
        # start from hop0, 6 hops at most
        self.root_uid = root_uid
        self.circle[self.root_uid] = {
            "friends": set([]),
            "name": "王琛",
            "network_class": "城市",
            "network_name": "上海市",
            "hop": 0,
        }

    def start_crawl(self):
        for cur_hop in range(0, self.depths):
            hop_circle = {}
            for friend in self.circle:
                if(self.circle[friend]["hop"] == cur_hop):
                    parent = Friends(friend)
                    parent_circle = parent.parse_friends(cur_hop)
                    hop_circle.update(parent_circle)
            else:
                self.circle.update(hop_circle)
                Friends.store_friends()
        else:
#            Friends.print_friends()  #!!! For Debug
            print("Crawling finished")


class Friends():
    '''User's friends and their relationship
    '''
    def __init__(self, core_uid):
        self.core_uid = core_uid
        self.curpage = 0
        self.url = (
            "http://friend.renren.com/GetFriendList.do?"
            "curpage={0}&id={1}").format(self.curpage, self.core_uid)

    @staticmethod
    def store_friends():
        '''Store friends via shelve and pickle
        '''
        with closing(shelve.open('./circle.db', writeback=True)) as s:
            s["circle"] = pickle.dumps(crawl.circle)

    #!!! For Debug
    @staticmethod
    def print_friends():
        '''Print friends via shelve and pickle
        '''
        with closing(shelve.open('./circle.db')) as s:
            circle = pickle.loads(s["circle"])
            for friend in circle:
                print(friend, end=',')
                print (circle[friend]["name"], end=',')
                print (circle[friend]["network_class"], end=',')
                print (circle[friend]["network_name"], end=',')
                print (circle[friend]["hop"], end=',')
                print (circle[friend]["friends"])

    def friend_pages(self):
        '''Count friend pages
        '''
        self.url.format(self.curpage, self.core_uid)
        http_request = Request(self.url)
        rsp_src = http_request.get_response()
        if not rsp_src:
            raise Error()
        
            print("http_request.get_response() failed and return nothing",
                  file=error_log)
            print("Fail to get the friend's total page numbers, "
                  "Check your network and cookie, "
                  "See 'error.log' for more details")
        soup = BeautifulSoup(rsp_src)
        text = str(soup.findAll("a", attrs={"title": unicode("最后页", "utf-8")}))
        pattern = "curpage=[0-9]+"
        r = re.search(pattern, text)
        try:
            result = int(text[r.start() + 8: r.end()])
        except AttributeError as e:
#!!! Error
            print (r, pattern, text, "re.search fail")
            return
        return result

    def parse_friends(self, cur_hop):
        '''Parse the friend list page and get the friends info
        '''
        parent_circle = {}
        pages = self.friend_pages()
        if not pages:
            return
        for self.curpage in range(0, pages + 1):
            self.url = ("http://friend.renren.com/GetFriendList.do?"
                        "curpage={0}&id={1}"\
                        .format(self.curpage, self.core_uid))
            http_request = Request(self.url)
            rsp_src = http_request.get_response()

# !!!         For debug
#             print(rsp_src)
#             with open("./page.html", "wb") as f:
#                 f.write(rsp_src)

            soup = BeautifulSoup(rsp_src)
            friends_list_divs = soup.findAll("div", attrs={"class": "info"})

            for dl in friends_list_divs:
                # Fetch uid as int type
                uid = int(dl.dd.a["href"][36:])
                # Add new friend to my circle
                if uid not in crawl.circle:
                    # Being string rather than NavigableString, shelve later
                    name = str(dl.dd.a.string)
                    network_class = str(dl.findAll("dt")[1].string)
                    network_name = str(dl.findAll("dd")[1].string)
                    userinfo = {
                        "friends": set([]),
                        "name": name,
                        "network_class": network_class,
                        "network_name": network_name,
                        "hop": cur_hop + 1,
                    }
                    parent_circle[uid] = userinfo
                    # Update relationship
                    # Add parent
                    parent_circle[uid]["friends"].add(self.core_uid)
                    # Add child
                    crawl.circle[self.core_uid]["friends"].add(uid)

                    #!!! For Debug
                    print (self.core_uid, end=',')
                    print (uid, end=',')
                    print (parent_circle[uid]["name"], end=',')
                    print (parent_circle[uid]["network_class"], end=',')
                    print (parent_circle[uid]["network_name"], end=',')
                    print (parent_circle[uid]["hop"], end=',')
                    print (parent_circle[uid]["friends"].__sizeof__())

        return parent_circle


#**************************************************************


# Run as main module
if __name__ == '__main__':
    crawl = Crawl("247631683", 2)
    crawl.start_crawl()
