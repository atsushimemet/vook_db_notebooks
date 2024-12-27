import numpy as np
import pandas as pd


def generate_mock_data_actual(num_rows=5):
    """
    テストデータを生成する関数。

    この関数は、指定された行数のモックデータを生成し、データフレームとして返します。
    主に、`df_bulk`というデータが作成された後の実装修正時に使用されます。
    本関数に反映されているデータは仮のデータです。
    ・参考までに2024/12/24 16:32時点でcheck_df_bulk_interface.ipynbを実行して作成されました。

    Args:
        num_rows (int): 生成する行数。デフォルトは30行。実装修正の規模に合わせて行数を調整できます。

    Returns:
        pd.DataFrame:

    使用例:
      - 修正点に応じたテストデータを簡単に作成するために利用します。
      - 修正点が発生した場合はテスト要件、ケースを言語化し、そのケースを確認できるようなdf_bulkをこの関数内部の実装を修正することで作成します。
      - 作成方法はtest_utils.pyの末尾に__<issue_no>_<test_case_no>を付与しファイル自体をコピーした後、内部の実装を修正してください。
      - 内部の実装でgenerate_mock_data_actualとgenerate_mock_data_expected関数を作成してください。
    """
    data = {
        "id": [np.nan for _ in range(num_rows)],
        "name": [
            "【中古】リーバイス 501Z-XX",
            "【中古】Lee｜リー デニム ジャケット 101-J 50年代後期 ヴィンテージ ブルー サイズ：42 / アメカジ【f93】",
            "【中古】Levi’s◆70s/ベルボトム/RED",
            "古着 00'S パタゴニア Patagonia ORGANIC COTTON オーガニックコットン 11339F7 ダック地ショーツ ショートパンツ メンズw36相当 /eaa485969 【中古】 【240903】",
            "【中古】Levi’s◆60s/4th/トラッカージャケット/BIGE/ボタン裏52/Gジャン/コットン/IDG/70505//【メンズウェア】",
        ],
        "url": [
            "https://hb.afl.rakuten.co.jp/hgc/g00tpkue.brn1qeb9.g00tpkue.brn1r3b3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fkaitori-gekijo%2Frc_iti2vmepfolk_ralt%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fkaitori-gekijo%2Fi%2F10013668%2F&rafcid=wsc_i_is_1040242227042771333",
            "https://hb.afl.rakuten.co.jp/hgc/g00qxgae.brn1qd0c.g00qxgae.brn1rd0a/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fotaichi%2F20166700476205%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fotaichi%2Fi%2F10531907%2F&rafcid=wsc_i_is_1040242227042771333",
            "https://hb.afl.rakuten.co.jp/hgc/g00r3cee.brn1qd11.g00r3cee.brn1r0ee/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fjumblestore%2F2320332329241%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fjumblestore%2Fi%2F31004574%2F&rafcid=wsc_i_is_1040242227042771333",
            "https://hb.afl.rakuten.co.jp/hgc/g00qhzfe.brn1q668.g00qhzfe.brn1rb64/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fjam-ing%2Feaa485969%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fjam-ing%2Fi%2F11385570%2F&rafcid=wsc_i_is_1040242227042771333",
            "https://hb.afl.rakuten.co.jp/hgc/g00r3cee.brn1qd11.g00r3cee.brn1r0ee/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fjumblestore%2F2329041972731%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fjumblestore%2Fi%2F32831699%2F&rafcid=wsc_i_is_1040242227042771333",
        ],
        "price": [
            67980,
            98000,
            18260,
            8360,
            31460,
        ],
        "knowledge_id": [
            10,
            107,
            36,
            31,
            38,
        ],
        "platform_id": [
            1,
            1,
            1,
            1,
            1,
        ],
        "size_id": [999 for _ in range(num_rows)],
        "created_at": [
            "2024-12-24 15:41:38.556295",
            "2024-12-24 15:46:38.781377",
            "2024-12-24 15:47:55.986734",
            "2024-12-24 15:42:42.617846",
            "2024-12-24 15:43:20.847997",
        ],
        "updated_at": [
            "2024-12-24 15:41:38.556295",
            "2024-12-24 15:46:38.781377",
            "2024-12-24 15:47:55.986734",
            "2024-12-24 15:42:42.617846",
            "2024-12-24 15:43:20.847997",
        ],
    }

    # ランダムなモックデータの生成
    df = pd.DataFrame(data)

    return df


def generate_mock_data_expected(num_rows=5):
    """
    テストデータを生成する関数。

    この関数は、指定された行数のモックデータを生成し、データフレームとして返します。
    主に、`df_bulk`というデータが作成された後の実装修正時に使用されます。
    本関数に反映されているデータは仮のデータです。
    ・参考までに2024/12/24 16:32時点でcheck_df_bulk_interface.ipynbを実行して作成されました。

    Args:
        num_rows (int): 生成する行数。デフォルトは30行。実装修正の規模に合わせて行数を調整できます。

    Returns:
        pd.DataFrame:

    使用例:
      - 修正点に応じたテストデータを簡単に作成するために利用します。
      - 修正点が発生した場合はテスト要件、ケースを言語化し、そのケースを確認できるようなdf_bulkをこの関数内部の実装を修正することで作成します。
      - 作成方法はtest_utils.pyの末尾に__<issue_no>_<test_case_no>を付与しファイル自体をコピーした後、内部の実装を修正してください。
      - 内部の実装でgenerate_mock_data_actualとgenerate_mock_data_expected関数を作成してください。
    """
    data = {
        "id": [np.nan for _ in range(num_rows - 2)],
        "name": [
            "【中古】Lee｜リー デニム ジャケット 101-J 50年代後期 ヴィンテージ ブルー サイズ：42 / アメカジ【f93】",
            "古着 00'S パタゴニア Patagonia ORGANIC COTTON オーガニックコットン 11339F7 ダック地ショーツ ショートパンツ メンズw36相当 /eaa485969 【中古】 【240903】",
            "【中古】Levi’s◆60s/4th/トラッカージャケット/BIGE/ボタン裏52/Gジャン/コットン/IDG/70505//【メンズウェア】",
        ],
        "url": [
            "https://hb.afl.rakuten.co.jp/hgc/g00qxgae.brn1qd0c.g00qxgae.brn1rd0a/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fotaichi%2F20166700476205%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fotaichi%2Fi%2F10531907%2F&rafcid=wsc_i_is_1040242227042771333",
            "https://hb.afl.rakuten.co.jp/hgc/g00qhzfe.brn1q668.g00qhzfe.brn1rb64/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fjam-ing%2Feaa485969%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fjam-ing%2Fi%2F11385570%2F&rafcid=wsc_i_is_1040242227042771333",
            "https://hb.afl.rakuten.co.jp/hgc/g00r3cee.brn1qd11.g00r3cee.brn1r0ee/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fjumblestore%2F2329041972731%2F&m=http%3A%2F%2Fm.rakuten.co.jp%2Fjumblestore%2Fi%2F32831699%2F&rafcid=wsc_i_is_1040242227042771333",
        ],
        "price": [
            98000,
            8360,
            31460,
        ],
        "knowledge_id": [
            107,
            31,
            38,
        ],
        "platform_id": [
            1,
            1,
            1,
        ],
        "size_id": [999 for _ in range(num_rows - 2)],
        "created_at": [
            "2024-12-24 15:46:38.781377",
            "2024-12-24 15:42:42.617846",
            "2024-12-24 15:43:20.847997",
        ],
        "updated_at": [
            "2024-12-24 15:46:38.781377",
            "2024-12-24 15:42:42.617846",
            "2024-12-24 15:43:20.847997",
        ],
    }

    # ランダムなモックデータの生成
    df = pd.DataFrame(data)

    return df
