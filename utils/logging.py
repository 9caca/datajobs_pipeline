import logging
import os
from datetime import datetime


def setup_logging(log_dir="logs"):
    """
    Configura o sistema de logging para o projeto.
    
    Args:
        log_dir (str): Diretório onde os logs serão armazenados
        
    Returns:
        logging.Logger: Logger configurado
    """
    # Criar diretório de logs se não existir
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Nome do arquivo de log baseado na data
    log_filename = f"{log_dir}/datajobs_pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Configuração do logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()  # Exibe logs no console também
        ]
    )
    
    # Logger raiz
    logger = logging.getLogger()
    logger.info(f"Logging inicializado. Arquivo de log: {log_filename}")
    
    return logger
