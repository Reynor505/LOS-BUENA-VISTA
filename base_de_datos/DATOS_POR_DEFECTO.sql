USE aldeas_sos;

INSERT INTO rol (nombre, descripcion) 
VALUES("Administrador", "Acceso total al sistema"),
("Trabajador social", "Registra y consulta participantes"),
("Consulta", "Solo lectura");

INSERT INTO permiso (nombre, descripcion) 
VALUES("ver_participantes", "Ver datos de participantes"),
("editar_participantes", "Registrar y modificar participantes"),
("gestionar_usuarios", "Crear y administrar usuarios"),
("ver_accesos", "Ver el registro de accesos");

INSERT INTO rol_permiso (id_rol, id_permiso) 
VALUES(1, 1), 
(1, 2), 
(1, 3), 
(1, 4),
(2, 1), 
(2, 2),
(3, 1);
INSERT INTO usuario (id_rol, nombre, apellido, ci, nombre_usuario, contrasena_hash, fecha_de_ingreso) 
VALUES(1, "Ana", "Mamani", "1234567", "admin", SHA2("admin123", 256), "2026-01-10"),
(2, "Carlos", "Quispe", "2345678", "cquispe", SHA2("trabajo123", 256), "2026-02-01"),
(3, "Lucía", "Flores", "3456789", "lflores", SHA2("consulta123", 256), "2026-03-15");

INSERT INTO registro_acceso (id_usuario, resultado) 
VALUES(1, "exitoso"),
(2, "fallido"),
(2, "exitoso");

INSERT INTO hogar (numero_hogar, nombre_hogar, zona, direccion, capacidad) 
VALUES(1, "Hogar Esperanza", "Zona Sur", "Calle 21 de Calacoto", 8),
(2, "Hogar Alegría", "Zona Central", "Av. Arce 1500", 6);


INSERT INTO cuidadora (id_hogar, nombres, apellidos, ci, telefono, direccion) 
VALUES (1, "María", "Condori", "4567890", "71234567", "Calle Los Pinos 12"),
(2, "Rosa", "Choque", "5678901", "72345678", "Av. Busch 340");

-- Cuidadora responsable de cada hogar
UPDATE hogar SET id_cuidadora_responsable = 1 WHERE id_hogar = 1;
UPDATE hogar SET id_cuidadora_responsable = 2 WHERE id_hogar = 2;

INSERT INTO participantes (nombre, apellido, fecha_de_nacimiento, sexo, fecha_de_ingreso) 
VALUES ("Juan", "Apaza", "2012-05-14", "M", "2020-03-01"),
("Sofía", "Mamani", "2015-09-02", "F", "2021-07-10"),
("Diego", "Ramos", "2005-11-23", "M", "2015-01-20");


INSERT INTO asignacion_hogar (id_participante, id_hogar, fecha_inicio, fecha_fin) 
VALUES(1, 1, "2020-03-01", "2023-06-30"),
(1, 2, "2023-07-01", NULL),
(2, 1, "2021-07-10", NULL),
(3, 2, "2015-01-20", "2023-12-15");

INSERT INTO historial (id_participante, fecha_ingreso, situacion_previa, situacion_actual) 
VALUES (1, "2020-03-01", "Derivado por riesgo familiar", "Asiste a la escuela"),
(2, "2021-07-10", "Pérdida del cuidado parental", "Buen desarrollo escolar"),
(3, "2015-01-20", "Abandono", "Egresado");


INSERT INTO egreso (id_participante, fecha_egreso, motivo_egreso) 
VALUES (3, "2023-12-15", "Mayoría de edad");

INSERT INTO situacion (nombre_situacion) 
VALUES("Estudia"), 
("Trabaja"), 
("Vive de forma independiente");

INSERT INTO seguimiento_egreso (id_egreso, fecha_seguimiento, residencia_actual) 
VALUES (1, "2024-06-15", "La Paz, El Alto");

INSERT INTO seguimiento_situacion (id_seguimiento, id_situacion) 
VALUES (1, 1), 
(1, 3);