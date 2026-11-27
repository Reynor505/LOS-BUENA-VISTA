import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import Conexion
import Componentes
import Tabla

ANCHOS = [85, 150, 235, 125, 135, 120]
ENCABEZADOS = ["NUMERO", "NOMBRE HOGAR", "UBICACION", "CAPACIDAD", "CUIDADORAS", "ESTADO"]


def mostrar(contenedor):
    Componentes.limpiar_contenedor(contenedor)
    Componentes.crear_titulo(contenedor, "RESUMEN DE HOGARES")

    entrada_buscar = Componentes.crear_barra_busqueda(contenedor, "Buscar por nombre del hogar...")
    barra_filtros = Componentes.crear_barra_filtros(contenedor)

    combo_dep = Componentes.agregar_filtro_combo(barra_filtros, "DEPARTAMENTO", ["Todos"], ancho=15)
    combo_ciudad = Componentes.agregar_filtro_combo(barra_filtros, "CIUDAD", ["Todas"], ancho=18)
    combo_zona = Componentes.agregar_filtro_combo(barra_filtros, "ZONA", ["Todas"], ancho=18)

    try:
        deps_db = Conexion.consultar("SELECT id_departamento, nombre FROM departamentos ORDER BY nombre")
        ciudades_db = Conexion.consultar("SELECT id_ciudad, nombre, id_departamento FROM ciudad ORDER BY nombre")
        zonas_db = Conexion.consultar("SELECT id_zona, nombre, id_ciudad FROM zona ORDER BY nombre")
        filas = Conexion.consultar(
            "SELECT h.numero_hogar, h.nombre_hogar, d.nombre, c.nombre, z.nombre, ca.nombre, "
            "h.capacidad, h.estado, "
            "(SELECT COUNT(*) FROM asignacion_hogar a WHERE a.id_hogar = h.id_hogar AND a.fecha_fin IS NULL), "
            "(SELECT COUNT(*) FROM cuidadora cu WHERE cu.id_hogar = h.id_hogar AND cu.estado = 'activo'), "
            "h.id_departamento, h.id_ciudad, h.id_zona "
            "FROM hogar h "
            "JOIN departamentos d ON d.id_departamento = h.id_departamento "
            "JOIN ciudad c ON c.id_ciudad = h.id_ciudad "
            "JOIN zona z ON z.id_zona = h.id_zona "
            "JOIN calles ca ON ca.id_calle = h.id_calle "
            "ORDER BY h.numero_hogar")
    except pymysql.MySQLError as error:
        messagebox.showerror("Base de datos", f"No se pudo cargar el resumen:\n{error}")
        deps_db, ciudades_db, zonas_db, filas = [], [], [], []

    ids_dep = [None] + [d[0] for d in deps_db]
    combo_dep["values"] = ["Todos"] + [d[1] for d in deps_db]
    combo_dep.current(0)

    ids_ciudad = [None]
    ids_zona = [None]

    def actualizar_ciudades(reiniciar_zona=True):
        dep_idx = combo_dep.current()
        id_dep = ids_dep[dep_idx] if dep_idx >= 0 else None
        ids_ciudad.clear()
        ids_ciudad.append(None)
        nombres = ["Todas"]
        for id_c, nom_c, dep_c in ciudades_db:
            if id_dep is None or dep_c == id_dep:
                ids_ciudad.append(id_c)
                nombres.append(nom_c)
        combo_ciudad["values"] = nombres
        combo_ciudad.current(0)
        if reiniciar_zona:
            actualizar_zonas()

    def actualizar_zonas():
        dep_idx = combo_dep.current()
        ciu_idx = combo_ciudad.current()
        id_dep = ids_dep[dep_idx] if dep_idx >= 0 else None
        id_ciu = ids_ciudad[ciu_idx] if ciu_idx >= 0 else None
        ciudades_validas = {c[0] for c in ciudades_db if id_dep is None or c[2] == id_dep}

        ids_zona.clear()
        ids_zona.append(None)
        nombres = ["Todas"]
        for id_z, nom_z, ciu_z in zonas_db:
            if id_ciu is not None:
                if ciu_z == id_ciu:
                    ids_zona.append(id_z)
                    nombres.append(nom_z)
            elif ciu_z in ciudades_validas:
                ids_zona.append(id_z)
                nombres.append(nom_z)
        combo_zona["values"] = nombres
        combo_zona.current(0)

    registros = []
    for fila in filas:
        ubicacion = f"-{fila[2]}\n-{fila[3]}\n-{fila[4]}\n-{fila[5]}"
        capacidad = f"{fila[8]}/{fila[6]}"
        cuidadoras = f"{fila[9]}/{Componentes.MAX_CUIDADORAS}"
        registros.append({
            "valores": [fila[0], fila[1], ubicacion, capacidad, cuidadoras, fila[7]],
            "nombre": fila[1].lower(),
            "id_dep": fila[10],
            "id_ciu": fila[11],
            "id_zona": fila[12],
        })

    def dibujar(evento=None):
        Tabla.vaciar_tabla(filas_tabla)
        buscado = Componentes.obtener_texto_entrada(entrada_buscar).lower()
        id_dep = ids_dep[combo_dep.current()] if combo_dep.current() >= 0 else None
        id_ciu = ids_ciudad[combo_ciudad.current()] if combo_ciudad.current() >= 0 else None
        id_zon = ids_zona[combo_zona.current()] if combo_zona.current() >= 0 else None

        for reg in registros:
            if buscado and buscado not in reg["nombre"]:
                continue
            if id_dep is not None and reg["id_dep"] != id_dep:
                continue
            if id_ciu is not None and reg["id_ciu"] != id_ciu:
                continue
            if id_zon is not None and reg["id_zona"] != id_zon:
                continue
            Tabla.agregar_fila(filas_tabla, reg["valores"], ANCHOS, lineas=4)

    def al_elegir_dep(evento=None):
        actualizar_ciudades(reiniciar_zona=True)
        dibujar()

    def al_elegir_ciudad(evento=None):
        actualizar_zonas()
        dibujar()

    def limpiar_filtros():
        Componentes.agregar_placeholder(entrada_buscar, "Buscar por nombre del hogar...")
        combo_dep.current(0)
        actualizar_ciudades(reiniciar_zona=True)
        dibujar()

    btn_limpiar = tk.Button(barra_filtros, text="LIMPIAR FILTROS", font=(Componentes.FUENTE, 9, "bold"),
                            bg=Componentes.COLOR_MENU, fg="White", activebackground="#2B3B4E",
                            activeforeground="White", relief="flat", cursor="hand2", padx=12, pady=6,
                            command=limpiar_filtros)
    btn_limpiar.pack(side="right", padx=12, pady=8)

    filas_tabla = Tabla.crear_tabla(contenedor, ENCABEZADOS, ANCHOS)

    actualizar_ciudades(reiniciar_zona=True)
    combo_dep.bind("<<ComboboxSelected>>", al_elegir_dep)
    combo_ciudad.bind("<<ComboboxSelected>>", al_elegir_ciudad)
    combo_zona.bind("<<ComboboxSelected>>", dibujar)
    entrada_buscar.bind("<KeyRelease>", dibujar)
    dibujar()
