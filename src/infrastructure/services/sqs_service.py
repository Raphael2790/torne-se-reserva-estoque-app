import json

from botocore.exceptions import ClientError
import boto3
from domain.services.queue_service import MensagemEstoqueConfirmado, ServicoFila


class ServicoSQS(ServicoFila):
    def __init__(self, sqs_client: boto3.client):
        self.sqs = sqs_client
    
    def enviar_mensagem(self, mensagem: MensagemEstoqueConfirmado, url_fila: str) -> None:
        try:
            message_dict = mensagem.to_dict()
            message_body = json.dumps(message_dict)
                   
            self.sqs.send_message(
                QueueUrl=url_fila,
                MessageBody=message_body
            )
        except ClientError as e:
            print(f"Erro ao enviar mensagem para SQS: {e}")
            raise
