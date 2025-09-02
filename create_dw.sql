-- ===============================================
-- CREACIÓN DEL DATA WAREHOUSE SABER 11
-- Esquema en estrella
-- ===============================================

CREATE SCHEMA IF NOT EXISTS dw_saber;
USE dw_saber;

-- ========================
-- Dimensión Estudiante
-- ========================
CREATE TABLE IF NOT EXISTS dim_estudiante (
    id_estudiante INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    estu_consecutivo VARCHAR(50),
    estu_estudiante VARCHAR(255),
    estu_tipodocumento VARCHAR(50),
    estu_genero VARCHAR(50),
    estu_fechanacimiento DATE,
    estu_etnia VARCHAR(50),
    estu_discapacidad VARCHAR(50),
    estu_repite VARCHAR(50),
    estu_privado_libertad VARCHAR(50),
    estu_tieneetnia VARCHAR(50),
    estu_tiporemuneracion VARCHAR(50),
    estu_grado VARCHAR(50),
    estu_horassemanatrabaja VARCHAR(50),
    estu_inse_individual FLOAT,
    estu_nse_individual VARCHAR(50),
    estu_dedicacioninternet VARCHAR(50),
    estu_dedicacionlecturadiaria VARCHAR(50),
    estu_pais_reside VARCHAR(50),
    estu_depto_reside VARCHAR(50),
    estu_mcpio_reside VARCHAR(50)
);

-- ========================
-- Dimensión Colegio
-- ========================
CREATE TABLE IF NOT EXISTS dim_colegio (
    id_colegio INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    cole_cod_dane_establecimiento VARCHAR(50),
    cole_cod_dane_sede VARCHAR(50),
    cole_nombre_establecimiento VARCHAR(255),
    cole_nombre_sede VARCHAR(255),
    cole_sede_principal VARCHAR(50),
    cole_area_ubicacion VARCHAR(50),
    cole_depto_ubicacion VARCHAR(50),
    cole_mcpio_ubicacion VARCHAR(50),
    cole_cod_depto_ubicacion VARCHAR(50),
    cole_cod_mcpio_ubicacion VARCHAR(50),
    cole_naturaleza VARCHAR(50),
    cole_bilingue VARCHAR(50),
    cole_calendario VARCHAR(50),
    cole_caracter VARCHAR(50),
    cole_genero VARCHAR(50),
    cole_jornada VARCHAR(50),
    cole_codigo_icfes VARCHAR(50),
    estu_nse_establecimiento VARCHAR(50)
);

-- ========================
-- Dimensión Familia
-- ========================
CREATE TABLE IF NOT EXISTS dim_familia (
    id_familia INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    fami_comecarnepescadohuevo VARCHAR(50),
    fami_comecerealfrutoslegumbre VARCHAR(50),
    fami_comelechederivados VARCHAR(50),
    fami_cuartoshogar INT,
    fami_educacionmadre VARCHAR(50),
    fami_educacionpadre VARCHAR(50),
    fami_estratovivienda VARCHAR(50),
    fami_numlibros INT,
    fami_personashogar INT,
    fami_situacioneconomica VARCHAR(50),
    fami_tieneautomovil VARCHAR(50),
    fami_tienecomputador VARCHAR(50),
    fami_tieneconsolavideojuegos VARCHAR(50),
    fami_tienehornomicroogas VARCHAR(50),
    fami_tieneinternet VARCHAR(50),
    fami_tienelavadora VARCHAR(50),
    fami_tienemotocicleta VARCHAR(50),
    fami_tieneserviciotv VARCHAR(50),
    fami_trabajolabormadre VARCHAR(255),
    fami_trabajolaborpadre VARCHAR(255)
);

-- ========================
-- Dimensión Tiempo
-- ========================
CREATE TABLE IF NOT EXISTS dim_tiempo (
    id_tiempo INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    periodo VARCHAR(50),
    anio INT,
    semestre INT
);

-- ========================
-- Tabla de Hechos
-- ========================
CREATE TABLE IF NOT EXISTS hechos_resultados (
    id_resultado INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT UNSIGNED,
    id_colegio INT UNSIGNED,
    id_familia INT UNSIGNED,
    id_tiempo INT UNSIGNED,
    punt_global FLOAT,
    punt_matematicas FLOAT,
    punt_lectura_critica FLOAT,
    punt_sociales_ciudadanas FLOAT,
    punt_c_naturales FLOAT,
    punt_ingles FLOAT,
    percentil_global FLOAT,
    percentil_matematicas FLOAT,
    percentil_lectura_critica FLOAT,
    percentil_sociales_ciudadanas FLOAT,
    percentil_c_naturales FLOAT,
    percentil_ingles FLOAT,
    desemp_matematicas VARCHAR(50),
    desemp_lectura_critica VARCHAR(50),
    desemp_sociales_ciudadanas VARCHAR(50),
    desemp_c_naturales VARCHAR(50),
    desemp_ingles VARCHAR(50),
    nivel_estudiante VARCHAR(20),
    CONSTRAINT fk_estudiante FOREIGN KEY (id_estudiante) REFERENCES dim_estudiante(id_estudiante),
    CONSTRAINT fk_colegio FOREIGN KEY (id_colegio) REFERENCES dim_colegio(id_colegio),
    CONSTRAINT fk_familia FOREIGN KEY (id_familia) REFERENCES dim_familia(id_familia),
    CONSTRAINT fk_tiempo FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo(id_tiempo)
);

