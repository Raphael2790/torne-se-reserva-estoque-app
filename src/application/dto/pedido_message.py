from pydantic import BaseModel


class PedidoMessage(BaseModel):
    DataPedido: str
    Status: int
    Id: str
    PedidoId: str
    Timestamp: str
