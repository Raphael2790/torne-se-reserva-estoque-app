from abc import ABC, abstractmethod
from typing import Optional

from ..entities.item_estoque import ItemEstoque


class RepositorioItemEstoque(ABC):
    @abstractmethod
    def obter_por_sku(self, id_sku: int) -> Optional[ItemEstoque]:
        pass
    
    @abstractmethod
    def salvar(self, item: ItemEstoque) -> None:
        pass
    
    @abstractmethod
    def atualizar(self, item: ItemEstoque) -> None:
        pass 