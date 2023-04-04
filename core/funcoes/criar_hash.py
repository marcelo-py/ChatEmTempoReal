import hashlib


# esse função serve para retornar a combinação da hash entre dois IDs não importanto a ordem.
def gerar_nome_da_sala(id1, id2):
    ids = [str(id1), str(id2)]

    ids.sort()  # ordena os IDs em ordem crescente
    ids_separados = '-'.join(ids).encode('utf-8')  # junta os IDs em uma string e codifica como bytes
    hash_object = hashlib.blake2b(ids_separados, digest_size=18).hexdigest()  # aplica a função de hash SHA256 como string hexadecimal
    
    return hash_object   # retorna o resultado como uma string
    