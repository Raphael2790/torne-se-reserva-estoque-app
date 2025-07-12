import boto3
from dependency_injector import containers, providers

from configuration.config import Config
from infrastructure.repositories.dynamodb_product_repository import RepositorioItemEstoqueDynamoDB
from infrastructure.services.sqs_service import ServicoSQS
from application.use_cases.reservar_estoque_uc import ReservarEstoque
from infrastructure.repositories.dynamodb_pedido_repository import RepositorioPedidoDynamoDB
from utils.app_logger import AppLogger
from application.mappings.app_mapper import AppMapper


class Container(containers.DeclarativeContainer):
    # Configuração
    config = providers.Singleton(Config)
    
    # Utilitários
    logger = providers.Factory(
        AppLogger,
        level=config.provided.LOG_LEVEL
    )

    # Clientes AWS
    aws_dynamodb_client = providers.Singleton(
        boto3.resource,
        'dynamodb',
        region_name=config.provided.AWS_REGION
    )

    aws_sqs_client = providers.Singleton(
        boto3.client,
        'sqs',
        region_name=config.provided.AWS_REGION
    )

    # Repositórios
    repositorio_item_estoque = providers.Singleton(
        RepositorioItemEstoqueDynamoDB,
        dynamodb_client=aws_dynamodb_client,
        nome_tabela=config.provided.DYNAMODB_TABLE_NAME,
        logger=logger
    )

    # Serviços
    servico_fila = providers.Singleton(
        ServicoSQS,
        sqs_client=aws_sqs_client,
        logger=logger
    )

    app_mapper = providers.Singleton(
        AppMapper
    )
    
    caso_uso_reservar_estoque = providers.Singleton(
        ReservarEstoque,
        repositorio_item_estoque=repositorio_item_estoque,
        servico_fila=servico_fila,
        config=config,
        logger=logger
    )
    
    repositorio_pedido = providers.Singleton(
        RepositorioPedidoDynamoDB,
        dynamodb_client=aws_dynamodb_client,
        nome_tabela=config.provided.DYNAMODB_PEDIDO_TABLE_NAME,
        logger=logger
    )