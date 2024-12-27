import datetime

from vook_db_lambda.local_config import CLIENT_ME, pid, sid

# Yahoo
REQ_URL_CATE = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"
BRAND = "リーバイス"
ITEM = "デニム"
LINE = "501"
KNOWLEDGE = "66前期"
KNOWLEDGE_ID = 1
COL_NAMES = [
    "id",
    "name",
    "url",
    "price",
    "knowledge_id",
    "platform_id",
    "size_id",
    "created_at",
    "updated_at",
]

aff_id = f"//ck.jp.ap.valuecommerce.com/servlet/referral?vs={sid}&vp={pid}&vc_url="
run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

start_num = 1
step = 100
max_products = 1000

# Rakuten
REQ_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
MAX_PAGE = 10  # NOTE: auto_postが300ほどしかできない。
HITS_PER_PAGE = 30


req_params = {
    "applicationId": CLIENT_ME["APPLICATION_ID"],
    "affiliateId": CLIENT_ME["AFF_ID"],
    "format": "json",
    "formatVersion": "2",
    "keyword": "",
    "hits": HITS_PER_PAGE,
    "sort": "-itemPrice",
    "page": 0,
    "minPrice": 100,
}
WANT_ITEMS_RAKUTEN = [
    "itemName",
    "itemPrice",
    "itemUrl",
]

WANT_ITEMS_YAHOO = [
    "id",
    "name",
    "url",
    "price",
    "knowledge_id",
    "platform_id",
    "size_id",
    "created_at",
    "updated_at",
]


platform_id = 2
size_id = 999
sleep_second = 1

s3_bucket = "vook-vook"
# s3_bucket = "vook-bucket"
s3_file_name_products_raw_prev = f"vook_db/products_raw_prev_{platform_id}.csv"
