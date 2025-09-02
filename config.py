# config.py
import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# Archivos fuente
DATASET_2023 = "Examen_Saber_11_20231.csv"
DATASET_2024 = "Examen_Saber_11_20241.csv"
OUTPUT_FILE = "dataset_combinado.csv"

# Configuración de la base de datos (MySQL) desde .env
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}


