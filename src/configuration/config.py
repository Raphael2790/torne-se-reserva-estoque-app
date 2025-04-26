import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Configurações AWS
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    
    # Configurações DynamoDB
    DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME', 'inventory')
    
    # Configurações SQS
    URL_FILA_RESERVA = os.getenv('RESERVATION_QUEUE_URL')
    URL_FILA_SEM_ESTOQUE = os.getenv('OUT_OF_STOCK_QUEUE_URL')
    
    # Configurações de Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')