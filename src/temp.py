#-*-coding:utf-8-*-

'''
Created on 2013-5-18

@author: chenko
'''

from __future__ import print_function
import cPickle as pickle
import shelve
from contextlib import closing


with closing(shelve.open('./friends.db')) as s:
    circle = {}
    circle[12345] = {
        "friends": set([]),
        "name": "王琛",
        "network_class": "城市",
        "network": "上海市",
        "hop": 0,
    }
    s["circle"] = pickle.dumps(circle)

with closing(shelve.open('./friends.db')) as s:
    circle = pickle.loads(s["circle"])
    for friend in circle:
        print(friend, end=' ')
        print (circle[friend]["name"], end=' ')
        print (circle[friend]["network_class"], end=' ')
        print (circle[friend]["network"], end=' ')
        print (circle[friend]["hop"], end=' ')
        print (circle[friend]["friends"])
