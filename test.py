import pandas as pd
import requests
import time

API_KEY = '여기에_카카오_REST_API_KEY_입력'  # 본인 REST API 키 입력

def get_coords(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    params = {"query": address}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        if result['documents']:
            x = result['documents'][0]['x']  # 경도
            y = result['documents'][0]['y']  # 위도
            return y, x
    return None, None

# 1번 그룹 파일 리스트 # 여기를 각자 할거로 바꾸세요 !!!!!!!!!!!!!!!!!!!!!!
# file_list = [
#     'Busan_heritage_with_detail_and_desc.csv',
#     'Chungbuk_heritage_with_detail_and_desc.csv',
#     'Chungnam_heritage_with_detail_and_desc.csv',
#     'Daegu_heritage_with_detail_and_desc.csv',
#     'Daejeon_heritage_with_detail_and_desc.csv'
# ]

for input_filename in file_list:
    place_name = input_filename.split('_')[0]
    output_filename = f"{place_name}_coords.csv"

    df = pd.read_csv(input_filename)

    latitudes = []
    longitudes = []
    for addr in df['소재지(상세)']:
        lat, lon = get_coords(str(addr))
        latitudes.append(lat)
        longitudes.append(lon)
        time.sleep(0.2)  # API 호출 제한 방지

    df['위도'] = latitudes
    df['경도'] = longitudes

    df.to_csv(output_filename, index=False)