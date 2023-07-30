from selenium import webdriver
from selenium.webdriver.common.by import By
from get_chrome_driver import GetChromeDriver
import base64
import json
import time
import os
import shutil
import sys
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--userID", help="AtCoder userID")

userID = parser.parse_args().userID

# load confing.json
# config = None
# try:
#     with open("./config.json", "r") as f:
#         config = json.load(f)
# except:
#     print("Not found error: config.json", file=sys.stderr)
#     exit(1)

get_driver = GetChromeDriver()
get_driver.install()


def driver_init():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    return webdriver.Chrome(options=options)


browser = driver_init()

# userID = config["userID"]
algoURL = f"https://atcoder.jp/users/{userID}?contestType=algo&lang=ja"
heuristicURL = f"https://atcoder.jp/users/{userID}?contestType=heuristic&lang=ja"


# canvas要素を画像に変換
def get_canvas(id, out):
    global browser
    try:
        canvas_first = browser.find_element(by=By.ID, value=id)
    except:
        print("Invalid username", file=sys.stderr)
        browser.quit()
        exit(1)

    dataURLs = browser.execute_script(
        "return arguments[0].toDataURL('image/png').substring(21);", canvas_first
    )
    first_png = base64.b64decode(dataURLs)

    # デコードしたデータを保存する
    with open(out, "wb") as f:
        f.write(first_png)


# tmpフォルダ作成
try:
    os.mkdir("./tmp")
except:
    pass

# アルゴのstatusとgraphを取得
browser.get(algoURL)
time.sleep(2)

get_canvas("ratingStatus", "./tmp/1.png")
get_canvas("ratingGraph", "./tmp/2.png")

# ヒューのstatusとgraphを取得
browser.get(heuristicURL)
time.sleep(2)

get_canvas("ratingStatus", "./tmp/3.png")
get_canvas("ratingGraph", "./tmp/4.png")


# 横に繋げる
# この時に比率を height:width = 1:3 にする
def get_concat_h(im1, im2):
    dst = None
    if im1.height * 3 < im1.width * 2:
        # 縦の余白あり
        height = int(im1.width * 2 / 3)
        dst = Image.new("RGBA", (im1.width * 2, height), (255, 255, 255))
        dst.paste(im1, (0, int((height - im1.height) / 2)), im1)
        dst.paste(im2, (im1.width, int((height - im1.height) / 2)), im2)
    else:
        # 横の余白あり
        width = im1.height * 3
        dst = Image.new("RGBA", (width, im1.height), (255, 255, 255))
        dst.paste(im1, (int((width / 2 - im1.width) / 2), 0), im1)
        dst.paste(im2, (width - (int((width / 2 - im1.width) / 2) + im1.width), 0), im2)
    return dst


# 縦に繋げる
def get_concat_v(im1, im2):
    dst = Image.new("RGBA", (im1.width, im1.height + im2.height), (255, 255, 255))
    dst.paste(im1, (0, 0), im1)
    dst.paste(im2, (0, im1.height), im2)
    return dst


# 表の外側を切り取る
def clip_left(img):
    res = img.crop((int(img.width * 0.064), 0, img.width, img.height))
    return res


def clip_under(img):
    res = img.crop((0, 0, img.width, int(img.height * 0.923)))
    return res


algo_status = Image.open("./tmp/1.png")
algo_graph = Image.open("./tmp/2.png")
heu_status = Image.open("./tmp/3.png")
heu_graph = Image.open("./tmp/4.png")

algo = get_concat_v(algo_status, algo_graph)
clip_algo_status = clip_left(algo_status)
clip_algo_graph = clip_left(clip_under(algo_graph))
clip_algo = get_concat_v(clip_algo_status, clip_algo_graph)

heu = get_concat_v(heu_status, heu_graph)
clip_heu_status = clip_left(heu_status)
clip_heu_graph = clip_left(clip_under(heu_graph))
clip_heu = get_concat_v(clip_heu_status, clip_heu_graph)


try:
    os.mkdir("./result")
except:
    pass

get_concat_h(algo, heu).save("result/status_graph.png")
get_concat_h(clip_algo, clip_heu).save("result/status_graph_clip.png")
get_concat_h(algo_graph, heu_graph).save("result/graph.png")
get_concat_h(clip_algo_graph, clip_heu_graph).save("result/graph_clip.png")

shutil.rmtree("./tmp")
browser.quit()
