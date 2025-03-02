import re
from datetime import datetime


def parse_salary(salary_text):
    """
    Padroniza o formato de salário de diferentes fontes.
    
    Args:
        salary_text (str): Texto contendo informações de salário
        
    Returns:
        str: Salário formatado de maneira consistente
    """
    if not salary_text or salary_text.lower() == "not specified":
        return "Not specified"
    
    # Padronização para formato "$X to $Y period"
    try:
        # Extrai números do texto
        numbers = re.findall(r'\d+[.,]?\d*', salary_text)
        if len(numbers) >= 2:
            min_val = numbers[0]
            max_val = numbers[1]
            
            # Detecta período (anual, mensal, por hora)
            period = "hourly"
            if "year" in salary_text.lower() or "annual" in salary_text.lower():
                period = "yearly"
            elif "month" in salary_text.lower():
                period = "monthly"
            elif "week" in salary_text.lower():
                period = "weekly"
                
            return f"${min_val} to ${max_val} {period}"
        else:
            return salary_text
    except:
        return salary_text


def normalize_location(location):
    """
    Padroniza o formato de localização de diferentes fontes.
    
    Args:
        location (str): Texto contendo informações de localização
        
    Returns:
        str: Localização formatada de maneira consistente
    """
    if not location:
        return "Not specified"
    
    location = location.strip()
    
    # Verificar se é remoto
    if re.search(r'remote|home|remote work', location.lower()):
        return "Remote"
    
    # Remover palavras-chave desnecessárias
    location = re.sub(r'location\s*[:;-]?\s*', '', location, flags=re.IGNORECASE)
    
    return location.strip() or "Not specified"


def normalize_date(date_text):
    """
    Padroniza datas de diferentes formatos para ISO (YYYY-MM-DD).
    
    Args:
        date_text (str): Texto contendo data
        
    Returns:
        str: Data formatada no padrão ISO
    """
    if not date_text:
        return datetime.now().strftime('%Y-%m-%d')
    
    try:
        # Tenta diferentes formatos de data
        formats = [
            '%d %B %Y',           # 10 January 2023
            '%B %d, %Y',          # January 10, 2023
            '%Y-%m-%d',           # 2023-01-10
            '%d/%m/%Y',           # 10/01/2023
            '%m/%d/%Y',           # 01/10/2023
            '%d-%m-%Y',           # 10-01-2023
            '%Y/%m/%d'            # 2023/01/10
        ]
        
        for fmt in formats:
            try:
                date_obj = datetime.strptime(date_text, fmt)
                return date_obj.strftime('%Y-%m-%d')
            except:
                continue
        
        # Se não conseguir interpretar, tenta extrair com regex
        date_match = re.search(r'(\d+)\s+([A-Za-z]+)\s+(\d{4})', date_text)
        if date_match:
            day, month_name, year = date_match.groups()
            month_names = {
                "January": 1, "February": 2, "March": 3, "April": 4,
                "May": 5, "June": 6, "July": 7, "August": 8,
                "September": 9, "October": 10, "November": 11, "December": 12
            }
            month_num = month_names.get(month_name, 1)
            return f"{year}-{month_num:02d}-{int(day):02d}"
        
        # Última opção: usar data atual
        return datetime.now().strftime('%Y-%m-%d')
    except:
        return datetime.now().strftime('%Y-%m-%d')
