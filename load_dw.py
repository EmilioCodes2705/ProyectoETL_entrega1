import pandas as pd
import mysql.connector
from mysql.connector import Error
import config

# ========================
# FUNCIONES AUXILIARES
# ========================
def get_connection():
    return mysql.connector.connect(**config.DB_CONFIG)


def insert_and_get_id(cur, table, columns, values):
    # Normalizar valores: convertir NaN, None o strings "nan" en NULL
    clean_values = []
    for v in values:
        if v is None:
            clean_values.append(None)
        elif isinstance(v, float) and pd.isna(v):  # NaN de pandas
            clean_values.append(None)
        elif isinstance(v, str) and v.strip().lower() == "nan":
            clean_values.append(None)
        else:
            clean_values.append(v)

    placeholders = ", ".join(["%s"] * len(columns))
    sql = f"""
        INSERT INTO {table} ({", ".join(columns)})
        VALUES ({placeholders})
    """
    cur.execute(sql, clean_values)
    return cur.lastrowid

def safe_float(val):
    try:
        if pd.isna(val):
            return None
        return float(val)
    except:
        return None



# ========================
# PROCESO DE CARGA AL DW
# ========================
def load_dw():
    df = pd.read_csv(config.OUTPUT_FILE, sep=",", encoding="utf-8", low_memory=False)

    # Normalizar columnas
    df.columns = df.columns.str.lower().str.strip()

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():
        # ---- DIM ESTUDIANTE ----
        id_estudiante = insert_and_get_id(cur, "dim_estudiante", [
            "estu_consecutivo","estu_estudiante","estu_tipodocumento","estu_genero",
            "estu_fechanacimiento","estu_etnia","estu_discapacidad","estu_repite",
            "estu_privado_libertad","estu_tieneetnia","estu_tiporemuneracion","estu_grado",
            "estu_horassemanatrabaja","estu_inse_individual","estu_nse_individual",
            "estu_dedicacioninternet","estu_dedicacionlecturadiaria","estu_pais_reside",
            "estu_depto_reside","estu_mcpio_reside"
        ], [
            row.get("estu_consecutivo"), row.get("estu_estudiante"), row.get("estu_tipodocumento"),
            row.get("estu_genero"), row.get("estu_fechanacimiento"), row.get("estu_etnia"),
            row.get("estu_discapacidad"), row.get("estu_repite"), row.get("estu_privado_libertad"),
            row.get("estu_tieneetnia"), row.get("estu_tiporemuneracion"), row.get("estu_grado"),
            row.get("estu_horassemanatrabaja"), row.get("estu_inse_individual"),
            row.get("estu_nse_individual"), row.get("estu_dedicacioninternet"),
            row.get("estu_dedicacionlecturadiaria"), row.get("estu_pais_reside"),
            row.get("estu_depto_reside"), row.get("estu_mcpio_reside")
        ])

        # ---- DIM COLEGIO ----
        id_colegio = insert_and_get_id(cur, "dim_colegio", [
            "cole_cod_dane_establecimiento","cole_cod_dane_sede","cole_nombre_establecimiento",
            "cole_nombre_sede","cole_sede_principal","cole_area_ubicacion","cole_depto_ubicacion",
            "cole_mcpio_ubicacion","cole_cod_depto_ubicacion","cole_cod_mcpio_ubicacion",
            "cole_naturaleza","cole_bilingue","cole_calendario","cole_caracter",
            "cole_genero","cole_jornada","cole_codigo_icfes","estu_nse_establecimiento"
        ], [
            row.get("cole_cod_dane_establecimiento"), row.get("cole_cod_dane_sede"),
            row.get("cole_nombre_establecimiento"), row.get("cole_nombre_sede"),
            row.get("cole_sede_principal"), row.get("cole_area_ubicacion"),
            row.get("cole_depto_ubicacion"), row.get("cole_mcpio_ubicacion"),
            row.get("cole_cod_depto_ubicacion"), row.get("cole_cod_mcpio_ubicacion"),
            row.get("cole_naturaleza"), row.get("cole_bilingue"), row.get("cole_calendario"),
            row.get("cole_caracter"), row.get("cole_genero"), row.get("cole_jornada"),
            row.get("cole_codigo_icfes"), row.get("estu_nse_establecimiento")
        ])

        # ---- DIM FAMILIA ----
        id_familia = insert_and_get_id(cur, "dim_familia", [
            "fami_comecarnepescadohuevo","fami_comecerealfrutoslegumbre","fami_comelechederivados",
            "fami_cuartoshogar","fami_educacionmadre","fami_educacionpadre","fami_estratovivienda",
            "fami_numlibros","fami_personashogar","fami_situacioneconomica","fami_tieneautomovil",
            "fami_tienecomputador","fami_tieneconsolavideojuegos","fami_tienehornomicroogas",
            "fami_tieneinternet","fami_tienelavadora","fami_tienemotocicleta","fami_tieneserviciotv",
            "fami_trabajolabormadre","fami_trabajolaborpadre"
        ], [
            row.get("fami_comecarnepescadohuevo"), row.get("fami_comecerealfrutoslegumbre"),
            row.get("fami_comelechederivados"), row.get("fami_cuartoshogar"),
            row.get("fami_educacionmadre"), row.get("fami_educacionpadre"),
            row.get("fami_estratovivienda"), row.get("fami_numlibros"),
            row.get("fami_personashogar"), row.get("fami_situacioneconomica"),
            row.get("fami_tieneautomovil"), row.get("fami_tienecomputador"),
            row.get("fami_tieneconsolavideojuegos"), row.get("fami_tienehornomicroogas"),
            row.get("fami_tieneinternet"), row.get("fami_tienelavadora"),
            row.get("fami_tienemotocicleta"), row.get("fami_tieneserviciotv"),
            row.get("fami_trabajolabormadre"), row.get("fami_trabajolaborpadre")
        ])

        # ---- DIM TIEMPO ----
        periodo = row.get("periodo")

        anio, semestre = None, None
        if periodo and isinstance(periodo, str) and "-" in periodo:
            try:
                anio, semestre = periodo.split("-")
            except:
                anio, semestre = (None, None)

        # Validaciones
        try:
            anio = int(anio) if anio else 2023
        except:
            anio = 2023

        try:
            semestre = int(semestre) if semestre else 1
        except:
            semestre = 1

        periodo_final = periodo if periodo else f"{anio}-{semestre}"

        id_tiempo = insert_and_get_id(cur, "dim_tiempo", [
            "periodo","anio","semestre"
        ], [
            periodo_final, anio, semestre
        ])

        # ---- HECHOS ----

        cur.execute("""
                INSERT INTO dw_saber.hechos_resultados (
                    id_estudiante,id_colegio,id_familia,id_tiempo,
                    punt_global,punt_matematicas,punt_lectura_critica,
                    punt_sociales_ciudadanas,punt_c_naturales,punt_ingles,
                    percentil_global,percentil_matematicas,percentil_lectura_critica,
                    percentil_sociales_ciudadanas,percentil_c_naturales,percentil_ingles,
                    desemp_matematicas,desemp_lectura_critica,desemp_sociales_ciudadanas,
                    desemp_c_naturales,desemp_ingles,nivel_estudiante
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            """, (
                id_estudiante, id_colegio, id_familia, id_tiempo,
                row.get("punt_global"), row.get("punt_matematicas"),
                row.get("punt_lectura_critica"), row.get("punt_sociales_ciudadanas"),
                row.get("punt_c_naturales"), row.get("punt_ingles"),
                row.get("percentil_global"), row.get("percentil_matematicas"),
                row.get("percentil_lectura_critica"), row.get("percentil_sociales_ciudadanas"),
                row.get("percentil_c_naturales"), row.get("percentil_ingles"),
                row.get("desemp_matematicas"), row.get("desemp_lectura_critica"),
                row.get("desemp_sociales_ciudadanas"), row.get("desemp_c_naturales"),
                row.get("desemp_ingles"), row.get("nivel_estudiante")
            ))


    conn.commit()
    cur.close()
    conn.close()
    print("✅ Carga al DW finalizada con éxito.")

if __name__ == "__main__":
    load_dw()
