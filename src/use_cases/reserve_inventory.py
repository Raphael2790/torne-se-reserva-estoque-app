from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from domain.models.resposta import RespostaExecucao
from domain.repositories.product_repository import RepositorioItemEstoque


class ItemPedido(BaseModel):
    nome_produto: str = Field(..., description="Nome do produto")
    valor: float = Field(..., description="Valor unitário do produto")
    quantidade: int = Field(..., gt=0, description="Quantidade solicitada")
    id_sku: int = Field(..., description="ID do SKU do produto")


class RequisicaoReservaEstoque(BaseModel):
    data_pedido: datetime = Field(..., description="Data do pedido")
    pedido_completo: str = Field(..., description="Dados completos do pedido em formato JSON")
    valor_total: float = Field(..., description="Valor total do pedido")
    status: str = Field(..., description="Status do pedido")
    itens: List[ItemPedido] = Field(..., description="Itens do pedido")


class ReservarEstoque:
    def __init__(self, repositorio_item_estoque: RepositorioItemEstoque):
        self.repositorio_item_estoque = repositorio_item_estoque
    
    def executar(self, requisicao: RequisicaoReservaEstoque) -> RespostaExecucao:
        try:
            resultados_reserva = []
            
            for item in requisicao.itens:
                item_estoque = self.repositorio_item_estoque.obter_por_sku(item.id_sku)
                
                if not item_estoque:
                    return RespostaExecucao(
                        sucesso=False,
                        mensagem=f"Item de estoque não encontrado: SKU {item.id_sku}",
                        dados={
                            'data_pedido': requisicao.data_pedido,
                            'pedido_completo': requisicao.pedido_completo,
                            'valor_total': requisicao.valor_total,
                            'status': requisicao.status,
                            'itens': requisicao.itens
                        }
                    )
                
                if not item_estoque.pode_reservar(item.quantidade):
                    return RespostaExecucao(
                        sucesso=False,
                        mensagem=f"Estoque insuficiente para o item: {item.nome_produto} (SKU: {item.id_sku})",
                        dados={
                            'data_pedido': requisicao.data_pedido,
                            'pedido_completo': requisicao.pedido_completo,
                            'valor_total': requisicao.valor_total,
                            'status': requisicao.status,
                            'itens': requisicao.itens
                        }
                    )
                
                item_estoque.reservar(item.quantidade)
                self.repositorio_item_estoque.atualizar(item_estoque)
                
                resultados_reserva.append({
                    'id_sku': item.id_sku,
                    'nome_produto': item.nome_produto,
                    'quantidade': item.quantidade,
                    'reservado': True
                })
            
            return RespostaExecucao(
                sucesso=True,
                mensagem="Estoque reservado com sucesso para todos os itens",
                dados={
                    'data_pedido': requisicao.data_pedido,
                    'pedido_completo': requisicao.pedido_completo,
                    'valor_total': requisicao.valor_total,
                    'status': requisicao.status,
                    'itens': requisicao.itens,
                    'resultados_reserva': resultados_reserva
                }
            )
        except Exception as e:
            return RespostaExecucao(
                sucesso=False,
                mensagem="Erro ao processar reserva de estoque",
                erro=str(e)
            ) 