import unittest
from unittest.mock import MagicMock, patch
import json
from src.handler import handler, UseCaseEnum

class TestHandler(unittest.TestCase):

    @patch('src.handler.container')
    def test_handler_reserva_sucesso(self, mock_container):
        # Arrange
        event = {
            'Records': [
                {
                    'body': json.dumps({'PedidoId': '123', 'DataPedido': '2023-10-26T10:00:00Z'}),
                    'messageAttributes': {
                        'action': {
                            'stringValue': UseCaseEnum.RESERVAR_ESTOQUE.value
                        }
                    }
                }
            ]
        }

        mock_use_case = MagicMock()
        mock_use_case.executar.return_value = MagicMock(sucesso=True, mensagem="Reserva com sucesso", dados={}, erro=None)
        mock_container.caso_uso_reservar_estoque.return_value = mock_use_case

        # Act
        response = handler(event, {})

        # Assert
        self.assertTrue(response['sucesso'])
        self.assertEqual(response['mensagem'], "Processamento concluído")
        self.assertEqual(len(response['resultados']), 1)
        self.assertTrue(response['resultados'][0]['sucesso'])

    @patch('src.handler.container')
    def test_handler_cancelamento_sucesso(self, mock_container):
        # Arrange
        event = {
            'Records': [
                {
                    'body': json.dumps({'PedidoId': '123', 'DataPedido': '2023-10-26T10:00:00Z'}),
                    'messageAttributes': {
                        'action': {
                            'stringValue': UseCaseEnum.CANCELAR_RESERVA.value
                        }
                    }
                }
            ]
        }

        mock_use_case = MagicMock()
        mock_use_case.executar.return_value = MagicMock(sucesso=True, mensagem="Cancelamento com sucesso", dados={}, erro=None)
        mock_container.caso_uso_cancelar_reserva.return_value = mock_use_case

        # Act
        response = handler(event, {})

        # Assert
        self.assertTrue(response['sucesso'])
        self.assertEqual(response['mensagem'], "Processamento concluído")
        self.assertEqual(len(response['resultados']), 1)
        self.assertTrue(response['resultados'][0]['sucesso'])

    def test_handler_evento_invalido(self):
        # Arrange
        event = {'invalid': 'event'}

        # Act
        response = handler(event, {})

        # Assert
        self.assertFalse(response['sucesso'])
        self.assertEqual(response['mensagem'], "Formato de evento inválido")

    @patch('src.handler.container')
    def test_handler_processamento_com_erro(self, mock_container):
        # Arrange
        event = {
            'Records': [
                {
                    'body': json.dumps({'PedidoId': '123', 'DataPedido': '2023-10-26T10:00:00Z'}),
                    'messageAttributes': {
                        'action': {
                            'stringValue': UseCaseEnum.RESERVAR_ESTOQUE.value
                        }
                    }
                }
            ]
        }

        mock_container.repositorio_pedido.obter_por_id_e_data_pedido.side_effect = Exception("Erro de teste")

        # Act
        response = handler(event, {})

        # Assert
        self.assertFalse(response['sucesso'])
        self.assertEqual(response['mensagem'], "Processamento concluído")
        self.assertEqual(len(response['resultados']), 1)
        self.assertFalse(response['resultados'][0]['sucesso'])
        self.assertEqual(response['resultados'][0]['erro'], "Erro de teste")

if __name__ == '__main__':
    unittest.main()
