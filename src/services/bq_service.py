from google.cloud import bigquery
from config import PROJECT_ID, DATASET_ID

class BigQueryService:
    def __init__(self):
        self.client = bigquery.Client(project=PROJECT_ID)

    def criar_tabela(self,table_id="dados_openmeteo"):
        """Cria uma tabela particionada por mês e clusterizada por subprefeitura no BigQuery, se ela ainda não existir."""
        client = bigquery.Client(project=PROJECT_ID)
        tabela_ref = client.dataset(DATASET_ID).table(table_id)

        try:
            client.get_table(tabela_ref)
            print(f"Tabela já existe: {PROJECT_ID}.{DATASET_ID}.{table_id}")
        except Exception:
            schema = [
                bigquery.SchemaField("datahora", "TIMESTAMP"),
                bigquery.SchemaField("temperatura", "FLOAT"),
                bigquery.SchemaField("sensacao_termica", "FLOAT"),
                bigquery.SchemaField("latitude", "FLOAT"),
                bigquery.SchemaField("longitude", "FLOAT"),
                bigquery.SchemaField("subprefeitura", "STRING"),
                bigquery.SchemaField("zona", "STRING"),
            ]

            tabela = bigquery.Table(tabela_ref, schema=schema)

            
            tabela.time_partitioning = bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.MONTH,
                field="datahora",
                expiration_ms=None 
            )

            tabela.clustering_fields = ["subprefeitura"]

            tabela = client.create_table(tabela)
            print(f"Tabela criada com sucesso: {tabela.full_table_id}")

        return table_id

    def carregar_dataframe(self, df, table_id,write_disposition="WRITE_APPEND"):
        tabela_id = f"{PROJECT_ID}.{DATASET_ID}.{table_id}"

        job_config = bigquery.LoadJobConfig(
            write_disposition=write_disposition,
            autodetect=False,
            require_partition_filter=True,
        )

        job = self.client.load_table_from_dataframe(df, tabela_id, job_config=job_config)
        job.result()
        print(f"Dados carregados na tabela {tabela_id}")