from dataclasses import dataclass


@dataclass
class Produto:
    id: str
    nome: str
    quantidade: int
    quantidade_reservada: int = 0
    
    @property
    def quantidade_disponivel(self) -> int:
        return self.quantidade - self.quantidade_reservada

    def pode_reservar(self, quantidade_solicitada: int) -> bool:
        return self.quantidade_disponivel >= quantidade_solicitada

    def reservar(self, quantidade: int) -> bool:
        if not self.pode_reservar(quantidade):
            return False
        self.quantidade_reservada += quantidade
        return True
    
    def cancelar_reserva(self, quantidade: int) -> None:
        self.quantidade_reservada = max(0, self.quantidade_reservada - quantidade)
