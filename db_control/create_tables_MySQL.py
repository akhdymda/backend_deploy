from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base,sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv

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

# Baseクラスの作成
Base = declarative_base()

# テーブル定義
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(10), unique=True, nullable=False)
    customer_name = Column(String(100), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))

    def __repr__(self):
        return f"<Customer(customer_id='{self.customer_id}', name='{self.customer_name}')>"

# テーブル作成
Base.metadata.create_all(engine)

# セッション作成
Session = sessionmaker(bind=engine)
session = Session()

def add_test_data():
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM customers"))
        connection.commit()

    test_customers = [
        Customer(customer_id="C1111", customer_name="aaa", age=6, gender="男"),
        Customer(customer_id="C110", customer_name="浦島太郎", age=10, gender="女")
    ]

    for customer in test_customers:
        session.add(customer)
    
    try:
        session.commit()
        print("テストデータを追加しました")
    except Exception as e:
        session.rollback()
        print(f"エラーが発生しました:{e}")
    finally:
        session.close()
    
if __name__ == "__main__":
    add_test_data()


# def init_db():
    # インスペクターを作成
    # inspector = inspect(engine)

    # 既存のテーブルを取得
    # existing_tables = inspector.get_table_names()

    # print("Checking tables...")

    # customersテーブルが存在しない場合は作成
    # if 'customers' not in existing_tables:
        #print("Creating tables >>> ")
        #try:
            #Base.metadata.create_all(bind=engine)
            #print("Tables created successfully!")
        #except Exception as e:
            #print(f"Error creating tables: {e}")
            #raise
    #else:
        #print("Tables already exist.")


