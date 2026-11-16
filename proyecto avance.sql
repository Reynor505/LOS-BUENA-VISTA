show DATABASES;
USE aldeas_sos;
SHOW TABLE STATUS;
CREATE TABLE rol (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(75)
);
CREATE TABLE permiso (
    id_permiso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    descripcion VARCHAR(150)
);
CREATE TABLE rol_permiso (
   id_rol_permiso INT AUTO_INCREMENT PRIMARY KEY,
   id_rol INT NOT NULL,
   id_permiso INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol),
    FOREIGN KEY (id_permiso) REFERENCES permiso(id_permiso)
);
CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_rol INT NOT NULL,
    nombre VARCHAR(60) NOT NULL,
    apellido VARCHAR(60) NOT NULL,
    ci VARCHAR(20) NOT NULL UNIQUE,
    nombre_usuario VARCHAR(40) NOT NULL UNIQUE,
    contrasena_hash CHAR(64) NOT NULL,
    fecha_de_ingreso DATE NOT NULL,
    intentos_fallidos INT NOT NULL DEFAULT 0,
    bloqueo_hasta DATETIME NULL,
    estado VARCHAR(15) NOT NULL DEFAULT 'activo',
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
);

drop TABLE rol_permiso;
CREATE TABLE registro_acceso (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resultado VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE hogar (
    id_hogar INT AUTO_INCREMENT PRIMARY KEY,
    numero_hogar INT NOT NULL,
    nombre_hogar VARCHAR(40) NOT NULL,
    zona VARCHAR(40),
    direccion VARCHAR(50),
    capacidad INT NOT NULL,
    estado VARCHAR(15) NOT NULL DEFAULT 'activo'
);
show table status;