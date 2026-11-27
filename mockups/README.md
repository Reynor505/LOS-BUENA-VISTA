# SISTEMA DE GESTIÓN DE PARTICIPANTES — ALDEAS INFANTILES SOS

> **PROYECTO INTEGRADOR** · Universidad Privada Franz Tamayo · Ingeniería de Sistemas e Innovación Digital · Primer semestre, gestión 2-2026

---

## ÍNDICE

1. [Descripción](#descripción)
2. [Objetivo](#objetivo)
3. [Integrantes](#integrantes)
4. [Tecnologías utilizadas](#tecnologías-utilizadas)
5. [Requisitos](#requisitos)
6. [Descargar el proyecto](#descargar-el-proyecto)
7. [Estructura del proyecto](#estructura-del-proyecto)
8. [Base de datos](#base-de-datos)
9. [Configurar la conexión](#configurar-la-conexión)
10. [Ejecutar el sistema](#ejecutar-el-sistema)
11. [Bitácora](#bitácora)

---

## DESCRIPCIÓN

Sistema de información de escritorio para registrar y dar seguimiento a los participantes (niños, niñas, adolescentes y jóvenes) de Aldeas Infantiles SOS.

El sistema permite:

- Gestionar el historial de desarrollo de cada participante.
- Asignar a cada participante a un hogar y conservar el historial de hogares por los que pasó.
- Registrar la información de las cuidadoras a cargo de cada hogar.
- Registrar el egreso y el seguimiento posterior a la salida del programa.
- Registrar a los trabajadores como usuarios del sistema y asignarles distintos niveles de acceso según su rol.
- Guardar un registro de los ingresos al sistema para mayor seguridad.

---

## OBJETIVO

Contar con un sistema que organice y proteja los datos de los participantes de Aldeas Infantiles SOS, los asigne a un hogar con su cuidadora y mantenga un historial confiable de cada uno, con acceso solo para el personal autorizado.

---

## INTEGRANTES

- Callisaya Loza Miguel Mauricio
- Cruz Chino Ronald
- Machaca Flores Denilson Davis
- Saucedo Quispe Williams Rodrigo

---

## TECNOLOGÍAS UTILIZADAS

| Herramienta | Uso en el proyecto |
| --- | --- |
| Python | Lenguaje de programación del sistema |
| tkinter | Interfaz gráfica (inicio de sesión, formularios y tablas de consulta) |
| MySQL Server | Gestor de la base de datos |
| MySQL Workbench | Creación y administración de la base de datos |
| PyMySQL | Conexión entre Python y MySQL |
| Pillow | Manejo de imágenes en la interfaz |
| hashlib | Cifrado de contraseñas (SHA-256) |
| draw.io | Diagramas (modelo entidad-relación y otros) |
| Visual Studio Code | Editor de código |
| GitHub | Repositorio y trabajo en grupo |
| [Google Drive](https://drive.google.com/drive/folders/1D1oKaEpIoHGvtTVGoowuFFJGCXfZ78w0) | Almacenamiento de la documentación |

---

## REQUISITOS

### SOFTWARE NECESARIO

| Herramienta | Versión | Para qué |
| --- | --- | --- |
| MySQL Server | **8.0.16 o superior** (en versiones anteriores las reglas `CHECK` se ignoran) | Gestor de la base de datos, en ejecución como instancia local |
| MySQL Workbench | 8.0 o superior | Ejecutar los scripts `.sql` y ver las tablas |
| Python | 3.10 o superior | Ejecutar los archivos `.py` |
| Visual Studio Code | Opcional (recomendado) | Editor para correr el proyecto |

Para comprobar las versiones instaladas:

```sql
SELECT VERSION();
```

```bash
python --version
```

### LIBRERÍAS DE PYTHON

Instala las dependencias con:

```bash
pip install pymysql pillow
```

| Librería | Uso |
| --- | --- |
| `pymysql` | Conexión del programa con la base de datos MySQL |
| `pillow` | Manejo de imágenes en la interfaz |

---

## DESCARGAR EL PROYECTO

Descarga el repositorio ejecutando en la consola:

```bash
git clone https://github.com/Reynor505/LOS-BUENA-VISTA.git
cd LOS-BUENA-VISTA
```

---

## ESTRUCTURA DEL PROYECTO

El sistema está dividido en módulos de Python (programación modular) y dos carpetas de apoyo (`base_de_datos` y `mockups`):

```text
LOS-BUENA-VISTA/
├── README.md
├── BITACORA.md
├── .gitignore
├── main.py                  # Punto de entrada: abre el login y luego el panel
├── Conexion.py              # Conexión a MySQL y mensajes de error
├── Login2_0.py              # Ventana de inicio de sesión (hash, intentos, bloqueo)
├── Panel_Inicial.py         # Menú principal con tarjetas de resumen
├── Componentes.py           # Componentes reutilizables (campos, combos, fechas, dirección)
├── Participantes.py         # Formulario de registro de participantes
├── Cuidadoras.py            # Formulario de registro de cuidadoras
├── Hogares.py               # Formulario de registro de hogares
├── Resumen_Hogares.py       # Tabla de resumen de hogares con buscador
├── Resumen_Participantes.py # Tabla de resumen de participantes con buscador
├── Tabla.py                 # Tabla reutilizable con scroll
├── LOGO_ALDEAS_SOS.jpg      # Logo de la pantalla de login
├── LOGO_NEGATIVO.png        # Logo del menú lateral
├── base_de_datos/           # Scripts SQL (esquema y datos)
└── mockups/                 # Prototipos de la interfaz
```

### MÓDULOS DE PYTHON

| Archivo | Descripción |
| --- | --- |
| `main.py` | Une los módulos: si el login es correcto, abre el panel inicial. |
| `Conexion.py` | Crea la conexión con MySQL y traduce los errores del motor a mensajes claros. |
| `Login2_0.py` | Valida usuario y contraseña (SHA-256), controla intentos fallidos y bloqueo temporal. |
| `Panel_Inicial.py` | Menú lateral y tarjetas con los conteos de participantes, hogares, egresos y seguimientos. |
| `Componentes.py` | Funciones reutilizadas por los formularios (campos, combos, fechas, selectores de dirección). |
| `Participantes.py` | Formulario para registrar un participante y asignarlo a un hogar. |
| `Cuidadoras.py` | Formulario para registrar una cuidadora y asignarla a un hogar. |
| `Hogares.py` | Formulario para registrar un hogar con su dirección y capacidad. |
| `Resumen_Hogares.py` | Muestra en tabla los hogares con su ubicación, capacidad y cuidadoras. |
| `Resumen_Participantes.py` | Muestra en tabla los participantes con su hogar y estado (activo/egresado). |
| `Tabla.py` | Tabla reutilizable con encabezados y barra de desplazamiento. |

---

## BASE DE DATOS

El sistema usa una base de datos **MySQL** llamada `aldeas_sos`, con **19 tablas**, llaves foráneas y reglas de validación (`UNIQUE`, `CHECK`) que protegen la integridad de los datos.

### ORDEN DE EJECUCIÓN DE LOS SCRIPTS

Los scripts están en la carpeta `base_de_datos/`:

| Orden | Archivo | Qué hace |
| --- | --- | --- |
| 1.º | `base_datos_ordenada.sql` | Crea la base y las tablas principales (roles, usuarios, hogares, participantes, etc.). |
| 2.º | `normalizacion_direccion.sql` | Crea las tablas de dirección: `departamentos`, `ciudad`, `zona`, `calles` y `numero_puerta`. |
| 3.º | `DATOS_POR_DEFECTO.sql` | Carga roles, permisos, usuarios y datos de ejemplo. |

> Primero se deben crear las tablas y la dirección; los datos por defecto no funcionan sin ellas.
>
> Los archivos `alteraciones_de_tablas .sql` y `proyecto_avance_agregacion_tablas.sql` son scripts de apoyo que se usaron durante el desarrollo (agregan restricciones y tablas de seguimiento). El esquema definitivo es la suma de los tres primeros scripts.

### INSTALACIÓN PASO A PASO

#### PASO 1: CONECTARSE A MYSQL

1. Abre **MySQL Workbench**.
2. Haz clic en tu conexión local (normalmente `Local instance MySQL80`).
3. Ingresa la contraseña de tu usuario de MySQL.

#### PASO 2: CREAR LAS TABLAS

1. Menú **File → Open SQL Script...**
2. Selecciona **`base_datos_ordenada.sql`** y ejecútalo completo con el ícono del rayo (o `Ctrl + Shift + Enter`).
3. Abre **`normalizacion_direccion.sql`** y ejecútalo completo.
4. Revisa el panel *Output*: no debe haber errores en rojo.

#### PASO 3: CARGAR LOS DATOS POR DEFECTO

1. Abre **`DATOS_POR_DEFECTO.sql`**.
2. Ejecútalo completo con el ícono del rayo.

> Ejecútalo **una sola vez**. Si lo repites sin reiniciar la base, MySQL da errores `Duplicate entry` porque los datos ya existen.

#### PASO 4: VERIFICAR LA INSTALACIÓN

```sql
USE aldeas_sos;
SHOW TABLES;
```

Deben aparecer las 19 tablas de la lista de más abajo.

### TABLAS DE LA BASE DE DATOS

| # | Tabla | Descripción |
| --- | --- | --- |
| 1 | `rol` | Roles del sistema |
| 2 | `permiso` | Permisos disponibles |
| 3 | `rol_permiso` | Qué permisos tiene cada rol |
| 4 | `usuario` | Usuarios del sistema (acceso, intentos y bloqueo) |
| 5 | `registro_acceso` | Quién ingresó y cuándo |
| 6 | `hogar` | Hogares SOS, su capacidad y cuidadora responsable |
| 7 | `cuidadora` | Cuidadoras de cada hogar |
| 8 | `participantes` | Niños, niñas, adolescentes y jóvenes |
| 9 | `asignacion_hogar` | Historial de hogares de cada participante |
| 10 | `historial` | Situación previa y actual |
| 11 | `egreso` | Salida del participante |
| 12 | `seguimiento_egreso` | Seguimiento posterior al egreso |
| 13 | `situacion` | Catálogo de situaciones |
| 14 | `seguimiento_situacion` | Situaciones registradas en cada seguimiento |
| 15 | `departamentos` | Departamentos de Bolivia (direcciones) |
| 16 | `ciudad` | Ciudades por departamento |
| 17 | `zona` | Zonas por ciudad |
| 18 | `calles` | Calles por zona |
| 19 | `numero_puerta` | Número de puerta por calle |

### USUARIOS POR DEFECTO

| Usuario | Contraseña | Rol | Permisos |
| --- | --- | --- | --- |
| `admin` | `admin123` | Administrador | Todos |
| `cquispe` | `trabajo123` | Trabajador social | `ver_participantes`, `editar_participantes` |
| `lflores` | `consulta123` | Consulta | `ver_participantes` |

> Estos usuarios son solo para pruebas. Cambia las contraseñas antes de usar el sistema con datos reales.
>
> Las contraseñas se guardan como **hash SHA-256** (código de 64 caracteres), nunca en texto plano.

### DATOS QUE CARGA `DATOS_POR_DEFECTO.sql`

| Tabla | Registros |
| --- | --- |
| `rol` | 3 roles: Administrador, Trabajador social, Consulta |
| `permiso` | 4 permisos: `ver_participantes`, `editar_participantes`, `gestionar_usuarios`, `ver_accesos` |
| `rol_permiso` | 7 asignaciones de permisos a roles |
| `usuario` | 3 usuarios (ver tabla de usuarios por defecto) |
| `registro_acceso` | 3 accesos de ejemplo |
| `departamentos` | 9 departamentos de Bolivia |
| `ciudad` | 18 ciudades |
| `zona` | 36 zonas |
| `calles` | 36 calles |
| `numero_puerta` | 4 números de puerta |
| `hogar` | 2 hogares: Hogar Esperanza y Hogar Alegría |
| `cuidadora` | 2 cuidadoras, cada una responsable de un hogar |
| `participantes` | 3 participantes: Juan, Sofía y Diego |
| `asignacion_hogar` | 4 asignaciones (Juan pasó de un hogar a otro) |
| `historial` | 3 historiales |
| `egreso` | 1 egreso (Diego, por mayoría de edad) |
| `seguimiento_egreso` | 1 seguimiento de Diego |
| `situacion` | 3 situaciones: Estudia, Trabaja, Vive de forma independiente |
| `seguimiento_situacion` | 2 situaciones asociadas al seguimiento |

### REGLAS DE VALIDACIÓN

| Tabla | Reglas |
| --- | --- |
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

### REINICIAR LA BASE DE DATOS

Si quieres volver a empezar (**esto borra todos los datos**):

```sql
DROP DATABASE aldeas_sos;
```

Después repite los pasos 2 y 3.

### PROBLEMAS COMUNES

| Error | Causa | Solución |
| --- | --- | --- |
| Se guardan datos inválidos (no salen errores de `CHECK`) | MySQL anterior a 8.0.16 | Actualizar MySQL |
| `Table '...' already exists` | Se ejecutó un script de tablas dos veces | Reiniciar la base de datos y repetir |
| `Duplicate entry ...` al cargar los datos | `DATOS_POR_DEFECTO.sql` ya se había ejecutado | Reiniciar la base de datos |
| `Unknown database 'aldeas_sos'` | No se ejecutó antes `base_datos_ordenada.sql` | Seguir el orden: primero las tablas, luego los datos |
| `Access denied for user` | Usuario o contraseña de MySQL incorrectos | Revisar las credenciales en `Conexion.py` |
| `Can't connect to MySQL server` | El servicio de MySQL no está iniciado | Iniciar el servicio (en Windows: *Servicios* → MySQL80 → Iniciar) |
| `Table '...' doesn't exist` al usar direcciones | No se ejecutó `normalizacion_direccion.sql` | Ejecutar el script de normalización de dirección |

---

## CONFIGURAR LA CONEXIÓN

Antes de ejecutar el sistema, se deben cambiar los valores de conexión dentro del archivo **`Conexion.py`** para que coincidan con tu instalación de MySQL:

```python
HOST = "localhost"
USUARIO = "root"
CONTRA = "TU_CONTRASEÑA_DE_MYSQL"
BASE_DE_DATOS = "aldeas_sos"
```

| Valor | Qué poner |
| --- | --- |
| `HOST` | `localhost` si MySQL está en tu computadora |
| `USUARIO` | Tu usuario de MySQL (normalmente `root`) |
| `CONTRA` | La contraseña que usas en MySQL Workbench |
| `BASE_DE_DATOS` | `aldeas_sos` (debe coincidir con la base creada por el script) |

> Nunca subas tu contraseña real de MySQL a GitHub.

---

## EJECUTAR EL SISTEMA

1. Verifica que el servicio de **MySQL esté en ejecución**.
2. Verifica que ejecutaste los scripts de la base de datos, en orden.
3. Instala las librerías de Python (`pip install pymysql pillow`).
4. Ejecuta el sistema:

```bash
python main.py
```

5. Inicia sesión con uno de los usuarios por defecto (por ejemplo `admin` / `admin123`).

---

## BITÁCORA

El avance del proyecto se documenta en el archivo [`BITACORA.md`](BITACORA.md).