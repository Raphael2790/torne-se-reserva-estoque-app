import json
import pytest
from src.application.mappings.app_mapper import AppMapper
from pydantic import ValidationError


class TestAppMapperMessage:
    def test_map_to_pedido_message(self):
        mapper = AppMapper()
        data = {
            "DataPedido": "2025-04-25T01:48:22.5386879Z",
            "Status": 1,
            "Id": "4cea43ea-2b80-47ff-9e58-98621322b043",
            "PedidoId": "pedido-123",
            "Timestamp": "2025-04-11T22:48:25.9030961-03:00"
        }
        result = mapper.map_to_pedido_message(json.dumps(data))
        assert result.DataPedido == data["DataPedido"]
        assert result.Status == data["Status"]
        assert result.Id == data["Id"]
        assert result.PedidoId == data["PedidoId"]
        assert result.Timestamp == data["Timestamp"]

    def test_map_to_pedido_message_com_json_invalido(self):
        mapper = AppMapper()
        invalid_json = "dados invalidos"
        with pytest.raises(json.JSONDecodeError):
            mapper.map_to_pedido_message(invalid_json)

    def test_map_to_pedido_message_missing_fields(self):
        mapper = AppMapper()
        incomplete_data = {
            "DataPedido": "2025-04-25T01:48:22.5386879Z",
            "Status": 1,
            "Id": "4cea43ea-2b80-47ff-9e58-98621322b043"
        }
        with pytest.raises(ValidationError):
            mapper.map_to_pedido_message(json.dumps(incomplete_data))
