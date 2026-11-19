
CREATE DATABASE IF NOT EXISTS aldeas_sos;
USE aldeas_sos;
CREATE TABLE rol (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(75) NOT NULL,
    CONSTRAINT uq_rol_nombre UNIQUE (nombre)
    
);

CREATE TABLE permiso (
    id_permiso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL,
    descripcion VARCHAR(75) NOT NULL,
    CONSTRAINT uq_permiso_nombre UNIQUE (nombre)
);

CREATE TABLE rol_permiso (
    id_rol_permiso INT AUTO_INCREMENT PRIMARY KEY,
    id_rol INT NOT NULL,
    id_permiso INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol),
    FOREIGN KEY (id_permiso) REFERENCES permiso(id_permiso),
    CONSTRAINT uq_rol_permiso UNIQUE (id_rol, id_permiso)
);

CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_rol INT NOT NULL,
    nombre VARCHAR(60) NOT NULL,
    apellido VARCHAR(60) NOT NULL,
    ci VARCHAR(10) NOT NULL UNIQUE,
    nombre_usuario VARCHAR(40) NOT NULL UNIQUE,
    contrasena_hash CHAR(64) NOT NULL,
    fecha_de_ingreso DATE NOT NULL,
    intentos_fallidos INT NOT NULL DEFAULT 0,
    bloqueo_hasta DATETIME NULL,
    estado VARCHAR(15) NOT NULL DEFAULT 'activo',
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol),
    CONSTRAINT ck_usuario_nombre CHECK (TRIM(nombre) <> '' AND TRIM(apellido) <> ''),
    CONSTRAINT ck_usuario_intentos CHECK (intentos_fallidos BETWEEN 0 AND 3),
    CONSTRAINT ck_usuario_estado CHECK (estado IN ('activo', 'inactivo'))
);

CREATE TABLE registro_acceso (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resultado VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    CONSTRAINT ck_acceso_resultado CHECK (resultado IN ('exitoso', 'fallido', 'bloqueado'))
);

CREATE TABLE hogar (
    id_hogar INT AUTO_INCREMENT PRIMARY KEY,
    numero_hogar INT NOT NULL,
    nombre_hogar VARCHAR(40) NOT NULL,
    direccion VARCHAR(50) NOT NULL,
    capacidad INT NOT NULL,
    estado VARCHAR(15) NOT NULL DEFAULT 'activo',
    CONSTRAINT uq_hogar_numero UNIQUE (numero_hogar),
    CONSTRAINT uq_hogar_nombre UNIQUE (nombre_hogar),
    CONSTRAINT ck_hogar_numero CHECK (numero_hogar > 0),
    CONSTRAINT ck_hogar_nombre CHECK (TRIM(nombre_hogar) <> ''),
    CONSTRAINT ck_hogar_capacidad CHECK (capacidad > 0),
    CONSTRAINT ck_hogar_estado CHECK (estado IN ('activo', 'inactivo'))
    
);

CREATE TABLE cuidadora (
    id_cuidadora INT AUTO_INCREMENT PRIMARY KEY,
    id_hogar INT NOT NULL,
    nombres VARCHAR(40) NOT NULL,
    apellidos VARCHAR(40) NOT NULL,
    ci VARCHAR(10) NOT NULL UNIQUE,
    telefono VARCHAR(20) NOT NULL,
    direccion VARCHAR(75)NOT NULL,
    estado VARCHAR(15) NOT NULL DEFAULT 'activo',
    FOREIGN KEY (id_hogar) REFERENCES hogar(id_hogar),
    CONSTRAINT ck_cuidadora_nombre CHECK (TRIM(nombres) <> '' AND TRIM(apellidos) <> ''),
    CONSTRAINT ck_cuidadora_estado CHECK (estado IN ('activo', 'inactivo'))
);
ALTER TABLE hogar
    ADD COLUMN id_cuidadora_responsable INT NOT NULL,
    ADD CONSTRAINT fk_hogar_responsable
        FOREIGN KEY (id_cuidadora_responsable) REFERENCES cuidadora(id_cuidadora);

CREATE TABLE participantes (
    id_participante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL,
    apellido VARCHAR(40) NOT NULL,
    fecha_de_nacimiento DATE NOT NULL,
    ci VARCHAR(10) NOT NULL UNIQUE,
    sexo CHAR(1) NOT NULL,
    fecha_de_ingreso DATE NOT NULL,
    CONSTRAINT uq_participante UNIQUE (nombre, apellido, fecha_de_nacimiento),
    CONSTRAINT ck_part_nombre CHECK (TRIM(nombre) <> '' AND TRIM(apellido) <> ''),
    CONSTRAINT ck_part_sexo CHECK (sexo IN ('M', 'F')),
    CONSTRAINT ck_part_fechas CHECK (fecha_de_ingreso >= fecha_de_nacimiento)
);

CREATE TABLE asignacion_hogar (
    id_asignacion INT AUTO_INCREMENT PRIMARY KEY,
    id_participante INT NOT NULL,
    id_hogar INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NULL,
    FOREIGN KEY (id_participante) REFERENCES participantes(id_participante),
    FOREIGN KEY (id_hogar) REFERENCES hogar(id_hogar),
    CONSTRAINT uq_asignacion_inicio UNIQUE (id_participante, fecha_inicio),
    CONSTRAINT ck_asig_fechas CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio)
);

CREATE TABLE historial (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_participante INT NOT NULL,
    fecha_ingreso DATE NOT NULL,
    situacion_previa VARCHAR(150),
    situacion_actual VARCHAR(150),
    FOREIGN KEY (id_participante) REFERENCES participantes(id_participante)
);

CREATE TABLE egreso (
    id_egreso INT AUTO_INCREMENT PRIMARY KEY,
    id_participante INT NOT NULL,
    fecha_egreso DATE NOT NULL,
    motivo_egreso VARCHAR(60) NOT NULL,
    FOREIGN KEY (id_participante) REFERENCES participantes(id_participante),
    CONSTRAINT uq_egreso_participante UNIQUE (id_participante),
    CONSTRAINT ck_egreso_motivo CHECK (TRIM(motivo_egreso) <> '')
);

CREATE TABLE seguimiento_egreso (
    id_seguimiento INT AUTO_INCREMENT PRIMARY KEY,
    id_egreso INT NOT NULL,
    fecha_seguimiento DATE NOT NULL,
    residencia_actual VARCHAR(60),
    FOREIGN KEY (id_egreso) REFERENCES egreso(id_egreso),
    CONSTRAINT uq_seguimiento UNIQUE (id_egreso, fecha_seguimiento)
);

CREATE TABLE situacion (
    id_situacion INT AUTO_INCREMENT PRIMARY KEY,
    nombre_situacion VARCHAR(60) NOT NULL,
    CONSTRAINT uq_situacion UNIQUE (nombre_situacion),
    CONSTRAINT ck_situacion_nombre CHECK (TRIM(nombre_situacion) <> '')
);

CREATE TABLE seguimiento_situacion (
    id_seguimiento_situacion INT AUTO_INCREMENT PRIMARY KEY,
    id_seguimiento INT NOT NULL,
    id_situacion INT NOT NULL,
    FOREIGN KEY (id_seguimiento) REFERENCES seguimiento_egreso(id_seguimiento),
    FOREIGN KEY (id_situacion) REFERENCES situacion(id_situacion),
    CONSTRAINT uq_seg_sit UNIQUE (id_seguimiento, id_situacion)
);