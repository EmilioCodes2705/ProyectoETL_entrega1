import pandas as pd
import config

def load_datasets():
    df_2023 = pd.read_csv(config.DATASET_2023, sep=";", encoding="utf-8", low_memory=False)
    df_2024 = pd.read_csv(config.DATASET_2024, sep=";", encoding="utf-8", low_memory=False)

    # Agregar columna periodo
    df_2023["periodo"] = "2023-1"
    df_2024["periodo"] = "2024-1"

    return df_2023, df_2024
