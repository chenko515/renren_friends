
try:
    import cPickle as pickle
except:
    import pickle


_list1 = [1, 2, 3]
_dict1 = {"a": 4, "b": 5, "c": 6}

t1 = pickle.dumps(_list1)
t2 = pickle.dumps(_dict1)

print(t1)
print(t2)

_list2 = pickle.loads(t1)
_dict2 = pickle.loads(t2)
_dict2["d"] = 4


print(_list2)
print(_dict2)
