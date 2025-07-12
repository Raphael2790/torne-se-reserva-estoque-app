import json

from application.dto.reserva_estoque_request import PedidoCompleto, ReservaEstoqueRequest
from application.dto.pedido_message import PedidoMessage


class AppMapper:
    def __init__(self):
        pass

    def map_to_reserva_estoque_request(self, string_json: str) -> ReservaEstoqueRequest:
        """
        Converte uma string JSON em um objeto ReservaEstoqueRequest.
        
        Args:
            string_json: String JSON contendo os dados da requisição
            
        Returns:
            Objeto ReservaEstoqueRequest
        """
        corpo = json.loads(string_json)
        pedido_completo_obj = json.loads(corpo['PedidoCompleto'])
        pedido_completo = PedidoCompleto(**pedido_completo_obj)
        
        # Cria o objeto ReservaEstoqueRequest
        # Os validadores do Pydantic cuidarão da conversão das datas
        return ReservaEstoqueRequest(
            DataPedido=corpo['DataPedido'],
            PedidoCompleto=pedido_completo,
            ValorTotal=corpo['ValorTotal'],
            Status=corpo['Status'],
            Id=corpo['Id'],
            Timestamp=corpo['Timestamp']
        )
    
    def map_to_pedido_message(self, string_json: str) -> PedidoMessage:
        return PedidoMessage(**json.loads(string_json))
