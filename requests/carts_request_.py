# Bibliotecas
import requests
import pandas as pd
import json
import numpy as np
import schedule
import time
import os

# Função e
def fetch():
    # Requisição
    base_url = "https://api.dooki.com.br/v2"

    alias = 'seu_alias_aqui'
    user_token = "seu_token_aqui"
    user_secret_key = "sua_secret_key_aqui"

    headers = {
        "User-Token": user_token,
        "User-Secret-Key": user_secret_key,
        "Content-Type": "application/json"
    }

    endpoint = f"/{alias}/checkout/carts"

    all_orders = []

    page = 1
    while True:
        params = {
            "page": page,
            "limit": 50  # da pra ajustar esse limite conforme for necessário
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

    print(f"Total de carrinhos coletados: {len(all_orders)}")

    # salvando em um json
    with open("json/all_orders.json", 'w') as file:
        json.dump(all_orders, file, indent=4)
    print("Tudo salvo em all_orders.json")

    # tratamento do json
    def extract_keys(d, parent_key=''):
        items = {}
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(extract_keys(v, new_key))
            else:
                items[new_key] = v
        return items

    orders_list = []

    for order in all_orders:
        order_info = extract_keys(order)
        orders_list.append(order_info)

    # Para csv
    df = pd.DataFrame(orders_list)

    df.to_csv('csv/all_orders_complete.csv', index=False)
    print("Tudo salvo em csv/all_orders_complete.csv")

    # Tratamento
    df = pd.read_csv('csv/all_orders_complete.csv')

    df2 = df.drop(columns=[ 'merchant_id', 'token',
                            'has_recommendation', 'is_upsell',
                            'totalizers.discount','totalizers.subtotal',
                            'totalizers.shipment', 'totalizers.shipment_original_value',
                            'totalizers.shipment_discount_value',
                            'totalizers.progressive_discount_value',
                            'totalizers.combos_discount_value',
                            'totalizers.shipment_formated', 'totalizers.subtotal_formated',
                            'totalizers.discount_formated', 'tracking_data.name', 'tracking_data.email',
                            'unauth_simulate_url','utm_source', 'utm_campaign', 'utm_content', 'utm_term',
                            'utm_medium','last_transaction_status','created_at.timezone_type',
                            'created_at.timezone','updated_at.date', 'updated_at.timezone_type',
                            'updated_at.timezone', 'customer.data.id',
                            'customer.data.merchant_id', 'customer.data.marketplace_id',
                            'customer.data.cluster_id', 'customer.data.active',
                            'customer.data.type','customer.data.name','customer.data.cnpj',
                            'customer.data.birthday','customer.data.phone.full_number',
                            'customer.data.phone.area_code', 'customer.data.phone.number',
                            'customer.data.social_driver', 'customer.data.social_id','customer.data.newsletter',
                            'customer.data.whatsapp','customer.data.utm_source',
                            'customer.data.utm_campaign','customer.data.ip','customer.data.notes',
                            'customer.data.token','customer.data.login_url','customer.data.anonymized',
                            'customer.data.created_at.date','customer.data.created_at.timezone_type',
                            'customer.data.created_at.timezone','customer.data.updated_at.date',
                            'customer.data.updated_at.timezone_type','customer.data.updated_at.timezone',
                            'items.data','transactions.data','spreadsheet.data.customer_phone',
                            'spreadsheet.data.last_order_date','spreadsheet.data.categories',
                             'spreadsheet.data.brands','spreadsheet.data.purchase_url',
                             'metadata.data','search.data.has_shipment_service','search.data.has_address',
                             'search.data.has_customer','search.data.has_refused_payment','search.data.abandoned_step',
                             'search.data.count_recover_mail_sent','search.data.created_at','search.data.updated_at',
                             'emails.data','last_transaction_status.alias','last_transaction_status.name','customer.data.generic_name',
                             'totalizers.total', 'customer.data.state_registration', 'customer.data.razao_social'])

    df2 = df2.fillna('null')

    df2['customer.data.first_name'] = df2['customer.data.first_name'].apply(lambda x: x.capitalize() if isinstance(x, str) else x)

    df2 = df2.applymap(lambda x: x.replace('R$ ', '') if isinstance(x, str) else x)

    df2.to_csv('csv/table_carts.csv', index=False)

# Agendamento da Execução
schedule.every(1).minutes.do(fetch)


while True:
    schedule.run_pending()
    time.sleep(1)
