from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service
import base64
import json
import time
import os
import shutil
import sys
from PIL import Image

config = None
try:
    with open("./config.json", "r") as f:
        config = json.load(f)
except:
    print("Error: Run init.py first", file=sys.stderr)
    exit(1)


chrome_driver = config["driver_path"]
chrome_service = service.Service(executable_path=chrome_driver)
browser = webdriver.Chrome(service=chrome_service)

userID = config["userID"]
algoURL = f"https://atcoder.jp/users/{userID}?contestType=algo"
heuristicURL = f"https://atcoder.jp/users/{userID}?contestType=heuristic"


# canvas要素を画像に変換
def get_canvas(id, out):
    global browser
    canvas_first = browser.find_element(by=By.ID, value=id)
    dataURLs = browser.execute_script("return arguments[0].toDataURL('image/png').substring(21);",
                                      canvas_first)
    first_png = base64.b64decode(dataURLs)

    # デコードしたデータを保存する
    with open(out, 'wb') as f:
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
    if(im1.height * 3 < im1.width * 2):
        # 縦の余白あり
        height = int(im1.width * 2 / 3)
        dst = Image.new('RGBA', (im1.width * 2, height), (255, 255, 255))
        dst.paste(im1, (0, int((height-im1.height)/2)), im1)
        dst.paste(im2, (im1.width, int((height-im1.height)/2)), im2)
    else:
        # 横の余白あり
        width = im1.height*3
        dst = Image.new('RGBA', (width, im1.height), (255, 255, 255))
        dst.paste(im1, (int((width/2 - im1.width)/2), 0), im1)
        dst.paste(im2, (im1.width + int((width/2 - im1.width)/2), 0), im2)
    return dst


# 縦に繋げる
def get_concat_v(im1, im2):
    dst = Image.new('RGBA', (im1.width, im1.height +
                             im2.height), (255, 255, 255))
    dst.paste(im1, (0, 0), im1)
    dst.paste(im2, (0, im1.height), im2)
    return dst


# 表の外側を切り取る
def clip_image(img):
    res = img.crop((82, 0, img.width, img.height-55))
    return res


algo_status = Image.open("./tmp/1.png")
algo_graph = Image.open("./tmp/2.png")
heu_status = Image.open("./tmp/3.png")
heu_graph = Image.open("./tmp/4.png")

# statusアリ
algo = get_concat_v(algo_status, algo_graph)
heu = get_concat_v(heu_status, heu_graph)
res = get_concat_h(algo, heu)
res.save("result/status_graph.png")
res_clip = get_concat_h(clip_image(algo), clip_image(heu))
res_clip.save("result/status_graph_clip.png")


# statusナシ
algo = algo_graph
heu = heu_graph
res = get_concat_h(algo, heu)
res.save("result/graph.png")
res_clip = get_concat_h(clip_image(algo), clip_image(heu))
res_clip.save("result/graph_clip.png")


shutil.rmtree("./tmp")
browser.quit()
