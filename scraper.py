import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime
import re
import os
import logging
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    filename="datajobs_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Carrega variáveis do arquivo .env
load_dotenv()

# Configurações do banco de dados
db_params = {
    "host": "localhost",
    "port": "5432",
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

# Conectar ao banco de dados
def connect_to_db():
    try:
        conn = psycopg2.connect(**db_params)
        logging.info("Conexão com o banco de dados bem-sucedida!")
        return conn
    except Exception as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Verificar se a vaga já existe no banco de dados
def job_exists(conn, link):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jobs WHERE link = %s", (link,))
    return cursor.fetchone() is not None

# Inserir ou obter ID da empresa
def insert_or_get_company(conn, company_name, location):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM companies WHERE name = %s", (company_name,))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        cursor.execute(
            "INSERT INTO companies (name, location) VALUES (%s, %s) RETURNING id",
            (company_name, location)
        )
        company_id = cursor.fetchone()[0]
        conn.commit()
        return company_id

# Extrair faixa salarial da página individual
def extract_salary_range(soup):
    salary_tag = soup.find("span", {"property": "baseSalary", "typeof": "MonetaryAmount"})
    if not salary_tag:
        return "Not specified"
    
    try:
        min_value = salary_tag.find("span", {"property": "minValue"}).text.strip()
        max_value = salary_tag.find("span", {"property": "maxValue"}).text.strip()
        unit_text = salary_tag.find("span", {"property": "unitText"}).get("class", ["HOUR"])[0]
        
        if unit_text == "HOUR":
            return f"${min_value} to ${max_value} hourly"
        elif unit_text == "YEAR":
            return f"${min_value} to ${max_value} yearly"
        else:
            return f"${min_value} to ${max_value} {unit_text.lower()}"
    except Exception as e:
        logging.error(f"Erro ao extrair faixa salarial: {e}")
        return "Not specified"

# Extrair experiência requerida
def extract_experience(soup):
    experience_section = soup.find("h4", text="Experience")
    if experience_section and experience_section.find_next("p"):
        return experience_section.find_next("p").text.strip()
    return "Not specified"

# Extrair configuração de trabalho
def extract_work_setting(soup):
    # Verificar se é remoto
    remote_tag = soup.find("span", text="Remote")
    if remote_tag:
        return "Remote"
    
    # Verificar outras configurações
    work_setting_tag = soup.find("h4", text="Work setting")
    if work_setting_tag and work_setting_tag.find_next("ul"):
        settings = [li.text.strip() for li in work_setting_tag.find_next("ul").find_all("li")]
        return ", ".join(settings)
    
    return "Not specified"

# Extrair tarefas principais
def extract_tasks(soup):
    tasks_tag = soup.find("h4", text="Tasks")
    if tasks_tag and tasks_tag.find_next("ul"):
        return [li.text.strip() for li in tasks_tag.find_next("ul").find_all("li")]
    return []

# Extrair tecnologias e ferramentas
def extract_technologies(soup):
    tech_tag = soup.find("h4", text="Computer and technology knowledge")
    if tech_tag and tech_tag.find_next("ul"):
        return [li.text.strip() for li in tech_tag.find_next("ul").find_all("li")]
    return []

# Inserir tarefas no banco de dados
def insert_tasks(conn, job_id, tasks):
    cursor = conn.cursor()
    for task in tasks:
        try:
            cursor.execute(
                "INSERT INTO job_tasks (job_id, task) VALUES (%s, %s)",
                (job_id, task)
            )
        except Exception as e:
            conn.rollback()
            logging.error(f"Erro ao inserir tarefa {task}: {e}")
            return False
    
    conn.commit()
    return True

# Inserir tecnologias no banco de dados
def insert_technologies(conn, job_id, technologies):
    cursor = conn.cursor()
    for tech in technologies:
        try:
            cursor.execute(
                "INSERT INTO job_technologies (job_id, technology) VALUES (%s, %s)",
                (job_id, tech)
            )
        except Exception as e:
            conn.rollback()
            logging.error(f"Erro ao inserir tecnologia {tech}: {e}")
            return False
    
    conn.commit()
    return True

# Inserir vaga no banco de dados
def insert_job(conn, title, company_id, location, salary_range, job_type, date_posted, 
               source, link, experience_required, work_setting):
    cursor = conn.cursor()
    
    # Extrai data de postagem
    date_match = re.search(r'(\d+)\s+([A-Za-z]+)\s+(\d{4})', date_posted)
    month_names = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }
    
    if date_match:
        day, month_name, year = date_match.groups()
        month_num = month_names.get(month_name, 1)
        formatted_date = f"{year}-{month_num:02d}-{int(day):02d}"
        date_obj = datetime.strptime(formatted_date, '%Y-%m-%d').date()
    else:
        date_obj = datetime.now().date()

    try:
        cursor.execute(
            """
            INSERT INTO jobs (title, company_id, location, salary_range, job_type, date_posted, 
                             source, link, created_at, experience_required, work_setting)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s)
            RETURNING id
            """,
            (title, company_id, location, salary_range, job_type, date_obj, 
             source, link, experience_required, work_setting)
        )
        job_id = cursor.fetchone()[0]
        conn.commit()
        logging.info(f"Vaga inserida com sucesso! ID: {job_id}")
        return job_id
    except Exception as e:
        conn.rollback()
        logging.error(f"Erro ao inserir vaga: {e}")
        return None

# URL da busca no Job Bank para todo o Canadá
url = "https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=data+engineer"
headers = {"User-Agent": "Mozilla/5.0"}

# Conectar ao banco de dados
conn = connect_to_db()
if not conn:
    logging.error("Não foi possível conectar ao banco de dados. Encerrando.")
    exit(1)

# Fazer requisição à página
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("a", class_="resultJobItem")
    seen_links = set()
    job_count = 0

    for job in jobs:
        title = job.find("span", class_="noctitle").get_text(strip=True)
        company = job.find("li", class_="business").get_text(strip=True)

        location_tag = job.find("li", class_="location")
        location = location_tag.get_text(strip=True).replace("Location", "") if location_tag else "Not specified"

        remote_tag = job.find("span", class_="telework")
        if remote_tag and "Remote" in remote_tag.get_text(strip=True):
            location = "Remote"

        date_posted = job.find("li", class_="date").get_text(strip=True)
        job_type = "Remote" if location == "Remote" else "On-site"
        link = "https://www.jobbank.gc.ca" + job["href"]
        
        # Evitar duplicatas
        if link in seen_links or job_exists(conn, link):
            logging.info(f"Vaga já processada ou duplicada: {title}")
            continue
        seen_links.add(link)

        try:
            # Acessar a página individual da vaga para obter detalhes adicionais
            job_response = requests.get(link, headers=headers)
            if job_response.status_code == 200:
                job_soup = BeautifulSoup(job_response.text, "html.parser")
                
                # Extrair informações adicionais
                salary_range = extract_salary_range(job_soup)
                experience_required = extract_experience(job_soup)
                work_setting = extract_work_setting(job_soup)
                tasks = extract_tasks(job_soup)
                technologies = extract_technologies(job_soup)
                
                # Inserir empresa e vaga no banco de dados
                company_id = insert_or_get_company(conn, company, location)
                job_id = insert_job(
                    conn, title, company_id, location, salary_range, job_type, 
                    date_posted, "Job Bank", link, experience_required, work_setting
                )
                
                # Inserir tarefas e tecnologias
                if job_id:
                    if tasks:
                        insert_tasks(conn, job_id, tasks)
                    if technologies:
                        insert_technologies(conn, job_id, technologies)
                    job_count += 1
                    logging.info(f"Processada vaga {title} com {len(tasks)} tarefas e {len(technologies)} tecnologias")
            else:
                logging.error(f"Erro ao acessar página individual da vaga {title}: {job_response.status_code}")
        
        except Exception as e:
            logging.error(f"Erro ao processar vaga {title}: {e}")

    logging.info(f"Total de vagas inseridas: {job_count}")

else:
    logging.error(f"Falha ao recuperar vagas. Status code: {response.status_code}")

# Fechar conexão com o banco
if conn:
    conn.close()
    logging.info("Conexão com o banco de dados fechada.")