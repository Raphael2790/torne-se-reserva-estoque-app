from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from uuid import UUID

from application.dto.reserva_estoque_request import PedidoCompleto


@dataclass
class MensagemEstoqueConfirmado:
    id_pedido: UUID
    status: str
    data_pedido: date
    pedido_completo: PedidoCompleto
    valor_total: float

    def to_dict(self) -> dict:
        pedido_completo = self.pedido_completo.model_dump()
        # Garante que todos os UUIDs e datas no pedido_completo sejam strings
        if 'id' in pedido_completo:
            pedido_completo['id'] = str(pedido_completo['id'])
        if 'cliente' in pedido_completo and 'id' in pedido_completo['cliente']:
            pedido_completo['cliente']['id'] = str(pedido_completo['cliente']['id'])
        if 'dataPedido' in pedido_completo:
            data_pedido = pedido_completo['dataPedido']
            pedido_completo['dataPedido'] = (
                data_pedido.isoformat() 
                if hasattr(data_pedido, 'isoformat')
                else str(data_pedido)
            )
        if 'dataCriacao' in pedido_completo:
            data_criacao = pedido_completo['dataCriacao']
            pedido_completo['dataCriacao'] = (
                data_criacao.isoformat() 
                if hasattr(data_criacao, 'isoformat') 
                else str(data_criacao)
            )

        return {
            'id_pedido': str(self.id_pedido),
            'status': self.status,
            'data_pedido': self.data_pedido.isoformat(),
            'pedido_completo': pedido_completo,
            'valor_total': self.valor_total
        }

        
@dataclass
class MensagemEstoqueCancelada:
    id_pedido: UUID
    status: str
    motivo: str
    data_hora_evento: date
    
    def to_dict(self) -> dict:
        return {
            'id_pedido': str(self.id_pedido),
            'status': self.status,
            'data_hora_evento': self.data_hora_evento.isoformat()
        }
        

class ServicoFila(ABC):
    @abstractmethod
    def enviar_mensagem(self, mensagem: MensagemEstoqueConfirmado, url_fila: str) -> None:
        pass
