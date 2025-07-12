from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.pedido import Pedido


class RepositorioPedido(ABC):
    @abstractmethod
    def obter_por_id_e_data_pedido(self, pedido_id: str, data_pedido: str) -> Optional[Pedido]:
        """
        Obtém um pedido pelo ID e data do pedido.
        
        Args:
            pedido_id: ID do pedido
            data_pedido: Data do pedido
            
        Returns:
            Pedido ou None se não encontrado
        """
        pass
