import os
import sys
from unittest import TestCase

import pandas as pd

from tests.test_utils_10_1 import (
    generate_mock_data_actual as generate_mock_data_actual_1,
)
from tests.test_utils_10_1 import (
    generate_mock_data_expected as generate_mock_data_expected_1,
)
from tests.test_utils_10_2 import (
    generate_mock_data_actual as generate_mock_data_actual_2,
)
from tests.test_utils_10_2 import (
    generate_mock_data_expected as generate_mock_data_expected_2,
)
from tests.test_utils_16_1 import (
    generate_mock_data_actual as generate_mock_data_actual_16_1,
)
from tests.test_utils_16_1 import (
    generate_mock_data_expected as generate_mock_data_expected_16_1,
)
from vook_db_lambda.exclude_noise import (  # 実際のモジュール名に置き換え
    product_noise_judge_brand,
    product_noise_judge_knowledge,
)
from vook_db_lambda.utils import (
    DataFrame_maker_rakuten,
    DataFrame_maker_yahoo,
    create_api_input,
    repeat_dataframe_maker,
)

# rakuten_api_call_bulk_from_table.py のディレクトリをパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# rakuten_api_call_bulk_from_table から main をインポート
from rakuten_api_call_bulk_from_table import main  # noqa


def test_product_noise_judge_brand():
    """ブランドレベルのノイズが除外されていることをdf_bulkのname列を使用して確認"""
    # テスト用データ
    df_bulk_actual = generate_mock_data_actual_1()

    # 関数を実行
    df_cleaned = product_noise_judge_brand(df_bulk_actual)

    # 期待される出力
    df_bulk_expected = generate_mock_data_expected_1()

    # name列をセットとして比較
    actual_names = set(df_cleaned["name"])
    expected_names = set(df_bulk_expected["name"])

    # 集合が一致しているかを確認
    assert (
        actual_names == expected_names
    ), f"Actual names: {actual_names}, Expected names: {expected_names}"


def test_product_noise_judge_knowledge():
    """知識レベルのノイズが除外されていることをdf_bulkのname列を使用して確認"""
    # テスト用データ
    df_bulk_actual = generate_mock_data_actual_2()

    # 関数を実行
    df_cleaned = product_noise_judge_knowledge(df_bulk_actual)

    # 期待される出力
    df_bulk_expected = generate_mock_data_expected_2()

    # name列をセットとして比較
    actual_names = set(df_cleaned["name"])
    expected_names = set(df_bulk_expected["name"])

    # 集合が一致しているかを確認
    assert (
        actual_names == expected_names
    ), f"Actual names: {actual_names}, Expected names: {expected_names}"


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
        print("product_noise_judge_brandとproduct_noise_judge_knowledgeの完了")
        self.assertIsInstance(df_bulk_not_noise_ng_word, pd.DataFrame)
        print("df_bulk_not_noise_ng_wordがDataFrameであることを確認")
        self.assertTrue(len(df_bulk_not_noise_ng_word))
        print("df_bulk_not_noise_ng_word が1行以上のデータを持っていることを確認")
        print("product_noise_judge_brand, knowledgeの正常終了を確認")


def test_product_noise_judge_knowledge_keyword():
    """知識レベルの必須キーワードが含まれていることをdf_bulkのname列を使用して確認"""
    # テスト用データ
    df_bulk_actual = generate_mock_data_actual_16_1()

    # 関数を実行
    df_cleaned = product_noise_judge_knowledge(df_bulk_actual)

    # 期待される出力
    df_bulk_expected = generate_mock_data_expected_16_1()

    # name列をセットとして比較
    actual_names = set(df_cleaned["name"])
    expected_names = set(df_bulk_expected["name"])

    # 集合が一致しているかを確認
    assert (
        actual_names == expected_names
    ), f"Actual names: {actual_names}, Expected names: {expected_names}"
