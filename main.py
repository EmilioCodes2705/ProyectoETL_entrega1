import extract
import transform
import load_dw
#import analysis
import config
import mysql.connector

def init_database():
    """Ejecuta el script SQL para crear la base de datos y las tablas del DW."""
    print("🛠️ Creando base de datos y tablas (si no existen)...")
    try:
        # Conexión sin especificar DB (para poder crearla)
        conn = mysql.connector.connect(
            host=config.DB_CONFIG["host"],
            user=config.DB_CONFIG["user"],
            password=config.DB_CONFIG["password"]
        )
        cur = conn.cursor()

        # Leer el archivo SQL
        with open("create_dw.sql", "r", encoding="utf-8") as f:
            sql_script = f.read()

        # Ejecutar comandos (separados por ;)
        for statement in sql_script.split(";"):
            stmt = statement.strip()
            if stmt:
                cur.execute(stmt)

        conn.commit()
        cur.close()
        conn.close()
        print("✅ Base de datos y tablas listas.")
    except Exception as e:
        print("❌ Error al inicializar la base de datos:", e)

def run_pipeline():
    print("📥 [1/5] Creando base de datos y tablas...")
    init_database()

    print("📥 [2/5] Extrayendo datos...")
    df_2023, df_2024 = extract.load_datasets()

    print("🧹 [3/5] Transformando datos...")
    df = transform.clean_and_merge(df_2023, df_2024)

    print(f"💾 Guardando dataset combinado en {config.OUTPUT_FILE}...")
    df.to_csv(config.OUTPUT_FILE, index=False, encoding="utf-8")

    print("📤 [4/5] Cargando datos al Data Warehouse (MySQL)...")
    load_dw.load_dw()  # este script lee dataset_combinado.csv

    #print("📊 [5/5] Generando análisis y visualizaciones...")
    #analysis.analyze(df)

    print("✅ Pipeline ETL + DW completado con éxito.")

if __name__ == "__main__":
    run_pipeline()
