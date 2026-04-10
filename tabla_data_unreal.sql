-- ============================================
-- PASO 1 — Nueva tabla dim_alumno
-- ============================================
CREATE TABLE datos_reales.dim_alumno (
    id_alumno           SERIAL PRIMARY KEY,
    matricula           VARCHAR(20)  NOT NULL UNIQUE,
    fecha_nacimiento    DATE,
    nacionalidad        VARCHAR(50),
    lugar_nacimiento    VARCHAR(100),
    colonia             VARCHAR(100),
    año_ingreso         SMALLINT
);

COMMENT ON TABLE datos_reales.dim_alumno IS
    'Datos individuales del alumno — solo se llena con datos sintéticos, NULL para datos reales';

-- ============================================
-- PASO 2 — Agregar turno a dim_carrera
-- ============================================
ALTER TABLE datos_reales.dim_carrera
    ADD COLUMN IF NOT EXISTS turno VARCHAR(20)
    CHECK (turno IN ('Matutino', 'Vespertino', 'Sabatino'));

COMMENT ON COLUMN datos_reales.dim_carrera.turno IS
    'NULL para registros reales donde no se tiene este dato';

-- ============================================
-- PASO 3 — Agregar ubicacion a dim_escuela_procedencia
-- ============================================
ALTER TABLE datos_reales.dim_escuela_procedencia
    ADD COLUMN IF NOT EXISTS ubicacion VARCHAR(20)
    CHECK (ubicacion IN ('Merida', 'Municipio', 'Foraneo'));

COMMENT ON COLUMN datos_reales.dim_escuela_procedencia.ubicacion IS
    'Clasificación geográfica simplificada — se llena desde datos sintéticos';

-- ============================================
-- PASO 4 — Agregar id_alumno a fact_matricula
-- ============================================
ALTER TABLE datos_reales.fact_matricula
    ADD COLUMN IF NOT EXISTS id_alumno INT
    REFERENCES datos_reales.dim_alumno(id_alumno);

COMMENT ON COLUMN datos_reales.fact_matricula.id_alumno IS
    'NULL para datos reales (no tienen alumno individual), poblado solo con datos sintéticos';

-- Índice para búsquedas por alumno
CREATE INDEX IF NOT EXISTS idx_matricula_alumno
    ON datos_reales.fact_matricula(id_alumno);