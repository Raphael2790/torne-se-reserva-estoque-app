from datetime import datetime
from domain.models.resposta import RespostaExecucao
from domain.repositories.product_repository import RepositorioItemEstoque
from application.dto.reserva_estoque_request import ReservaEstoqueRequest
from domain.services.queue_service import MensagemEstoqueConfirmado, MensagemEstoqueCancelada
from infrastructure.services.sqs_service import ServicoSQS
from typing import List
from domain.entities.item_estoque import ItemEstoque
from configuration.config import Config
from utils.app_logger import AppLogger


class ReservarEstoque:
    def __init__(self, repositorio_item_estoque: RepositorioItemEstoque, servico_fila: ServicoSQS, config: Config, logger: AppLogger):
        self.repositorio_item_estoque = repositorio_item_estoque
        self.servico_fila = servico_fila
        self.config = config
        self.logger = logger

    def executar(self, requisicao: ReservaEstoqueRequest) -> RespostaExecucao:
        try:
            resultados_reserva: List[ItemEstoque] = []
            item_sem_estoque: List[ItemEstoque] = []

            for item in requisicao.PedidoCompleto.itens:
                self.logger.info(f"Buscando item de estoque para SKU: {item.idSku} e data de pedido: {requisicao.DataPedido}")
                item_estoque = self.repositorio_item_estoque.obter_por_sku(item.idSku, requisicao.DataPedido)
                
                if not item_estoque:
                    self.__devolver_estoque(resultados_reserva)
                    return RespostaExecucao(
                        sucesso=False,
                        mensagem=f"Item de estoque não encontrado: SKU {item.idSku}",
                        dados={
                            'data_pedido': requisicao.DataPedido.strftime("%Y-%m-%dT%H:%M:%S%:z"),
                            'pedido_completo_id': str(requisicao.PedidoCompleto.id),
                            'valor_total': requisicao.ValorTotal,
                            'status': 'ITEM_NAO_ENCONTRADO',
                            'itens_nao_reservados': [],
                            'resultados_reserva': []
                        }
                    )
                
                if not item_estoque.pode_reservar(item.quantidade):
                    self.__devolver_estoque(resultados_reserva)
                    resultados_reserva.clear()
                    item_sem_estoque.append(item_estoque)
                    break
                
                item_estoque.reservar(item.quantidade)
                self.repositorio_item_estoque.atualizar(item_estoque)
                
                resultados_reserva.append(item_estoque)
            
            if len(resultados_reserva) == 0:
                mensagem_fila = MensagemEstoqueCancelada(
                        id_pedido=requisicao.Id,
                        status='CANCELADO',
                        motivo='Um dos itens não possui estoque suficiente',
                        data_hora_evento=datetime.now()
                    )
                self.servico_fila.enviar_mensagem(mensagem_fila, self.config.URL_FILA_SEM_ESTOQUE)
                return RespostaExecucao(
                    sucesso=False,
                    mensagem="Estoque insuficiente para os items",
                    dados={
                        'data_pedido': requisicao.DataPedido.strftime("%Y-%m-%dT%H:%M:%S%:z"),
                        'pedido_completo_id': str(requisicao.PedidoCompleto.id),
                        'valor_total': requisicao.ValorTotal,
                        'status': 'CANCELADO',
                        'itens_nao_reservados': [item.id_sku for item in item_sem_estoque],
                        'resultados_reserva': []
                    }
                )
            
            mensagem_fila = MensagemEstoqueConfirmado(
                id_pedido=requisicao.Id,
                data_pedido=requisicao.DataPedido,
                pedido_completo=requisicao.PedidoCompleto,
                status='RESERVADO',
                valor_total=sum([item.valor * item.quantidade for item in requisicao.PedidoCompleto.itens])
            )
            self.servico_fila.enviar_mensagem(mensagem_fila, self.config.URL_FILA_RESERVA)
            
            return RespostaExecucao(
                sucesso=True,
                mensagem="Estoque reservado com sucesso para todos os itens",
                dados={
                    'data_pedido': requisicao.DataPedido.strftime("%Y-%m-%dT%H:%M:%S%:z"),
                    'pedido_completo_id': str(requisicao.PedidoCompleto.id),
                    'valor_total': requisicao.ValorTotal,
                    'status': 'RESERVADO',
                    'itens_nao_reservados': [],
                    'resultados_reserva': [item.id_sku for item in resultados_reserva]
                }
            )
        except Exception as e:
            self.logger.error(f"Erro ao processar reserva de estoque: {e}")
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
