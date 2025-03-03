from address_to_latlng import address_to_latlng
import requests
from bs4 import BeautifulSoup
import json
from retry import retry
import urllib
import time
import os

# 物件データリスト
data_samples = []

# スクレイピングするページ数
max_page = 100
# SUUMOの検索結果URL（ページフォーマットあり）
url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&sc=13106&sc=13107&sc=13108&sc=13118&sc=13121&sc=13122&sc=13123&sc=13109&sc=13110&sc=13111&sc=13112&sc=13114&sc=13115&sc=13120&sc=13116&sc=13117&sc=13119&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=25&pc=50&page={}'

# リクエストのリトライ処理
@retry(tries=3, delay=10, backoff=2)
def load_page(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    return soup

# 処理時間計測
start = time.time()
times = []

# ページごとの処理
for page in range(1, max_page + 1):
    before = time.time()
    
    # ページのスクレイピング
    soup = load_page(url.format(page))
    mother = soup.find_all(class_='cassetteitem')  # 物件情報リスト

    # 物件ごとの処理
    for child in mother:
        # 建物情報の辞書
        data_home = {
            "category": child.find(class_='ui-pct ui-pct--util1').text.strip(),  # 物件のカテゴリ（例：マンション、アパート）
            "name": child.find(class_='cassetteitem_content-title').text.strip(),  # 建物名
            "address": child.find(class_='cassetteitem_detail-col1').text.strip(),  # 住所
            "stations": [],  # 最寄り駅リスト
            "age": "",  # 築年数
            "floors": ""  # 建物の階数
        }

        # 最寄り駅の情報
        station_info = child.find(class_='cassetteitem_detail-col2')
        for station in station_info.find_all(class_='cassetteitem_detail-text'):
            data_home["stations"].append(station.text.strip())

        # 築年数と階数
        detail_info = child.find(class_='cassetteitem_detail-col3').find_all('div')
        if len(detail_info) >= 2:
            data_home["age"] = detail_info[0].text.strip()  # 築年数
            data_home["floors"] = detail_info[1].text.strip()  # 階数

        # 部屋情報リスト
        data_rooms = []
        rooms = child.find(class_='cassetteitem_other')
        for room in rooms.find_all(class_='js-cassette_link'):
            room_data = {}
            
            # 各部屋の情報取得
            room_details = room.find_all('td')
            if len(room_details) >= 9:
                room_data["floor"] = room_details[2].text.strip()  # 何階の部屋か
                room_data["rent"] = room_details[3].find(class_='cassetteitem_other-emphasis ui-text--bold').text.strip()  # 家賃
                room_data["management_fee"] = room_details[3].find(class_='cassetteitem_price--administration').text.strip()  # 管理費
                room_data["deposit"] = room_details[4].find(class_='cassetteitem_price--deposit').text.strip()  # 敷金
                room_data["key_money"] = room_details[4].find(class_='cassetteitem_price--gratuity').text.strip()  # 礼金
                room_data["layout"] = room_details[5].find(class_='cassetteitem_madori').text.strip()  # 間取り（例：1K、2LDK）
                room_data["size"] = room_details[5].find(class_='cassetteitem_menseki').text.strip()  # 部屋の面積（㎡）
                
                # URLの取得
                get_url = room_details[8].find(class_='js-cassette_link_href cassetteitem_other-linktext').get('href')
                room_data["url"] = urllib.parse.urljoin(url, get_url)  # 部屋の詳細ページURL

                data_rooms.append(room_data)

        # 物件情報と部屋情報をまとめて辞書に格納
        data_samples.append({
            "building": data_home,  # 建物情報
            "rooms": data_rooms  # 部屋情報リスト
        })

    # 1アクセスごとに1秒休む
    time.sleep(1)

    # 進捗確認
    after = time.time()
    running_time = after - before
    times.append(running_time)
    print(f'{page}ページ目：{running_time:.2f}秒')
    print(f'総取得件数：{len(data_samples)}')

    # 作業の進捗
    complete_ratio = round(page / max_page * 100, 3)
    print(f'完了：{complete_ratio}%')

    # 残り時間の目安
    running_mean = sum(times) / len(times)
    remaining_time = running_mean * (max_page - page)
    hour, rem = divmod(int(remaining_time), 3600)
    minute, second = divmod(rem, 60)
    print(f'残り時間：{hour}時間{minute}分{second}秒\n')


for item in data_samples:
    address = item["building"]["address"]
    latlng = address_to_latlng(address)
    print("adress:",address,"\t\t緯度経度:",latlng)
    if latlng:
        item["building"]["latitude"] = latlng[0]
        item["building"]["longitude"] = latlng[1]
    time.sleep(0.1)


# 処理時間計測
finish = time.time()
running_all = finish - start
print('総経過時間：', running_all)

#データ数
print("合計建物数：",len(data_samples),"個")

# 出力ファイルパス
output_file_path = 'data/home_data.json'

# フォルダがない場合は作成
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# JSONファイルとして保存
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(data_samples, f, indent=2, ensure_ascii=False)

print(f"{output_file_path} に物件情報を出力しました")
