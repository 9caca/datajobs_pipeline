import requests
from bs4 import BeautifulSoup
import psycopg2
import logging
from utils.logging import setup_logging  # Importa configuração de logs
from database.db import get_db_connection  # Função para conectar ao PostgreSQL

# Configura os logs
setup_logging()
logger = logging.getLogger(__name__)

# URL da busca no Job Bank para Halifax
url = "https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=data+engineer&locationstring=&locationparam=&sort=M"

# Faz a requisição HTTP para obter o HTML da página
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("a", class_="resultJobItem")

    conn = get_db_connection()
    cursor = conn.cursor()

    for job in jobs:
        try:
            title = job.find("span", class_="noctitle").text.strip()
            company_name = job.find("li", class_="business").text.strip()

            # Obtém a data de postagem
            date_posted = job.find("li", class_="date").text.strip()

            # Obtém a localização
            location_tag = job.find("li", class_="location")
            location = location_tag.text.replace("Location", "").strip() if location_tag else "Not specified"

            # Verifica se é remoto
            remote_tag = job.find("span", class_="telework")
            is_remote = remote_tag and "Remote" in remote_tag.text
            if is_remote:
                location = "Remote"

            # Obtém o salário
            salary_tag = job.find("li", class_="salary")
            salary_range = salary_tag.text.replace("Salary:", "").strip() if salary_tag else None

            # Obtém o link da vaga
            link = "https://www.jobbank.gc.ca" + job["href"]

            # Faz uma requisição à página detalhada para obter mais informações
            job_detail_response = requests.get(link)
            job_detail_soup = BeautifulSoup(job_detail_response.content, "html.parser")

            # Extrai a experiência requerida
            experience_element = job_detail_soup.find("p", property="experienceRequirements qualification")
            experience_required = None
            if experience_element:
                experience_required = experience_element.text.strip()

            # Verifica se já existe essa vaga no banco de dados
            cursor.execute("""
                SELECT id FROM jobs
                WHERE title = %s AND company_id = (
                    SELECT id FROM companies WHERE name = %s
                ) AND date_posted = %s
            """, (title, company_name, date_posted))

            existing_job = cursor.fetchone()
            if existing_job:
                logger.info(f"Job '{title}' from {company_name} on {date_posted} already exists. Skipping...")
                continue  # Pula a inserção

            # Busca ou insere a empresa no banco
            cursor.execute("SELECT id FROM companies WHERE name = %s", (company_name,))
            company_id = cursor.fetchone()
            if not company_id:
                cursor.execute("INSERT INTO companies (name) VALUES (%s) RETURNING id", (company_name,))
                company_id = cursor.fetchone()[0]
            else:
                company_id = company_id[0]

            # Insere a vaga na tabela jobs
            cursor.execute("""
                INSERT INTO jobs (title, company_id, location, salary_range, date_posted, source, link, work_setting, experience_required)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (title, company_id, location, salary_range, date_posted, "Job Bank", link, "Remote" if is_remote else "On-site", experience_required))

            job_id = cursor.fetchone()[0]
                # Extrai as tarefas/responsabilidades
            tasks_div = job_detail_soup.find("div", property="responsibilities")
            if tasks_div:
                tasks_list = tasks_div.find_all("li")
                for task_item in tasks_list:
                    task_text = task_item.find("span").text.strip()
                    # Insere cada tarefa na tabela job_tasks
                    cursor.execute("""
                        INSERT INTO job_tasks (job_id, task)
                        VALUES (%s, %s)
                    """, (job_id, task_text))
            
            # Extrai os requisitos de conhecimento
            requirements_div = job_detail_soup.find("div", property="experienceRequirements")
            if requirements_div:
                tech_knowledge_header = requirements_div.find("h4", string="Computer and technology knowledge")
                if tech_knowledge_header:
                    req_list = tech_knowledge_header.find_next("ul").find_all("li")
                    for req_item in req_list:
                        req_text = req_item.find("span").text.strip()
                        
                        # Verifica se o requisito já existe na tabela requirements
                        cursor.execute("SELECT id FROM requirements WHERE name = %s", (req_text,))
                        req_id = cursor.fetchone()
                        
                        if not req_id:
                            # Insere o novo requisito
                            cursor.execute("""
                                INSERT INTO requirements (name, category)
                                VALUES (%s, %s) RETURNING id
                            """, (req_text, "Technology"))
                            req_id = cursor.fetchone()[0]
                        else:
                            req_id = req_id[0]
                        
                        # Associa o requisito à vaga
                        cursor.execute("""
                            INSERT INTO job_requirements (job_id, requirement_id)
                            VALUES (%s, %s)
                        """, (job_id, req_id))
            conn.commit()
            logger.info(f"Job '{title}' from {company_name} inserted successfully.")

        except Exception as e:
            logger.error(f"Error processing job: {e}")
            conn.rollback()  # Reverte a transação para evitar problemas

    cursor.close()
    conn.close()

else:
    logger.error(f"Failed to retrieve job listings. Status code: {response.status_code}")
