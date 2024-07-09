# Bibliotecas
import requests
import pandas as pd
import numpy as np
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import dados_api

# Requisição
base_url = "https://api.dooki.com.br/v2"

alias = dados_api.alias
user_token = dados_api.user_token
user_secret_key = dados_api.user_secret_key

headers = {
    "User-Token": user_token,
    "User-Secret-Key": user_secret_key,
    "Content-Type": "application/json"
}

endpoint = f"/{alias}/orders"

all_orders = []

page = 1
while True:
    params = {
        "page": page,
        "limit": 50  
    }
    response = requests.get(f"{base_url}{endpoint}", headers=headers, params=params)

    if response.status_code == 200:
        orders = response.json()

        if not orders['data']:
            break

        all_orders.extend(orders['data'])

        page += 1
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)
        break

print(f"Total de pedidos coletados: {len(all_orders)}")

# Salvar em um JSON
if not os.path.exists("json"):
    os.makedirs("json")

with open("json/pedidos.json", 'w') as file:
    json.dump(all_orders, file, indent=4)
print("Tudo salvo em pedidos.json")

with open('json/pedidos.json') as file:
    all_orders = json.load(file)

# Extrair chaves de dicionários aninhados
def extract_keys(d, parent_key=''):
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}.{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(extract_keys(v, new_key))
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.update(extract_keys(item, f"{new_key}.{i}"))
                else:
                    items[f"{new_key}.{i}"] = item
        else:
            items[new_key] = v
    return items

orders_list = []

for order in all_orders:
    order_info = extract_keys(order)
    orders_list.append(order_info)

# Converte em CSV
df = pd.DataFrame(orders_list)

if not os.path.exists("csv"):
    os.makedirs("csv")

df.to_csv('csv/pedidos_complete.csv', index=False)
print("Tudo salvo em csv/pedidos_complete.csv")

# Definir o escopo
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

try:
    # teste de autenticação
    creds = ServiceAccountCredentials.from_json_keyfile_name(dados_api.credentials, scope)
    client = gspread.authorize(creds)

    
    df = pd.read_csv('csv/pedidos_complete.csv')

    # Tratamento adicional (dados nulos e tendendo ao infinito)
    
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.fillna(0, inplace=True)

    
    spreadsheet_id = '15Arw0PpMMwRLUBdkVEKbshJwrTB3i1b1VgaB4gli2x4'

    try:
        sheet = client.open_by_key(spreadsheet_id)

        worksheet = sheet.get_worksheet(0)

        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        print("Dados atualizados com sucesso na planilha.")
    
    except gspread.SpreadsheetNotFound:
        print(f"Planilha com ID '{spreadsheet_id}' não foi encontrada.")
    except gspread.exceptions.APIError as e:
        print(f"Erro na API do Google Sheets: {e}")
    except PermissionError:
        print("Erro de permissão ao acessar a planilha. Verifique se o arquivo JSON tem as permissões corretas.")
    
except FileNotFoundError:
    print("Arquivo de credenciais JSON não encontrado.")
except ValueError as e:
    print(f"Erro no arquivo de credenciais JSON: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")