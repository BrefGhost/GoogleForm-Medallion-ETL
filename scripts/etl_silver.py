import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB = os.getenv("POSTGRES_DB")
PORT = os.getenv("POSTGRES_PORT")
HOST = os.getenv("POSTGRES_HOST", "localhost")

db_url = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
engine = create_engine(db_url)

def clean_and_load_silver():
    print("1. อ่านข้อมูลดิบจาก Bronze Layer...")
    df_bronze = pd.read_sql("SELECT * FROM bronze_google_forms", con=engine)

    print("2. เริ่มกระบวนการ Data Cleaning...")

    string_cols = ['Full Name', 'Email', 'Faculty', 'Comments']
    for col in string_cols:
        df_bronze[col] = df_bronze[col].astype(str).str.strip()

    df_bronze['Full Name'] = df_bronze['Full Name'].str.title()
    df_bronze['Faculty'] = df_bronze['Faculty'].str.capitalize()
    df_bronze['Email'] = df_bronze['Email'].str.lower()

    df_bronze['Email'] = df_bronze['Email'].replace(['nan', 'none', ''], 'not_specified@email.com')
    df_bronze['Comments'] = df_bronze['Comments'].replace(['nan', 'none', ''], 'No comment')

    df_cleaned = df_bronze.drop_duplicates(subset=['Timestamp', 'Email'])

    print(f"คลีนข้อมูลสำเร็จ! เหลือข้อมูลทั้งหมด {len(df_cleaned)} รายการ (ลบแถวซ้ำออกแล้ว)")

    print("3. กำลังส่งข้อมูลเข้า Silver Layer (PostgreSQL)...")

    records = df_cleaned.to_dict(orient='records')
    buffer = []

    df_cleaned.iloc[0:0].to_sql("silver_google_forms", con=engine, if_exists="replace", index=False)

    BATCH_SIZE = 2

    for i, row in enumerate(records, start=1):
        buffer.append(row)

        if i % BATCH_SIZE == 0 or i == len(records):
            df_batch = pd.DataFrame(buffer)
            df_batch.to_sql("silver_google_forms", con=engine, if_exists="append", index=False)
            print(f" บันทึก Batch สำเร็จ! (สะสมรวม {i}/{len(records)} รายการ)")
            buffer = []

    print(" โหลดข้อมูลเข้า Silver Layer เรียบร้อยแล้ว!")

if __name__ == "__main__":
    clean_and_load_silver()