

def reservar_estoque_uc(estoque, produto_id, quantidade):
    """
    Função para reservar estoque de um produto.

    :param estoque: Dicionário representando o estoque de produtos.
    :param produto_id: ID do produto a ser reservado.
    :param quantidade: Quantidade a ser reservada.
    :return: Mensagem de sucesso ou erro.
    """
    if produto_id not in estoque:
        return "Produto não encontrado no estoque."

    if estoque[produto_id] < quantidade:
        return "Estoque insuficiente para reserva."

    estoque[produto_id] -= quantidade
    return f"Reserva de {quantidade} unidades do produto {produto_id} realizada com sucesso."


# Exemplo de uso
if __name__ == "__main__":
    estoque = {
        "produto_1": 10,
        "produto_2": 5,
        "produto_3": 0
    }

    produto_id = "produto_1"
    quantidade = 3

    print(__name__)

    resultado = reservar_estoque_uc(estoque, produto_id, quantidade)
    print(resultado)  # Saída: Reserva de 3 unidades do produto produto_1 realizada com sucesso.
    print(estoque)  # Saída: {'produto_1': 7, 'produto_2': 5, 'produto_3': 0}
