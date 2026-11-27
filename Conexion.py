import pymysql

HOST="localhost"
USUARIO="root"
CONTRA="denil"
BASE_DE_DATOS="aldeas_sos"


def conectar():
    return pymysql.connect(host=HOST,
                           user=USUARIO,
                           password=CONTRA,
                           database=BASE_DE_DATOS,
                           charset="utf8mb4")


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
