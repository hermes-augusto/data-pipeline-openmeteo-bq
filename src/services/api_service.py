import requests
import pandas as pd

def extrair_dados(latitude=-23.55, longitude=-46.63, start_date="2024-01-01", end_date="2024-01-02"):
    """Extrai dados horários do Open-Meteo Archive API com temperatura e sensação térmica"""
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m", "apparent_temperature"],
        "timezone": "America/Sao_Paulo"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Erro na requisição: {response.status_code} - {response.text}")

    data = response.json()
    hourly_data = data.get("hourly", {})

    if not hourly_data:
        raise Exception("Resposta da API não contém dados horários válidos")

    df = pd.DataFrame({
        "datahora": pd.to_datetime(hourly_data.get("time", [])),
        "temperatura": hourly_data.get("temperature_2m", []),
        "sensacao_termica": hourly_data.get("apparent_temperature", [])
    })

    df["latitude"] = latitude
    df["longitude"] = longitude
    df["datahora"] = pd.to_datetime(df["datahora"], utc=True)

    return df
