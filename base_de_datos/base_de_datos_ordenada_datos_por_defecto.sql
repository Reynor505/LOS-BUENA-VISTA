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

CREATE TABLE departamentos (
    id_departamento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL,
    CONSTRAINT uq_departamento_nombre UNIQUE (nombre)
);

CREATE TABLE ciudad (
    id_ciudad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    id_departamento INT NOT NULL,
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento),
    CONSTRAINT uq_ciudad UNIQUE (nombre, id_departamento)
);

CREATE TABLE zona (
    id_zona INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    id_ciudad INT NOT NULL,
    FOREIGN KEY (id_ciudad) REFERENCES ciudad(id_ciudad),
    CONSTRAINT uq_zona UNIQUE (nombre, id_ciudad)
);

CREATE TABLE calles (
    id_calle INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    id_zona INT NOT NULL,
    FOREIGN KEY (id_zona) REFERENCES zona(id_zona),
    CONSTRAINT uq_calle UNIQUE (nombre, id_zona)
);

CREATE TABLE numero_puerta (
    id_puerta INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(10) NOT NULL,
    id_calle INT NOT NULL,
    FOREIGN KEY (id_calle) REFERENCES calles(id_calle),
    CONSTRAINT uq_puerta UNIQUE (numero, id_calle)
);

CREATE TABLE hogar (
    id_hogar INT AUTO_INCREMENT PRIMARY KEY,
    numero_hogar INT NOT NULL,
    nombre_hogar VARCHAR(40) NOT NULL,
    id_departamento INT NOT NULL,
    id_ciudad INT NOT NULL,
    id_zona INT NOT NULL,
    id_calle INT NOT NULL,
    id_puerta INT NULL,
    capacidad INT NOT NULL,
    estado VARCHAR(15) NOT NULL DEFAULT 'activo',
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento),
    FOREIGN KEY (id_ciudad) REFERENCES ciudad(id_ciudad),
    FOREIGN KEY (id_zona) REFERENCES zona(id_zona),
    FOREIGN KEY (id_calle) REFERENCES calles(id_calle),
    FOREIGN KEY (id_puerta) REFERENCES numero_puerta(id_puerta),
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
    fecha_nacimiento DATE NOT NULL,
    fecha_ingreso DATE NOT NULL,
    id_departamento INT NOT NULL,
    id_ciudad INT NOT NULL,
    id_zona INT NOT NULL,
    id_calle INT NOT NULL,
    id_puerta INT NULL,
    estado VARCHAR(15) NOT NULL DEFAULT 'activo',
    FOREIGN KEY (id_hogar) REFERENCES hogar(id_hogar),
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento),
    FOREIGN KEY (id_ciudad) REFERENCES ciudad(id_ciudad),
    FOREIGN KEY (id_zona) REFERENCES zona(id_zona),
    FOREIGN KEY (id_calle) REFERENCES calles(id_calle),
    FOREIGN KEY (id_puerta) REFERENCES numero_puerta(id_puerta),
    CONSTRAINT ck_cuidadora_nombre CHECK (TRIM(nombres) <> '' AND TRIM(apellidos) <> ''),
    CONSTRAINT ck_cuidadora_fechas CHECK (fecha_ingreso >= fecha_nacimiento),
    CONSTRAINT ck_cuidadora_estado CHECK (estado IN ('activo', 'inactivo'))
);

ALTER TABLE hogar
    ADD COLUMN id_cuidadora_responsable INT NULL,
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

ALTER TABLE participantes ADD COLUMN situacion_inicial VARCHAR(350) NOT NULL;

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

-- NUEVO: seguimiento_egreso usa la ubicación en vez de "residencia_actual"
CREATE TABLE seguimiento_egreso (
    id_seguimiento INT AUTO_INCREMENT PRIMARY KEY,
    id_egreso INT NOT NULL,
    fecha_seguimiento DATE NOT NULL,
    id_departamento INT NOT NULL,
    id_ciudad INT NOT NULL,
    id_zona INT NOT NULL,
    id_calle INT NOT NULL,
    id_puerta INT NULL,
    FOREIGN KEY (id_egreso) REFERENCES egreso(id_egreso),
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento),
    FOREIGN KEY (id_ciudad) REFERENCES ciudad(id_ciudad),
    FOREIGN KEY (id_zona) REFERENCES zona(id_zona),
    FOREIGN KEY (id_calle) REFERENCES calles(id_calle),
    FOREIGN KEY (id_puerta) REFERENCES numero_puerta(id_puerta),
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

USE aldeas_sos;

INSERT INTO rol (nombre, descripcion) VALUES
('Administrador', 'Acceso total al sistema'),
('Trabajador social', 'Registra y consulta participantes'),
('Consulta', 'Solo lectura');

INSERT INTO permiso (nombre, descripcion) VALUES
('ver_participantes', 'Ver datos de participantes'),
('editar_participantes', 'Registrar y modificar participantes'),
('gestionar_usuarios', 'Crear y administrar usuarios'),
('ver_accesos', 'Ver el registro de accesos');

INSERT INTO rol_permiso (id_rol, id_permiso) VALUES
(1, 1), (1, 2), (1, 3), (1, 4),
(2, 1), (2, 2),
(3, 1);

INSERT INTO usuario (id_rol, nombre, apellido, ci, nombre_usuario, contrasena_hash, fecha_de_ingreso) VALUES
(1, 'Ana',    'Mamani', '1234567', 'admin',   SHA2('admin123', 256),    '2026-01-10'),
(2, 'Carlos', 'Quispe', '2345678', 'cquispe', SHA2('trabajo123', 256),  '2026-02-01'),
(3, 'Lucía',  'Flores', '3456789', 'lflores', SHA2('consulta123', 256), '2026-03-15');

INSERT INTO registro_acceso (id_usuario, resultado) VALUES
(1, 'exitoso'),
(2, 'fallido'),
(2, 'exitoso');

INSERT INTO departamentos (nombre) VALUES
('LPZ'), ('BN'), ('CH'), ('CBBA'), ('ORU'), ('PND'), ('PTS'), ('SCZ'), ('TJA');

INSERT INTO ciudad (nombre, id_departamento) VALUES
('Trinidad', 2),
('Riberalta', 2),
('Sucre', 3),
('Monteagudo', 3),
('Cochabamba', 4),
('Quillacollo', 4),
('La Paz', 1),
('El Alto', 1),
('Oruro', 5),
('Huanuni', 5),
('Cobija', 6),
('Porvenir', 6),
('Potosí', 7),
('Uyuni', 7),
('Santa Cruz de la Sierra', 8),
('Montero', 8),
('Tarija', 9),
('Yacuiba', 9);

INSERT INTO zona (nombre, id_ciudad) VALUES
('Pompeya', 1), ('San Vicente', 1),
('Villa Británica', 2), ('La Cruz', 2),
('Recoleta', 3), ('San Roque', 3),
('Barrio Lindo', 4), ('San José', 4),
('Cala Cala', 5), ('Queru Queru', 5),
('Tacata', 6), ('Piñami', 6),
('Sopocachi', 7), ('Miraflores', 7),
('Ciudad Satélite', 8), ('Villa Adela', 8),
('Agua de Castilla', 9), ('Villa Challacollo', 9),
('Santa Elena', 10), ('Cataricagua', 10),
('Cataratas', 11), ('Mapajo', 11),
('Central', 12), ('San Luis', 12),
('San Gerardo', 13), ('Cantumarca', 13),
('Ferroviaria', 14), ('Avaroa', 14),
('Equipetrol', 15), ('Urbarí', 15),
('Villa Cochabamba', 16), ('Guabirá', 16),
('Las Panosas', 17), ('El Molino', 17),
('Barrio Nuevo', 18), ('San José de Pocitos', 18);

INSERT INTO calles (nombre, id_zona) VALUES
('Av. 6 de Agosto', 1),
('Calle Mamoré', 2),
('Av. Héroes del Chaco', 3),
('Calle Nicolás Suárez', 4),
('Calle Dalence', 5),
('Calle Grau', 6),
('Calle Sucre', 7),
('Av. Petrolera', 8),
('Av. América', 9),
('Av. Simón López', 10),
('Av. Blanco Galindo', 11),
('Calle Pacheco', 12),
('Av. 20 de Octubre', 13),
('Av. Saavedra', 14),
('Av. Alfredo Sanjinés', 15),
('Av. Bolivia', 16),
('Calle Potosí', 17),
('Av. Dehene', 18),
('Calle Camacho', 19),
('Av. Bolívar', 20),
('Av. 9 de Febrero', 21),
('Calle Bruno Racua', 22),
('Calle Pando', 23),
('Av. Brasil', 24),
('Calle Hoyos', 25),
('Av. Antofagasta', 26),
('Av. Ferroviaria', 27),
('Calle Potosí', 28),
('Av. San Martín', 29),
('Av. Grigotá', 30),
('Av. Circunvalación', 31),
('Av. Fabril', 32),
('Calle Domingo Paz', 33),
('Calle Ingavi', 34),
('Calle Comercio', 35),
('Av. Internacional', 36);

INSERT INTO numero_puerta (numero, id_calle) VALUES
('2100', 13),
('1500', 14),
('12',   15),
('340',  16);

INSERT INTO hogar (numero_hogar, nombre_hogar, id_departamento, id_ciudad, id_zona, id_calle, id_puerta, capacidad) VALUES
(1, 'Hogar Esperanza', 1, 7, 13, 13, 1, 8),
(2, 'Hogar Alegría',   1, 7, 14, 14, 2, 6);

INSERT INTO cuidadora (id_hogar, nombres, apellidos, ci, telefono, fecha_nacimiento, fecha_ingreso, id_departamento, id_ciudad, id_zona, id_calle, id_puerta) VALUES
(1, 'María', 'Condori', '4567890', '71234567', '1985-04-12', '2018-02-01', 1, 8, 15, 15, 3),
(2, 'Rosa',  'Choque',  '5678901', '72345678', '1990-08-25', '2019-06-15', 1, 8, 16, 16, 4);

UPDATE hogar SET id_cuidadora_responsable = 1 WHERE id_hogar = 1;
UPDATE hogar SET id_cuidadora_responsable = 2 WHERE id_hogar = 2;

INSERT INTO participantes (nombre, apellido, fecha_de_nacimiento, ci, sexo, fecha_de_ingreso, situacion_inicial) VALUES
('Juan',  'Apaza',  '2012-05-14', '6789012', 'M', '2020-03-01', 'Derivado por riesgo familiar'),
('Sofía', 'Mamani', '2015-09-02', '7890123', 'F', '2021-07-10', 'Pérdida del cuidado parental'),
('Diego', 'Ramos',  '2005-11-23', '8901234', 'M', '2015-01-20', 'Abandono');

INSERT INTO asignacion_hogar (id_participante, id_hogar, fecha_inicio, fecha_fin) VALUES
(1, 1, '2020-03-01', '2023-06-30'),
(1, 2, '2023-07-01', NULL),
(2, 1, '2021-07-10', NULL),
(3, 2, '2015-01-20', '2023-12-15');

INSERT INTO historial (id_participante, fecha_ingreso, situacion_previa, situacion_actual) VALUES
(1, '2020-03-01', 'Derivado por riesgo familiar',  'Asiste a la escuela'),
(2, '2021-07-10', 'Pérdida del cuidado parental',  'Buen desarrollo escolar'),
(3, '2015-01-20', 'Abandono',                      'Egresado');

INSERT INTO egreso (id_participante, fecha_egreso, motivo_egreso) VALUES
(3, '2023-12-15', 'Mayoría de edad');

INSERT INTO situacion (nombre_situacion) VALUES
('Estudia'),
('Trabaja'),
('Vive de forma independiente');

INSERT INTO seguimiento_egreso (id_egreso, fecha_seguimiento, id_departamento, id_ciudad, id_zona, id_calle, id_puerta) VALUES
(1, '2024-06-15', 1, 8, 16, 16, 4);

INSERT INTO seguimiento_situacion (id_seguimiento, id_situacion) VALUES
(1, 1),
(1, 3);
