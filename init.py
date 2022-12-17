import os
import json

userID = input("AtCoder userID: ")

with open("./config.json", "w") as f:
    json.dump({"userID": userID}, f)
