from address_to_latlng import address_to_latlng
from calc_distance import calc_distance
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

# Jinja2のテンプレート設定
templates = Jinja2Templates(directory="templates")

# staticディレクトリをマウント
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def search_page(request: Request):
    """ 検索ページを返す """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return {}


@app.get("/homes")
def read_item():
    """スクレイピングによって得られた物件情報をjsonで返す"""
    path = "data/home_data.json"
    with open(path, 'r', encoding="utf-8") as fp:
        home_data = json.load(fp)
    return home_data[:10]


@app.get("/get_property/")
def get_property(address: str, dist: float):
    """
    指定された住所 (address) と距離 (dist) を受け取るエンドポイント

    :param address: 住所（文字列）
    :param dist: 距離（浮動小数）
    """
    pos = address_to_latlng(address)
    if pos ==None:
        return {"adress error"}
    
    file_path = "data/home_data.json"
    data = read_json_file(file_path)
    if data == None:
        return {"process error"}
    
    num = 0
    result_data = []
    for one_case in data:
        tmp = one_case
        if "latitude" not in tmp["building"].keys() and "longitude" not in tmp["building"].keys():
            continue
        distance = calc_distance(pos[0],pos[1],tmp["building"]["latitude"],tmp["building"]["longitude"])
        if distance < dist:
            tmp["distance"] = f"{distance:.2f}"
            result_data.append(tmp)
            num += 1

    #距離で昇順にソート
    result_data.sort(key=lambda x:x["distance"])
    res_data = {"num": num,"whole": len(data), "result_data": result_data}
    return JSONResponse(content=res_data)



def read_json_file(file_path: str):
    """jsonファイルの読み込みの処理"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)  # JSONを読み込む
        return data
    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません -> {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"エラー: JSONのフォーマットが不正です -> {file_path}")
        return None
    except PermissionError:
        print(f"エラー: ファイルのアクセス権限がありません -> {file_path}")
        return None
    except Exception as e:
        print(f"エラー: 予期しない問題が発生しました -> {str(e)}")
        return None