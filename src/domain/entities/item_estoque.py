from dataclasses import dataclass
from datetime import date


@dataclass
class ItemEstoque:
    id_sku: int
    nome: str
    quantidade_disponivel: int
    quantidade_reservada: int
    ativo: bool
    data_base: date
    
    def pode_reservar(self, quantidade_solicitada: int) -> bool:
        return self.ativo and self.quantidade_disponivel >= quantidade_solicitada
    
    def reservar(self, quantidade: int) -> bool:
        if not self.pode_reservar(quantidade):
            return False
        self.quantidade_reservada += quantidade
        self.quantidade_disponivel -= quantidade
        return True
    
    def cancelar_reserva(self, quantidade: int) -> None:
        self.quantidade_reservada = max(0, self.quantidade_reservada - quantidade)
        self.quantidade_disponivel += quantidade
