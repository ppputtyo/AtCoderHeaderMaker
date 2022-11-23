from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service
import base64
import json
import time
import os
import shutil
from PIL import Image

config = None
with open("./config.json", "r") as f:
    config = json.load(f)

if(config == None):
    print("config.json is not found.")


chrome_driver = config["driver_path"]
chrome_service = service.Service(executable_path=chrome_driver)
browser = webdriver.Chrome(service=chrome_service)

userID = config["userID"]
algoURL = f"https://atcoder.jp/users/{userID}?contestType=algo"
heuristicURL = f"https://atcoder.jp/users/{userID}?contestType=heuristic"


def get_canvas(id, out):
    global browser
    canvas_first = browser.find_element(by=By.ID, value=id)
    dataURLs = browser.execute_script("return arguments[0].toDataURL('image/png').substring(21);",
                                      canvas_first)
    first_png = base64.b64decode(dataURLs)

    # デコードしたデータを保存する
    with open(out, 'wb') as f:
        f.write(first_png)


try:
    os.mkdir("./tmp")
except:
    pass


browser.get(algoURL)
time.sleep(3)

get_canvas("ratingStatus", "./tmp/1.png")
get_canvas("ratingGraph", "./tmp/2.png")

browser.get(heuristicURL)
time.sleep(3)


get_canvas("ratingStatus", "./tmp/3.png")
get_canvas("ratingGraph", "./tmp/4.png")


def get_concat_h(im1, im2):
    dst = Image.new('RGBA', (im1.width + im2.width,
                             im1.height), (255, 255, 255))
    dst.paste(im1, (0, 0), im1)
    dst.paste(im2, (im1.width, 0), im2)
    return dst


def get_concat_v(im1, im2):
    dst = Image.new('RGBA', (im1.width, im1.height +
                             im2.height), (255, 255, 255))
    dst.paste(im1, (0, 0), im1)
    dst.paste(im2, (0, im1.height), im2)
    return dst


img1 = Image.open("./tmp/1.png")
img2 = Image.open("./tmp/2.png")
img3 = Image.open("./tmp/3.png")
img4 = Image.open("./tmp/4.png")

algo = get_concat_v(img1, img2)
heu = get_concat_v(img3, img4)
res = get_concat_h(algo, heu)
res.save("result/result.png")

shutil.rmtree("./tmp")
browser.quit()
