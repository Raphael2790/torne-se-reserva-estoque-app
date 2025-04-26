import json
from typing import Any, Dict

from pydantic import ValidationError
from utils.logger_decorator import log_execution
from utils.timer_decorator import timer_execution
from ioc.container import Container

container = Container()
container.init_resources()

logger = container.logger()
app_mapper = container.app_mapper()
caso_uso = container.caso_uso_reservar_estoque()


def __processar_mensagem(mensagem: Dict[str, Any]) -> Dict[str, Any]:
    """Processa uma única mensagem do SQS."""
    try:
        logger.info(f"Processando mensagem: {mensagem}")
        requisicao = app_mapper.map_to_reserva_estoque_request(mensagem['body'])
        resposta = caso_uso.executar(requisicao)

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
            for mensagem in event['Records']:
                resultado = __processar_mensagem(mensagem)
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
