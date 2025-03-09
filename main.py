import sys
from utils.logging import setup_logging
import logging

setup_logging()
logger = logging.getLogger("job_scraper")

from scrapers.jobbank import scrape_jobbank

def main():
    try:
        logger.info("Iniciando scraper do JobBank")
        jobs_count = scrape_jobbank()
        logger.info(f"JobBank scraper concluído - {jobs_count} vagas processadas")        
        logger.info("Todos os scrapers executados com sucesso")
    except Exception as e:
        logger.error(f"Erro ao executar scrapers: {e}")

if __name__ == "__main__":
    main()