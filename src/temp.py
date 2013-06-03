#-*-coding:utf-8-*-

'''
Created on 2013-5-18

@author: chenko
'''

import cPickle as pickle
import shelve
from contextlib import closing    


with closing(shelve.open('./friends.db')) as s:
    _list1 = [1, 2, 3]
    _dict1 = {"a": 4, "b": 5, "c": 6}     
    t1 = pickle.dumps(_list1)
    t2 = pickle.dumps(_dict1)    
    s['t1'] = t1
    s['t2'] = t2

with closing(shelve.open('./friends.db')) as s:
    t11 = s['t1']
    t22 = s['t2']

print(pickle.loads(t11))
print(pickle.loads(t22))

#     print(t1)
#     print(t2)
     
#     _list2 = pickle.loads(t1)
#     _dict2 = pickle.loads(t2)
#     _dict2["d"] = 4
      
#     print(_list2)
#     print(_dict2)
