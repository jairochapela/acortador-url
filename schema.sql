CREATE TABLE IF NOT EXISTS rutas (
    ruta_corta CHAR(10) PRIMARY KEY,
    url_original VARCHAR(1000) NOT NULL
);