#!/bin/bash

# Nome da imagem base
IMAGE="python:3.10-slim"
CONTAINER_NAME="download-dependencies"

# Caminho local do arquivo requirements.txt
REQUIREMENTS_PATH="./src/requirements.txt"
SRC_PATH="./src"
LOCAL_OUTPUT_DIR="./build/package"

# Verifica se o arquivo existe
if [ ! -f "$REQUIREMENTS_PATH" ]; then
  echo "Arquivo requirements.txt não encontrado em $REQUIREMENTS_PATH"
  exit 1
fi

# Garante que a pasta de saída esteja limpa
rm -rf "$LOCAL_OUTPUT_DIR"
mkdir -p "$LOCAL_OUTPUT_DIR"

# Cria o container
docker run --name $CONTAINER_NAME -dit $IMAGE bash

# Executa a instalação com cache em um diretório fixo
docker exec -it $CONTAINER_NAME bash -c "
  apt-get update &&
  apt-get install -y gcc &&
  apt-get install -y zip &&
  python -m ensurepip --upgrade &&
  python -m pip install --upgrade pip &&
  mkdir -p /app
"

# Copia com verificação
if docker cp "$REQUIREMENTS_PATH" "$CONTAINER_NAME:/app/requirements.txt"; then
  echo "✔️ Arquivo requirements.txt copiado com sucesso."
else
  echo "❌ Falha ao copiar o requirements.txt para o container."
  docker rm -f $CONTAINER_NAME
  exit 1
fi

# Copia com verificação
if docker cp "$SRC_PATH" "$CONTAINER_NAME:/app/src"; then
  echo "✔️ Arquivo src copiado com sucesso."
else
  echo "❌ Falha ao copiar o src para o container."
  docker rm -f $CONTAINER_NAME
  exit 1
fi

docker exec -it $CONTAINER_NAME bash -c "
  mkdir -p /app/cache &&
  pip install --no-cache-dir -r /app/requirements.txt -t /app/cache &&
  cp -r /app/src/* /app/cache &&
  cd /app/cache &&
  zip -r9 /app/reserva_estoque_lambda.zip .
"

# Copia a pasta de cache de volta para a máquina local
docker cp "$CONTAINER_NAME:/app/reserva_estoque_lambda.zip" "$LOCAL_OUTPUT_DIR"

# Mostra os pacotes instalados como resultado
docker exec -it $CONTAINER_NAME pip list

echo "📦 Pacotes baixados foram copiados para: $LOCAL_OUTPUT_DIR"

# Opcional: remove o container
docker rm -f $CONTAINER_NAME

exit 0