import psycopg2
import os
import logging
from datetime import datetime


class DatabaseManager:
    """
    Gerencia todas as operações relacionadas ao banco de dados.
    """
    
    def __init__(self):
        """Inicializa o gerenciador de banco de dados"""
        self.logger = logging.getLogger(__name__)
        self.conn = None
        self.db_params = {
            "host": "localhost",
            "port": "5432",
            "database": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD")
        }
    
    def connect(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.conn = psycopg2.connect(**self.db_params)
            self.logger.info("Conexão com o banco de dados bem-sucedida!")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao conectar ao banco de dados: {e}")
            return False
    
    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
            self.logger.info("Conexão com o banco de dados fechada.")
    
    def job_exists(self, external_id):
        """Verifica se uma vaga já existe no banco de dados pelo ID externo"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM jobs WHERE external_id = %s", (external_id,))
        result = cursor.fetchone()
        return result is not None
    
    def insert_or_get_company(self, company_name, location):
        """Insere ou obtém ID da empresa"""
        if not self.conn:
            return None
            
        cursor = self.conn.cursor()
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
            self.conn.commit()
            return company_id
    
    def parse_date(self, date_posted):
        """Extrai e formata a data de postagem da vaga"""
        import re
        
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
            return datetime.strptime(formatted_date, '%Y-%m-%d').date()
        else:
            return datetime.now().date()
    
    def insert_job(self, job_id, title, company_id, location, salary_range, job_type, 
              date_posted, source, link, experience_required, work_setting):
        """Insere uma vaga no banco de dados"""
        if not self.conn:
            return None
            
        # Verifica se a vaga já existe pelo job_id (ID externo)
        if job_id and self.job_exists(job_id):
            self.logger.info(f"Vaga com ID externo {job_id} já existe no banco de dados.")
            # Opcionalmente, recuperar e retornar o ID interno
            cursor = self.conn.cursor()
            cursor.execute("SELECT id FROM jobs WHERE job_id = %s", (job_id,))
            return cursor.fetchone()[0]
            
        cursor = self.conn.cursor()
        
        # Extrai data de postagem
        date_obj = self.parse_date(date_posted)  # Adicionado aqui

        # Insere a vaga deixando o ID ser gerado automaticamente
        cursor.execute("""
            INSERT INTO jobs (job_id, title, company_id, location, salary_range, 
                        job_type, date_posted, source, link, experience_required, work_setting)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (job_id, title, company_id, location, salary_range, job_type, date_obj,  # Usando date_obj aqui
            source, link, experience_required, work_setting))
        
        result = cursor.fetchone()
        self.conn.commit()
        return result[0]  # Retorna o ID interno gerado
    
    def insert_tasks(self, job_id, tasks):
        """Insere tarefas associadas a uma vaga"""
        if not self.conn:
            return False
            
        cursor = self.conn.cursor()
        for task in tasks:
            try:
                cursor.execute(
                    "INSERT INTO job_tasks (job_id, task) VALUES (%s, %s)",
                    (job_id, task)
                )
            except Exception as e:
                self.conn.rollback()
                self.logger.error(f"Erro ao inserir tarefa {task}: {e}")
                return False
        
        self.conn.commit()
        return True
    
    def insert_technologies(self, job_id, technologies):
        """Insere tecnologias associadas a uma vaga"""
        if not self.conn:
            return False
            
        cursor = self.conn.cursor()
        for tech in technologies:
            try:
                cursor.execute(
                    "INSERT INTO job_technologies (job_id, technology) VALUES (%s, %s)",
                    (job_id, tech)
                )
            except Exception as e:
                self.conn.rollback()
                self.logger.error(f"Erro ao inserir tecnologia {tech}: {e}")
                return False
        
        self.conn.commit()
        return True
