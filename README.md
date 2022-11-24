# AtCoderHeaderMaker

以下のような Twitter のヘッダー画像を自動で作れます

<img src="https://user-images.githubusercontent.com/52311998/203693576-80f6c6c5-201d-4373-8f9b-f2caa591c842.png" width=400><img src="https://user-images.githubusercontent.com/52311998/203693581-0192eabe-81a9-4d26-81b3-e9e9f5547b84.png" width=400>
<img src="https://user-images.githubusercontent.com/52311998/203693583-d6ce0ac7-dc3d-4946-a9b8-484cd842ab17.png" width=400><img src="https://user-images.githubusercontent.com/52311998/203693586-0870b0d5-6a80-43bc-9160-22398a2f9bc9.png" width=400>


# 使い方

## selenium のインストール

1. `pip3 install selenium`

## chromedriver のインストール

1. Google Chrome を開き、「ヘルプ > Google Chrome について」からバージョンを確認します
   <img width="370" alt="スクリーンショット 2022-11-24 13 28 05" src="https://user-images.githubusercontent.com/52311998/203694538-8c6fe681-e6b2-4114-a39b-339719c38751.png">

   <img width="355" alt="スクリーンショット 2022-11-24 13 31 05" src="https://user-images.githubusercontent.com/52311998/203694751-0f25bedb-1407-488b-ab9a-e9dce8cb8191.png">

2. [Google Chrome のバージョンに合った chromedriver をダウンロード](https://chromedriver.chromium.org/downloads)
3. zip を解凍して含まれる実行ファイルを任意の場所に移動します

## AtCoderHeaderMaker の実行

1. こちらのリポジトリをクローン
1. `python3 init.py` (初回実行時のみ)
   - `AtCoder userID`: 画像を生成したいユーザの AtCoder 上での ID を入力
   - `chromedriver path`: 先ほどインストールした chromedriver のパスを入力 </br> **パスには chromedriver まで含めてください(winの場合はchromedriver.exe)** 
      * 例(macOS): /Users/hogehoge/chromedriver
      * 例(windows): C:\\chromedriver.exe
1. `python3 run.py`
1. result ディレクトリに画像が生成されます
