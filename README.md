# 📘 Proyecto ETL – SABER 11

Este proyecto implementa un **pipeline ETL (Extract, Transform, Load)** para procesar los datos de los exámenes **Saber 11** y cargarlos en un **Data Warehouse** en **MySQL** con un esquema en estrella.

---

## 📋 Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado lo siguiente:

- [Python 3.10+](https://www.python.org/downloads/)  
- [MySQL Server 8+](https://dev.mysql.com/downloads/mysql/)  
- [Git](https://git-scm.com/downloads) (opcional, si clonas el repo)  

### Librerías de Python necesarias

Instálalas con:

```bash
pip install -r requirements.txt
```

Si no tienes `requirements.txt`, puedes instalar manualmente:

```bash
pip install pandas numpy mysql-connector-python python-dotenv
```

---

## 🗄️ Configuración de la base de datos

1. Ingresa a MySQL como root:

```bash
mysql -u root -p
```

2. Crea un usuario dedicado al proyecto y dale permisos:

```sql
CREATE USER 'etl_user'@'localhost' IDENTIFIED BY 'password_etl';
GRANT ALL PRIVILEGES ON dw_saber.* TO 'etl_user'@'localhost';
FLUSH PRIVILEGES;
```

> 🔑 **Recomendación**: no uses el usuario `root` para el pipeline.

3. El pipeline creará automáticamente el esquema `dw_saber` y sus tablas al ejecutarse.

---

## 🔑 Variables de entorno

El proyecto usa un archivo **`.env`** para almacenar credenciales de la base de datos.  
Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
DB_HOST=localhost
DB_USER=etl_user
DB_PASSWORD=password_etl
DB_NAME=dw_saber
```

⚠️ Importante: agrega `.env` a tu **`.gitignore`** para no subirlo a GitHub.

---

## 📊 Datos de entrada

Los datasets de **Saber 11** no están incluidos en este repositorio.  
Debes solicitarlos en la página oficial:

👉 [Formulario para solicitar datos](https://forms.office.com/pages/responsepage.aspx?id=EE6GJ-RbT02ttburUSAp6POGIb-ryxBJmGcBwbyeHXdUQk1TTjZLTUMzV0FJWTRYRjg3RE9FVUlLVy4u&origin=lprLink&route=shorturl)

Una vez descargados los archivos `.csv`, colócalos en la carpeta del proyecto.

Ejemplo:  
```
Proyecto_ETL/
├── Examen_saber_11_20231.csv
├── Examen_Saber_11_20241.csv
├── main.py
├── transform.py
├── load_dw.py
├── create_dw.sql
├── config.py
└── .env
```

---

## ▶️ Ejecución del pipeline

Ejecuta el pipeline con:

```bash
python main.py --csv "Examen_saber_11_20231.csv","Examen_Saber_11_20241.csv" --out .
```

El pipeline hará lo siguiente:

1. Crear base de datos y tablas (`create_dw.sql`).
2. Extraer y unificar datos desde los archivos `.csv`.
3. Transformar los datos (limpieza, imputación de valores, normalización de fechas).
4. Guardar el dataset combinado en `dataset_combinado.csv`.
5. Cargar los datos en el Data Warehouse `dw_saber`.

Si todo sale bien, verás:

```
✅ Carga al DW finalizada con éxito.
```

---

## ⚠️ Notas importantes

- El pipeline está preparado para manejar valores faltantes (`NaN`, `None`, etc.) y asignar valores por defecto en algunos casos (ejemplo: fechas, periodos).  
- La tabla de hechos **no incluye la columna `id_resultado` en los inserts**, ya que es `AUTO_INCREMENT`.  
- Si modificas los nombres de columnas en los CSV, deberás ajustar también el código en `transform.py` y `load_dw.py`.  

---

## 📦 Dependencias utilizadas

- **pandas** → manipulación de datos.  
- **numpy** → operaciones numéricas.  
- **mysql-connector-python** → conexión a MySQL.  
- **python-dotenv** → manejo de variables de entorno.  

---

## 👨‍💻 Autores
Emilio Marquez Gallego
Samuel Uribe Zamora
Juan Pablo Lopez Paruam


Proyecto desarrollado para la materia **ETL - Ing. de datos e Inteligencia Artificial**.  
