import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as credenciais do .env

def get_db_connection():
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