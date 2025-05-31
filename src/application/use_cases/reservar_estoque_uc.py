from domain.models.resposta import RespostaExecucao
from domain.repositories.product_repository import RepositorioItemEstoque
from application.dto.reserva_estoque_request import ReservaEstoqueRequest
from domain.services.queue_service import MensagemFila
from infrastructure.services.sqs_service import ServicoSQS
from typing import List
from domain.entities.item_estoque import ItemEstoque
from configuration.config import Config


class ReservarEstoque:
    def __init__(self, repositorio_item_estoque: RepositorioItemEstoque, servico_fila: ServicoSQS, config: Config):
        self.repositorio_item_estoque = repositorio_item_estoque
        self.servico_fila = servico_fila
        self.config = config

    def executar(self, requisicao: ReservaEstoqueRequest) -> RespostaExecucao:
        try:
            resultados_reserva = []

            for item in requisicao.PedidoCompleto.itens:
                item_estoque = self.repositorio_item_estoque.obter_por_sku(item.idSku, requisicao.DataPedido)
                
                if not item_estoque:
                    self.__devolver_estoque(resultados_reserva)
                    return RespostaExecucao(
                        sucesso=False,
                        mensagem=f"Item de estoque não encontrado: SKU {item.idSku}",
                        dados={
                            'data_pedido': requisicao.DataPedido,
                            'pedido_completo_id': str(requisicao.PedidoCompleto.id),
                            'valor_total': requisicao.ValorTotal,
                            'status': requisicao.Status,
                            'quantidade_itens': len(requisicao.PedidoCompleto.itens)
                        }
                    )
                
                if not item_estoque.pode_reservar(item.quantidade):
                    self.__devolver_estoque(resultados_reserva)
                    mensagem_fila = MensagemFila(
                        id_pedido=str(requisicao.Id),
                        id_produto=str(item.idSku),
                        quantidade=item.quantidade,
                        status='SEM_ESTOQUE',
                        mensagem=f"Estoque insuficiente para o item: {item.nomeProduto} (SKU: {item.idSku})"
                    )
                    self.servico_fila.enviar_mensagem(mensagem_fila, self.config.URL_FILA_SEM_ESTOQUE)
                    return RespostaExecucao(
                        sucesso=False,
                        mensagem=f"Estoque insuficiente para o item: {item.nomeProduto} (SKU: {item.idSku})",
                        dados={
                            'data_pedido': requisicao.DataPedido,
                            'pedido_completo': requisicao.PedidoCompleto,
                            'valor_total': requisicao.ValorTotal,
                            'status': requisicao.Status,
                            'itens': requisicao.PedidoCompleto.itens
                        }
                    )
                
                item_estoque.reservar(item.quantidade)
                self.repositorio_item_estoque.atualizar(item_estoque)
                
                resultados_reserva.append(item_estoque)
            
            mensagem_fila = MensagemFila(
                id_pedido=str(requisicao.Id),
                id_produto=str(requisicao.PedidoCompleto.itens[0].idSku),
                quantidade=sum(item.quantidade for item in requisicao.PedidoCompleto.itens),
                status='RESERVADO',
                mensagem="Estoque reservado com sucesso para todos os itens"
            )
            self.servico_fila.enviar_mensagem(mensagem_fila, self.config.URL_FILA_RESERVA)
            
            return RespostaExecucao(
                sucesso=True,
                mensagem="Estoque reservado com sucesso para todos os itens",
                dados={
                    'data_pedido': requisicao.DataPedido,
                    'pedido_completo': requisicao.PedidoCompleto,
                    'valor_total': requisicao.ValorTotal,
                    'status': requisicao.Status,
                    'itens': requisicao.PedidoCompleto.itens,
                    'resultados_reserva': resultados_reserva
                }
            )
        except Exception as e:
            return RespostaExecucao(
                sucesso=False,
                mensagem="Erro ao processar reserva de estoque",
                erro=str(e)
            )

    def __devolver_estoque(self, itens_reservados: List[ItemEstoque]) -> RespostaExecucao:
        if not itens_reservados:
            return RespostaExecucao(
                sucesso=True,
                mensagem="Nenhum item reservado para devolver"
            )
        for item in itens_reservados:
            item.cancelar_reserva(item.quantidade_reservada)
            self.repositorio_item_estoque.atualizar(item)
        return RespostaExecucao(
            sucesso=True,
            mensagem="Estoque devolvido com sucesso"
        )
