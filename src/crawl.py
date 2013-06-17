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
import copy

from request import Request


error_log = r"./error.log"


class Crawl():
    '''Crawl the friends circle
    '''
    circle = {}
    buffer_circle = {}

    def __init__(self, root_uid, hops):
        '''Initialize the root_uid
        '''
        self.depths = hops
        # start from hop0, 6 hops at most
        self.root_uid = root_uid
        userinfo = {
            "friends": set([]),
            "name": "王琛",
            "network_class": "城市",
            "network_name": "上海市",
            "hop": 0,
        }
        self.circle[self.root_uid] = userinfo
        with closing(shelve.open('./circle.db', writeback=True)) as s:
            s[str(self.root_uid)] = userinfo

    def start_crawl(self):
        '''Start to crawl from the root_uid
        '''
        for cur_hop in range(0, self.depths):
            buffer_circle = copy.deepcopy(self.circle)
            for friend in self.circle:
                if(self.circle[friend]["hop"] == cur_hop):
                    parent = Friends(friend)
                    parent.parse_friends(cur_hop, buffer_circle)
            else:
                self.circle = buffer_circle
        else:
            print("Crawling finished")


class Friends():
    '''User's friends and their relationship
    '''
    @staticmethod
    def store_friends():
        '''Store friends via shelve and pickle
        '''
        with closing(shelve.open('./circle.db', writeback=True)) as s:
            s["circle"] = pickle.dumps(crawl.circle)

    def __init__(self, core_uid):
        '''Initialize the self.url
        '''
        self.core_uid = core_uid
        self.curpage = 0
        self.url = (
            "http://friend.renren.com/GetFriendList.do?"
            "curpage={0}&id={1}").format(self.curpage, self.core_uid)

    def friend_pages(self):
        '''Get friend's total page numbers
        '''
        self.url.format(self.curpage, self.core_uid)
        http_request = Request(self.url)
        rsp_src = http_request.get_response()
        # Empty rsp_src will raise parse error
        try:
            assert rsp_src
        except AssertionError:
            print("except AssertionError, "
                  "http_request.get_response() failed and return nothing, "
                  "Check your network and cookie, ",
                  file=error_log)
            return
        # Parse the page and get friend's total page numbers
        soup = BeautifulSoup(rsp_src)
        text = str(soup.findAll("a", attrs={"title": unicode("最后页", "utf-8")}))
        pattern = "curpage=[0-9]+"
        r = re.search(pattern, text)
        #
        try:
            result = int(text[r.start() + 8: r.end()])
        except AttributeError:
            with open(r"./error.log", 'a+') as error_log:
                print("except AttributeError, re.search fail:", file=error_log)
                print("soup: ", soup, file=error_log)
                print("pattern: ", pattern, file=error_log)
                print("text: ", text, file=error_log)
                print("r: ", r, '\n', file=error_log)
                return
        return result

    def parse_friends(self, cur_hop, buffer_circle):
        '''Parse the friend list page and get the friends info
        '''
        pages = self.friend_pages()
        # If pages is empty, skip the parse
        pages = [pages, 0][pages == None]
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
                # Being string rather than NavigableString, shelve later
                name = str(dl.dd.a.string)
                network_class = str(dl.findAll("dt")[1].string)
                network_name = str(dl.findAll("dd")[1].string)
                userinfo = {}
                userinfo["name"] = name
                userinfo["network_class"] = network_class
                userinfo["network_name"] = network_name

                if uid not in buffer_circle:
                    userinfo["friends"] = set([])
                    userinfo["hop"] = cur_hop + 1
                else:
                    userinfo["friends"] = buffer_circle[uid]["friends"]
                    userinfo["hop"] = buffer_circle[uid]["hop"]

                buffer_circle[uid] = userinfo
                # Add child to parent
                buffer_circle[self.core_uid]["friends"].add(uid)
                # Add parent to child
                buffer_circle[uid]["friends"].add(self.core_uid)

                with closing(shelve.open('./circle.db', writeback=True)) as s:
                    s[str(uid)] = pickle.dumps(userinfo)

                #!!! For Debug
                print(self.core_uid, end=',')
                print(uid, end=',')
                print(buffer_circle[uid]["name"], end=',')
                print(buffer_circle[uid]["network_class"], end=',')
                print(buffer_circle[uid]["network_name"], end=',')
                print(buffer_circle[uid]["hop"], end=',')
                print(buffer_circle[uid]["friends"].__sizeof__())


#**************************************************************


# Run as main module
if __name__ == '__main__':
    crawl = Crawl("247631683", 2)  # Start from chenko, recursion depth = 2
    crawl.start_crawl()
