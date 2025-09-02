import pandas as pd
import numpy as np

def clean_and_merge(df1, df2):
    # Normalizar columnas
    df1.columns = df1.columns.str.lower().str.strip()
    df2.columns = df2.columns.str.lower().str.strip()

    # Completar periodos vacíos
    df1["periodo"] = df1["periodo"].fillna("2023-1")
    df2["periodo"] = df2["periodo"].fillna("2024-1")

    # Unir datasets
    df = pd.concat([df1, df2], ignore_index=True)

    # Eliminar duplicados por identificador único
    df.drop_duplicates(subset=["estu_consecutivo"], inplace=True)

    # Limpiar strings vacíos y "nan"/"none"
    df = df.applymap(lambda x: np.nan if (pd.isna(x) or str(x).strip().lower() in ["", "nan", "none"]) else x)

    # Identificar columnas numéricas y categóricas
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns

    # Rellenar columnas numéricas con la media
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            mean_value = df[col].mean()
            df[col].fillna(mean_value, inplace=True)

    # Rellenar columnas categóricas con la moda
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            mode_value = df[col].mode()[0] if not df[col].mode().empty else "SIN_DATO"
            df[col].fillna(mode_value, inplace=True)

    # Normalizar género
    if "estu_genero" in df.columns:
        df["estu_genero"] = df["estu_genero"].str.upper().str.strip()
        df["estu_genero"] = df["estu_genero"].replace({"FEMENINO": "F", "MASCULINO": "M"})

    # Normalizar fechas
    if "estu_fechanacimiento" in df.columns:
        df["estu_fechanacimiento"] = pd.to_datetime(df["estu_fechanacimiento"], errors="coerce")
        df["estu_fechanacimiento"] = df["estu_fechanacimiento"].dt.strftime("%Y-%m-%d")
        df["estu_fechanacimiento"] = df["estu_fechanacimiento"].replace("NaT", np.nan)
        # Rellenar fechas nulas con la moda (fecha más frecuente)
        mode_fecha = df["estu_fechanacimiento"].mode()[0] if not df["estu_fechanacimiento"].mode().empty else "2000-01-01"
        df["estu_fechanacimiento"].fillna(mode_fecha, inplace=True)

    # Crear variable categórica "nivel_estudiante"
    def categorizar(puntaje):
        try:
            puntaje = float(puntaje)
            if puntaje >= 300:
                return "Alto"
            elif puntaje >= 250:
                return "Medio"
            else:
                return "Bajo"
        except:
            return "SIN_DATO"

    df["nivel_estudiante"] = df["punt_global"].apply(categorizar)

    def texto_a_int(valor):
        if pd.isna(valor):
            return 0
        if isinstance(valor, str):
            valor = valor.strip().lower()
            mapa = {
                "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
                "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10
            }
            if valor in mapa:
                return mapa[valor]
            # Si es un número en texto, conviértelo
            try:
                return int(valor)
            except:
                return 0
        try:
            return int(valor)
        except:
            return 0

    # Aplica la función a las columnas INT de familia
    for col in ["fami_cuartoshogar", "fami_numlibros", "fami_personashogar"]:
        if col in df.columns:
            df[col] = df[col].apply(texto_a_int).astype(int)

    return df
