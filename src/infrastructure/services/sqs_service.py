import json

from botocore.exceptions import ClientError

from domain.services.queue_service import MensagemFila, ServicoFila


class ServicoSQS(ServicoFila):
    def __init__(self, sqs_client):
        self.sqs = sqs_client
    
    def enviar_mensagem(self, mensagem: MensagemFila, url_fila: str) -> None:
        try:
            corpo_mensagem = {
                'id_pedido': mensagem.id_pedido,
                'id_produto': mensagem.id_produto,
                'quantidade': mensagem.quantidade,
                'status': mensagem.status,
                'mensagem': mensagem.mensagem
            }
            
            self.sqs.send_message(
                QueueUrl=url_fila,
                MessageBody=json.dumps(corpo_mensagem)
            )
        except ClientError as e:
            print(f"Erro ao enviar mensagem para SQS: {e}")
            raise 