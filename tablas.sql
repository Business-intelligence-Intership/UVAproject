-- ============================================
-- SCHEMA: datos_reales
-- ============================================
CREATE SCHEMA IF NOT EXISTS datos_reales;

-- --------------------------------------------
-- DIM_CARRERA
-- --------------------------------------------
CREATE TABLE datos_reales.dim_carrera (
    id_carrera      SERIAL PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    clave_carrera   VARCHAR(5)   NOT NULL,
    modalidad       VARCHAR(20)  NOT NULL 
                    CHECK (modalidad IN ('Escolarizada', 'Mixto/Sabatino')),
    tipo_ciclo      VARCHAR(20)  NOT NULL 
                    CHECK (tipo_ciclo IN ('Cuatrimestral', 'Semestral')),
    ciclos_periodo  VARCHAR(50)[] NOT NULL, -- ej: '{Enero-Abril,Mayo-Agosto,Septiembre-Diciembre}'
    año_inicio      SMALLINT     NOT NULL,
    UNIQUE (nombre, modalidad)
);

-- --------------------------------------------
-- DIM_PERIODO
-- --------------------------------------------
CREATE TABLE datos_reales.dim_periodo (
    id_periodo      SERIAL PRIMARY KEY,
    año             SMALLINT    NOT NULL,
    nombre_ciclo    VARCHAR(30) NOT NULL, -- ej: 'Enero-Abril'
    numero_ciclo    SMALLINT    NOT NULL, -- 1, 2 o 3 (cuatri) / 1 o 2 (semestral)
    tipo_ciclo      VARCHAR(20) NOT NULL 
                    CHECK (tipo_ciclo IN ('Cuatrimestral', 'Semestral')),
    fecha_inicio    DATE,
    fecha_fin       DATE,
    UNIQUE (año, nombre_ciclo, tipo_ciclo)
);

-- --------------------------------------------
-- DIM_ESCUELA_PROCEDENCIA
-- (Incluye escuelas generales Y de odontología)
-- --------------------------------------------
CREATE TABLE datos_reales.dim_escuela_procedencia (
    id_escuela      SERIAL PRIMARY KEY,
    nombre          VARCHAR(200) NOT NULL UNIQUE,
    municipio       VARCHAR(100),
    estado          VARCHAR(100),
    direccion       TEXT,
    latitud         DECIMAL(9,6),
    longitud        DECIMAL(9,6),
    es_odontologia  BOOLEAN      NOT NULL DEFAULT FALSE
);

-- --------------------------------------------
-- FACT_MATRICULA
-- --------------------------------------------
CREATE TABLE datos_reales.fact_matricula (
    id_matricula        SERIAL PRIMARY KEY,
    id_carrera          INT      NOT NULL REFERENCES datos_reales.dim_carrera(id_carrera),
    id_periodo          INT      NOT NULL REFERENCES datos_reales.dim_periodo(id_periodo),
    id_escuela          INT      REFERENCES datos_reales.dim_escuela_procedencia(id_escuela), -- NULL permitido
    edad                SMALLINT NOT NULL CHECK (edad BETWEEN 14 AND 80),
    sexo                VARCHAR(10) NOT NULL CHECK (sexo IN ('Masculino', 'Femenino')),
    cantidad_alumnos    SMALLINT NOT NULL CHECK (cantidad_alumnos > 0),
    es_dato_real        BOOLEAN  NOT NULL DEFAULT TRUE
);

-- --------------------------------------------
-- ÍNDICES para queries BI frecuentes
-- --------------------------------------------
CREATE INDEX idx_matricula_carrera  ON datos_reales.fact_matricula(id_carrera);
CREATE INDEX idx_matricula_periodo  ON datos_reales.fact_matricula(id_periodo);
CREATE INDEX idx_matricula_escuela  ON datos_reales.fact_matricula(id_escuela);
CREATE INDEX idx_escuela_odonto     ON datos_reales.dim_escuela_procedencia(es_odontologia);