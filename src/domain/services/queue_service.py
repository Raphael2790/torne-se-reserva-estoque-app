from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


@dataclass
class MensagemFila:
    status: str
    data_pedido: date
    pedido_completo: str
    valor_total: float


class ServicoFila(ABC):
    @abstractmethod
    def enviar_mensagem(self, mensagem: MensagemFila, url_fila: str) -> None:
        pass 