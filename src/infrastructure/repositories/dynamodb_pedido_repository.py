from typing import Optional
from domain.repositories.pedido_repository import RepositorioPedido
from utils.app_logger import AppLogger
from domain.entities.pedido import Pedido
from botocore.exceptions import ClientError


class RepositorioPedidoDynamoDB(RepositorioPedido):
    def __init__(self, dynamodb_client, nome_tabela: str, logger: AppLogger):
        self.dynamodb = dynamodb_client
        self.tabela = self.dynamodb.Table(nome_tabela)
        self.logger = logger

    def obter_por_id_e_data_pedido(self, pedido_id: str, data_pedido: str) -> Optional[Pedido]:
        try:
            resposta = self.tabela.get_item(Key={'id': pedido_id, 'data_pedido': data_pedido}, ConsistentRead=True)
            self.logger.info(f"Resposta da consulta: {resposta}")
            item = resposta.get('Item')
            
            if not item:
                return None
            
            return Pedido(
                id=item['Id'],
                data_pedido=item['DataPedido'],
                pedido_completo=item['PedidoCompleto'],
                valor_total=item['ValorTotal'],
                status=item['Status']
            )
        except ClientError as e:
            self.logger.error(f"Erro ao obter pedido: {e}")
            return None