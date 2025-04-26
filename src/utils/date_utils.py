from datetime import datetime
from typing import Optional


def parse_iso_date(date_string: str) -> Optional[datetime]:
    """
    Converte uma string de data no formato ISO 8601 para um objeto datetime.
    
    Args:
        date_string: String de data no formato ISO 8601 (ex: '2025-04-12T01:48:22.5386879Z')
        
    Returns:
        Objeto datetime ou None se a conversão falhar
    """
    try:
        # Remove o 'Z' do final (indicador de UTC) e adiciona o fuso horário
        if date_string.endswith('Z'):
            date_string = date_string[:-1] + '+00:00'
        
        return datetime.fromisoformat(date_string)
    except (ValueError, TypeError):
        return None 