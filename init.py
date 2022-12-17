import os
import json

try:
    os.mkdir("./result")
except:
    pass

userID = input("AtCoder userID: ")

with open("./config.json", "w") as f:
    json.dump({"userID": userID}, f)
