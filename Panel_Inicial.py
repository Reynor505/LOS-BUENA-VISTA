import math
from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pymysql
import Conexion
import Componentes
import Login2_0
import Participantes
import Cuidadoras
import Hogares
import Resumen_Hogares
import Resumen_Participantes


COLOR_MENU = "#1F2B3A"
COLOR_MENU_HOVER = "#2B3B4E"
COLOR_SELECCION = "#7CCFF1"
COLOR_TARJETA = "#F1F5F9"
COLORES_ACENTO = ["#004AAD", "#009FE3", "#1F2B3A", "#0284C7"]


def calcular_estadisticas_markov():
    """Calcula las matrices M1 (edades), C (cupos) y la cadena de Markov usando math."""
    hoy = date.today()
    hogares_rows = []
    part_rows = []
    asig_rows = []
    egresos_total = 0
    try:
        hogares_rows = Conexion.consultar(
            "SELECT h.id_hogar, h.numero_hogar, h.nombre_hogar, h.capacidad, "
            "(SELECT COUNT(*) FROM asignacion_hogar a WHERE a.id_hogar = h.id_hogar AND a.fecha_fin IS NULL) "
            "FROM hogar h WHERE h.estado = 'activo' ORDER BY h.numero_hogar")
        part_rows = Conexion.consultar(
            "SELECT a.id_hogar, p.fecha_de_nacimiento "
            "FROM participantes p "
            "JOIN asignacion_hogar a ON a.id_participante = p.id_participante AND a.fecha_fin IS NULL "
            "WHERE p.id_participante NOT IN (SELECT id_participante FROM egreso)")
        asig_rows = Conexion.consultar("SELECT fecha_fin FROM asignacion_hogar")
        egresos_total = Conexion.consultar("SELECT COUNT(*) FROM egreso")[0][0]
    except pymysql.MySQLError:
        pass

    # Matriz M1: filas = hogares activos, columnas = [0-5, 6-11, 12-17]
    indice_hogar = {h[0]: idx for idx, h in enumerate(hogares_rows)}
    matriz_m1 = [[0, 0, 0] for _ in hogares_rows]
    for id_hog, fnac in part_rows:
        if id_hog not in indice_hogar or fnac is None:
            continue
        edad = hoy.year - fnac.year - ((hoy.month, hoy.day) < (fnac.month, fnac.day))
        col = 0 if edad <= 5 else (1 if edad <= 11 else 2)
        matriz_m1[indice_hogar[id_hog]][col] += 1

    totales_rango = [sum(fila[c] for fila in matriz_m1) for c in range(3)]
    total_m1 = int(math.fsum(totales_rango))
    porc_rango = [round((c / total_m1) * 100, 2) if total_m1 > 0 else 0.0 for c in totales_rango]

    # Matriz C: filas = hogares activos, columnas = [capacidad, ocupados]
    matriz_c = [[int(h[3]), int(h[4])] for h in hogares_rows]
    cap_total = int(math.fsum(fila[0] for fila in matriz_c))
    ocu_total = int(math.fsum(fila[1] for fila in matriz_c))
    disp_total = max(0, cap_total - ocu_total)
    porc_ocupacion = round((ocu_total / cap_total) * 100, 2) if cap_total > 0 else 0.0
    porc_disponible = round((disp_total / cap_total) * 100, 2) if cap_total > 0 else 0.0

    # Cadena de Markov: estados [En Hogar, Traslado, Egreso]
    activas = sum(1 for (ffin,) in asig_rows if ffin is None)
    cerradas = sum(1 for (ffin,) in asig_rows if ffin is not None)
    traslados = max(0, cerradas - egresos_total)
    total_eventos = activas + traslados + egresos_total

    if total_eventos > 0:
        v0 = [activas / total_eventos, traslados / total_eventos, egresos_total / total_eventos]
        denom_hogar = activas + traslados + egresos_total
        p_stay = activas / denom_hogar
        p_move = traslados / denom_hogar
        p_exit = egresos_total / denom_hogar
    else:
        v0 = [1.0, 0.0, 0.0]
        p_stay, p_move, p_exit = 0.85, 0.10, 0.05

    matriz_transicion = [
        [p_stay, p_move, p_exit],
        [0.75, 0.10, 0.15],
        [0.0, 0.0, 1.0],
    ]

    # Proyeccion de Markov v_k = v_0 * T^3
    vector = list(v0)
    for _ in range(3):
        siguiente = []
        for col in range(3):
            siguiente.append(math.fsum(vector[fil] * matriz_transicion[fil][col] for fil in range(3)))
        vector = siguiente

    datos_hogares = [
        (h[1], h[2], int(h[3]), int(h[4]), max(0, int(h[3]) - int(h[4])))
        for h in hogares_rows
    ]
    return {
        "m1": matriz_m1,
        "c": matriz_c,
        "porc_rango": porc_rango,
        "porc_ocupacion": porc_ocupacion,
        "porc_disponible": porc_disponible,
        "cap_total": cap_total,
        "ocu_total": ocu_total,
        "disp_total": disp_total,
        "markov_actual": [round(x * 100, 1) for x in v0],
        "markov_proyeccion": [round(x * 100, 1) for x in vector],
        "hogares": datos_hogares,
    }


def _dibujar_barras_canvas(canvas, titulo, etiquetas, valores, colores):
    canvas.delete("all")
    ancho = canvas.winfo_width()
    alto = canvas.winfo_height()
    if ancho < 60 or alto < 60:
        return

    pad_izq, pad_der, pad_sup, pad_inf = 42, 16, 32, 42
    area_w = max(40, ancho - pad_izq - pad_der)
    area_h = max(40, alto - pad_sup - pad_inf)

    canvas.create_text(ancho / 2, 15, text=titulo, font=(Componentes.FUENTE, 10, "bold"), fill=COLOR_MENU)

    # Lineas guia (0% - 100%)
    for paso in range(0, 101, 25):
        y = pad_sup + area_h - (paso / 100.0) * area_h
        canvas.create_line(pad_izq, y, ancho - pad_der, y, fill="#E2E8F0", dash=(3, 3))
        canvas.create_text(pad_izq - 6, y, text=f"{paso}%", anchor="e",
                           font=(Componentes.FUENTE, 8), fill="#64748B")

    canvas.create_line(pad_izq, pad_sup, pad_izq, pad_sup + area_h, fill="#94A3B8", width=1.5)
    canvas.create_line(pad_izq, pad_sup + area_h, ancho - pad_der, pad_sup + area_h, fill="#94A3B8", width=1.5)

    n = len(etiquetas)
    if n == 0:
        return

    paso_x = area_w / n
    ancho_barra = min(46, paso_x * 0.54)

    for i in range(n):
        val = max(0.0, min(100.0, float(valores[i])))
        cx = pad_izq + paso_x * (i + 0.5)
        x0 = cx - ancho_barra / 2
        x1 = cx + ancho_barra / 2
        y1 = pad_sup + area_h
        altura_barra = math.ceil((val / 100.0) * area_h) if val > 0 else 0
        y0 = max(pad_sup, y1 - altura_barra)

        canvas.create_rectangle(x0, y0, x1, y1, fill=colores[i % len(colores)], outline="")
        canvas.create_text(cx, max(pad_sup + 8, y0 - 9), text=f"{val:.1f}%",
                           font=(Componentes.FUENTE, 8, "bold"), fill="#1E293B")
        canvas.create_text(cx, y1 + 19, text=etiquetas[i], justify="center",
                           font=(Componentes.FUENTE, 8, "bold"), fill="#334155")


def _crear_tabla_panel(padre, columnas, anchos, tags_colores=False):
    estilo = ttk.Style()
    estilo.configure("Panel.Treeview", font=(Componentes.FUENTE, 9), rowheight=26)
    estilo.configure("Panel.Treeview.Heading", font=(Componentes.FUENTE, 9, "bold"))

    marco = tk.Frame(padre, bg="White")
    marco.pack(fill="both", expand=True, padx=10, pady=(4, 10))

    tree = ttk.Treeview(marco, columns=columnas, show="headings", style="Panel.Treeview")
    barra = tk.Scrollbar(marco, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=barra.set)

    for col, ancho in zip(columnas, anchos):
        tree.heading(col, text=col)
        tree.column(col, width=ancho, anchor="center" if ancho < 120 else "w")

    if tags_colores:
        tree.tag_configure("exitoso", foreground="#15803D")
        tree.tag_configure("fallido", foreground="#B91C1C")
        tree.tag_configure("bloqueado", foreground="#B45309")

    tree.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")
    return tree


def mostrar_resumen(contenedor):
    Componentes.limpiar_contenedor(contenedor)

    Componentes.crear_titulo(contenedor, "PANEL INICIAL")

    marco_tarjetas = tk.Frame(contenedor, bg="White")
    marco_tarjetas.pack(fill="x", padx=12, pady=(4, 8))
    for i in range(4):
        marco_tarjetas.grid_columnconfigure(i, weight=1, uniform="col")

    titulos = ["PARTICIPANTES\nACTIVOS", "HOGARES\nACTIVOS", "EGRESOS", "SEGUIMIENTOS"]
    consultas = [
        "SELECT COUNT(*) FROM participantes WHERE id_participante NOT IN (SELECT id_participante FROM egreso)",
        "SELECT COUNT(*) FROM hogar WHERE estado = 'activo'",
        "SELECT COUNT(*) FROM egreso",
        "SELECT COUNT(*) FROM seguimiento_egreso"]

    for i in range(4):
        try:
            numero = Conexion.consultar(consultas[i])[0][0]
        except pymysql.MySQLError:
            numero = "-"

        tarjeta = tk.Frame(marco_tarjetas, bg=COLOR_TARJETA, height=135,
                           highlightbackground="#CBD5E1", highlightthickness=1)
        tarjeta.pack_propagate(False)
        tarjeta.grid(row=0, column=i, padx=8, pady=4, sticky="nsew")

        tk.Frame(tarjeta, bg=COLORES_ACENTO[i], height=5).pack(fill="x")
        tk.Label(tarjeta, text=titulos[i], font=("Segoe UI", 11, "bold"),
                 bg=COLOR_TARJETA, fg="#1E293B").pack(pady=(12, 0))
        tk.Label(tarjeta, text=str(numero), font=("Segoe UI", 34, "bold"),
                 bg=COLOR_TARJETA, fg=COLORES_ACENTO[i]).pack(expand=True)

    estadisticas = calcular_estadisticas_markov()

    panel_inferior = tk.Frame(contenedor, bg="White")
    panel_inferior.pack(fill="both", expand=True, padx=20, pady=(4, 16))
    panel_inferior.grid_columnconfigure(0, weight=1, uniform="panel_inf")
    panel_inferior.grid_columnconfigure(1, weight=1, uniform="panel_inf")
    panel_inferior.grid_rowconfigure(0, weight=1)

    # Lado izquierdo abajo: SOLO gráficos en Canvas (barras con matrices M1, C y Markov)
    marco_graficos = tk.Frame(panel_inferior, bg="#F8FAFC", highlightbackground="#CBD5E1", highlightthickness=1)
    marco_graficos.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

    canvas_m1_c = tk.Canvas(marco_graficos, bg="#F8FAFC", highlightthickness=0)
    canvas_m1_c.pack(fill="both", expand=True, padx=6, pady=(6, 2))

    canvas_markov = tk.Canvas(marco_graficos, bg="#F8FAFC", highlightthickness=0)
    canvas_markov.pack(fill="both", expand=True, padx=6, pady=(2, 6))

    etiquetas_1 = ["0-5\naños", "6-11\naños", "12-17\naños", "Ocupado\n(C)", "Disp.\n(C)"]
    valores_1 = estadisticas["porc_rango"] + [estadisticas["porc_ocupacion"], estadisticas["porc_disponible"]]
    colores_1 = ["#004AAD", "#009FE3", "#0284C7", "#1F2B3A", "#15803D"]

    etiquetas_2 = ["En Hogar\n(t0)", "Traslado\n(t0)", "Egreso\n(t0)", "En Hogar\n(t3)", "Egreso\n(t3)"]
    valores_2 = [
        estadisticas["markov_actual"][0],
        estadisticas["markov_actual"][1],
        estadisticas["markov_actual"][2],
        estadisticas["markov_proyeccion"][0],
        estadisticas["markov_proyeccion"][2],
    ]
    colores_2 = ["#004AAD", "#009FE3", "#B91C1C", "#1D4ED8", "#991B1B"]

    canvas_m1_c.bind("<Configure>", lambda e: _dibujar_barras_canvas(
        canvas_m1_c, "M₁ (Rango Edad) y C (Cupos %)", etiquetas_1, valores_1, colores_1))
    canvas_markov.bind("<Configure>", lambda e: _dibujar_barras_canvas(
        canvas_markov, "Cadena de Markov: Estado Actual vs Proyección (%)", etiquetas_2, valores_2, colores_2))

    # Lado derecho abajo: Tabla de capacidad por hogar O Registro de accesos si es Administrador
    marco_derecho = tk.Frame(panel_inferior, bg="White", highlightbackground="#CBD5E1", highlightthickness=1)
    marco_derecho.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

    es_admin = (Login2_0.rol_actual or "").strip().lower() == "administrador"

    if es_admin:
        tk.Label(marco_derecho, text="REGISTRO DE ACCESO DE USUARIOS", font=("Segoe UI", 11, "bold"),
                 bg=COLOR_MENU, fg="White", pady=9).pack(fill="x")
        tree_acc = _crear_tabla_panel(marco_derecho, ("USUARIO", "FECHA Y HORA", "RESULTADO"),
                                      [135, 145, 90], tags_colores=True)
        try:
            accesos = Conexion.consultar(
                "SELECT CONCAT(u.nombre, ' ', u.apellido, ' (', u.nombre_usuario, ')'), "
                "DATE_FORMAT(r.fecha_hora, '%Y-%m-%d %H:%i'), r.resultado "
                "FROM registro_acceso r "
                "JOIN usuario u ON u.id_usuario = r.id_usuario "
                "ORDER BY r.fecha_hora DESC, r.id_registro DESC LIMIT 50")
            for usr, fhora, res in accesos:
                tree_acc.insert("", "end", values=(usr, fhora, res.upper()), tags=(res.lower(),))
        except pymysql.MySQLError as error:
            tk.Label(marco_derecho, text=f"Error al cargar accesos:\n{error}",
                     bg="White", fg="#B91C1C").pack(pady=10)
    else:
        tk.Label(marco_derecho, text="CAPACIDAD Y OCUPACIÓN POR HOGAR", font=("Segoe UI", 11, "bold"),
                 bg=COLOR_MENU, fg="White", pady=9).pack(fill="x")
        tree_hog = _crear_tabla_panel(marco_derecho, ("HOGAR", "CAPACIDAD", "OCUPADO", "DISPONIBLE"),
                                      [155, 78, 72, 80])
        for num, nom, cap, ocu, disp in estadisticas["hogares"]:
            tree_hog.insert("", "end", values=(f"{num} - {nom}", cap, ocu, disp))

        resumen_txt = (f"Total (1·C): Capacidad {estadisticas['cap_total']}   |   "
                       f"Ocupado {estadisticas['ocu_total']}   |   "
                       f"Disponible {estadisticas['disp_total']}")
        tk.Label(marco_derecho, text=resumen_txt, font=("Segoe UI", 9, "bold"),
                 bg=Componentes.COLOR_SECCION, fg=COLOR_MENU, pady=7).pack(fill="x", side="bottom")


def abrir_panel():
    cerrar_sesion_solicitado = False

    ventana=tk.Tk()
    ventana.title("Sistema de Gestión - Aldeas SOS")
    ventana.minsize(1050, 700)
    Componentes.centrar_ventana(ventana, 1200, 800)

    panel_izquierdo=tk.Frame(ventana,bg=COLOR_MENU,width=280)
    panel_izquierdo.pack_propagate(False)
    panel_izquierdo.pack(side="left",fill="y")

    panel_derecho=tk.Frame(ventana,bg="White")
    panel_derecho.pack_propagate(False)
    panel_derecho.pack(fill="both",expand=True)

    tk.Label(panel_izquierdo,text="GESTIÓN\nDE HOGARES",font=("Segoe UI",18,"bold"),
             bg=COLOR_MENU,fg="White").pack(pady=(20, 12))

    tarjeta_rol = tk.Frame(panel_izquierdo, bg="#2B3B4E", highlightbackground="#3B4D63", highlightthickness=1)
    tarjeta_rol.pack(fill="x", padx=16, pady=(0, 14))
    nombre_usuario = Login2_0.usuario_actual or "Usuario"
    rol_usuario = Login2_0.rol_actual or "Sin rol"
    tk.Label(tarjeta_rol, text=nombre_usuario, font=("Segoe UI", 10, "bold"),
             bg="#2B3B4E", fg="White", anchor="w").pack(fill="x", padx=12, pady=(8, 0))
    tk.Label(tarjeta_rol, text=f"Rol: {rol_usuario}", font=("Segoe UI", 9, "bold"),
             bg="#2B3B4E", fg="#7CCFF1", anchor="w").pack(fill="x", padx=12, pady=(2, 8))

    tk.Frame(panel_izquierdo, bg="#334155", height=1).pack(fill="x", padx=20, pady=(0, 10))

    Nombres=["Panel inicial","Participantes","Cuidadoras","Hogares","Resumen - Hogares","Resumen-Participantes"]
    botones=[]
    actual = {"nombre": "Panel inicial"}

    def seleccionar(nombre):
        actual["nombre"] = nombre
        for i in range(len(Nombres)):
            if Nombres[i] == nombre:
                botones[i].config(bg=COLOR_SELECCION, fg=COLOR_MENU)
            else:
                botones[i].config(bg=COLOR_MENU, fg="White")

        match nombre:
            case "Panel inicial":
                mostrar_resumen(panel_derecho)
            case "Participantes":
                Participantes.mostrar(panel_derecho)
            case "Cuidadoras":
                Cuidadoras.mostrar(panel_derecho)
            case "Hogares":
                Hogares.mostrar(panel_derecho)
            case "Resumen - Hogares":
                Resumen_Hogares.mostrar(panel_derecho)
            case "Resumen-Participantes":
                Resumen_Participantes.mostrar(panel_derecho)

    for nombre in Nombres:
        boton=tk.Button(panel_izquierdo,
                        text=nombre.upper(),
                        font=("Segoe UI",12,"bold"),
                        bg=COLOR_MENU,
                        fg="White",
                        pady=12,
                        relief="flat",activebackground=COLOR_SELECCION,
                        activeforeground=COLOR_MENU,anchor="w",padx=20,
                        cursor="hand2",
                        command=lambda n=nombre: seleccionar(n))
        boton.pack(fill="x",pady=(2,0))
        boton.bind("<Enter>", lambda e, b=boton, n=nombre: b.config(bg=COLOR_MENU_HOVER) if actual["nombre"] != n else None)
        boton.bind("<Leave>", lambda e, b=boton, n=nombre: b.config(bg=COLOR_MENU) if actual["nombre"] != n else None)
        botones.append(boton)

    def cerrar_sesion():
        nonlocal cerrar_sesion_solicitado
        if messagebox.askyesno("Cerrar sesión", "¿Deseas cerrar la sesión actual?"):
            cerrar_sesion_solicitado = True
            ventana.destroy()

    Abrir_imagen=Image.open("LOGO_NEGATIVO.png").convert("RGBA")
    filtro = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
    Imagen_redimensionada=Abrir_imagen.resize((220,80), filtro)
    Imagen_logo=ImageTk.PhotoImage(Imagen_redimensionada)
    lbl_logo = tk.Label(panel_izquierdo,image=Imagen_logo,bg=COLOR_MENU,fg="White")
    lbl_logo.image = Imagen_logo
    lbl_logo.pack(side="bottom",padx=15,pady=(8,18))

    btn_cerrar = tk.Button(panel_izquierdo, text="CERRAR SESIÓN", font=("Segoe UI", 11, "bold"),
                           bg="#991B1B", fg="White", activebackground="#B91C1C", activeforeground="White",
                           relief="flat", cursor="hand2", pady=10, command=cerrar_sesion)
    btn_cerrar.pack(side="bottom", fill="x", padx=16, pady=(6, 10))
    btn_cerrar.bind("<Enter>", lambda e: btn_cerrar.config(bg="#B91C1C"))
    btn_cerrar.bind("<Leave>", lambda e: btn_cerrar.config(bg="#991B1B"))
    
    seleccionar("Panel inicial")

    ventana.mainloop()
    return cerrar_sesion_solicitado
