import pytest
from src.application.mappings.app_mapper import AppMapper
import json


@pytest.fixture
def mapper():
    """Fixture que retorna uma instância do mapper."""
    return AppMapper()


@pytest.fixture
def event_json():
    """Fixture que retorna o JSON do evento."""
    pedido_completo = {
        "cliente": {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "nome": "Raphael",
            "email": "raphael@email.com",
            "telefone": "11999999999",
            "endereco": {
                "logradouro": "Rua Logo Ali",
                "numero": "309",
                "complemento": "Casa 2",
                "bairro": "Bem Ali",
                "cidade": "São Paulo",
                "estado": "SP",
                "cep": "1011010"
            }
        },
        "dataPedido": "2025-04-25T01:48:22.5386879Z",
        "status": 1,
        "itens": [
            {
                "nomeProduto": "Panela de pressão",
                "valor": 100.50,
                "quantidade": 2,
                "total": 201.00,
                "idSku": 91818181
            },
            {
                "nomeProduto": "Jogo de panela",
                "valor": 601.99,
                "quantidade": 1,
                "total": 601.99,
                "idSku": 91818181
            }
        ],
        "valorTotal": 802.99,
        "enderecoEntrega": {
            "logradouro": "Rua Logo Ali",
            "numero": "309",
            "complemento": "Casa 2",
            "bairro": "Bem Ali",
            "cidade": "São Paulo",
            "estado": "SP",
            "cep": "1011010"
        },
        "id": "4cea43ea-2b80-47ff-9e58-98621322b043",
        "dataCriacao": "2025-04-11T22:48:22.5378405-03:00"
    }

    return {
        "Records": [
            {
                "messageId": "1a2b3c4d-5678-9101-1121-314151617181",
                "receiptHandle": "AQEB1234+abcd5678xyz/...",
                "body": {
                    "DataPedido": "2025-04-25T01:48:22.5386879Z",
                    "PedidoCompleto": json.dumps(pedido_completo),
                    "ValorTotal": 802.99,
                    "Status": 1,
                    "Id": "4cea43ea-2b80-47ff-9e58-98621322b043",
                    "Timestamp": "2025-04-11T22:48:25.9030961-03:00"
                },
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1711611234567",
                    "SenderId": "AIDAEXAMPLE:usuario-exemplo",
                    "ApproximateFirstReceiveTimestamp": "1711611234578"
                },
                "messageAttributes": {
                    "TipoEvento": {
                        "stringValue": "PedidoCriado",
                        "dataType": "String"
                    }
                },
                "md5OfBody": "1a79a4d60de6718e8e5b326e338ae533",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:minha-fila",
                "awsRegion": "us-east-1"
            }
        ]
    }
