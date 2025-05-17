import os
from dotenv import load_dotenv
import pathlib

# .env ファイルのパスを取得（カレントディレクトリの .env）
dotenv_path = pathlib.Path(__file__).parent / '.env'

# .env ファイルから環境変数を読み込む
load_dotenv(dotenv_path=dotenv_path)

# AWS 認証情報
AWS_CONFIG = {
    'ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
    'SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'REGION_NAME': os.getenv('AWS_REGION_NAME', 'us-east-1')
}
