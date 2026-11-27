import pymysql
from tkinter import messagebox
import Conexion
import Componentes
import Tabla

ANCHOS = [105, 215, 150, 190, 80, 110]
ENCABEZADOS = ["CI", "NOMBRE COMPLETO", "FECHA DE NACIMIENTO", "HOGAR ASIGNADO", "SEXO", "ESTADO"]


def mostrar(contenedor):
    Componentes.limpiar_contenedor(contenedor)
    Componentes.crear_titulo(contenedor, "RESUMEN DE PARTICIPANTES")

    entrada_buscar = Componentes.crear_barra_busqueda(contenedor)
    filas_tabla = Tabla.crear_tabla(contenedor, ENCABEZADOS, ANCHOS)

    try:
        filas = Conexion.consultar(
            "SELECT p.ci, p.nombre, p.apellido, p.fecha_de_nacimiento, h.numero_hogar, h.nombre_hogar, "
            "p.sexo, e.id_egreso "
            "FROM participantes p "
            "LEFT JOIN asignacion_hogar a ON a.id_participante = p.id_participante AND a.fecha_fin IS NULL "
            "LEFT JOIN hogar h ON h.id_hogar = a.id_hogar "
            "LEFT JOIN egreso e ON e.id_participante = p.id_participante "
            "ORDER BY p.apellido, p.nombre")
    except pymysql.MySQLError as error:
        messagebox.showerror("Base de datos", f"No se pudo cargar el resumen:\n{error}")
        filas = []

    registros = []
    textos = []
    for fila in filas:
        nombre_completo = f"{fila[1]} {fila[2]}"
        if fila[4] is None:
            hogar = "-"
        else:
            hogar = f"{fila[4]} - {fila[5]}"
        if fila[6] == "M":
            sexo = "Masculino"
        else:
            sexo = "Femenino"
        if fila[7] is None:
            estado = "Activo"
        else:
            estado = "Egresado"
        registros.append([fila[0], nombre_completo, fila[3], hogar, sexo, estado])
        textos.append(f"{fila[0]} {nombre_completo} {fila[3]} {hogar} {sexo} {estado}".lower())

    def dibujar(evento=None):
        Tabla.vaciar_tabla(filas_tabla)
        buscado = entrada_buscar.get().strip().lower()
        for i in range(len(registros)):
            if buscado in textos[i]:
                Tabla.agregar_fila(filas_tabla, registros[i], ANCHOS)

    entrada_buscar.bind("<KeyRelease>", dibujar)
    dibujar()
