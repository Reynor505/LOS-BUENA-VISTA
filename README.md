# Sistema de Gestión de Participantes — Aldeas Infantiles SOS

# Proyecto integrador 

## Descripción
Sistema de información para registrar y dar seguimiento a los participantes (niños, niñas, adolescentes y jóvenes) de Aldeas Infantiles SOS. Permite gestionar su historial de desarrollo, su asignación a hogares y la información de las cuidadoras a cargo, así como el egreso y el seguimiento posterior a la salida del programa. También permite registrar a los trabajadores como usuarios del sistema y asignarles distintos niveles de acceso según su rol, con un registro de los ingresos para mayor seguridad.

## Requisitos

### Software necesario

- **MySQL Server 8.0.46* en ejecución (instancia local).
- **MySQL Workbench 26.10.0* para ejecutar el script *"".sql*
- **Python 3.15.2* para ejecutar el archivo `.py`.
- **Visual Studio Code** (opcional, recomendado) como editor para correr el proyecto.

### Librerías de Python

Instala las dependencias con:

```bash
pip install pymysql
pip install pillow
```

| Librería | Uso |
| --- | --- |
| `pymysql` | Conexión del programa con la base de datos MySQL |
| `pillow` | Manejo de imágenes en la interfaz |
## Integrantes
* Callisaya Loza Miguel Mauricio
* Cruz Chino Ronald
* Machaca Flores Denilson Davis
* Saucedo Quispe Williams Rodrigo

## Objetivo

Contar con un sistema que organice y proteja los datos de los participantes de Aldeas Infantiles SOS, los asigne a un hogar con su cuidadora y mantenga un historial
confiable de cada uno, con acceso solo para el personal autorizado.

## Tecnologías utilizadas

| Herramienta | Uso en el proyecto |
| --- | --- |
| Python | Lenguaje de programación del sistema |
| tkinter | Interfaz gráfica (inicio de sesión, formularios y tablas de consulta) |
| MySQLserver| Gestor de la base de datos |
| MySQL Workbench | Creación y administración de la base de datos |
| PyMySQL | Conexión entre Python y MySQL |
| Pillow | Manejo de imágenes en la interfaz |
| draw.io | Diagramas (modelo entidad-relación y otros) |
| Visual Studio Code | Editor de código |
| GitHub | Repositorio y trabajo en grupo |
[Google Drive](https://drive.google.com/drive/folders/1D1oKaEpIoHGvtTVGoowuFFJGCXfZ78w0) | Almacenamiento de la documentación |

## 1 Descargar el proyecto
primero se debe descargar el repositorio ejecutando el siguiente comando en la consola.
```bash
  git clone https://github.com/Reynor505/LOS-BUENA-VISTA.git
  ```
## verificar los archivos
```bash
  cooming soon dearly/sea que falta compañero
  ```
## SE DEBE DE INICIAR EL SCRIP "base_datos_ordenada.sql"

🗄️ Base de datos

El sistema usa una base de datos MySQL llamada aldeas_sos, con 14 tablas, llaves foráneas y reglas de validación (UNIQUE, CHECK) que protegen la integridad de los datos.

📋 Requisitos
Herramienta	Versión	Para qué
MySQL Server	8.0.16 o superior (en versiones anteriores los CHECK se ignoran)	Gestor de la base de datos
MySQL Workbench	Cualquiera reciente	Ejecutar los scripts y ver las tablas
Python	3.10 o superior	Ejecutar el sistema
mysql-connector-python	Última	Conexión Python ↔ MySQL

Para ver tu versión de MySQL:

sql
SELECT VERSION();
Instalación paso a paso
Paso 1: Clonar el repositorio
bash
git clone https://github.com/Reynor505/LOS-BUENAVISTA.git
cd LOS-BUENAVISTA





se debe tener en cuenta que al correr el archivo *base_de_datos_ordenada.sql* se deben tener las siguientes tablas

## se debe cambiar los valores se la siguiente linea de codigo dentro del archivo.py

```
conexion_datos = dict(host="localhost", port=3307, user="root", password="112367", database="aldeas_sos")
```
todo esto es con el objetivo de conectarse a la base de datos 
## 
