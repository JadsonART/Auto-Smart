import os
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

# ================== CONFIGURAÇÕES ==================

load_dotenv()  # Carrega variáveis do arquivo .env

PIPEDRIVE_TOKEN = os.getenv('PIPEDRIVE_TOKEN')
LIMITE_POR_EXECUCAO = 50
ARQUIVO_CONTROLE = 'controle_start.txt'

# ================== FUNÇÕES =========================


def call_pipedrive(endpoint, method='GET', payload=None):
    sep = '&' if '?' in endpoint else '?'
    url = f'https://api.pipedrive.com/v1/{endpoint}{sep}api_token={PIPEDRIVE_TOKEN}'
    headers = {'Content-Type': 'application/json'}
    response = requests.request(
        method.upper(), url, headers=headers, json=payload)
    json_data = response.json()
    if not json_data.get('success', False):
        raise Exception(json_data.get('error') or json_data)
    return json_data['data']


def listar_todos_os_deals():
    todos = []
    start = 0
    limit = 500

    while True:
        data = call_pipedrive(f'deals?start={start}&limit={limit}', 'GET')
        if not data:
            break
        todos.extend(data)
        if len(data) < limit:
            break
        start += limit
    print(f"Total de negócios: {len(todos)}")
    return todos


def salvar_start(novo_start):
    with open(ARQUIVO_CONTROLE, 'w') as f:
        f.write(str(novo_start))


def carregar_start():
    try:
        with open(ARQUIVO_CONTROLE, 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0


def calcular_tempo_setores():
    start = carregar_start()
    todos_deals = listar_todos_os_deals()
    deals = todos_deals[start:start + LIMITE_POR_EXECUCAO]
    hoje = datetime.now()
    negocios_atualizados = []

    def parse_date(value):
        return datetime.fromisoformat(value) if value else None

    def dias_entre(inicio, fim):
        return (fim - inicio).days if inicio and fim else None

    for deal in deals:
        def get(k): return parse_date(deal.get(k))
        contratacao = get('26c684e1bb3fe6db7d6506cf5307b7d1a59ca9e1')

        fim_itbi = get('069bf183917fb89a77a63f5cf793db5c7a2b2c48')
        fim_registro = get('8e1b76dc0501ad8514f3ac51616746851028840e')
        base_registro = max(
            filter(None, [fim_itbi, fim_registro]), default=None)

        campos = {
            "triagem":      {'tempo': 'bbac0e070ec5e5f0a9a3f0e7c1fb424b7b6a2f89', 'fim': 'fb1aa427746a8e05d6dadc6eccfc51dd1cdc992d', 'base': contratacao},
            "contratos":    {'tempo': '4e8d2da58746cbc340d5b932f506df740181eb4a', 'fim': 'f7eba1ca53326f57f7e2d5da4d4fe9d155e99651', 'base': contratacao},
            "itbi":         {'tempo': '8b9a654b5b711d2cbd2b8ded2dc65ad98870bea0', 'fim': '069bf183917fb89a77a63f5cf793db5c7a2b2c48', 'base': contratacao},
            "titularidade": {'tempo': '1d842804127719c86a4dc13a9b145ca34c51fb00', 'fim': '3022a1c39e2c992e3cb38fe82e0f22ef421cc033', 'base': fim_itbi},
            "averbacao":    {'tempo': 'fd4ba7019e40b30720079318877bd107ee2d6183', 'fim': 'd477e9641dba9e9c71a49c181b0997b94705fa54', 'base': fim_registro},
            "registro":     {'tempo': '061ddf05a7e166a22185f97862a08daf124ef117', 'fim': '8e1b76dc0501ad8514f3ac51616746851028840e', 'base': base_registro},
            "iptu":         {'tempo': '39b6db06f14596b3733eb0f4bbab55654207946e', 'fim': '46f5eea72dbdcd18c9c19d2ddee73bff046fc14b', 'base': contratacao},
            "condominio":   {'tempo': '4d954dd4295820415fc6cb2994877161ae0d4749', 'fim': '2c3da637bcb6a12f68f20a24f734c89698d98f81', 'base': contratacao},
            "desocupacao":  {'tempo': '9ee390bc15ad631c18d6addff7c18e2f01aff114', 'fim': '7b8d8be1f1e06a6f33930aa8e59ac82fcfc3f0ea', 'base': fim_registro},
        }

        body = {}
        for setor, info in campos.items():
            fim = get(info['fim'])
            base = info['base']
            if not fim and base:
                dias = dias_entre(base, hoje)
                if dias is not None:
                    body[info['tempo']] = dias

        if body:
            url = f'https://api.pipedrive.com/v1/deals/{deal["id"]}?api_token={PIPEDRIVE_TOKEN}'
            try:
                res = requests.put(
                    url, headers={'Content-Type': 'application/json'}, json=body)
                res.raise_for_status()
                negocios_atualizados.append({
                    "id": deal["id"],
                    "titulo": deal.get("title", "Sem título")
                })
            except requests.RequestException as e:
                print(f"Erro ao atualizar negócio {deal['id']}: {e}")
                continue

        time.sleep(0.3)

    novo_start = start + LIMITE_POR_EXECUCAO
    if novo_start >= len(todos_deals):
        salvar_start(0)
        print("Todos os negócios foram processados.")
    else:
        salvar_start(novo_start)
        print(f"Próxima execução continuará do índice {novo_start}.")

    if negocios_atualizados:
        print("Negócios atualizados nesta execução:")
        for n in negocios_atualizados:
            print(f"→ ID: {n['id']} | Título: {n['titulo']}")
    else:
        print("Nenhum negócio foi atualizado nesta execução.")


def listar_campos_customizados():
    campos = call_pipedrive('dealFields', 'GET')
    for campo in campos:
        print(
            f"Nome: {campo['name']} | Key: {campo['key']} | Tipo: {campo['field_type']}")
    return campos


# ================== EXECUÇÃO =========================

if __name__ == '__main__':
    calcular_tempo_setores()
