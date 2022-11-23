import os
import json

try:
    os.mkdir("./result")
except:
    pass

userID = input("AtCoder userID: ")
driver_path = input("Chromium path: ")

with open("./config.json", "w") as f:
    json.dump({"userID": userID, "driver_path": driver_path}, f)
