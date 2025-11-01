from datetime import datetime
from pydantic import BaseModel
from application.dto.reserva_estoque_request import PedidoCompleto


class CancelarReservaRequest(BaseModel):
    id_pedido: str
    data_pedido: datetime
    pedido_completo: PedidoCompleto

class CancelamentoMessage(BaseModel):
    MessageId: str
    PedidoId: str
    DataPedido: datetime
