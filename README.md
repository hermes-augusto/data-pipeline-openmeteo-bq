# Projeto: Pipeline Open-Meteo → BigQuery → Looker Studio

Este projeto tem como objetivo criar um pipeline simples para **extrair dados meteorológicos da API Open-Meteo**, armazená-los no **Google BigQuery** e disponibilizá-los para visualização no **Looker Studio**.

---

## Estrutura inicial (Scaffolding)

Essa branch contém apenas a **estrutura inicial** do projeto com:

- Gerenciador de dependências: **Poetry**
- Arquivos de configuração
- Ambiente `.env` para variáveis sensíveis
- Script principal do pipeline (`main.py`)

---

## Estrutura do Projeto
```plaintext
data-pipeline-openmeteo-bq/
├── src/
│   ├── main.py                      # Orquestra o pipeline
│   ├── config.py                    # Configurações e env
│   ├── services/
│   │   ├── bigquery_service.py      # Classe para interagir com BigQuery
│   │   └── meteo_service.py         # Funções para chamar API Open-Meteo
├── notebooks/
│   ├── data
│   │   ├── subprefeituras_sp_lat_lon_zona.csv  # Dados de lat/long subpref
│   ├── teste_carga_dados.ipynb
│   ├── teste_zonas.ipynb
├── pyproject.toml          # Configuração do Poetry e dependências
├── poetry.lock             # Lockfile para controle de versão
├── .env                    # Exemplo de variáveis de ambiente
└── README.md               # Este arquivo
```

## Dependências

O projeto utiliza as seguintes bibliotecas:

| Pacote                  | Finalidade                                         |
|-------------------------|----------------------------------------------------|
| `pandas`                | Manipulação de dados                               |
| `requests`              | Consumo da API Open-Meteo                          |
| `google-cloud-bigquery` | Integração com o Google BigQuery                   |
| `python-dotenv`         | Leitura de variáveis de ambiente do arquivo `.env` |

As dependências estão controladas pelo **Poetry** no arquivo `pyproject.toml`.

---

## Pré-requisitos

Antes de rodar o pipeline, você precisa:

1. Ter um projeto ativo no **Google Cloud Platform (GCP)**
2. Criar um **Dataset e uma Tabela** no BigQuery
3. Gerar uma **chave de conta de serviço** e salvar o arquivo `.json`
4. Criar um arquivo `.env` com as variáveis necessárias:
5. Ter o **Poetry** instalado:
```bash
pip install poetry
```
```bash
.env
GCP_PROJECT_ID=seu-projeto-id
BQ_DATASET_ID=seu_dataset
BQ_TABLE_ID=sua_tabela
GOOGLE_APPLICATION_CREDENTIALS=/caminho/para/key.json
```