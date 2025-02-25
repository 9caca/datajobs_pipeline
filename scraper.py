import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime
import re
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configurações de conexão com o banco de dados a partir das variáveis de ambiente
db_params = {
    "host": "localhost",
    "port": "5432",
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

# Função para conectar ao banco de dados
def connect_to_db():
    try:
        conn = psycopg2.connect(**db_params)
        print("Conexão com o banco de dados bem-sucedida!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para inserir uma empresa no banco de dados (ou obter o ID se já existir)
def insert_or_get_company(conn, company_name, location):
    cursor = conn.cursor()
    
    # Verifica se a empresa já existe
    cursor.execute("SELECT id FROM companies WHERE name = %s", (company_name,))
    result = cursor.fetchone()
    
    if result:
        return result[0]  # Retorna o ID da empresa existente
    else:
        # Insere a nova empresa
        cursor.execute(
            "INSERT INTO companies (name, location) VALUES (%s, %s) RETURNING id",
            (company_name, location)
        )
        company_id = cursor.fetchone()[0]
        conn.commit()
        return company_id

# Função para inserir uma vaga de trabalho no banco de dados
def insert_job(conn, title, company_id, location, salary_range, job_type, date_posted, source, link):
    cursor = conn.cursor()
    
    # Converte a data de texto para objeto date
    # Exemplo de formato: "Date posted: 11 February 2025"
    date_match = re.search(r'(\d+)\s+([A-Za-z]+)\s+(\d{4})', date_posted)
    if date_match:
        day, month_name, year = date_match.groups()
        
        # Traduz nomes de meses em inglês para português, se necessário
        month_names = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }
        
        month_num = month_names.get(month_name, 1)  # Padrão para janeiro se não encontrar
        formatted_date = f"{year}-{month_num:02d}-{int(day):02d}"
        date_obj = datetime.strptime(formatted_date, '%Y-%m-%d').date()
    else:
        # Se não conseguir extrair a data, usa a data atual
        date_obj = datetime.now().date()
    
    try:
        # Insere a vaga
        cursor.execute(
            """
            INSERT INTO jobs (title, company_id, location, salary_range, job_type, date_posted, source, link, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING id
            """,
            (title, company_id, location, salary_range, job_type, date_obj, source, link)
        )
        job_id = cursor.fetchone()[0]
        conn.commit()
        return job_id
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir vaga: {e}")
        return None

# URL da busca no Job Bank para Halifax
url = "https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=data+engineer&location=Halifax"

# Conectar ao banco de dados
conn = connect_to_db()
if not conn:
    print("Não foi possível conectar ao banco de dados. Encerrando.")
    exit(1)

# Faz a requisição HTTP para obter o HTML da página
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("a", class_="resultJobItem")
    seen_links = set()  # Para evitar duplicatas
    
    job_count = 0

    for job in jobs:
        title = job.find("span", class_="noctitle").text.strip()
        company = job.find("li", class_="business").text.strip()

        # Verifica se é remoto
        remote_tag = job.find("span", class_="telework")
        is_remote = remote_tag and "Remote" in remote_tag.text

        # Obtém a localização
        location_tag = job.find("li", class_="location")
        location = location_tag.text.replace("Location", "").strip() if location_tag else "Not specified"

        # Se for remoto, sobrescrevemos a localização
        if is_remote:
            location = "Remote"

        # Filtrar apenas Halifax e Remote
        if location != "Halifax (NS)" and location != "Remote":
            continue  # Pula a vaga se não for de interesse

        # Obtém o salário
        salary_tag = job.find("li", class_="salary")
        salary = salary_tag.text.replace("Salary:", "").strip() if salary_tag else "Not specified"

        # Obtém a data de postagem
        date_posted = job.find("li", class_="date").text.strip()

        # Método de aplicação
        apply_method_tag = job.find("span", class_="appmethod")
        apply_method = apply_method_tag.text.strip() if apply_method_tag else "Not specified"

        # Link da vaga
        link = "https://www.jobbank.gc.ca" + job["href"]

        # Evita duplicatas
        if link in seen_links:
            continue
        seen_links.add(link)

        # Determina o tipo de trabalho (simplificado)
        job_type = "Remote" if is_remote else "On-site"

        # Exibindo os dados formatados
        print(f"Title: {title}")
        print(f"Company: {company}")
        print(f"Location: {location}")
        print(f"Salary: {salary}")
        print(f"Date Posted: {date_posted}")
        print(f"Apply Method: {apply_method}")
        print(f"Link: {link}")
        
        # Inserir dados no banco de dados
        try:
            # Primeiro insere ou obtém a empresa
            company_id = insert_or_get_company(conn, company, location)
            
            # Depois insere a vaga
            job_id = insert_job(
                conn, 
                title, 
                company_id, 
                location, 
                salary, 
                job_type, 
                date_posted, 
                "Job Bank", 
                link
            )
            
            if job_id:
                print(f"Vaga inserida com sucesso! ID: {job_id}")
                job_count += 1
            else:
                print("Falha ao inserir a vaga.")
        except Exception as e:
            print(f"Erro durante o processamento da vaga: {e}")
        
        print("-" * 50)
    
    print(f"Total de vagas inseridas: {job_count}")

else:
    print("Failed to retrieve job listings. Status code:", response.status_code)

# Fechar a conexão com o banco
if conn:
    conn.close()
    print("Conexão com o banco de dados fechada.")