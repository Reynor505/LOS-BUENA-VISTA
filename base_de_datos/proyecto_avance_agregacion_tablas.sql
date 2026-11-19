use aldeas_sos;
show TABLE STATUS;
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
motivo_egreso VARCHAR(60),
FOREIGN KEY (id_participante) REFERENCES participantes(id_participante)
);
CREATE TABLE seguimiento_egreso (
id_seguimiento  INT AUTO_INCREMENT PRIMARY KEY,
id_egreso  INT NOT NULL,
fecha_seguimiento DATE NOT NULL,
residencia_actual VARCHAR(60),
FOREIGN KEY (id_egreso) REFERENCES egreso (id_egreso)
 );

 drop TABLE egreso;

 CREATE TABLE situacion (
id_situacion INT AUTO_INCREMENT PRIMARY KEY,
nombre_situacion VARCHAR (60) NOT NULL
 );
 
 CREATE TABLE seguimiento_situacion (
id_seguimiento_situacion INT AUTO_INCREMENT PRIMARY KEY,
id_seguimiento INT NOT NULL,
id_situacion INT NOT NULL,
FOREIGN KEY (id_seguimiento) REFERENCES seguimiento_egreso(id_seguimiento),
FOREIGN KEY (id_situacion) REFERENCES situacion (id_situacion)  
 );

SHOW CREATE TABLE participantes;


