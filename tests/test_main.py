from unittest import TestCase

import pandas as pd

from vook_db_lambda.exclude_noise import (
    filter_bulk_by_knowledge,
    product_line_judge,
    product_noise_judge_brand,
    product_noise_judge_knowledge,
)
from vook_db_lambda.rds_handler import get_products, put_products
from vook_db_lambda.tests import run_all_if_checker
from vook_db_lambda.utils import (
    DataFrame_maker_rakuten,
    DataFrame_maker_yahoo,
    create_api_input,
    repeat_dataframe_maker,
    set_id,
    upload_s3,
)


class TestMainFunction(TestCase):

    def test_main_function(self):
        print("APIのインプットデータ作成")
        df_api_input = create_api_input()
        print("df_bulkの作成")
        l_df_bulk = []
        for platform_id, func in zip(
            [1, 2], [DataFrame_maker_rakuten, DataFrame_maker_yahoo]
        ):
            df_bulk = repeat_dataframe_maker(df_api_input, platform_id, func)
            l_df_bulk.append(df_bulk)
        df_bulk = pd.concat(l_df_bulk, axis=0, ignore_index=True)
        df_bulk_not_noise_ng_word_brand = product_noise_judge_brand(df_bulk)
        df_bulk_not_noise_ng_word = product_noise_judge_knowledge(
            df_bulk_not_noise_ng_word_brand
        )
        df_bulk_not_noise_ng_line = product_line_judge(df_bulk_not_noise_ng_word)
        df_bulk_not_noise_filter_only_knowledge = filter_bulk_by_knowledge(
            df_bulk_not_noise_ng_line
        )
        s3_file_name_products_raw_prev = "lambda_output/products_raw_prev.csv"
        df_bulk_not_noise = set_id(
            df_bulk_not_noise_filter_only_knowledge, s3_file_name_products_raw_prev
        )
        run_all_if_checker(df_bulk_not_noise)
        print("df_bulkをs3に保存")
        upload_s3(df_bulk_not_noise, s3_file_name_products_raw_prev)
        print("df_bulkをRDSに保存")
        put_products(df_bulk_not_noise)
        print("RDSに保存したデータを確認")
        df_from_db = get_products()
        print("shape:", df_from_db.shape)
        print("id min:", df_from_db["id"].min())
        print("id max:", df_from_db["id"].max())
