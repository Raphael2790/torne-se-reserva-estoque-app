#!/bin/bash

set -e

ZIP_NAME=lambda_package.zip
BUILD_DIR=build

echo "🧹 Limpando pacotes anteriores..."
rm -rf $BUILD_DIR $ZIP_NAME

echo "📁 Criando diretório de build..."
mkdir -p $BUILD_DIR

echo "📦 Instalando dependências no diretório '$BUILD_DIR'..."
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r src/requirements.txt -t $BUILD_DIR/

echo "📂 Copiando código-fonte da aplicação para o build..."
cp -r src/* $BUILD_DIR/

echo "🗜️ Gerando pacote .zip..."
cd $BUILD_DIR
zip -r9 ../$ZIP_NAME .
cd ..

echo "✅ Pacote '$ZIP_NAME' gerado com sucesso!"