from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

from domain.entities.item_estoque import ItemEstoque


class RepositorioItemEstoque(ABC):
    @abstractmethod
    def obter_por_sku(self, id_sku: int, data_pedido: Optional[datetime] = None) -> Optional[ItemEstoque]:
        """
        Obtém um item de estoque pelo SKU.
        
        Args:
            id_sku: ID do SKU do item
            data_pedido: Data do pedido (opcional)
            
        Returns:
            ItemEstoque ou None se não encontrado
        """
        pass
    
    @abstractmethod
    def salvar(self, item: ItemEstoque) -> None:
        pass
    
    @abstractmethod
    def atualizar(self, item: ItemEstoque) -> None:
        pass
