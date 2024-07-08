# Data Collect from API REST

Este repositório contém um script Python para coletar e processar dados, neste exemplo são pedidos, de um endpoint específico. O script coleta os dados em um intervalo de 5 minutos e realiza o tratamento e salvamento dos dados em arquivos JSON e CSV.

## Requisitos

- Python 3.x
- Bibliotecas Python: `requests`, `pandas`, `numpy`, `schedule`

## Instalação

Clone este repositório e instale as dependências:

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
pip install -r requirements.txt

.
├── json/
│   └── all_orders.json
├── csv/
│   └── all_orders_complete.csv
│   └── table_carts.csv
├── carts_requests_.py
└── README.md
