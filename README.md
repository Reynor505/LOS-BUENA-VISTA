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

##  Base de datos

El sistema usa una base de datos **MySQL** llamada `base_datos_ordenada`, con **14 tablas**, llaves foráneas y reglas de validación (`UNIQUE`, `CHECK`) que protegen la integridad de los datos.

---

###  Requisitos

| Herramienta | Versión | Para qué |
|---|---|---|
| MySQL Server | **8.0.16 o superior** (en versiones anteriores los `CHECK` se ignoran) | Gestor de la base de datos |
| MySQL Workbench | Cualquiera reciente | Ejecutar los scripts y ver las tablas |

Para ver tu versión de MySQL:

```sql
SELECT VERSION();
```

---

###  Archivos de la base de datos

| Archivo | Qué hace | Orden |
|---|---|---|
| `aldeas_sos.sql` | Crea la base de datos y las 14 tablas con sus reglas | **1.º** |
| `DATOS_POR_DEFECTO.sql` | Carga roles, permisos, usuarios y datos de ejemplo | **2.º** |

---

###  Instalación paso a paso

#### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/Reynor505/LOS-BUENAVISTA.git
cd LOS-BUENAVISTA
```

#### Paso 2: Conectarte a MySQL

1. Abre **MySQL Workbench**.
2. Haz clic en tu conexión local (normalmente `Local instance MySQL80`).
3. Ingresa la contraseña de tu usuario de MySQL.

#### Paso 3: Crear las tablas

1. Menú **File → Open SQL Script...**
2. Selecciona **`aldeas_sos.sql`**.
3. Ejecuta **todo el script** con el rayo  (o `Ctrl + Shift + Enter`).
4. Revisa el panel *Output*: no debe haber errores en rojo.

#### Paso 4: Cargar los datos por defecto

1. Abre **`DATOS_POR_DEFECTO.sql`**.
2. Ejecútalo completo con el rayo .

>  Ejecútalo **una sola vez**. Si lo repites sin reiniciar la base, MySQL da errores `Duplicate entry` porque los datos ya existen.

#### Paso 5: Verificar la instalación

```sql
USE aldeas_sos;
SHOW TABLES;          -- deben aparecer las 14 tablas
```

---

###  Usuarios por defecto

| Usuario | Contraseña | Rol | Permisos |
|---|---|---|---|
| `admin` | `admin123` | Administrador | Todos |
| `cquispe` | `trabajo123` | Trabajador social | `ver_participantes`, `editar_participantes` |
| `lflores` | `consulta123` | Consulta | `ver_participantes` |

>
> Las contraseñas se guardan como **hash** (código de 64 caracteres), nunca en texto plano.

---

###  Datos que carga `DATOS_POR_DEFECTO.sql`

| Tabla | Registros |
|---|---|
| `rol` | 3 roles: Administrador, Trabajador social, Consulta |
| `permiso` | 4 permisos: `ver_participantes`, `editar_participantes`, `gestionar_usuarios`, `ver_accesos` |
| `rol_permiso` | 7 asignaciones de permisos a roles |
| `usuario` | 3 usuarios (ver tabla de arriba) |
| `registro_acceso` | 3 accesos de ejemplo |
| `hogar` | 2 hogares: Hogar Esperanza y Hogar Alegría |
| `cuidadora` | 2 cuidadoras, cada una responsable de un hogar |
| `participantes` | 3 participantes: Juan, Sofía y Diego |
| `asignacion_hogar` | 4 asignaciones (Juan pasó de un hogar a otro) |
| `historial` | 3 historiales |
| `egreso` | 1 egreso (Diego, por mayoría de edad) |
| `seguimiento_egreso` | 1 seguimiento de Diego |
| `situacion` | 3 situaciones: Estudia, Trabaja, Vive de forma independiente |
| `seguimiento_situacion` | 2 situaciones asociadas al seguimiento |

---

###  Reglas de validación

| Tabla | Reglas |
|---|---|
| `rol`, `permiso`, `situacion` | El nombre no se repite |
| `rol_permiso` | Un permiso no se repite dentro del mismo rol |
| `usuario` | CI y nombre de usuario únicos; intentos fallidos de 0 a 3; estado `activo` o `inactivo` |
| `registro_acceso` | Resultado: `exitoso`, `fallido` o `bloqueado` |
| `hogar` | Número y nombre únicos; número y capacidad mayores a 0 |
| `cuidadora` | CI único; nombres no vacíos |
| `participantes` | No se registra dos veces a la misma persona; sexo `M` o `F`; ingreso no anterior al nacimiento |
| `asignacion_hogar` | La fecha de fin no puede ser anterior a la de inicio |
| `egreso` | Un solo egreso por participante; el motivo es obligatorio |
| `seguimiento_egreso` | No hay dos seguimientos del mismo egreso en la misma fecha |
| `seguimiento_situacion` | No se repite la misma situación en un seguimiento |

---

###  Tablas de la base de datos

| # | Tabla | Descripción |
|---|---|---|
| 1 | `rol` | Roles del sistema |
| 2 | `permiso` | Permisos disponibles |
| 3 | `rol_permiso` | Qué permisos tiene cada rol |
| 4 | `usuario` | Usuarios del sistema (acceso, intentos y bloqueo) |
| 5 | `registro_acceso` | Quién ingresó y cuándo |
| 6 | `hogar` | Hogares SOS y su cuidadora responsable |
| 7 | `cuidadora` | Cuidadoras de cada hogar |
| 8 | `participantes` | Niños, niñas, adolescentes y jóvenes |
| 9 | `asignacion_hogar` | Historial de hogares de cada participante |
| 10 | `historial` | Situación previa y actual |
| 11 | `egreso` | Salida del participante |
| 12 | `seguimiento_egreso` | Seguimiento posterior al egreso |
| 13 | `situacion` | Catálogo de situaciones |
| 14 | `seguimiento_situacion` | Situaciones registradas en cada seguimiento |

---




se debe tener en cuenta que al correr el archivo *base_de_datos_ordenada.sql* se deben tener las siguientes tablas

## se debe cambiar los valores se la siguiente linea de codigo dentro del archivo.py

```
conexion_datos = dict(host="localhost", port=3306, user="root", password="", database="aldeas_sos")
```
todo esto es con el objetivo de conectarse a la base de datos 
## 
