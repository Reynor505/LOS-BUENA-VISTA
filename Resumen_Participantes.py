import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import pymysql
import Conexion
import Componentes
import Tabla

ANCHOS = [105, 215, 150, 190, 80, 110]
ENCABEZADOS = ["CI", "NOMBRE COMPLETO", "FECHA DE NACIMIENTO", "HOGAR ASIGNADO", "SEXO", "ESTADO"]


def _crear_treeview(padre, columnas, anchos, altura=5):
    estilo = ttk.Style()
    estilo.configure("Historial.Treeview", font=(Componentes.FUENTE, 10), rowheight=28)
    estilo.configure("Historial.Treeview.Heading", font=(Componentes.FUENTE, 10, "bold"))

    marco = tk.Frame(padre, bg="White")
    marco.pack(fill="both", expand=True, pady=(4, 8))

    tree = ttk.Treeview(marco, columns=columnas, show="headings", height=altura, style="Historial.Treeview")
    barra = tk.Scrollbar(marco, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=barra.set)

    for col, ancho in zip(columnas, anchos):
        tree.heading(col, text=col)
        tree.column(col, width=ancho, anchor="center" if ancho < 160 else "w")

    tree.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")
    return tree


def abrir_ventana_historial(padre, id_participante):
    try:
        datos = Conexion.consultar(
            "SELECT p.nombre, p.apellido, p.ci, p.fecha_de_nacimiento, p.sexo, "
            "p.fecha_de_ingreso, p.situacion_inicial, e.fecha_egreso, e.motivo_egreso "
            "FROM participantes p "
            "LEFT JOIN egreso e ON e.id_participante = p.id_participante "
            "WHERE p.id_participante = %s", (id_participante,))
        if not datos:
            messagebox.showerror("Error", "No se encontró el participante seleccionado.", parent=padre)
            return
        nombre, apellido, ci, fnac, sexo, fingreso, sit_inicial, fecha_egreso, motivo_egreso = datos[0]

        asignaciones = Conexion.consultar(
            "SELECT CONCAT(h.numero_hogar, ' - ', h.nombre_hogar), a.fecha_inicio, a.fecha_fin "
            "FROM asignacion_hogar a "
            "JOIN hogar h ON h.id_hogar = a.id_hogar "
            "WHERE a.id_participante = %s "
            "ORDER BY a.fecha_inicio DESC", (id_participante,))

        seguimientos = Conexion.consultar(
            "SELECT se.fecha_seguimiento, "
            "CONCAT(d.nombre, ', ', c.nombre, ', ', z.nombre, ', ', ca.nombre), "
            "COALESCE(GROUP_CONCAT(s.nombre_situacion SEPARATOR ', '), '-') "
            "FROM seguimiento_egreso se "
            "JOIN egreso e ON e.id_egreso = se.id_egreso "
            "JOIN departamentos d ON d.id_departamento = se.id_departamento "
            "JOIN ciudad c ON c.id_ciudad = se.id_ciudad "
            "JOIN zona z ON z.id_zona = se.id_zona "
            "JOIN calles ca ON ca.id_calle = se.id_calle "
            "LEFT JOIN seguimiento_situacion ss ON ss.id_seguimiento = se.id_seguimiento "
            "LEFT JOIN situacion s ON s.id_situacion = ss.id_situacion "
            "WHERE e.id_participante = %s "
            "GROUP BY se.id_seguimiento, se.fecha_seguimiento, d.nombre, c.nombre, z.nombre, ca.nombre "
            "ORDER BY se.fecha_seguimiento DESC", (id_participante,))
    except pymysql.MySQLError as error:
        messagebox.showerror("Base de datos", f"No se pudo cargar el historial:\n{error}", parent=padre)
        return

    modal = tk.Toplevel(padre)
    modal.title(f"Historial de {nombre} {apellido}")
    modal.config(bg="#F8FAFC")
    modal.minsize(820, 620)
    Componentes.centrar_ventana(modal, 920, 680)
    modal.transient(padre.winfo_toplevel())
    modal.grab_set()

    encabezado = tk.Frame(modal, bg=Componentes.COLOR_MENU)
    encabezado.pack(fill="x")
    tk.Label(encabezado, text=f"HISTORIAL DEL PARTICIPANTE: {nombre.upper()} {apellido.upper()}",
             font=(Componentes.FUENTE, 14, "bold"), bg=Componentes.COLOR_MENU, fg="White",
             pady=12, padx=20).pack(side="left")
    estado_txt = "Egresado" if fecha_egreso else "Activo"
    estado_bg = "#B91C1C" if fecha_egreso else "#15803D"
    tk.Label(encabezado, text=estado_txt.upper(), font=(Componentes.FUENTE, 10, "bold"),
             bg=estado_bg, fg="White", padx=12, pady=4).pack(side="right", padx=20)

    cuerpo = Componentes.crear_contenedor_desplazable(modal)
    cuerpo.config(bg="#F8FAFC")

    # Datos generales
    ficha = tk.Frame(cuerpo, bg=Componentes.COLOR_SECCION,
                     highlightbackground=Componentes.COLOR_BORDE_SECCION, highlightthickness=1)
    ficha.pack(fill="x", padx=20, pady=(12, 8))
    sexo_txt = "Masculino" if sexo == "M" else "Femenino"
    info_lineas = [
        f"CI: {ci}    |    Fecha de nacimiento: {fnac}    |    Sexo: {sexo_txt}    |    Ingreso al sistema: {fingreso}",
        f"Situación inicial: {sit_inicial}",
    ]
    if fecha_egreso:
        info_lineas.append(f"Egreso: {fecha_egreso}    |    Motivo: {motivo_egreso}")
    for idx, linea in enumerate(info_lineas):
        tk.Label(ficha, text=linea, font=(Componentes.FUENTE, 10, "bold" if idx == 0 else "normal"),
                 bg=Componentes.COLOR_SECCION, fg=Componentes.COLOR_TEXTO,
                 anchor="w", justify="left", wraplength=840).pack(fill="x", padx=14, pady=(8 if idx == 0 else 2, 8 if idx == len(info_lineas) - 1 else 2))

    # Asignaciones de hogar
    sec_hog = tk.Frame(cuerpo, bg="#F8FAFC")
    sec_hog.pack(fill="x", padx=20, pady=(4, 4))
    tk.Label(sec_hog, text="ASIGNACIONES DE HOGAR", font=(Componentes.FUENTE, 11, "bold"),
             bg="#F8FAFC", fg=Componentes.COLOR_BOTON).pack(anchor="w")
    tree_hogares = _crear_treeview(sec_hog, ("HOGAR", "FECHA INICIO", "FECHA FIN"), [420, 180, 180], altura=3)
    for hog_nom, f_ini, f_fin in asignaciones:
        tree_hogares.insert("", "end", values=(hog_nom, f_ini, f_fin if f_fin else "Actual"))

    if seguimientos:
        sec_seg = tk.Frame(cuerpo, bg="#F8FAFC")
        sec_seg.pack(fill="x", padx=20, pady=(4, 4))
        tk.Label(sec_seg, text="SEGUIMIENTOS DE EGRESO", font=(Componentes.FUENTE, 11, "bold"),
                 bg="#F8FAFC", fg=Componentes.COLOR_BOTON).pack(anchor="w")
        tree_seg = _crear_treeview(sec_seg, ("FECHA", "UBICACIÓN", "SITUACIONES"), [120, 380, 280], altura=3)
        for f_seg, ubic, sits in seguimientos:
            tree_seg.insert("", "end", values=(f_seg, ubic, sits))

    # Tabla de historial
    sec_hist = tk.Frame(cuerpo, bg="#F8FAFC")
    sec_hist.pack(fill="x", padx=20, pady=(4, 4))
    tk.Label(sec_hist, text="REGISTROS DE HISTORIAL", font=(Componentes.FUENTE, 11, "bold"),
             bg="#F8FAFC", fg=Componentes.COLOR_BOTON).pack(anchor="w")
    tree_hist = _crear_treeview(sec_hist, ("FECHA", "SITUACIÓN PREVIA", "SITUACIÓN ACTUAL"), [120, 330, 330], altura=5)

    def cargar_registros_historial():
        for item in tree_hist.get_children():
            tree_hist.delete(item)
        try:
            filas_hist = Conexion.consultar(
                "SELECT fecha_ingreso, COALESCE(situacion_previa, '-'), COALESCE(situacion_actual, '-') "
                "FROM historial WHERE id_participante = %s ORDER BY fecha_ingreso DESC, id_historial DESC",
                (id_participante,))
            for fh in filas_hist:
                tree_hist.insert("", "end", values=fh)
        except pymysql.MySQLError as error:
            messagebox.showerror("Base de datos", f"No se pudo actualizar el historial:\n{error}", parent=modal)

    cargar_registros_historial()

    # Formulario para agregar nueva entrada al historial
    sec_nuevo = tk.Frame(cuerpo, bg=Componentes.COLOR_SECCION,
                         highlightbackground=Componentes.COLOR_BORDE_SECCION, highlightthickness=1)
    sec_nuevo.pack(fill="x", padx=20, pady=(6, 16))
    sec_nuevo.grid_columnconfigure(0, weight=1)
    sec_nuevo.grid_columnconfigure(1, weight=2)
    sec_nuevo.grid_columnconfigure(2, weight=2)

    tk.Label(sec_nuevo, text="AÑADIR NUEVA ENTRADA AL HISTORIAL", font=(Componentes.FUENTE, 10, "bold"),
             bg=Componentes.COLOR_SECCION, fg=Componentes.COLOR_BOTON).grid(row=0, column=0, columnspan=3, sticky="w", padx=12, pady=(8, 4))

    tk.Label(sec_nuevo, text="FECHA (AAAA-MM-DD)", font=(Componentes.FUENTE, 9, "bold"),
             bg=Componentes.COLOR_SECCION, fg=Componentes.COLOR_TEXTO).grid(row=1, column=0, sticky="w", padx=12)
    tk.Label(sec_nuevo, text="SITUACIÓN PREVIA", font=(Componentes.FUENTE, 9, "bold"),
             bg=Componentes.COLOR_SECCION, fg=Componentes.COLOR_TEXTO).grid(row=1, column=1, sticky="w", padx=12)
    tk.Label(sec_nuevo, text="SITUACIÓN ACTUAL", font=(Componentes.FUENTE, 9, "bold"),
             bg=Componentes.COLOR_SECCION, fg=Componentes.COLOR_TEXTO).grid(row=1, column=2, sticky="w", padx=12)

    ent_fecha = tk.Entry(sec_nuevo, font=(Componentes.FUENTE, 10), relief="flat", bg="#FFFFFF",
                         highlightthickness=1, highlightbackground=Componentes.COLOR_BORDE_CAMPO)
    ent_fecha.insert(0, date.today().strftime("%Y-%m-%d"))
    ent_fecha.grid(row=2, column=0, sticky="ew", padx=12, pady=(2, 10), ipady=4)

    ent_previa = tk.Entry(sec_nuevo, font=(Componentes.FUENTE, 10), relief="flat", bg="#FFFFFF",
                          highlightthickness=1, highlightbackground=Componentes.COLOR_BORDE_CAMPO)
    ent_previa.grid(row=2, column=1, sticky="ew", padx=12, pady=(2, 10), ipady=4)

    ent_actual = tk.Entry(sec_nuevo, font=(Componentes.FUENTE, 10), relief="flat", bg="#FFFFFF",
                          highlightthickness=1, highlightbackground=Componentes.COLOR_BORDE_CAMPO)
    ent_actual.grid(row=2, column=2, sticky="ew", padx=12, pady=(2, 10), ipady=4)

    def guardar_entrada():
        fecha_val = Componentes.validar_fecha(ent_fecha.get())
        previa = ent_previa.get().strip()
        actual = ent_actual.get().strip()

        if fecha_val is None:
            messagebox.showwarning("Fecha incorrecta", "Ingresa la fecha con el formato AAAA-MM-DD.", parent=modal)
            return
        if fecha_val < fnac:
            messagebox.showwarning("Fecha incorrecta", "La fecha no puede ser anterior al nacimiento.", parent=modal)
            return
        if not previa or not actual:
            messagebox.showwarning("Datos incompletos", "Completa la situación previa y la situación actual.", parent=modal)
            return
        if len(previa) > 150 or len(actual) > 150:
            messagebox.showwarning("Datos incorrectos", "Cada situación puede tener máximo 150 caracteres.", parent=modal)
            return

        try:
            conex = Conexion.conectar()
            try:
                cursor = conex.cursor()
                cursor.execute(
                    "INSERT INTO historial (id_participante, fecha_ingreso, situacion_previa, situacion_actual) "
                    "VALUES (%s, %s, %s, %s)",
                    (id_participante, fecha_val, previa, actual))
                conex.commit()
            finally:
                conex.close()
            ent_previa.delete(0, "end")
            ent_actual.delete(0, "end")
            cargar_registros_historial()
            messagebox.showinfo("Guardado", "Entrada agregada al historial.", parent=modal)
        except pymysql.MySQLError as error:
            messagebox.showerror("Error al guardar", Conexion.mensaje_error(error), parent=modal)

    btn_guardar = tk.Button(sec_nuevo, text="GUARDAR ENTRADA", font=(Componentes.FUENTE, 10, "bold"),
                            bg=Componentes.COLOR_BOTON, fg="White", activebackground=Componentes.COLOR_BOTON_HOVER,
                            activeforeground="White", relief="flat", cursor="hand2", padx=16, pady=6,
                            command=guardar_entrada)
    btn_guardar.grid(row=3, column=2, sticky="e", padx=12, pady=(0, 10))


def mostrar(contenedor):
    Componentes.limpiar_contenedor(contenedor)
    Componentes.crear_titulo(contenedor, "RESUMEN DE PARTICIPANTES")

    entrada_buscar = Componentes.crear_barra_busqueda(contenedor, "Buscar por nombre o CI...")

    def ver_seleccionado(id_part=None):
        seleccionado = id_part if id_part is not None else Tabla.obtener_dato_seleccionado(filas_tabla)
        if seleccionado is None:
            messagebox.showwarning("Selección requerida", "Selecciona un participante de la tabla para ver su historial.")
            return
        abrir_ventana_historial(contenedor, seleccionado)

    btn_historial = tk.Button(entrada_buscar.master, text="VER HISTORIAL", font=(Componentes.FUENTE, 10, "bold"),
                              bg=Componentes.COLOR_BOTON, fg="White", activebackground=Componentes.COLOR_BOTON_HOVER,
                              activeforeground="White", relief="flat", cursor="hand2", padx=16, pady=7,
                              command=ver_seleccionado)
    btn_historial.pack(side="right", padx=18, pady=10)

    barra_filtros = Componentes.crear_barra_filtros(contenedor)

    try:
        hogares_db = Conexion.consultar("SELECT id_hogar, numero_hogar, nombre_hogar FROM hogar ORDER BY numero_hogar")
        filas = Conexion.consultar(
            "SELECT p.id_participante, p.ci, p.nombre, p.apellido, p.fecha_de_nacimiento, "
            "h.id_hogar, h.numero_hogar, h.nombre_hogar, p.sexo, e.id_egreso "
            "FROM participantes p "
            "LEFT JOIN asignacion_hogar a ON a.id_participante = p.id_participante AND a.fecha_fin IS NULL "
            "LEFT JOIN hogar h ON h.id_hogar = a.id_hogar "
            "LEFT JOIN egreso e ON e.id_participante = p.id_participante "
            "ORDER BY p.apellido, p.nombre")
    except pymysql.MySQLError as error:
        messagebox.showerror("Base de datos", f"No se pudo cargar el resumen:\n{error}")
        hogares_db, filas = [], []

    opciones_hogar = ["Todos", "Sin hogar"] + [f"{h[1]} - {h[2]}" for h in hogares_db]
    ids_hogar_filtro = [None, "SIN_HOGAR"] + [h[0] for h in hogares_db]
    combo_hogar = Componentes.agregar_filtro_combo(barra_filtros, "HOGAR", opciones_hogar, ancho=22)
    combo_estado = Componentes.agregar_filtro_combo(barra_filtros, "ESTADO", ["Todos", "Activo", "Egresado"], ancho=14)

    registros = []
    for fila in filas:
        id_part, ci, nom, ape, fnac, id_hog, num_hog, nom_hog, sexo_cod, id_egr = fila
        nombre_completo = f"{nom} {ape}"
        hogar = "-" if num_hog is None else f"{num_hog} - {nom_hog}"
        sexo = "Masculino" if sexo_cod == "M" else "Femenino"
        estado = "Activo" if id_egr is None else "Egresado"
        registros.append({
            "id": id_part,
            "valores": [ci, nombre_completo, fnac, hogar, sexo, estado],
            "busqueda": f"{ci} {nombre_completo}".lower(),
            "id_hogar": id_hog,
            "estado": estado,
        })

    def dibujar(evento=None):
        Tabla.vaciar_tabla(filas_tabla)
        buscado = Componentes.obtener_texto_entrada(entrada_buscar).lower()
        filtro_hog = ids_hogar_filtro[combo_hogar.current()] if combo_hogar.current() >= 0 else None
        filtro_est = combo_estado.get()

        for reg in registros:
            if buscado and buscado not in reg["busqueda"]:
                continue
            if filtro_hog == "SIN_HOGAR" and reg["id_hogar"] is not None:
                continue
            if isinstance(filtro_hog, int) and reg["id_hogar"] != filtro_hog:
                continue
            if filtro_est != "Todos" and reg["estado"] != filtro_est:
                continue
            Tabla.agregar_fila(filas_tabla, reg["valores"], ANCHOS, dato=reg["id"])

    def limpiar_filtros():
        Componentes.agregar_placeholder(entrada_buscar, "Buscar por nombre o CI...")
        combo_hogar.current(0)
        combo_estado.current(0)
        dibujar()

    btn_limpiar = tk.Button(barra_filtros, text="LIMPIAR FILTROS", font=(Componentes.FUENTE, 9, "bold"),
                            bg=Componentes.COLOR_MENU, fg="White", activebackground="#2B3B4E",
                            activeforeground="White", relief="flat", cursor="hand2", padx=12, pady=6,
                            command=limpiar_filtros)
    btn_limpiar.pack(side="right", padx=12, pady=8)

    filas_tabla = Tabla.crear_tabla(contenedor, ENCABEZADOS, ANCHOS,
                                    seleccionable=True, al_doble_clic=ver_seleccionado)

    combo_hogar.bind("<<ComboboxSelected>>", dibujar)
    combo_estado.bind("<<ComboboxSelected>>", dibujar)
    entrada_buscar.bind("<KeyRelease>", dibujar)
    dibujar()
