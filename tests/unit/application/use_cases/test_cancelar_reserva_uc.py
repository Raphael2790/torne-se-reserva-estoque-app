import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.application.use_cases.cancelar_reserva_uc import CancelarReserva
from src.application.dto.cancelamento_reserva_request import CancelarReservaRequest
from src.domain.entities.item_estoque import ItemEstoque

class TestCancelarReserva(unittest.TestCase):

    def setUp(self):
        self.repositorio_item_estoque_mock = MagicMock()
        self.servico_fila_mock = MagicMock()
        self.config_mock = MagicMock()
        self.logger_mock = MagicMock()

        self.config_mock.URL_FILA_CANCELAMENTO = "dummy_url"

        self.cancelar_reserva_uc = CancelarReserva(
            repositorio_item_estoque=self.repositorio_item_estoque_mock,
            servico_fila=self.servico_fila_mock,
            config=self.config_mock,
            logger=self.logger_mock
        )

    def test_executar_sucesso(self):
        # Arrange
        pedido_completo = {
            "itens": [
                {"idSku": 1, "quantidade": 1},
                {"idSku": 2, "quantidade": 2}
            ]
        }
        requisicao = CancelarReservaRequest(
            id_pedido="123",
            data_pedido=datetime.now(),
            pedido_completo=pedido_completo
        )

        item_estoque_1 = ItemEstoque(id_sku=1, nome="item1", quantidade_disponivel=10, quantidade_reservada=1, ativo=True, data_base=datetime.now().date())
        item_estoque_2 = ItemEstoque(id_sku=2, nome="item2", quantidade_disponivel=20, quantidade_reservada=2, ativo=True, data_base=datetime.now().date())

        self.repositorio_item_estoque_mock.obter_por_sku.side_effect = [item_estoque_1, item_estoque_2]

        # Act
        resposta = self.cancelar_reserva_uc.executar(requisicao)

        # Assert
        self.assertTrue(resposta.sucesso)
        self.assertEqual(resposta.mensagem, "Reserva cancelada com sucesso para todos os itens")
        self.assertEqual(self.repositorio_item_estoque_mock.obter_por_sku.call_count, 2)
        self.assertEqual(self.repositorio_item_estoque_mock.atualizar.call_count, 2)
        self.servico_fila_mock.enviar_mensagem.assert_called_once()

    def test_executar_item_nao_encontrado(self):
        # Arrange
        pedido_completo = {
            "itens": [
                {"idSku": 1, "quantidade": 1}
            ]
        }
        requisicao = CancelarReservaRequest(
            id_pedido="123",
            data_pedido=datetime.now(),
            pedido_completo=pedido_completo
        )

        self.repositorio_item_estoque_mock.obter_por_sku.return_value = None

        # Act
        resposta = self.cancelar_reserva_uc.executar(requisicao)

        # Assert
        self.assertFalse(resposta.sucesso)
        self.assertEqual(resposta.mensagem, "Item de estoque não encontrado: SKU 1")
        self.repositorio_item_estoque_mock.obter_por_sku.assert_called_once_with(1, requisicao.data_pedido)
        self.repositorio_item_estoque_mock.atualizar.assert_not_called()
        self.servico_fila_mock.enviar_mensagem.assert_not_called()

    @patch('src.application.use_cases.cancelar_reserva_uc.datetime')
    def test_executar_com_excecao(self, mock_datetime):
        # Arrange
        mock_datetime.now.return_value = datetime(2023, 10, 26, 10, 0, 0)
        pedido_completo = {
            "itens": [
                {"idSku": 1, "quantidade": 1}
            ]
        }
        requisicao = CancelarReservaRequest(
            id_pedido="123",
            data_pedido=datetime.now(),
            pedido_completo=pedido_completo
        )

        self.repositorio_item_estoque_mock.obter_por_sku.side_effect = Exception("Erro de teste")

        # Act
        resposta = self.cancelar_reserva_uc.executar(requisicao)

        # Assert
        self.assertFalse(resposta.sucesso)
        self.assertEqual(resposta.mensagem, "Erro ao processar cancelamento de reserva de estoque")
        self.assertEqual(resposta.erro, "Erro de teste")
        self.logger_mock.error.assert_called_once_with("Erro ao processar cancelamento de reserva de estoque: Erro de teste")

if __name__ == '__main__':
    unittest.main()
