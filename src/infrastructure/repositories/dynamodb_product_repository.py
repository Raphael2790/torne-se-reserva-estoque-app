from datetime import date, datetime
from typing import Optional

from botocore.exceptions import ClientError

from domain.entities.item_estoque import ItemEstoque
from domain.repositories.product_repository import RepositorioItemEstoque


class RepositorioItemEstoqueDynamoDB(RepositorioItemEstoque):
    def __init__(self, dynamodb_client, nome_tabela: str):
        self.dynamodb = dynamodb_client
        self.tabela = self.dynamodb.Table(nome_tabela)
    
    def obter_por_sku(self, id_sku: int, data_pedido: Optional[datetime] = None) -> Optional[ItemEstoque]:
        try:
            # Se não for fornecida uma data, usa a data atual
            if data_pedido is None:
                data_pedido = datetime.now()
            
            # Converte a data do pedido para o formato de data base (YYYY-MM-DD)
            data_base = data_pedido.date().isoformat()
            
            resposta = self.tabela.get_item(Key={'id_sku': id_sku, 'data_base': data_base}, ConsistentRead=True)
            item = resposta.get('Item')
            
            if not item:
                return None
                
            return ItemEstoque(
                id_sku=item['id_sku'],
                nome=item['nome'],
                quantidade_disponivel=item['quantidade_disponivel'],
                quantidade_reservada=item.get('quantidade_reservada', 0),
                ativo=item.get('ativo', True),
                data_base=date.fromisoformat(item['data_base'])
            )
        except ClientError as e:
            print(f"Erro ao obter item de estoque: {e}")
            return None
    
    def salvar(self, item: ItemEstoque) -> None:
        try:
            self.tabela.put_item(
                Item={
                    'id_sku': item.id_sku,
                    'nome': item.nome,
                    'quantidade_disponivel': item.quantidade_disponivel,
                    'quantidade_reservada': item.quantidade_reservada,
                    'ativo': item.ativo,
                    'data_base': item.data_base.isoformat()
                }
            )
        except ClientError as e:
            print(f"Erro ao salvar item de estoque: {e}")
            raise
    
    def atualizar(self, item: ItemEstoque) -> None:
        try:
            self.tabela.update_item(
                Key={'id_sku': item.id_sku, 'data_base': item.data_base.isoformat()},
                UpdateExpression=(
                    "SET quantidade_disponivel = :qd, "
                    "quantidade_reservada = :qr, "
                    "ativo = :a"
                ),
                ExpressionAttributeValues={
                    ':qd': item.quantidade_disponivel,
                    ':qr': item.quantidade_reservada,
                    ':a': item.ativo
                }
            )
        except ClientError as e:
            print(f"Erro ao atualizar item de estoque: {e}")
            raise
