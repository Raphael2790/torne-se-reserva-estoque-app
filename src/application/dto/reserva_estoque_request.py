from pydantic import BaseModel, validator
from typing import List, Optional
from uuid import UUID
from utils.date_utils import parse_iso_date


class Endereco(BaseModel):
    logradouro: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    estado: str
    cep: str


class Cliente(BaseModel):
    id: UUID
    nome: str
    email: str
    telefone: str
    endereco: Endereco


class ItemPedido(BaseModel):
    nomeProduto: str
    valor: float
    quantidade: int
    total: float
    idSku: int


class PedidoCompleto(BaseModel):
    cliente: Cliente
    dataPedido: str
    status: int
    itens: List[ItemPedido]
    valorTotal: float
    enderecoEntrega: Endereco
    id: UUID
    dataCriacao: str
    
    @validator('dataPedido', 'dataCriacao')
    def parse_date(cls, v):
        if isinstance(v, str):
            return parse_iso_date(v)
        return v


class ReservaEstoqueRequest(BaseModel):
    DataPedido: str
    PedidoCompleto: PedidoCompleto
    ValorTotal: float
    Status: int
    Id: UUID
    Timestamp: str
    
    @validator('DataPedido', 'Timestamp')
    def parse_date(cls, v):
        if isinstance(v, str):
            return parse_iso_date(v)
        return v
