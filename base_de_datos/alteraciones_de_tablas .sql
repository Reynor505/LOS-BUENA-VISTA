use aldeas_sos;
show TABLE STATUS;
show CREATE TABLE egreso;


ALTER TABLE rol ADD CONSTRAINT uq_rol_nombre UNIQUE (nombre);
ALTER TABLE permiso ADD CONSTRAINT uq_permiso_nombre UNIQUE (nombre);
ALTER TABLE rol_permiso ADD CONSTRAINT uq_rol_permiso UNIQUE (id_rol, id_permiso);

ALTER TABLE usuario
    ADD CONSTRAINT ck_usuario_nombre CHECK (TRIM(nombre) <> '' AND TRIM(apellido) <> ''),
    ADD CONSTRAINT ck_usuario_intentos CHECK (intentos_fallidos BETWEEN 0 AND 3),
    ADD CONSTRAINT ck_usuario_estado CHECK (estado IN ('activo', 'inactivo'));

ALTER TABLE registro_acceso ADD CONSTRAINT ck_acceso_resultado CHECK (resultado IN ('exitoso', 'fallido', 'bloqueado'));
ALTER TABLE hogar
    ADD CONSTRAINT uq_hogar_numero UNIQUE (numero_hogar),
    ADD CONSTRAINT uq_hogar_nombre UNIQUE (nombre_hogar),
    ADD CONSTRAINT ck_hogar_numero CHECK (numero_hogar > 0),
    ADD CONSTRAINT ck_hogar_nombre CHECK (TRIM(nombre_hogar) <> ''),
    ADD CONSTRAINT ck_hogar_capacidad CHECK (capacidad > 0),
    ADD CONSTRAINT ck_hogar_estado CHECK (estado IN ('activo', 'inactivo'));

ALTER TABLE cuidadora
    ADD CONSTRAINT ck_cuidadora_nombre CHECK (TRIM(nombres) <> '' AND TRIM(apellidos) <> ''),
    ADD CONSTRAINT ck_cuidadora_estado CHECK (estado IN ('activo', 'inactivo'));

ALTER TABLE participantes
    ADD CONSTRAINT uq_participante UNIQUE (nombre, apellido, fecha_de_nacimiento),
    ADD CONSTRAINT ck_part_nombre CHECK (TRIM(nombre) <> '' AND TRIM(apellido) <> ''),
    ADD CONSTRAINT ck_part_sexo CHECK (sexo IN ('M', 'F')),
    ADD CONSTRAINT ck_part_fechas CHECK (fecha_de_ingreso >= fecha_de_nacimiento);
ALTER TABLE asignacion_hogar
    ADD CONSTRAINT uq_asignacion_inicio UNIQUE (id_participante, fecha_inicio),
    ADD CONSTRAINT ck_asig_fechas CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio);

ALTER TABLE egreso
    MODIFY COLUMN motivo_egreso VARCHAR(60) NOT NULL,
    ADD CONSTRAINT uq_egreso_participante UNIQUE (id_participante),
    ADD CONSTRAINT ck_egreso_motivo CHECK (TRIM(motivo_egreso) <> '');

ALTER TABLE seguimiento_egreso
    ADD CONSTRAINT uq_seguimiento UNIQUE (id_egreso, fecha_seguimiento);

ALTER TABLE situacion
    ADD CONSTRAINT uq_situacion UNIQUE (nombre_situacion),
    ADD CONSTRAINT ck_situacion_nombre CHECK (TRIM(nombre_situacion) <> '');

ALTER TABLE seguimiento_situacion
    ADD CONSTRAINT uq_seg_sit UNIQUE (id_seguimiento, id_situacion);

ALTER TABLE hogar
    ADD COLUMN id_cuidadora_responsable INT NULL,
    ADD CONSTRAINT fk_hogar_responsable
        FOREIGN KEY (id_cuidadora_responsable) REFERENCES cuidadora(id_cuidadora);

