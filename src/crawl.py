#-*-coding:utf-8-*-

'''
Created on 2013-5-18

@author: chenko
'''


import re
import cPickle as pickle
from BeautifulSoup import BeautifulSoup

from request import Request


class Crawl():
    '''Crawl friends
    '''
    def __init__(self, core_uid):
        self.core_uid = core_uid
        self.uid = "259219190"
        self.curpage = 0
        self.url = ("http://friend.renren.com/GetFriendList.do?"
                    "curpage={0}&id={1}")\
                    .format(self.curpage, self.uid)

    def friend_pages(self):
        '''Count friend pages
        '''
        self.url.format(self.curpage, self.uid)

        http_request = Request(self.url)
        rsp_src = http_request.get_response()
        soup = BeautifulSoup(rsp_src)
        text = str(soup.findAll("a", attrs={"title": "最后页"}))  # str()
        pattern = "curpage=[0-9]+"
        r = re.search(pattern, text)
        result = int(text[r.start() + 8: r.end()])
        return result

    def parse_friend(self):
        '''Parse the friend list page and get the friends info
        '''

        friends = Friends(self.core_uid)
        pages = self.friend_pages()
#         pages = 0  # For debug

        for self.curpage in range(0, pages + 1):
            self.url = ("http://friend.renren.com/GetFriendList.do?"
                        "curpage={0}&id={1}")\
                        .format(self.curpage, self.uid)
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
                # Being string rather than NavigableString, shelve later
                name = str(dl.dd.a.string)
                network_class = str(dl.findAll("dt")[1].string)
                network_name = str(dl.findAll("dd")[1].string)
                userinfo = {"name": name,
                            "network_class": network_class,
                            "network_name": network_name,
                            }
                friends.dict[uid] = userinfo
#                 # for debug
#                 print userinfo["name"], userinfo["network_class"], userinfo["network_name"]
        else:
            pass


class Friends():
    '''User's friends and their relationship
    '''
    dict = {}

    def __init__(self, root_uid):
        self.root_uid = root_uid


class Store():
    '''Store friends via shelve and pickle
    '''
    
    
    
#**************************************************************


# Run as main module
if __name__ == '__main__':
    crawl = Crawl("259219190")
    crawl.parse_friend()
