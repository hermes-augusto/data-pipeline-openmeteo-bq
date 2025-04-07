import requests
import pandas as pd
from google.cloud import bigquery
from config import PROJECT_ID, DATASET_ID

def criar_tabela(table_id="dados_openmeteo"):
    """Cria uma tabela no BigQuery com schema fixo, se ela ainda não existir"""
    client = bigquery.Client(project=PROJECT_ID)
    tabela_ref = client.dataset(DATASET_ID).table(table_id)

    try:
        client.get_table(tabela_ref)
        print(f"ℹ️ Tabela já existe: {PROJECT_ID}.{DATASET_ID}.{table_id}")
    except Exception:
        schema = [
            bigquery.SchemaField("latitude", "FLOAT"),
            bigquery.SchemaField("longitude", "FLOAT"),
            bigquery.SchemaField("temperatura", "FLOAT"),
            bigquery.SchemaField("vento", "FLOAT"),
            bigquery.SchemaField("hora", "TIMESTAMP"),
        ]
        tabela = bigquery.Table(tabela_ref, schema=schema)
        tabela = client.create_table(tabela)
        print(f"✅ Tabela criada com sucesso: {tabela.full_table_id}")

    return table_id

def extrair_dados(latitude=-23.55, longitude=-46.63):
    """Extrai dados do Open-Meteo para uma latitude/longitude"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }
    response = requests.get(url, params=params)
    data = response.json()
    current = data.get("current_weather", {})

    df = pd.DataFrame([{
        "latitude": latitude,
        "longitude": longitude,
        "temperatura": current.get("temperature"),
        "vento": current.get("windspeed"),
        "hora": current.get("time")
    }])

    return df

def carregar_no_bigquery(df: pd.DataFrame, table_id: str):
    """Carrega dados no BigQuery"""
    client = bigquery.Client(project=PROJECT_ID)
    tabela_id = f"{PROJECT_ID}.{DATASET_ID}.{table_id}"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
        autodetect=True,
    )

    job = client.load_table_from_dataframe(df, tabela_id, job_config=job_config)
    job.result()
    print(f"✅ Dados carregados na tabela {tabela_id}")

def main():
    table_id = criar_tabela("dados_openmeteo")
    df = extrair_dados()
    print("📥 Dados extraídos:")
    print(df)

    carregar_no_bigquery(df, table_id)
    print("🏁 Pipeline concluído com sucesso.")

if __name__ == "__main__":
    main()
