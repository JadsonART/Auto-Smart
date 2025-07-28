import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do .env

PIPEDRIVE_TOKEN = os.getenv("PIPEDRIVE_TOKEN")

if not PIPEDRIVE_TOKEN:
    raise Exception("❌ Token da API do Pipedrive não encontrado no .env")

def call_pipedrive(endpoint, method='GET', payload=None):
    sep = '&' if '?' in endpoint else '?'
    url = f'https://api.pipedrive.com/v1/{endpoint}{sep}api_token={PIPEDRIVE_TOKEN}'
    headers = {'Content-Type': 'application/json'}

    response = requests.request(method.upper(), url, headers=headers, json=payload)
    json_data = response.json()

    if not json_data.get('success', False):
        raise Exception(json_data.get('error') or json_data)

    return json_data['data']

# 👇 BLOCO DE TESTE
if __name__ == "__main__":
    print("🔐 Token carregado:", PIPEDRIVE_TOKEN[:6] + "..." if PIPEDRIVE_TOKEN else "NÃO carregado")
    
    try:
        # ✅ Faz uma chamada simples para obter os 1º negócios (deals)
        data = call_pipedrive('deals?limit=1', 'GET')
        print("✅ Conexão com a API do Pipedrive funcionando!")
        print("🔍 Resultado:", data)
    except Exception as e:
        print("❌ Erro ao conectar com a API:", e)
