# vook_db_lambdaについて
- 本プロジェクトは[VooktokyoのDiscovery](https://vook.tokyo/#:~:text=02-,Discovery,-%E4%BA%BA%E6%B0%97%E3%81%AE%E5%95%86%E5%93%81)（商品）ページの情報更新のために使用される。
- 当該ページでは、ヴィンテージファッションアイテムの商品情報が日次で更新される。ex. [Levi's > 501 > 66前期](https://vook.tokyo/products/5)
- 当該プロジェクトは、楽天APIとYahooショッピングAPIを使用してこれらの情報を日次で取得する。
- 取得されたデータはRDSデータベースに保存される。
- 保存されたデータは[vook_web_v3](https://github.com/atsushimemet/vook_web_v3)によって参照され、フロントエンドに表示される。

## 主な特徴
- **実行頻度**: 日次更新。AWS EventBridgeを使用して毎日深夜0時に情報を取得。
- **データソース**: 楽天APIおよびYahooショッピングAPIを利用して情報を取得。
- **ロジック**: AWS Lambdaのvook_db_lambda_rakutenでデータソースよりデータ取得、処理、保存のロジックを実装。
- **データベース管理**: 取得した商品情報をRDSに保存。RDBMSはMySQL。

## 前提条件
以下を実行できるようにする必要がある。
- **Docker**: Lambdaレイヤーおよび依存関係の管理。
- **マネコンへのログイン**: 本番環境での動作確認、ログの確認に必要。
- **AWS CLI**: リソースのデプロイに必要。

### 補足：Lambdaのレイヤー作成方法
1. 公式イメージの取得
```
docker pull amazon/aws-sam-cli-build-image-python3.9
# https://hub.docker.com/r/amazon/aws-sam-cli-build-image-python3.9
```
2. コンテナに入る
```
docker run -it -v $(pwd):/var/task amazon/aws-sam-cli-build-image-python3.9:latest
```
3. 必要なライブラリをインストール
```
pip install pandas -t ./python
pip install sshtunnel -t ./python
pip install pymysql -t ./python
pip install boto3 -t ./python
pip install requests -t ./python
```
4. zip化
```
zip -r lambda-layer.zip ./python
```
5. マネコンで作業
5.1. s3アップロード
5.2. httpsのURL取得
5.3. zipファイルをアップロードしてレイヤー作成
5.4. 関数側でレイヤーを指定

### 補足：マネコンへのログイン
- infra管理者にslackの[generalチャンネル](https://vook-tokyo.slack.com/archives/C04MXLWG4Q3)でIAMユーザーを作成してもらう。
- ユーザー名、パスワード、コンソールサインインURLが記載されたファイルを連携してもらう。
- ログイン後、IAM > ユーザー > <ユーザー名> > セキュリティ認証情報タブをクリックする。
- アクセスキーを発行する。

### 補足：AWS CLI
- 上記で発行されたアクセスキー、シークレットキーを利用してローカル開発環境でAWS CLIをアクティベートする。
- 詳細な手順はこちらを[参照](https://docs.aws.amazon.com/cli/)のこと。

# 修正からデプロイまでの手順
1. 修正イシューを起票する。内容の形式は問わないが目的、修正要件は明記しておくこと。
2. 設計については、時間に余裕がある場合に作成するものとする。
3. 当該イシュー番号を利用して、ローカルにてfeature_issue_<イシュー番号>ブランチを作成する。
4. 単体テストを実施する。
   1. イシューにテストケースを作成する。
   2. 修正する。
   3. テストする。
5. 結合テストを実施する。
   1. イシューにテストケースを作成する。
   2. 修正する。
   3. テストする。
6. デプロイする。
   1. デプロイ条件を満たしていることを確認する。
      1. 単体テストが完了していること ex. test_product_noise_judgeが合格していること
      2. 結合テストが完了していること ex. TestMainFunctionが合格していること
      3. deploy.sh内のzipファイル名を更新できていること
   2. コマンドラインで`./deploy.sh`を実行する。
      1. 標準出力された現行バージョンのバックアップリンクからバックアップを取得する
      2. デプロイできていることをLambdaのマネコンの関数一覧の最終更新、変更点を含むスクリプトから確認する
7. システムテスト（本番環境での動作確認）を実施する。
   1. イシューにテストケースを作成する。
   2. mainの実行すべきポイント以外をコメントアウトする。
   3. Lambdaの機能でテストする。
8. 完了後にPRをマージする。
9. ローカル開発環境のmainを最新にする。
