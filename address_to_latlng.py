from bs4 import BeautifulSoup
import requests
import urllib

def address_to_latlng(address:str):
    """
    :param address: 住所
    """
    
    url = f"https://www.google.co.jp/maps/place/{urllib.parse.quote(address)}"
    # HTTPリクエストを送信
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    
    if response.status_code != 200:
        print(f"エラー: ステータスコード {response.status_code}")
        return None

    # BeautifulSoupでHTMLを解析
    soup = BeautifulSoup(response.content, "html.parser")
    
    # <script>タグの抽出
    script_list =[script.get_text() for script in soup.find_all("script")]
    
    for text in script_list:
        if "/@" in text:
            divide = text.split("/")
            for part in divide:
                if part and part[0]=="@":
                    tmp = part.replace("@","").split(",")
                    latitude = float(tmp[0])
                    longitude = float(tmp[1])
                    return (latitude, longitude)
    
    return None


if __name__=='__main__':
    print(address_to_latlng("東京都新宿区市谷砂土原町３"))