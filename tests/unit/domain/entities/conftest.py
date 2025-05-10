from datetime import date
import pytest
from src.domain.entities.item_estoque import ItemEstoque


@pytest.fixture
def item_estoque_valido():
    """Fixture que retorna um item de estoque válido para testes."""
    return ItemEstoque(
        id_sku=12345,
        nome="Produto Teste",
        quantidade_disponivel=100,
        quantidade_reservada=0,
        ativo=True,
        data_base=date.today()
    )


@pytest.fixture
def item_estoque_inativo():
    """Fixture que retorna um item de estoque inativo para testes."""
    return ItemEstoque(
        id_sku=12345,
        nome="Produto Teste",
        quantidade_disponivel=100,
        quantidade_reservada=0,
        ativo=False,
        data_base=date.today()
    )


@pytest.fixture
def item_estoque_com_reserva():
    """Fixture que retorna um item de estoque com reserva para testes."""
    return ItemEstoque(
        id_sku=12345,
        nome="Produto Teste",
        quantidade_disponivel=80,
        quantidade_reservada=20,
        ativo=True,
        data_base=date.today()
    ) 