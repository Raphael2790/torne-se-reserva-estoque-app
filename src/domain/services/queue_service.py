from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass
class MensagemEstoqueConfirmado:
    id_pedido: UUID
    status: str
    data_pedido: date
    data_hora_evento: date

    def to_dict(self) -> dict:
        return {
            'id_pedido': str(self.id_pedido),
            'status': self.status,
            'data_pedido': self.data_pedido.isoformat(),
            'data_hora_evento': self.data_hora_evento.isoformat()
        }

        
@dataclass
class MensagemEstoqueCancelada:
    id_pedido: UUID
    data_pedido: date
    status: str
    motivo: str
    data_hora_evento: date
    
    def to_dict(self) -> dict:
        return {
            'id_pedido': str(self.id_pedido),
            'data_pedido': self.data_pedido.isoformat(),
            'status': self.status,
            'motivo': self.motivo,
            'data_hora_evento': self.data_hora_evento.isoformat()
        }
        

class ServicoFila(ABC):
    @abstractmethod
    def enviar_mensagem(self, mensagem: MensagemEstoqueConfirmado, url_fila: str) -> None:
        pass
