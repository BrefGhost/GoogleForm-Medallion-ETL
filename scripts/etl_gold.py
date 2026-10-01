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

def build_gold_layer():
    print(" 1. อ่านข้อมูลที่คลีนแล้วจาก Silver Layer...")
    df_silver = pd.read_sql("SELECT * FROM silver_google_forms", con=engine)

    print(" 2. คำนวณค่าสถิติ (Aggregation) สำหรับ Business...")

    df_silver['Satisfaction Score'] = pd.to_numeric(df_silver['Satisfaction Score'], errors='coerce')

    df_gold = df_silver.groupby('Faculty').agg(
        Total_Responses=('Email', 'count'),
        Avg_Satisfaction=('Satisfaction Score', 'mean')
    ).reset_index()

    df_gold['Avg_Satisfaction'] = df_gold['Avg_Satisfaction'].round(2)

    print(" 3. ส่งข้อมูลสรุปผลเข้า Gold Layer (PostgreSQL)...")
    df_gold.to_sql("gold_faculty_summary", con=engine, if_exists="replace", index=False)

    print("\n---  สรุปข้อมูลใน Gold Layer  ---")
    print(df_gold.to_string(index=False))
    print("\n โหลดข้อมูลเข้า Gold Layer เรียบร้อยแล้ว!")

if __name__ == "__main__":
    build_gold_layer()