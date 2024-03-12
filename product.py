import hmac
import hashlib
import binascii
import os
import time
import requests
import json
import urllib.request
import secrets
from urllib.parse import urlencode
import hmac
import hashlib
import binascii
import os
import time
import json
from time import gmtime, strftime
import Levenshtein

str1 = "[24SS 최신상] 아뜰리에 마졸리 클래식 트위드 재킷 1종"
str2 = "더엣지 심플 트위드 재킷"

similarity_ratio = Levenshtein.ratio(str1, str2)
print("Similarity Ratio:", similarity_ratio)


REQUEST_METHOD = "GET"
DOMAIN = "https://api-gateway.coupang.com"
keyword = urllib.parse.quote("[24SS 최신상] 아뜰리에 마졸리 클래식 트위드 재킷 1종")
URL = f"/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword={keyword}&limit=5"

def load_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(': ')
            credentials[key] = value
    return credentials


credentials_file_path = 'key.txt'
credentials = load_credentials(credentials_file_path)
ACCESS_KEY = credentials["ACCESS_KEY"]
SECRET_KEY = credentials["SECRET_KEY"]
def generateHmac(method, url, api_secret_key, api_access_key):
    path, *query = url.split('?')
    os.environ['TZ'] = 'GMT+0'
    dt_datetime = strftime('%y%m%d', gmtime()) + 'T' + strftime('%H%M%S', gmtime()) + 'Z'  # GMT+0
    msg = dt_datetime + method + path + (query[0] if query else '')
    signature = hmac.new(bytes(api_secret_key, 'utf-8'), msg.encode('utf-8'), hashlib.sha256).hexdigest()

    return 'CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}'.format(api_access_key, dt_datetime,
                                                                                          signature)


authorization = generateHmac(REQUEST_METHOD, URL, SECRET_KEY, ACCESS_KEY)
url = "{}{}".format(DOMAIN, URL)
resposne = requests.request(method=REQUEST_METHOD, url=url,
                            headers={
                                "Authorization": authorization,
                                "Content-Type": "application/json"
                            }
                            # ,
                            # data=json.dumps(REQUEST)
                            )
pretty_json = json.dumps(resposne.json(), indent=2, ensure_ascii=False)
print(pretty_json)
print(resposne.json()['data']['productData'][0]['productName'])
for x in range(5):
    string1 = "클래식 트위드 재킷 아뜰리에 마졸리"
    string2 = str(resposne.json()['data']['productData'][x]['productName'])
    similarity_ratio = Levenshtein.ratio(string1, string2)
    print(f"Similarity {x}번째 Ratio:", similarity_ratio)
