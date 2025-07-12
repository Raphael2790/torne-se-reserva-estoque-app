from dataclasses import dataclass


@dataclass
class Pedido:
    id: str
    data_pedido: str
    pedido_completo: str
    valor_total: float
    status: int
