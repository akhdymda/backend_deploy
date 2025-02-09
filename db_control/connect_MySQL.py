from sqlalchemy import create_engine
import pymysql
import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy.engine.url import URL

# 環境変数の読み込み
base_path = Path(__file__).parents[1] #backendへのディレクトリパス
env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)

# データベース接続情報
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# SSL証明書のパス
ssl_cert = str(base_path / 'DigiCertGlobalRootG2.crt.pem')

#DATABASE_URL = URL.create(
#drivername = 'mysql+pymysql',
#username = os.getenv('DB_USER'),
#password = os.getenv('DB_PASSWORD'),
#host = os.getenv('DB_HOST'),
#port = os.getenv('DB_PORT'),
#database = os.getenv('DB_NAME'))

# MySQLのURL構築
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# エンジンの作成
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ssl_ca":ssl_cert
        }
    },
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)

print("Current working directory:", os.getcwd())
print("Certificate file exists:", os.path.exists('DigiCertGlobalRootCA.crt.pem'))