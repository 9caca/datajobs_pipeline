import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
import re


class JobBankScraper(BaseScraper):
    """
    Scraper específico para o site Job Bank do Canadá.
    """
    
    def __init__(self, search_term="data engineer"):
        """
        Inicializa o scraper do Job Bank
        
        Args:
            search_term (str): Termo de busca para vagas
        """
        super().__init__(search_term=search_term, base_url="https://www.jobbank.gc.ca")
    
    def build_search_url(self):
        """Cria a URL de busca para o Job Bank"""
        return f"{self.base_url}/jobsearch/jobsearch?searchstring={self.search_term.replace(' ', '+')}"
    
    def extract_job_listings(self, soup):
        """Extrai a lista de vagas da página de resultados"""
        return soup.find_all("a", class_="resultJobItem")
    
    def extract_job_details_from_listing(self, job):
        """Extrai informações básicas de um item de vaga na página de resultados"""
        title = job.find("span", class_="noctitle").get_text(strip=True)
        company = job.find("li", class_="business").get_text(strip=True)

        location_tag = job.find("li", class_="location")
        location = location_tag.get_text(strip=True).replace("Location", "") if location_tag else "Not specified"

        remote_tag = job.find("span", class_="telework")
        if remote_tag and "Remote" in remote_tag.get_text(strip=True):
            location = "Remote"

        date_posted = job.find("li", class_="date").get_text(strip=True)
        job_type = "Remote" if location == "Remote" else "On-site"
        link = self.base_url + job["href"]
        
        return {
            "title": title,
            "company": company,
            "location": location,
            "date_posted": date_posted,
            "job_type": job_type,
            "link": link
        }
    
    def extract_salary_range(self, soup):
        """Extrai faixa salarial da página individual"""
        try:
            salary_tag = soup.find("span", {"property": "baseSalary", "typeof": "MonetaryAmount"})
            if not salary_tag:
                return "Not specified"
            
            min_value = salary_tag.find("span", {"property": "minValue"})
            max_value = salary_tag.find("span", {"property": "maxValue"})
            unit_text = salary_tag.find("span", {"property": "unitText"})
            
            if not min_value or not max_value or not unit_text:
                return "Not specified"
            
            min_value = min_value.text.strip()
            max_value = max_value.text.strip()
            unit_text = unit_text.get("class", ["HOUR"])[0]
            
            if unit_text == "HOUR":
                return f"${min_value} to ${max_value} hourly"
            elif unit_text == "YEAR":
                return f"${min_value} to ${max_value} yearly"
            else:
                return f"${min_value} to ${max_value} {unit_text.lower()}"
        except Exception as e:
            self.logger.error(f"Erro ao extrair faixa salarial: {e}")
            return "Not specified"
    
    def extract_experience(self, soup):
        """Extrai experiência requerida"""
        experience_section = soup.find("h4", text="Experience")
        if experience_section and experience_section.find_next("p"):
            return experience_section.find_next("p").text.strip()
        return "Not specified"
    
    def extract_work_setting(self, soup):
        """Extrai configuração de trabalho"""
        try:
            # Verificar se é remoto
            remote_tag = soup.find("span", text="Remote")
            if remote_tag:
                return "Remote"
            
            # Verificar outras configurações
            work_setting_tag = soup.find("h4", text="Work setting")
            if work_setting_tag:
                ul_tag = work_setting_tag.find_next("ul")
                if ul_tag:
                    settings = [li.text.strip() for li in ul_tag.find_all("li")]
                    return ", ".join(settings)
            
            return "Not specified"
        except Exception as e:
            self.logger.error(f"Erro ao extrair configuração de trabalho: {e}")
            return "Not specified"
    
    def extract_tasks(self, soup):
        """Extrai tarefas principais"""
        tasks_tag = soup.find("h4", text="Tasks")
        if tasks_tag and tasks_tag.find_next("ul"):
            return [li.text.strip() for li in tasks_tag.find_next("ul").find_all("li")]
        return []
    
    def extract_technologies(self, soup):
        """Extrai tecnologias e ferramentas"""
        tech_tag = soup.find("h4", text="Computer and technology knowledge")
        if tech_tag and tech_tag.find_next("ul"):
            return [li.text.strip() for li in tech_tag.find_next("ul").find_all("li")]
        return []
    
    def extract_job_id(self, soup, job_url=None, job_info=None):
        """Extrai o ID da vaga, procurando por qualquer padrão #número"""
        try:
            # Procura por qualquer string que contenha um # seguido de números
            for string in soup.stripped_strings:
                match = re.search(r'#(\d+)', string)
                if match:
                    return match.group(1)  # Retorna apenas os dígitos após o #
            
            # Fallback: Se não encontrar um ID específico, gera um hash baseado em outros campos
            if not job_info:
                job_info = {}
            
            # Use informações disponíveis para criar um identificador único
            unique_parts = []
            if 'title' in job_info and job_info['title']:
                unique_parts.append(job_info['title'])
            if 'company' in job_info and job_info['company']:
                unique_parts.append(job_info['company'])
            if 'location' in job_info and job_info['location']:
                unique_parts.append(job_info['location'])
            if 'link' in job_info and job_info['link']:
                unique_parts.append(job_info['link'])
                
            if unique_parts:
                import hashlib
                unique_string = "_".join(unique_parts)
                return hashlib.md5(unique_string.encode()).hexdigest()
            
            # Se não houver informações suficientes, gera um hash baseado na URL
            if job_url:
                import hashlib
                return hashlib.md5(job_url.encode()).hexdigest()
            
            # Se não houver URL, retorna None
            return None
        except Exception as e:
            self.logger.error(f"Erro ao extrair ID da vaga: {e}")
            return None
    
    def get_job_details(self, job_url):
        """Obtém detalhes de uma vaga específica a partir da URL da vaga"""
        try:
            job_response = requests.get(job_url, headers=self.headers)
            if job_response.status_code != 200:
                self.logger.error(f"Erro ao acessar página individual da vaga {job_url}: {job_response.status_code}")
                return None
                
            job_soup = BeautifulSoup(job_response.text, "html.parser")
            
            job_id = self.extract_job_id(job_soup, job_url=job_url)
            
            details = {
                "job_id": job_id,  # Adicionando o ID como campo
                "salary_range": self.extract_salary_range(job_soup),
                "experience_required": self.extract_experience(job_soup),
                "work_setting": self.extract_work_setting(job_soup),
                "tasks": self.extract_tasks(job_soup),
                "technologies": self.extract_technologies(job_soup)
            }
            
            return details
        except Exception as e:
            self.logger.error(f"Erro ao obter detalhes da vaga {job_url}: {e}")
            return None