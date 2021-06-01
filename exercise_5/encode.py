import json
import pickle


s= "string here"
print(s.encode())

a = ["test",5]

#k = json.dumps(a, sort_keys=True, indent=4)
#k = json.dumps(a)
#k= k.encode()
k = pickle.dumps(a)


print(k, type(k))
print(a, type(a))

