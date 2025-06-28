import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Configurações AWS
    AWS_REGION = os.getenv('AWS_REGION')
    
    if not AWS_REGION:
        raise ValueError('AWS_REGION não configurado')
    
    # Configurações DynamoDB
    DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')

    if not DYNAMODB_TABLE_NAME:
        raise ValueError('DYNAMODB_TABLE_NAME não configurado')
    
    # Configurações SQS
    URL_FILA_RESERVA = os.getenv('RESERVATION_QUEUE_URL')
    URL_FILA_SEM_ESTOQUE = os.getenv('OUT_OF_STOCK_QUEUE_URL')
    
    if not URL_FILA_RESERVA:
        raise ValueError('URL_FILA_RESERVA não configurado')
    
    if not URL_FILA_SEM_ESTOQUE:
        raise ValueError('URL_FILA_SEM_ESTOQUE não configurado')
    
    # Configurações de Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')