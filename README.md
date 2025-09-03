# ETL Project – Saber 11

This project implements an **ETL pipeline (Extract, Transform, Load)** to analyze the results of the Saber 11 exams in Colombia.  
The workflow goes from extracting the official datasets, transforming them into a clean and standardized format, and loading them into a **MySQL Data Warehouse** with a star schema.  
Finally, the data is consumed in an interactive dashboard.

---

## 📦 Requirements

1. **Python 3.10+**
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **MySQL 8+** (or MariaDB compatible).

---

## ⚙️ MySQL Configuration

1. Create a dedicated user for this project:
   ```sql
   CREATE USER 'etl_user'@'localhost' IDENTIFIED BY 'etl_password';
   GRANT ALL PRIVILEGES ON dw_saber.* TO 'etl_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

2. The script `create_dw.sql` will automatically create the schema `dw_saber` with the star schema.

---

## 📥 Data Acquisition

Due to licensing restrictions, the datasets are **not included** in this repository.  
They must be requested directly from the official ICFES page via this form:  

👉 [Request datasets](https://forms.office.com/pages/responsepage.aspx?id=EE6GJ-RbT02ttburUSAp6POGIb-ryxBJmGcBwbyeHXdUQk1TTjZLTUMzV0FJWTRYRjg3RE9FVUlLVy4u&origin=lprLink&route=shorturl)

---

## 🚀 Running the Pipeline

```bash
python main.py --csv "Examen_saber_11_20231.csv","Examen_Saber_11_20241.csv" --out .
```

The pipeline performs:
1. **Database and table creation.**
2. **Extraction** of CSV files.
3. **Transformation** of missing values, dates, and encodings.
4. **Loading** into the Data Warehouse in MySQL.
5. **Export** of a combined CSV (`dataset_combinado.csv`).

---

## 🗄️ Data Model (Star Schema)

The model follows a **star schema** design with four dimensions and one fact table:

![Star Schema Diagram](star_schema.png)

### Tables:

- **dim_estudiante** → Student information (socio-demographic and educational conditions).  
- **dim_colegio** → School and institution data.  
- **dim_familia** → Socioeconomic variables of the household.  
- **dim_tiempo** → Period, year, and semester of exam presentation.  
- **hechos_resultados** → Scores, percentiles, and performance levels in each subject.  

---

## 📊 Dashboard KPIs

The interactive dashboard was built in **Power BI** using the Data Warehouse. It includes the following key indicators:

1. **Average percentile in critical reading** → Measures relative performance in reading comprehension.  
2. **Average percentile in social and citizenship skills** → Evaluates critical thinking and civic participation skills.  
3. **Average percentile in natural sciences** → Assesses competencies in biology, chemistry, and physics.  
4. **Average percentile in English** → Measures English proficiency according to ICFES standards.  
5. **Average global percentile** → Overall relative performance compared to all students in the country.  
6. **Average global score by school shift** → Compares results between shifts (morning, afternoon, evening, etc.).  
7. **Department map visualization** → Displays average performance geographically.  
8. **Global score by socioeconomic strata and gender** → Analyzes performance gaps by socioeconomic level and gender.  

---

## 📂 Project Structure

```
Proyecto_ETL/
│── main.py              # Orchestrates the ETL pipeline
│── transform.py         # Data cleaning and transformation
│── load_dw.py           # Data loading into MySQL
│── create_dw.sql        # Data Warehouse schema
│── dataset_combinado.csv # Intermediate result
│── requirements.txt     # Python dependencies
│── README.md            # Project documentation
```

---

## 🔒 Notes

- Datasets are **not included** in the repository.  
- It is recommended to create a dedicated MySQL user with limited permissions.  
- The pipeline was tested on Windows 11 with Python 3.11 and MySQL 8.0
