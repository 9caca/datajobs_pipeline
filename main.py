import os
import argparse
from dotenv import load_dotenv
from utils.logging import setup_logging
from database.db import DatabaseManager
from scraper.jobbank import JobBankScraper

def main():
    """
    Função principal que orquestra o pipeline de extração de vagas
    """
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Configurar logging
    logger = setup_logging()
    
    # Configurar argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Data Jobs Pipeline - Extração e armazenamento de vagas de emprego')
    parser.add_argument('--sources', nargs='+', choices=['jobbank', 'linkedin', 'indeed', 'all'], 
                        default=['all'], help='Fontes para extrair vagas')
    parser.add_argument('--search', type=str, default="data engineer",
                        help='Termo de busca para vagas')
    
    args = parser.parse_args()
    
    # Definir fontes a serem utilizadas
    sources = args.sources
    if 'all' in sources:
        sources = ['jobbank', 'linkedin', 'indeed']
    
    # Inicializar banco de dados
    db_manager = DatabaseManager()
    if not db_manager.connect():
        logger.error("Não foi possível conectar ao banco de dados. Encerrando.")
        return 1
    
    try:
        # Executar scrapers selecionados
        search_term = args.search
        total_jobs = 0
        
        logger.info(f"Iniciando extração de vagas para '{search_term}' das fontes: {', '.join(sources)}")
        
        # Job Bank
        if 'jobbank' in sources:
            logger.info("Iniciando scraper do Job Bank...")
            jobbank_scraper = JobBankScraper(search_term=search_term)
            jobbank_scraper.run(db_manager)
            total_jobs += jobbank_scraper.job_count
            logger.info(f"Job Bank: {jobbank_scraper.job_count} vagas extraídas")
        
        logger.info(f"Pipeline concluído. Total de {total_jobs} vagas extraídas e armazenadas.")
        return 0
        
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")
        return 1
    
if __name__ == "__main__":
    print("Script iniciando...")
    main()
    print("Script finalizado.")