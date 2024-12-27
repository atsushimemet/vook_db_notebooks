import base64
import datetime
import hashlib
import json
import os
import re
import time
import urllib
from io import BytesIO, StringIO
from time import sleep

import boto3
import numpy as np
import pandas as pd
import requests

from vook_db_lambda.config import MAX_PAGE  # s3_file_name_products_raw_prev,
from vook_db_lambda.config import (
    REQ_URL,
    REQ_URL_CATE,
    WANT_ITEMS_RAKUTEN,
    WANT_ITEMS_YAHOO,
    req_params,
    s3_bucket,
    size_id,
    sleep_second,
)
from vook_db_lambda.local_config import ClientId, aff_id
from vook_db_lambda.rds_handler import get_knowledges


def DataFrame_maker_rakuten(keyword, platform_id, knowledge_id, size_id):
    """apiコールした結果からdataframeを出力する関数を定義"""
    cnt = 1
    df = pd.DataFrame(columns=WANT_ITEMS_RAKUTEN)
    req_params["page"] = cnt
    req_params["keyword"] = keyword
    while True:
        req_params["page"] = cnt
        res = requests.get(REQ_URL, req_params)
        res_code = res.status_code
        res = json.loads(res.text)
        if res_code != 200:
            print(
                f"""
            ErrorCode -> {res_code}\n
            Error -> {res['error']}\n
            Page -> {cnt}"""
            )
        else:
            if res["hits"] == 0:
                print("返ってきた商品数の数が0なので、ループ終了")
                break
            tmp_df = pd.DataFrame(res["Items"])[WANT_ITEMS_RAKUTEN]
            df = pd.concat([df, tmp_df], ignore_index=True)
        if cnt == MAX_PAGE:
            print("MAX PAGEに到達したので、ループ終了")
            break
        # logger.info(f"{cnt} end!")
        cnt += 1
        # リクエスト制限回避
        sleep(1)
        print("Finished!!")

    df["platform_id"] = platform_id
    df["knowledge_id"] = knowledge_id
    df["size_id"] = size_id
    df_main = df.rename(
        columns={"itemName": "name", "itemPrice": "price", "itemUrl": "url"}
    )
    df_main = df_main.reindex(
        columns=[
            "id",
            "name",
            "url",
            "price",
            "knowledge_id",
            "platform_id",
            "size_id",
        ]
    )
    print("price type before:", df_main["price"].dtype)
    df_main["price"] = df_main["price"].astype(int)
    print("price type after:", df_main["price"].dtype)
    run_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    df_main["created_at"] = run_time
    df_main["updated_at"] = run_time
    return df_main


def create_url_yahoo(aff_url):
    """アフィリエイトURLがリンク切れのため一時的に素のURLを返す"""
    return urllib.parse.unquote(aff_url.split("vc_url=")[1])


def DataFrame_maker_yahoo(keyword, platform_id, knowledge_id, size_id):
    start_num = 1
    step = 100
    max_products = 1000

    params = {
        "appid": ClientId,
        "output": "json",
        "query": keyword,
        "sort": "-price",
        "affiliate_id": aff_id,
        "affiliate_type": "vc",
        "results": 100,  # NOTE: 100個ずつしか取得できない。
    }

    l_df = []
    for inc in range(0, max_products, step):
        params["start"] = start_num + inc
        df = pd.DataFrame(columns=WANT_ITEMS_YAHOO)
        res = requests.get(url=REQ_URL_CATE, params=params)
        res_cd = res.status_code
        if res_cd != 200:
            print("Bad request")
            break
        else:
            res = json.loads(res.text)
            if len(res["hits"]) == 0:
                print("If the number of returned items is 0, the loop ends.")
            print("Get Data")
            l_hit = []
            for h in res["hits"]:
                l_hit.append(
                    (
                        h["index"],
                        h["name"],
                        create_url_yahoo(h["url"]),
                        h["price"],
                        knowledge_id,
                        platform_id,
                        size_id,
                        # 現在の日付と時刻を取得 & フォーマットを指定して文字列に変換
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                        # 現在の日付と時刻を取得 & フォーマットを指定して文字列に変換
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                    )
                )
            df = pd.DataFrame(l_hit, columns=WANT_ITEMS_YAHOO)
            l_df.append(df)
    if not l_df:
        print("no df")
    else:
        return pd.concat(l_df, ignore_index=True)


# エラーワードに対して対応表をもとにレスポンスする関数
def convertor(input_string, ng_ok_table):
    # 特定のワードが DataFrame に含まれているかどうかを確認し、行番号を表示
    row_indices = ng_ok_table.index[
        ng_ok_table.apply(lambda row: input_string in row.values, axis=1)
    ].tolist()
    if row_indices:
        output = ng_ok_table["corrected"][row_indices[0]]
        print(f"{input_string}を{output}に変換します")
        return output
    else:
        print(f"{input_string}は対応表に存在しません。")
        return input_string


# 対応表を読み出し
ng_ok_table = pd.read_csv("./data/input/query_ng_ok.csv")


def validate_input(input_string):
    """
    連続する2文字以上で構成されたワードのみをOKとし、単体1文字またはスペースの前後に単体1文字が含まれるワードをNGとするバリデータ関数
    """
    # 正規表現パターン: 単体1文字またはスペースの前後に単体1文字が含まれるワードを検出
    pattern_ng = re.compile(r"^[!-~]$|\s[!-~]$|^[!-~]\s")
    # 入力文字列がNGパターンに一致するか確認
    if not pattern_ng.search(input_string):
        return input_string
    else:
        # エラーワードがあればメッセージを吐き、convertor関数によって対応する
        print(f"エラーワード　{input_string}が存在しました:")
        return convertor(input_string, ng_ok_table)


def create_wort_list(df_from_db: pd.DataFrame, unit: str) -> list:
    """brand,line,knowledgeの連続2文字以上ワードかどうかを判定、修正する"""
    words = df_from_db[
        f"{unit}_name"
    ].values.copy()  # NOTE:copyしないと関数内部で_nameカラムが更新される。
    for row in np.arange(len(words)):
        word = words[row]
        words[row] = validate_input(word)
    return list(words)


def create_df_no_ng_keyword(
    df_from_db, words_knowledge_name, words_brand_name, words_line_name
):
    df_no_ng_keyword = pd.DataFrame(columns=df_from_db.columns)
    df_no_ng_keyword["knowledge_id"] = df_from_db["knowledge_id"].values
    df_no_ng_keyword["knowledge_name"] = words_knowledge_name
    df_no_ng_keyword["brand_name"] = words_brand_name
    df_no_ng_keyword["line_name"] = words_line_name
    return df_no_ng_keyword


def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__}の実行時間: {round(end_time - start_time)}秒")
        return result

    return wrapper


@time_decorator
def repeat_dataframe_maker(
    df_no_ng_keyword,
    platform_id,
    func,
    size_id=size_id,
    sleep_second=sleep_second,
):
    n_bulk = len(df_no_ng_keyword)
    df_bulk = pd.DataFrame()
    for i, n in enumerate(np.arange(n_bulk)):
        brand_name = df_no_ng_keyword.brand_name[n]
        line_name = df_no_ng_keyword.line_name[n]
        knowledge_name = df_no_ng_keyword.knowledge_name[n]
        query = f"{brand_name} {line_name} {knowledge_name} 中古"
        # query validatorが欲しい　半角1文字をなくす
        knowledge_id = df_no_ng_keyword.knowledge_id[n]
        print(f"{i:03}, 検索キーワード:[" + query + "]", "knowledge_id:", knowledge_id)
        output = func(query, platform_id, knowledge_id, size_id)
        df_bulk = pd.concat([df_bulk, output], ignore_index=True)
        sleep(sleep_second)
        # テストでは、1知識で試す
        # break
    return df_bulk  # TODO:lambda実行でempty dataframe 原因調査から


def upload_s3(
    df, s3_file_name_products_raw_prev, s3_bucket=s3_bucket, profile_name="vook"
):
    # Lambda環境を識別するための環境変数の存在をチェック
    if "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
        # Lambda環境用のクライアント初期化
        print("Now: Lambda env")
        s3_client = boto3.client("s3")
    else:
        # ローカル開発環境用のクライアント初期化
        print("Now: Local env")
        session = boto3.session.Session(profile_name=profile_name)
        s3_client = session.client("s3")
    # Pandas DataFrameをCSV形式の文字列に変換
    csv_data = df.to_csv(index=False)
    # 文字列IOを使ってCSVデータを書き込む
    csv_buffer = StringIO()
    csv_buffer.write(csv_data)
    # 文字列IOのカーソルを先頭に戻す
    csv_buffer.seek(0)
    # バイナリデータとしてエンコード
    csv_binary = csv_buffer.getvalue().encode("utf-8")
    # ファイルのハッシュを計算
    file_hash = hashlib.md5(csv_binary).digest()
    # Base64エンコード
    content_md5 = base64.b64encode(file_hash).decode("utf-8")
    # S3にCSVファイルをアップロード
    s3_client.put_object(
        Body=csv_binary,
        Bucket=s3_bucket,
        Key=s3_file_name_products_raw_prev,
        ContentMD5=content_md5,
    )
    print(f"CSV file uploaded to s3://{s3_bucket}/{s3_file_name_products_raw_prev}")


def read_csv_from_s3(bucket_name, file_key, profile_name="vook"):
    # Lambda環境を識別するための環境変数の存在をチェック
    if "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
        # Lambda環境用のクライアント初期化
        print("Now: Lambda env")
        s3_client = boto3.client("s3")
    else:
        # ローカル開発環境用のクライアント初期化
        print("Now: Local env")
        session = boto3.session.Session(profile_name=profile_name)
        s3_client = session.client("s3")
    # S3バケットからファイルを読み込む
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    # レスポンスからバイナリデータを取得
    file_content = response["Body"].read()
    # バイナリデータをPandas DataFrameに変換
    df = pd.read_csv(BytesIO(file_content), encoding="utf-8")
    return df


def create_api_input() -> pd.DataFrame:
    # 知識情報の取得
    df_from_db = get_knowledges()
    # 対象のワードリスト作成
    words_brand_name = create_wort_list(df_from_db, "brand")
    words_line_name = create_wort_list(df_from_db, "line")
    words_knowledge_name = create_wort_list(df_from_db, "knowledge")
    # 修正版のテーブルを作成
    df_api_input = create_df_no_ng_keyword(
        df_from_db, words_knowledge_name, words_brand_name, words_line_name
    )
    return df_api_input


def set_id(
    df_bulk: pd.DataFrame,
    s3_file_name_products_raw_prev: str,
    s3_bucket: str = s3_bucket,
):
    """IDの設定"""
    df_prev = read_csv_from_s3(s3_bucket, s3_file_name_products_raw_prev)
    nan_arr = np.isnan(df_prev["id"])
    if all(nan_arr):
        df_bulk["id"] = np.arange(1, len(df_bulk) + 1)
    elif any(nan_arr):
        Exception("一部に欠損が生じているという想定外の事象です。")
    else:
        PREV_ID_MAX = df_prev["id"].max()
        df_bulk["id"] = np.arange(PREV_ID_MAX, PREV_ID_MAX + len(df_bulk)) + 1
    return df_bulk
