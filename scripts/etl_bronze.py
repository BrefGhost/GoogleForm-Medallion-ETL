import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB = os.getenv("POSTGRES_DB")
PORT = os.getenv("POSTGRES_PORT")
HOST = "localhost"

db_url = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
engine = create_engine(db_url)

def load_bronze():
    file_path = "data/google_form_raw.csv"

    print("กำลังอ่านข้อมูลดิบจาก CSV...")
    df_raw = pd.read_csv(file_path)

    print("กำลังส่งข้อมูลเข้า Bronze Layer (PostgreSQL)...")
    df_raw.to_sql("bronze_google_forms", con=engine, if_exists="replace", index=False)

    print("โหลดข้อมูลเข้า Bronze Layer สำเร็จเรียบร้อย!")

if __name__ == "__main__":
    load_bronze()

