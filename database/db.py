import psycopg2
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_db_connection():
    if hasattr(st, 'secrets') and 'postgres' in st.secrets:
        return psycopg2.connect(
            dbname=st.secrets.postgres.DB_NAME,
            user=st.secrets.postgres.DB_USER,
            password=st.secrets.postgres.DB_PASSWORD,
            host=st.secrets.postgres.DB_HOST,
            port=st.secrets.postgres.DB_PORT
        )
    else:
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

def insert_job(title, company_id, location, salary_range, date_posted, link, is_remote, experience_required):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO jobs (title, company_id, location, salary_range, date_posted, source, link, work_setting, experience_required)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (title, company_id, location, salary_range, date_posted, "Job Bank", link, "Remote" if is_remote else "On-site", experience_required))
        
        job_id = cursor.fetchone()[0]
        conn.commit()
        return job_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()