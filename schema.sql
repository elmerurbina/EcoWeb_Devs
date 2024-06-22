-- Database schema
-- Campaign table
CREATE TABLE campaign (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_campania VARCHAR(255) NOT NULL,
    descripcion_campania TEXT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    presupuesto DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Foro debates table
CREATE TABLE foro_debates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    contenido TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sistema autenticacion table
CREATE TABLE sistemaautenticacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    correo VARCHAR(255) UNIQUE NOT NULL,
    contrasenia VARCHAR(255) NOT NULL,
    confirmar_contrasenia VARCHAR(255)
);
