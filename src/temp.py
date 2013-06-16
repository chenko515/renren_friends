#-*-coding:utf-8-*-

'''
Created on 2013-5-18

@author: chenko
'''

from __future__ import print_function
import cPickle as pickle
import shelve
from contextlib import closing


with closing(shelve.open('./circle.db')) as s:
    circle = pickle.loads(s["circle"])
    print(circle.keys())

    circle = pickle.loads(s["hop_circle"])
    print(circle.keys())
#     for friend in circle:
#         print(friend, end=',')
#         print(circle[friend]["name"], end=',')
#         print(circle[friend]["network_class"], end=',')
#         print(circle[friend]["network_name"], end=',')
#         print(circle[friend]["hop"], end=',')
#         print(circle[friend]["friends"])
