import json
import os
import pymysql

HOST="localhost"
USUARIO="root"
CONTRA="112367"
PUERTO=3307
BASE_DE_DATOS="aldeas_sos"
CONFIG_ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config_db.json")


def cargar_configuracion():
    global HOST, USUARIO, CONTRA, PUERTO, BASE_DE_DATOS
    if os.path.exists(CONFIG_ARCHIVO):
        try:
            with open(CONFIG_ARCHIVO, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            HOST = str(datos.get("host", HOST))
            PUERTO = int(datos.get("puerto", PUERTO))
            USUARIO = str(datos.get("usuario", USUARIO))
            CONTRA = str(datos.get("contra", CONTRA))
            BASE_DE_DATOS = str(datos.get("base_de_datos", BASE_DE_DATOS))
        except (OSError, ValueError, TypeError):
            pass


def obtener_configuracion():
    return {
        "host": HOST,
        "puerto": PUERTO,
        "usuario": USUARIO,
        "contra": CONTRA,
        "base_de_datos": BASE_DE_DATOS,
    }


def guardar_configuracion(host, puerto, usuario, contra, base_de_datos):
    global HOST, USUARIO, CONTRA, PUERTO, BASE_DE_DATOS
    HOST = host
    PUERTO = int(puerto)
    USUARIO = usuario
    CONTRA = contra
    BASE_DE_DATOS = base_de_datos
    with open(CONFIG_ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(obtener_configuracion(), archivo, indent=2, ensure_ascii=False)


def comprobar_conexion_datos(host, puerto, usuario, contra, base_de_datos):
    try:
        conex = pymysql.connect(host=host,
                                user=usuario,
                                port=int(puerto),
                                password=contra,
                                database=base_de_datos,
                                charset="utf8mb4",
                                connect_timeout=5)
        conex.close()
        return True, "Conexion Exitosa Con La Base De Datos"
    except pymysql.MySQLError as Error:
        return False, f"La Base De Datos No Se Pudo Conectar \n {Error}"


cargar_configuracion()


def conectar():
    return pymysql.connect(host=HOST,
                           user=USUARIO,
                           port=PUERTO,
                           password=CONTRA,
                           database=BASE_DE_DATOS,
                           charset="utf8mb4",
                           connect_timeout=5)


def comprobar_conexion():
    try:
        conex=conectar()
        conex.close()
        return True, "Conexion Exitosa Con La Base De Datos"
    except pymysql.MySQLError as Error:
        return False, f"La Base De Datos No Se Pudo Conectar \n {Error}"


def consultar(sql, datos=()):
    conex=conectar()
    try:
        cursor=conex.cursor()
        cursor.execute(sql, datos)
        filas=cursor.fetchall()
        cursor.close()
        return filas
    finally:
        conex.close()


def mensaje_error(error):
    codigo=0
    if len(error.args) > 0 and isinstance(error.args[0], int):
        codigo=error.args[0]

    if codigo == 1062:
        return "Ya existe un registro con esos datos (CI, número o nombre repetido)."
    if codigo in (3819, 4025):
        return "Algún dato no cumple las reglas de la base de datos (revisa fechas, sexo y capacidad)."
    if codigo == 1452:
        return "Alguno de los datos elegidos (hogar, departamento, ciudad, zona o calle) ya no existe en la base."
    if codigo in (1146, 1054, 1048, 1364):
        return ("La estructura de la base de datos no coincide con el programa.\n"
                "Revisa que hayas creado la base con BASE_DE_DATOS_corregida.sql.\n\n" + str(error))
    return str(error)
