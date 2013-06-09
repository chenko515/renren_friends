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
            "network": "上海市",
            "hop": 0,
        }

    def start_crawl(self):
        for cur_hop in range(0, self.depths):
            for friend in self.circle:
                if(self.circle[friend]["hop"] == cur_hop):
                    parent = Friends(friend)
                    buffer_circle = parent.parse_friends(cur_hop)
                    self.circle.update(buffer_circle)
                    parent.store_friends(cur_hop)
            else:
                cur_hop += 1
        else:
            print("Crawling finished")
            return


class Friends():
    '''User's friends and their relationship
    '''

    def __init__(self, core_uid):
        self.core_uid = core_uid
        self.curpage = 0
        self.url = (
            "http://friend.renren.com/GetFriendList.do?"
            "curpage={0}&id={1}").format(self.curpage, self.core_uid)

    def friend_pages(self):
        '''Count friend pages
        '''
        self.url.format(self.curpage, self.core_uid)

        http_request = Request(self.url)
        rsp_src = http_request.get_response()
        soup = BeautifulSoup(rsp_src)
        text = str(soup.findAll("a", attrs={"title": "最后页"}))
        pattern = "curpage=[0-9]+"
        r = re.search(pattern, text)
        result = int(text[r.start() + 8: r.end()])
        return result

    def parse_friends(self, cur_hop):
        '''Parse the friend list page and get the friends info
        '''
        buffer_circle = {}
        pages = self.friend_pages()
#         pages = 0  # For debug

        for self.curpage in range(0, pages + 1):
            self.url = ("http://friend.renren.com/GetFriendList.do?"
                        "curpage={0}&id={1}")\
                        .format(self.curpage, self.core_uid)
            http_request = Request(self.url)
            rsp_src = http_request.get_response()
#             print(rsp_src)  # For debug
#             with open("./page.html", "wb") as f:
#                 f.write(rsp_src)

            soup = BeautifulSoup(rsp_src)
            friends_list_divs = soup.findAll("div", attrs={"class": "info"})

            for dl in friends_list_divs:
                # Fetch uid as int type
                uid = int(dl.dd.a["href"][36:])
                # Add new friend to my circle
                if(uid not in crawl.circle):
                    # Being string rather than NavigableString, shelve later
                    name = str(dl.dd.a.string)
                    network_class = str(dl.findAll("dt")[1].string)
                    network_name = str(dl.findAll("dd")[1].string)
                    userinfo = {
                        "friends": set([]),
                        "name": name,
                        "network_class": network_class,
                        "network_name": network_name,
                        "hop": cur_hop,
                    }
                    buffer_circle[uid] = userinfo
                    # Update relationship
                    # Add parent
                    buffer_circle[uid]["friends"].add(self.core_uid)
                    # Add child
                    crawl.circle[self.core_uid]["friends"].add(uid)

                    #!!! For Debug
                    for i in buffer_circle[uid]:
                        print (buffer_circle[uid][i])
                    print()

        return buffer_circle

    def store_friends(self, children, cur_hop):
        '''Store friends via shelve and pickle
        '''

        with closing(shelve.open('./circle.db', writeback=True)) as s:
            s["circle"] = pickle.dumps(crawl.circle)

        #!!! For Debug
        with closing(shelve.open('./circle.db')) as s:
            tmp = s["circle"]
            print (pickle.loads(tmp), end='')

#**************************************************************


# Run as main module
if __name__ == '__main__':
    crawl = Crawl("247631683", 1)
    crawl.start_crawl()
