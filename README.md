# ETL

Este repositório contém um script Python para coletar e processar dados de pedidos de um endpoint específico. O script coleta os dados em um intervalo de 1 minuto, realiza o tratamento e salvamento dos dados em arquivos JSON e CSV, e faz a carga dos dados no Google Drive. Este projeto de ETL (Extração, Transformação e Carga) foi desenvolvido como um serviço prestado para a Vocaliza Digital.

## Requisitos

- Python 3.x
- Bibliotecas Python: `requests`, `pandas`, `numpy`, `schedule`

## Estrutura do Projeto

```plaintext
.
├── json/
│   └── all_orders.json
├── csv/
│   └── all_orders_complete.csv
│   └── table_carts.csv
├── config.py
├── etl.py
└── README.md
```

### Pipeline de ETL
1. Extração: O script faz uma requisição GET para a API REST fornecida, coletando os dados dos pedidos.
2. Transformação: Os dados são tratados usando pandas, realizando limpeza e formatação.
3. Carga: Os dados processados são salvos em arquivos JSON e CSV e enviados para o Google Drive.

### Automação com Schedule
O script etl.py utiliza a biblioteca schedule para ser executado automaticamente a cada 1 minuto.

### Sobre o projeto
Este projeto de ETL foi desenvolvido como um serviço prestado para a Vocaliza Digital.