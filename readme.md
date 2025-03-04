# 指定距離内の物件検索アプリ
python3.11.9  

## 仮想環境の実行
```
.\venv\Scripts\activate
```
  
## ライブラリ
インストール  
```
pip install -r requirements.txt
```
### 使用するライブラリ
fastAPI  
beautifulsoup  
etc..  
requirements.txt 参照

## windowsでの実行
```
main.bat
```

## その他の実行
```
uvicorn main:app --port 8000 --reload
```

## 各ファイルの説明
### main.py
fastAPIを用いたエンドポイント
### data_sercch.py
スクレイピングを実行し、物件情報のデータを作成する。  
**address_to_latlng.py** ファイルの関数を使用しており、住所から緯度経度を取得する。  
データは**data**フォルダに出力される。  
コード内の **max_page** の値を適宜変更。(1ページ当たり物件数50件)  
### address_to_latlng.py
住所を入力することで緯度・経度を返す。  
入力：住所  
戻り値：(緯度, 経度)  
取得できなかった場合、None
### calc_distance.py
2地点の緯度・経度から距離を計算する。  
入力:Aの緯度，Aの経度，Bの緯度，Bの経度  
戻り値：距離(km)