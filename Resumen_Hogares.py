import pymysql
from tkinter import messagebox
import Conexion
import Componentes
import Tabla

ANCHOS = [85, 150, 235, 125, 135, 120]
ENCABEZADOS = ["NUMERO", "NOMBRE HOGAR", "UBICACION", "CAPACIDAD", "CUIDADORAS", "ESTADO"]


def mostrar(contenedor):
    Componentes.limpiar_contenedor(contenedor)
    Componentes.crear_titulo(contenedor, "RESUMEN DE HOGARES")

    entrada_buscar = Componentes.crear_barra_busqueda(contenedor)
    filas_tabla = Tabla.crear_tabla(contenedor, ENCABEZADOS, ANCHOS)

    try:
        filas = Conexion.consultar(
            "SELECT h.numero_hogar, h.nombre_hogar, d.nombre, c.nombre, z.nombre, ca.nombre, "
            "h.capacidad, h.estado, "
            "(SELECT COUNT(*) FROM asignacion_hogar a WHERE a.id_hogar = h.id_hogar AND a.fecha_fin IS NULL), "
            "(SELECT COUNT(*) FROM cuidadora cu WHERE cu.id_hogar = h.id_hogar AND cu.estado = 'activo') "
            "FROM hogar h "
            "JOIN departamentos d ON d.id_departamento = h.id_departamento "
            "JOIN ciudad c ON c.id_ciudad = h.id_ciudad "
            "JOIN zona z ON z.id_zona = h.id_zona "
            "JOIN calles ca ON ca.id_calle = h.id_calle "
            "ORDER BY h.numero_hogar")
    except pymysql.MySQLError as error:
        messagebox.showerror("Base de datos", f"No se pudo cargar el resumen:\n{error}")
        filas = []

    registros = []
    textos = []
    for fila in filas:
        ubicacion = f"-{fila[2]}\n-{fila[3]}\n-{fila[4]}\n-{fila[5]}"
        capacidad = f"{fila[8]}/{fila[6]}"
        cuidadoras = f"{fila[9]}/{Componentes.MAX_CUIDADORAS}"
        registros.append([fila[0], fila[1], ubicacion, capacidad, cuidadoras, fila[7]])
        textos.append(f"{fila[0]} {fila[1]} {fila[2]} {fila[3]} {fila[4]} {fila[5]} {fila[7]}".lower())

    def dibujar(evento=None):
        Tabla.vaciar_tabla(filas_tabla)
        buscado = entrada_buscar.get().strip().lower()
        for i in range(len(registros)):
            if buscado in textos[i]:
                Tabla.agregar_fila(filas_tabla, registros[i], ANCHOS, lineas=4)

    entrada_buscar.bind("<KeyRelease>", dibujar) 
    dibujar()
