
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
