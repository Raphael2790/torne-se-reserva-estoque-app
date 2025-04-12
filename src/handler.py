import json
import os
from typing import Any, Dict

import boto3
from dotenv import load_dotenv

from domain.services.queue_service import MensagemFila
from infrastructure.repositories.dynamodb_product_repository import RepositorioItemEstoqueDynamoDB
from infrastructure.services.sqs_service import ServicoSQS
from use_cases.reserve_inventory import ReservarEstoque, RequisicaoReservaEstoque

load_dotenv()

# Inicializa os clients AWS
dynamodb_client = boto3.resource('dynamodb')
sqs_client = boto3.client('sqs')

# Inicializa os serviços
repositorio_item_estoque = RepositorioItemEstoqueDynamoDB(
    dynamodb_client=dynamodb_client,
    nome_tabela=os.getenv('DYNAMODB_TABLE_NAME', 'inventory')
)
servico_fila = ServicoSQS(sqs_client=sqs_client)

# URLs das filas
URL_FILA_RESERVA = os.getenv('RESERVATION_QUEUE_URL')
URL_FILA_SEM_ESTOQUE = os.getenv('OUT_OF_STOCK_QUEUE_URL')


def processar_mensagem(mensagem: Dict[str, Any]) -> Dict[str, Any]:
    """Processa uma única mensagem do SQS."""
    try:
        # Extrai o corpo da mensagem
        corpo = json.loads(mensagem['body'])
        requisicao = RequisicaoReservaEstoque(
            data_pedido=corpo['DataPedido'],
            pedido_completo=corpo['PedidoCompleto'],
            valor_total=corpo['ValorTotal'],
            status=corpo['Status']
        )
        
        # Executa o caso de uso
        caso_uso = ReservarEstoque(repositorio_item_estoque)
        resposta = caso_uso.executar(requisicao)
        
        # Envia mensagem apropriada para a fila baseado no resultado
        if resposta.sucesso:
            mensagem_fila = MensagemFila(
                id_pedido=requisicao.pedido_completo,  # Usando o pedido completo como ID
                id_produto=str(requisicao.itens[0].id_sku),  # Usando o primeiro SKU como referência
                quantidade=sum(item.quantidade for item in requisicao.itens),
                status='RESERVADO',
                mensagem=resposta.mensagem
            )
            servico_fila.enviar_mensagem(mensagem_fila, URL_FILA_RESERVA)
        else:
            mensagem_fila = MensagemFila(
                id_pedido=requisicao.pedido_completo,
                id_produto=str(requisicao.itens[0].id_sku),
                quantidade=sum(item.quantidade for item in requisicao.itens),
                status='SEM_ESTOQUE',
                mensagem=resposta.mensagem
            )
            servico_fila.enviar_mensagem(mensagem_fila, URL_FILA_SEM_ESTOQUE)
        
        return {
            'sucesso': resposta.sucesso,
            'mensagem': resposta.mensagem,
            'dados': resposta.dados,
            'erro': resposta.erro
        }
        
    except Exception as e:
        return {
            'sucesso': False,
            'mensagem': 'Erro ao processar requisição',
            'erro': str(e)
        }


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Processa o evento SQS que pode conter múltiplas mensagens."""
    try:
        resultados = []
        
        # Verifica se o evento contém o array Records
        if 'Records' in event:
            # Processa cada mensagem no array Records
            for mensagem in event['Records']:
                resultado = processar_mensagem(mensagem)
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
