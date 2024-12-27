#!/bin/bash

# 現在のディレクトリに存在するZIPファイルを削除
echo "Deleting existing ZIP files in the current directory..."
find . -maxdepth 1 -name "*.zip" -exec rm -v {} \;

# 新しいZIPファイル名を設定
ZIP_FILE="vook_db_lambda_20241227_2.zip"

# 新しいZIPファイルを作成
echo "Creating new ZIP file: $ZIP_FILE"
zip -r $ZIP_FILE . \
    -x ".env/*" \
    -x ".git/*" \
    -x ".mypy_cache/*" \
    -x "vook_db_lambda/__pycache__/*" \
    -x "notebook/*" \
    -x "data/.DS_Store" \
    -x "*/.ipynb_checkpoints/*"

# 関数コードの取得（オプション）
echo "Getting Lambda function code location..."
aws lambda get-function \
    --function-name vook_db_lambda_rakuten \
    --query 'Code.Location' \
    --output text

# Lambda 関数コードの更新
echo "Updating Lambda function code..."
aws lambda update-function-code \
    --function-name vook_db_lambda_rakuten \
    --zip-file fileb://$ZIP_FILE
