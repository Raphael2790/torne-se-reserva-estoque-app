from datetime import datetime
from domain.models.resposta import RespostaExecucao
from domain.repositories.product_repository import RepositorioItemEstoque
from application.dto.cancelamento_reserva_request import CancelarReservaRequest
from domain.services.queue_service import MensagemEstoqueCancelada
from infrastructure.services.sqs_service import ServicoSQS
from typing import List
from domain.entities.item_estoque import ItemEstoque
from configuration.config import Config
from utils.app_logger import AppLogger


class CancelarReserva:
    def __init__(self, repositorio_item_estoque: RepositorioItemEstoque, servico_fila: ServicoSQS, config: Config, logger: AppLogger):
        self.repositorio_item_estoque = repositorio_item_estoque
        self.servico_fila = servico_fila
        self.config = config
        self.logger = logger

    def executar(self, requisicao: CancelarReservaRequest) -> RespostaExecucao:
        try:
            itens_a_cancelar: List[ItemEstoque] = []
            for item in requisicao.pedido_completo.itens:
                self.logger.info(f"Buscando item de estoque para SKU: {item.idSku} e data de pedido: {requisicao.data_pedido}")
                item_estoque = self.repositorio_item_estoque.obter_por_sku(item.idSku, requisicao.data_pedido)

                if not item_estoque:
                    return RespostaExecucao(
                        sucesso=False,
                        mensagem=f"Item de estoque não encontrado: SKU {item.idSku}",
                    )

                item_estoque.cancelar_reserva(item.quantidade)
                self.repositorio_item_estoque.atualizar(item_estoque)
                itens_a_cancelar.append(item_estoque)

            mensagem_fila = MensagemEstoqueCancelada(
                    id_pedido=requisicao.id_pedido,
                    data_pedido=requisicao.data_pedido,
                    status='CANCELADO',
                    motivo='Cancelamento solicitado pelo sistema',
                    data_hora_evento=datetime.now()
                )
            self.servico_fila.enviar_mensagem(mensagem_fila, self.config.URL_FILA_CANCELAMENTO)

            return RespostaExecucao(
                sucesso=True,
                mensagem="Reserva cancelada com sucesso para todos os itens",
            )

        except Exception as e:
            self.logger.error(f"Erro ao processar cancelamento de reserva de estoque: {e}")
            return RespostaExecucao(
                sucesso=False,
                mensagem="Erro ao processar cancelamento de reserva de estoque",
                erro=str(e)
            )
