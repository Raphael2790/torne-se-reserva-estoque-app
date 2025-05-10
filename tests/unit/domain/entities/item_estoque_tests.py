from datetime import date
from src.domain.entities.item_estoque import ItemEstoque


class TestItemEstoque:
    """Testes para a classe ItemEstoque."""

    def test_criar_item_estoque(self):
        """Testa a criação de um item de estoque."""
        # Arrange
        id_sku = 12345
        nome = "Produto Teste"
        quantidade_disponivel = 100
        quantidade_reservada = 0
        ativo = True
        data_base = date.today()

        # Act
        item = ItemEstoque(
            id_sku=id_sku,
            nome=nome,
            quantidade_disponivel=quantidade_disponivel,
            quantidade_reservada=quantidade_reservada,
            ativo=ativo,
            data_base=data_base
        )

        # Assert
        assert item.id_sku == id_sku
        assert item.nome == nome
        assert item.quantidade_disponivel == quantidade_disponivel
        assert item.quantidade_reservada == quantidade_reservada
        assert item.ativo == ativo
        assert item.data_base == data_base

    def test_pode_reservar_quando_item_ativo_e_quantidade_suficiente(self, item_estoque_valido):
        """Testa se um item ativo com quantidade suficiente pode ser reservado."""
        # Act
        resultado = item_estoque_valido.pode_reservar(50)

        # Assert
        assert resultado is True

    def test_nao_pode_reservar_quando_item_inativo(self, item_estoque_inativo):
        """Testa se um item inativo não pode ser reservado."""
        # Act
        resultado = item_estoque_inativo.pode_reservar(10)

        # Assert
        assert resultado is False

    def test_nao_pode_reservar_quando_quantidade_insuficiente(self, item_estoque_valido):
        """Testa se um item não pode ser reservado quando a quantidade solicitada é maior que a disponível."""
        # Act
        resultado = item_estoque_valido.pode_reservar(150)

        # Assert
        assert resultado is False

    def test_reservar_quando_quantidade_suficiente(self, item_estoque_valido):
        """Testa a reserva de um item quando há quantidade suficiente."""
        # Arrange
        quantidade_inicial_disponivel = item_estoque_valido.quantidade_disponivel
        quantidade_inicial_reservada = item_estoque_valido.quantidade_reservada
        quantidade_reservar = 30

        # Act
        resultado = item_estoque_valido.reservar(quantidade_reservar)

        # Assert
        assert resultado is True
        assert item_estoque_valido.quantidade_disponivel == quantidade_inicial_disponivel - quantidade_reservar
        assert item_estoque_valido.quantidade_reservada == quantidade_inicial_reservada + quantidade_reservar

    def test_reservar_quando_quantidade_insuficiente(self, item_estoque_valido):
        """Testa a tentativa de reserva quando a quantidade é insuficiente."""
        # Arrange
        quantidade_inicial_disponivel = item_estoque_valido.quantidade_disponivel
        quantidade_inicial_reservada = item_estoque_valido.quantidade_reservada
        quantidade_reservar = 150

        # Act
        resultado = item_estoque_valido.reservar(quantidade_reservar)

        # Assert
        assert resultado is False
        assert item_estoque_valido.quantidade_disponivel == quantidade_inicial_disponivel
        assert item_estoque_valido.quantidade_reservada == quantidade_inicial_reservada

    def test_cancelar_reserva_quando_quantidade_menor_que_reservada(self, item_estoque_com_reserva):
        """Testa o cancelamento parcial de uma reserva."""
        # Arrange
        quantidade_inicial_disponivel = item_estoque_com_reserva.quantidade_disponivel
        quantidade_inicial_reservada = item_estoque_com_reserva.quantidade_reservada
        quantidade_cancelar = 10

        # Act
        item_estoque_com_reserva.cancelar_reserva(quantidade_cancelar)

        # Assert
        assert item_estoque_com_reserva.quantidade_disponivel == quantidade_inicial_disponivel + quantidade_cancelar
        assert item_estoque_com_reserva.quantidade_reservada == quantidade_inicial_reservada - quantidade_cancelar

    def test_cancelar_reserva_quando_quantidade_maior_que_reservada(self, item_estoque_com_reserva):
        """Testa o cancelamento de uma reserva quando a quantidade é maior que a reservada."""
        # Arrange
        quantidade_inicial_disponivel = item_estoque_com_reserva.quantidade_disponivel
        quantidade_inicial_reservada = item_estoque_com_reserva.quantidade_reservada
        quantidade_cancelar = 30  # Maior que a quantidade reservada (20)

        # Act
        item_estoque_com_reserva.cancelar_reserva(quantidade_cancelar)

        # Assert
        assert item_estoque_com_reserva.quantidade_disponivel == (
            quantidade_inicial_disponivel + quantidade_inicial_reservada
        )
        assert item_estoque_com_reserva.quantidade_reservada == 0  # Não pode ficar negativo 