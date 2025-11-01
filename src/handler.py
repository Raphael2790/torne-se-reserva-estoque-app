import json
from typing import Any, Dict
from enum import Enum
from pydantic import ValidationError
from utils.logger_decorator import log_execution
from utils.timer_decorator import timer_execution
from ioc.container import Container

class UseCaseEnum(Enum):
    RESERVAR_ESTOQUE = 'reservar_estoque'
    CANCELAR_RESERVA = 'cancelar_reserva'

container = Container()
container.init_resources()

logger = container.logger()
app_mapper = container.app_mapper()
caso_uso_reserva = container.caso_uso_reservar_estoque()
caso_uso_cancelamento = container.caso_uso_cancelar_reserva()
repositorio_pedido = container.repositorio_pedido()

def __processar_mensagem(mensagem: Dict[str, Any], message_attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Processa uma única mensagem do SQS."""
    try:
        logger.info(f"Processando mensagem: {mensagem}")
        
        action = message_attributes.get('action', {'stringValue': UseCaseEnum.RESERVAR_ESTOQUE.value})['stringValue']

        if action == UseCaseEnum.CANCELAR_RESERVA.value:
            cancelamento_message = app_mapper.map_to_cancelamento_message(mensagem['body'])
            pedido = repositorio_pedido.obter_por_id_e_data_pedido(cancelamento_message.PedidoId, cancelamento_message.DataPedido)
            requisicao = app_mapper.map_to_cancelar_reserva_request(pedido)
            resposta = caso_uso_cancelamento.executar(requisicao)
        else:
            pedido_message = app_mapper.map_to_pedido_message(mensagem['body'])
            pedido = repositorio_pedido.obter_por_id_e_data_pedido(pedido_message.PedidoId, pedido_message.DataPedido)
            requisicao = app_mapper.map_to_reserva_estoque_request(pedido.pedido_completo)
            resposta = caso_uso_reserva.executar(requisicao)

        return {
            'sucesso': resposta.sucesso,
            'mensagem': resposta.mensagem,
            'dados': resposta.dados,
            'erro': resposta.erro
        }
    except ValidationError as e:
        logger.error(f"Erro ao validar requisição: {e}")
        return {
            'sucesso': False,
            'mensagem': 'Erro ao processar requisição',
            'erro': str(e)
        }
    except Exception as e:
        logger.error(f"Erro ao processar requisição: {e}")
        return {
            'sucesso': False,
            'mensagem': 'Erro ao processar requisição',
            'erro': str(e)
        }


@log_execution(logger)
@timer_execution()
def handler(event: Dict[str, Any], _: Any) -> Dict[str, Any]:
    """Processa o evento SQS que pode conter múltiplas mensagens."""
    try:
        resultados = []
        
        # Verifica se o evento contém o array Records
        if 'Records' in event:
            # Processa cada mensagem no array Records
            for record in event['Records']:
                message_attributes = record.get('messageAttributes', {})
                resultado = __processar_mensagem(record, message_attributes)
                resultados.append(resultado)
            
            return {
                'sucesso': all(r['sucesso'] for r in resultados),
                'mensagem': 'Processamento concluído',
                'resultados': resultados
            }
        else:
            # Caso o evento não tenha o formato esperado
            return {
                'sucesso': False,
                'mensagem': 'Formato de evento inválido',
                'erro': 'O evento não contém o array Records'
            }
            
    except Exception as e:
        return {
            'sucesso': False,
            'mensagem': 'Erro ao processar evento',
            'erro': str(e)
        }


if __name__ == "__main__":
    with open('events/event.json', 'r') as file:
        event = json.load(file)
    print(handler(event, {}))
