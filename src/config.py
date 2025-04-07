import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Variáveis usadas no projeto
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET_ID")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
