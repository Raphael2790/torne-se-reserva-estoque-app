import json
import pytest
from uuid import UUID
from src.utils.date_utils import parse_iso_date
from src.application.dto.reserva_estoque_request import ReservaEstoqueRequest, PedidoCompleto


class TestAppMapper:
    """Testes para a classe AppMapper."""

    def test_map_to_reserva_estoque_request(self, mapper, event_json):
        """Testa o mapeamento de um evento para um objeto ReservaEstoqueRequest."""
        # Arrange
        string_json = json.dumps(event_json["Records"][0]["body"])

        # Act
        resultado = mapper.map_to_reserva_estoque_request(string_json)

        # Assert
        assert type(resultado).__class__ is ReservaEstoqueRequest.__class__
        assert resultado.DataPedido == parse_iso_date("2025-04-25T01:48:22.5386879Z")
        assert resultado.ValorTotal == 802.99
        assert resultado.Status == 1
        assert resultado.Id == UUID("4cea43ea-2b80-47ff-9e58-98621322b043")
        assert resultado.Timestamp == parse_iso_date("2025-04-11T22:48:25.9030961-03:00")

        # Verifica o PedidoCompleto
        assert type(resultado.PedidoCompleto).__class__ is PedidoCompleto.__class__
        assert resultado.PedidoCompleto.cliente.id == UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")
        assert resultado.PedidoCompleto.cliente.nome == "Raphael"
        assert resultado.PedidoCompleto.cliente.email == "raphael@email.com"
        assert resultado.PedidoCompleto.cliente.telefone == "11999999999"

        # Verifica o endereço do cliente
        assert resultado.PedidoCompleto.cliente.endereco.logradouro == "Rua Logo Ali"
        assert resultado.PedidoCompleto.cliente.endereco.numero == "309"
        assert resultado.PedidoCompleto.cliente.endereco.complemento == "Casa 2"
        assert resultado.PedidoCompleto.cliente.endereco.bairro == "Bem Ali"
        assert resultado.PedidoCompleto.cliente.endereco.cidade == "São Paulo"
        assert resultado.PedidoCompleto.cliente.endereco.estado == "SP"
        assert resultado.PedidoCompleto.cliente.endereco.cep == "1011010"

        # Verifica os itens do pedido
        assert len(resultado.PedidoCompleto.itens) == 2
        assert resultado.PedidoCompleto.itens[0].nomeProduto == "Panela de pressão"
        assert resultado.PedidoCompleto.itens[0].valor == 100.50
        assert resultado.PedidoCompleto.itens[0].quantidade == 2
        assert resultado.PedidoCompleto.itens[0].total == 201.00
        assert resultado.PedidoCompleto.itens[0].idSku == 91818181

        assert resultado.PedidoCompleto.itens[1].nomeProduto == "Jogo de panela"
        assert resultado.PedidoCompleto.itens[1].valor == 601.99
        assert resultado.PedidoCompleto.itens[1].quantidade == 1
        assert resultado.PedidoCompleto.itens[1].total == 601.99
        assert resultado.PedidoCompleto.itens[1].idSku == 91818181

        # Verifica o endereço de entrega
        assert resultado.PedidoCompleto.enderecoEntrega.logradouro == "Rua Logo Ali"
        assert resultado.PedidoCompleto.enderecoEntrega.numero == "309"
        assert resultado.PedidoCompleto.enderecoEntrega.complemento == "Casa 2"
        assert resultado.PedidoCompleto.enderecoEntrega.bairro == "Bem Ali"
        assert resultado.PedidoCompleto.enderecoEntrega.cidade == "São Paulo"
        assert resultado.PedidoCompleto.enderecoEntrega.estado == "SP"
        assert resultado.PedidoCompleto.enderecoEntrega.cep == "1011010"

    def test_map_to_reserva_estoque_request_com_json_invalido(self, mapper):
        """Testa o mapeamento com um JSON inválido."""
        # Arrange
        string_json = "json inválido"

        # Act & Assert
        with pytest.raises(json.JSONDecodeError):
            mapper.map_to_reserva_estoque_request(string_json)

    def test_map_to_reserva_estoque_request_com_pedido_completo_invalido(self, mapper):
        """Testa o mapeamento com um PedidoCompleto inválido."""
        # Arrange
        string_json = json.dumps({
            "DataPedido": "2025-04-25T01:48:22.5386879Z",
            "PedidoCompleto": "json inválido",
            "ValorTotal": 802.99,
            "Status": 1,
            "Id": "4cea43ea-2b80-47ff-9e58-98621322b043",
            "Timestamp": "2025-04-11T22:48:25.9030961-03:00"
        })

        # Act & Assert
        with pytest.raises(json.JSONDecodeError):
            mapper.map_to_reserva_estoque_request(string_json)
