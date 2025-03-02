import logging
import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class BaseScraper(ABC):
    """
    Classe base para todos os scrapers de vagas.
    Define a interface e funcionalidades comuns que todos os scrapers devem implementar.
    """
    
    def __init__(self, search_term="data engineer", base_url=None):
        """
        Inicializa o scraper com configurações padrão
        
        Args:
            search_term (str): Termo de busca para vagas
            base_url (str): URL base do site
        """
        # Configurações de scraping
        self.search_term = search_term
        self.base_url = base_url
        self.headers = {"User-Agent": "Mozilla/5.0"}
        
        # Contadores e controle
        self.seen_links = set()
        self.job_count = 0
        self.logger = logging.getLogger(__name__)
    
    @abstractmethod
    def build_search_url(self):
        """
        Cria a URL de busca específica para o site.
        Deve ser implementado por cada scraper específico.
        """
        pass
    
    @abstractmethod
    def extract_job_listings(self, page_content):
        """
        Extrai a lista de vagas da página de resultados.
        
        Args:
            page_content: Conteúdo HTML da página de resultados
            
        Returns:
            list: Lista de elementos HTML/objetos que representam vagas
        """
        pass
    
    @abstractmethod
    def extract_job_details_from_listing(self, job_listing):
        """
        Extrai informações básicas de um item de vaga na página de resultados.
        
        Args:
            job_listing: Elemento HTML/objeto que representa uma vaga
            
        Returns:
            dict: Dicionário com informações básicas da vaga
        """
        pass
    
    @abstractmethod
    def get_job_details(self, job_url):
        """
        Obtém detalhes completos de uma vaga a partir da URL.
        
        Args:
            job_url (str): URL da página de detalhes da vaga
            
        Returns:
            dict: Dicionário com detalhes da vaga
        """
        pass
    
    def process_job_listing(self, job_listing, db_manager):
        """
        Processa uma listagem de vaga completa e salva no banco de dados.
        
        Args:
            job_listing: Elemento HTML/objeto que representa uma vaga
            db_manager: Instância do gerenciador de banco de dados
            
        Returns:
            bool: True se a vaga foi processada com sucesso, False caso contrário
        """
        job_info = self.extract_job_details_from_listing(job_listing)
        
        # Verifica se já foi processada
        if job_info["job_id"] in self.seen_job_ids or db_manager.job_exists(job_info["job_id"]):
            self.logger.info(f"Vaga já processada ou duplicada: {job_info['title']}")
            return False
        
        self.seen_job_ids.add(job_info["job_id"])
        
        # Obtém detalhes completos da vaga
        details = self.get_job_details(job_info["link"])
        if not details:
            return False
        
        # Combina informações básicas com detalhes
        job_data = {**job_info, **details}
        
        # Insere no banco de dados
        company_id = db_manager.insert_or_get_company(job_data["company"], job_data["location"])
        job_id = db_manager.insert_job(
            job_data["job_id"], job_data["title"], company_id, job_data["location"], 
            job_data["salary_range"], job_data["job_type"], job_data["date_posted"],
            self.__class__.__name__, job_data["link"], job_data["experience_required"], 
            job_data["work_setting"]
        )
        
        # Insere tarefas e tecnologias
        if job_id:
            if job_data["tasks"]:
                db_manager.insert_tasks(job_id, job_data["tasks"])
            if job_data["technologies"]:
                db_manager.insert_technologies(job_id, job_data["technologies"])
            
            self.job_count += 1
            self.logger.info(
                f"Processada vaga {job_data['title']} com {len(job_data['tasks'])} tarefas e "
                f"{len(job_data['technologies'])} tecnologias"
            )
            return True
        
        return False

    
    def run(self, db_manager):
        """
        Executa o processo completo de scraping.
        
        Args:
            db_manager: Instância do gerenciador de banco de dados
            
        Returns:
            bool: True se o processo foi concluído com sucesso, False caso contrário
        """
        try:
            search_url = self.build_search_url()
            self.logger.info(f"Iniciando scraping de {self.__class__.__name__} com URL: {search_url}")
            
            # Faz requisição à página de resultados
            response = requests.get(search_url, headers=self.headers)
            
            if response.status_code != 200:
                self.logger.error(f"Falha ao recuperar vagas. Status code: {response.status_code}")
                return False
            
            soup = BeautifulSoup(response.text, "html.parser")
            job_listings = self.extract_job_listings(soup)
            
            self.logger.info(f"Encontradas {len(job_listings)} vagas para processar")
            
            for job_listing in job_listings:
                try:
                    self.process_job_listing(job_listing, db_manager)
                except Exception as e:
                    self.logger.error(f"Erro ao processar vaga: {e}")
            
            self.logger.info(f"Total de vagas inseridas: {self.job_count}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro durante o scraping: {e}")
            return False
