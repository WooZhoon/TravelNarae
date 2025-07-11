import requests
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
import json

# .env 파일 로드 (프로젝트 루트에 .env 파일이 있다고 가정)
load_dotenv()
TOUR_API_KEY = os.getenv("TOUR_API_KEY")

if not TOUR_API_KEY:
    print("환경 변수 TOUR_API_KEY가 설정되지 않았습니다. .env 파일을 확인해주세요.")
    exit()

url = "https://apis.data.go.kr/B551011/KorService2/areaBasedList2"
params = {
    'serviceKey': quote_plus(TOUR_API_KEY),
    'MobileOS': 'ETC',
    'MobileApp': 'MyApp',
    '_type': 'json',
    'numOfRows': 10,
    'pageNo': 1,
    'contentTypeId': 12,
    'areaCode': '1', # 서울 (테스트용)
}

print(f"API 호출 URL: {url}")
print(f"API 호출 Params: {params}")

try:
    # SSL 인증서 검증을 기본값(True)으로 유지
    response = requests.get(url, params=params, verify=False)
    response.raise_for_status() # HTTP 오류 발생 시 예외 발생

    data = response.json()
    print("\nAPI 호출 성공:")
    print(json.dumps(data, indent=2, ensure_ascii=False)) # 한글 깨짐 방지

except requests.exceptions.RequestException as e:
    print(f"\nAPI 호출 중 오류 발생: {e}")
except Exception as e:
    print(f"\n기타 오류 발생: {e}")
