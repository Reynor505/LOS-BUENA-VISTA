use aldeas_sos;
ALTER TABLE seguimiento_egreso; 

create table departamentos(
    Id_departamento int PRIMARY KEY auto_increment,
    nombre varchar (4) not null
);
ALTER TABLE departamentos MODIFY nombre VARCHAR(4) NOT NULL unique;

INSERT INTO departamentos (nombre)
VALUES ('LPZ'), ('BN'), ('CH'), ('CBBA'), ('ORU'), ('PND'), ('PTS'), ('SCZ'), ('TJA');

create table Ciudad(
    Id_ciudad int PRIMARY KEY AUTO_INCREMENT,
    nombre varchar(24) not null,
    id_departamento int,
    FOREIGN KEY (id_departamento) REFERENCES departamentos(Id_departamento)
);

ALTER TABLE Ciudad MODIFY nombre VARCHAR(24) NOT NULL unique;

select * from Ciudad;

UPDATE Ciudad SET id_departamento = 1 WHERE nombre IN ('La Paz', 'El Alto');
UPDATE Ciudad SET id_departamento = 2 WHERE nombre IN ('Trinidad', 'Riberalta');
UPDATE Ciudad SET id_departamento = 3 WHERE nombre IN ('Sucre', 'Monteagudo');
UPDATE Ciudad SET id_departamento = 4 WHERE nombre IN ('Cochabamba', 'Quillacollo');
UPDATE Ciudad SET id_departamento = 5 WHERE nombre IN ('Oruro', 'Huanuni');
UPDATE Ciudad SET id_departamento = 6 WHERE nombre IN ('Cobija', 'Porvenir');
UPDATE Ciudad SET id_departamento = 7 WHERE nombre IN ('Potosí', 'Uyuni');
UPDATE Ciudad SET id_departamento = 8 WHERE nombre IN ('Santa Cruz de la Sierra', 'Montero');
UPDATE Ciudad SET id_departamento = 9 WHERE nombre IN ('Tarija', 'Yacuiba');

DELETE FROM Ciudad WHERE id_ciudad = 25;


INSERT INTO Ciudad (nombre) 
VALUES("Trinidad"),
("Riberalta"),
("Sucre"),
("Monteagudo"),
("Cochabamba"),
("Quillacollo"),
("La Paz"),
("El Alto"),
("Oruro"),
("Huanuni"),
("Cobija"),
("Porvenir"),
("Potosí"),
("Uyuni"),
("Santa Cruz de la Sierra"),
("Montero"),
("Tarija"),
("Yacuiba");

create table zona (
    id_zona int primary key auto_increment,
    nombre varchar(45) not null,
    id_ciudad int,
    FOREIGN KEY (id_ciudad) REFERENCES Ciudad(Id_ciudad)
);

INSERT INTO zona (nombre, id_ciudad) VALUES
    ('Pompeya', 1),
    ('San Vicente', 1),
    ('Villa Británica', 2),
    ('La Cruz', 2),
    ('Recoleta', 3),
    ('San Roque', 3),
    ('Barrio Lindo', 4),
    ('San José', 4),
    ('Cala Cala', 5),
    ('Queru Queru', 5),
    ('Tacata', 6),
    ('Piñami', 6),
    ('Sopocachi', 7),
    ('Miraflores', 7),
    ('Ciudad Satélite', 8),
    ('Villa Adela', 8),
    ('Agua de Castilla', 9),
    ('Villa Challacollo', 9),
    ('Santa Elena', 10),
    ('Cataricagua', 10),
    ('Cataratas', 11),
    ('Mapajo', 11),
    ('Central', 12),
    ('San Luis', 12),
    ('San Gerardo', 13),
    ('Cantumarca', 13),
    ('Ferroviaria', 14),
    ('Avaroa', 14),
    ('Equipetrol', 15),
    ('Urbarí', 15),
    ('Villa Cochabamba', 16),
    ('Guabirá', 16),
    ('Las Panosas', 17),
    ('El Molino', 17),
    ('Barrio Nuevo', 18),
    ('San José de Pocitos', 18);

create table calles(
    id_calle int Primary key auto_increment,
    nombre varchar (100),
    id_zona int,
    foreign key (id_zona) references zona (id_zona)
    );

   ALTER TABLE calles MODIFY nombre VARCHAR(80) NOT NULL CHECK;


INSERT INTO calles (nombre, id_zona) VALUES
("Av. 6 de Agosto", 1),
("Calle Mamoré", 2),
("Av. Héroes del Chaco", 3),
("Calle Nicolás Suárez", 4),
("Calle Dalence", 5),
("Calle Grau", 6),
("Calle Sucre", 7),
("Av. Petrolera", 8),
("Av. América", 9),
("Av. Simón López", 10),
("Av. Blanco Galindo", 11),
("Calle Pacheco", 12),
("Av. 20 de Octubre", 13),
("Av. Saavedra", 14),
("Av. Alfredo Sanjinés", 15),
("Av. Bolivia", 16),
("Calle Potosí", 17),
("Av. Dehene", 18),
("Calle Camacho", 19),
("Av. Bolívar", 20),
("Av. 9 de Febrero", 21),
("Calle Bruno Racua", 22),
("Calle Pando", 23),
("Av. Brasil", 24),
("Calle Hoyos", 25),
("Av. Antofagasta", 26),
("Av. Ferroviaria", 27),
("Calle Potosí", 28),
("Av. San Martín", 29),
("Av. Grigotá", 30),
("Av. Circunvalación", 31),
("Av. Fabril", 32),
("Calle Domingo Paz", 33),
("Calle Ingavi", 34),
("Calle Comercio", 35),
("Av. Internacional", 36);


CREATE TABLE numero_puerta (
    id_puerta INT PRIMARY KEY AUTO_INCREMENT,
    numero VARCHAR(4) NOT NULL,
    id_calle INT NOT NULL,
    FOREIGN KEY (id_calle) REFERENCES calles(id_calle)
);
