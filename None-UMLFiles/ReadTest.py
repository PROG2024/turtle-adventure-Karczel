# Python program to read
# json file

import json

# Opening JSON file
f = open('../Level.json')

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
for i in data: #iterating through dict, ti get data use data[i]
    print(i, end=" : \n") # i == levels
    for j in data[i]: #iterating through list
        for k in j: # j is 1 element in list
            print(k, end=': ') #'Enemy'
            print(j[k]) # info at ; level['Enemy']
        print()
    print()

# Closing file
f.close()