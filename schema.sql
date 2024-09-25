-- Esquema de la base de datos

-- Crear Base de Datos
CREATE DATABASE VerdeNica;

       -- Tablas para almacenar la informacion
CREATE TABLE campaign (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_campania VARCHAR(255) NOT NULL,
    descripcion_campania TEXT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    presupuesto DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para manejar la informcion del foro
CREATE TABLE foro_debates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    punto_de_vista TEXT NOT NULL,
    otras_observaciones TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para las preguntas
CREATE TABLE foro_preguntas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    pregunta TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para las conversaciones
CREATE TABLE foro_hilos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    tema TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla del Sistema autenticacion
CREATE TABLE sistemaautenticacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    correo VARCHAR(255) UNIQUE NOT NULL,
    contrasenia VARCHAR(255) NOT NULL,
    confirmar_contrasenia VARCHAR(255)
);

-- Tabla de las denuncias
CREATE TABLE denuncias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    evidencia LONGBLOB,
    evidencia_filename VARCHAR(255),
    ubicacion VARCHAR(255) NOT NULL,
    denunciados VARCHAR(255),
    otros_detalles VARCHAR(500)
);

-- Tabla para los comentarios
CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    campaign_id INT NOT NULL,
    user_id INT NOT NULL,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaign(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES sistemaautenticacion(id) ON DELETE CASCADE
);

-- Tabla para guardar las respuestas
CREATE TABLE respuestas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    respuesta TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para las publicaciones de biodiversidad
CREATE TABLE publicaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image_data LONGBLOB
);


-- Tabla para guardar la informacion del reconocimiento de especies con IA
CREATE TABLE ia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    image_data LONGBLOB NOT NULL,
    species_name VARCHAR(255),
    species_description TEXT,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

