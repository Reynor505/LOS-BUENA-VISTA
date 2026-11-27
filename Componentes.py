import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import pymysql
import Conexion

COLOR_FONDO = "#FFFFFF"
COLOR_MENU = "#1F2B3A"
COLOR_SECCION = "#D6EBFF"
COLOR_BORDE_SECCION = "#A5D3FB"
COLOR_BORDE_CAMPO = "#CBD5E1"
COLOR_TEXTO = "#1E293B"
COLOR_BOTON = "#004AAD"
COLOR_BOTON_HOVER = "#003A8A"
MARCADOR_FECHA = "AAAA-MM-DD"
MAX_CUIDADORAS = 3
FUENTE = "Segoe UI"


def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = max(0, (ventana.winfo_screenwidth() - ancho) // 2)
    y = max(0, (ventana.winfo_screenheight() - alto) // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def limpiar_contenedor(contenedor):
    for widget in contenedor.winfo_children():
        widget.destroy()


def crear_titulo(padre, texto):
    tk.Label(padre, text=texto, font=(FUENTE, 20, "bold"),
             bg=COLOR_FONDO, fg=COLOR_MENU).pack(anchor="w", padx=20, pady=(16, 8))


def crear_marco(padre):
    marco = tk.Frame(padre, bg=COLOR_SECCION, highlightbackground=COLOR_BORDE_SECCION, highlightthickness=1)
    marco.pack(fill="x", padx=20, pady=(0, 6))
    marco.grid_columnconfigure(0, weight=1, uniform="col")
    marco.grid_columnconfigure(1, weight=1, uniform="col")
    return marco


def crear_seccion(padre, texto):
    tk.Label(padre, text=texto, font=(FUENTE, 13, "bold"),
             bg=COLOR_FONDO, fg=COLOR_BOTON).pack(anchor="w", padx=20, pady=(12, 4))
    return crear_marco(padre)


def crear_campo(marco, texto, fila, columna):
    tk.Label(marco, text=texto, font=(FUENTE, 10, "bold"),
             bg=COLOR_SECCION, fg=COLOR_TEXTO).grid(row=fila * 2, column=columna, sticky="w", padx=15, pady=(8, 2))
    entrada = tk.Entry(marco, font=(FUENTE, 11), relief="flat", bg="#FFFFFF", fg=COLOR_TEXTO,
                       highlightthickness=1, highlightbackground=COLOR_BORDE_CAMPO, highlightcolor=COLOR_BOTON)
    entrada.grid(row=fila * 2 + 1, column=columna, sticky="ew", padx=15, pady=(0, 8), ipady=5)
    return entrada


def crear_combo(marco, texto, fila, columna, valores):
    estilo = ttk.Style()
    estilo.configure("TCombobox", padding=4)
    tk.Label(marco, text=texto, font=(FUENTE, 10, "bold"),
             bg=COLOR_SECCION, fg=COLOR_TEXTO).grid(row=fila * 2, column=columna, sticky="w", padx=15, pady=(8, 2))
    combo = ttk.Combobox(marco, values=valores, state="readonly", font=(FUENTE, 11))
    combo.grid(row=fila * 2 + 1, column=columna, sticky="ew", padx=15, pady=(0, 8), ipady=3)
    return combo


def crear_campo_fecha(marco, texto, fila, columna):
    entrada = crear_campo(marco, texto, fila, columna)
    reiniciar_fecha(entrada)

    def al_entrar(evento):
        if entrada.get() == MARCADOR_FECHA:
            entrada.delete(0, "end")
            entrada.config(fg="black")

    def al_salir(evento):
        if entrada.get() == "":
            entrada.insert(0, MARCADOR_FECHA)
            entrada.config(fg="gray")

    entrada.bind("<FocusIn>", al_entrar)
    entrada.bind("<FocusOut>", al_salir)
    return entrada


def reiniciar_fecha(entrada):
    entrada.delete(0, "end")
    entrada.insert(0, MARCADOR_FECHA)
    entrada.config(fg="gray")


def validar_fecha(texto):
    try:
        return datetime.strptime(texto.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None

def crear_boton_registrar(padre, comando_registrar, fijo_abajo=False):
    marco = tk.Frame(padre, bg=COLOR_FONDO)
    if fijo_abajo:
        marco.pack(side="bottom", fill="x", padx=20, pady=12)
    else:
        marco.pack(fill="x", padx=20, pady=15)
    boton = tk.Button(marco, text="REGISTRAR", font=(FUENTE, 12, "bold"), bg=COLOR_BOTON, fg="White",
                      activebackground=COLOR_BOTON_HOVER, activeforeground="White", relief="flat",
                      cursor="hand2", padx=28, pady=10, command=comando_registrar)
    boton.pack(side="right")
    boton.bind("<Enter>", lambda e: boton.config(bg=COLOR_BOTON_HOVER))
    boton.bind("<Leave>", lambda e: boton.config(bg=COLOR_BOTON))
    return boton


def crear_contenedor_desplazable(padre):
    contenedor_scroll = tk.Frame(padre, bg=COLOR_FONDO)
    contenedor_scroll.pack(fill="both", expand=True)

    lienzo = tk.Canvas(contenedor_scroll, bg=COLOR_FONDO, highlightthickness=0)
    barra = tk.Scrollbar(contenedor_scroll, orient="vertical", command=lienzo.yview)
    lienzo.configure(yscrollcommand=barra.set)

    barra.pack(side="right", fill="y")
    lienzo.pack(side="left", fill="both", expand=True)

    interior = tk.Frame(lienzo, bg=COLOR_FONDO)
    ventana_id = lienzo.create_window((0, 0), window=interior, anchor="nw")

    interior.bind("<Configure>", lambda e: lienzo.configure(scrollregion=lienzo.bbox("all")))
    lienzo.bind("<Configure>", lambda e: lienzo.itemconfigure(ventana_id, width=e.width))

    def rueda(evento):
        if lienzo.winfo_exists() and interior.winfo_reqheight() > lienzo.winfo_height():
            lienzo.yview_scroll(int(-1 * (evento.delta / 120)), "units")

    lienzo.bind("<Enter>", lambda e: lienzo.bind_all("<MouseWheel>", rueda))
    lienzo.bind("<Leave>", lambda e: lienzo.unbind_all("<MouseWheel>"))
    lienzo.bind("<Destroy>", lambda e: lienzo.unbind_all("<MouseWheel>"))
    return interior


def agregar_placeholder(entrada, texto_placeholder):
    entrada._placeholder_texto = texto_placeholder
    entrada._placeholder_activo = True
    entrada.delete(0, "end")
    entrada.insert(0, texto_placeholder)
    entrada.config(fg="#64748B")

    def al_entrar(evento):
        if getattr(entrada, "_placeholder_activo", False):
            entrada.delete(0, "end")
            entrada.config(fg=COLOR_TEXTO)
            entrada._placeholder_activo = False

    def al_salir(evento):
        if entrada.get() == "":
            entrada._placeholder_activo = True
            entrada.insert(0, texto_placeholder)
            entrada.config(fg="#64748B")

    entrada.bind("<FocusIn>", al_entrar)
    entrada.bind("<FocusOut>", al_salir)


def obtener_texto_entrada(entrada):
    if getattr(entrada, "_placeholder_activo", False):
        return ""
    return entrada.get().strip()


def crear_barra_busqueda(padre, placeholder=""):
    barra = tk.Frame(padre, bg=COLOR_MENU)
    barra.pack(fill="x", padx=20, pady=(0, 10))
    tk.Label(barra, text="BUSCAR", font=(FUENTE, 11, "bold"), bg=COLOR_MENU,
             fg="White").pack(side="left", padx=(18, 12), pady=12)
    entrada = tk.Entry(barra, font=(FUENTE, 12), relief="flat", width=36, bg="#FFFFFF", fg=COLOR_TEXTO,
                       highlightthickness=1, highlightbackground=COLOR_BORDE_CAMPO, highlightcolor="#7CCFF1")
    entrada.pack(side="left", padx=(0, 14), pady=12, ipady=5)
    if placeholder:
        agregar_placeholder(entrada, placeholder)
    return entrada


def crear_barra_filtros(padre):
    marco = tk.Frame(padre, bg=COLOR_SECCION, highlightbackground=COLOR_BORDE_SECCION, highlightthickness=1)
    marco.pack(fill="x", padx=20, pady=(0, 10))
    return marco


def agregar_filtro_combo(barra_filtros, texto, valores, ancho=18):
    estilo = ttk.Style()
    estilo.configure("TCombobox", padding=3)
    bloque = tk.Frame(barra_filtros, bg=COLOR_SECCION)
    bloque.pack(side="left", padx=(12, 6), pady=8)
    tk.Label(bloque, text=texto, font=(FUENTE, 9, "bold"), bg=COLOR_SECCION, fg=COLOR_TEXTO).pack(anchor="w")
    combo = ttk.Combobox(bloque, values=valores, state="readonly", font=(FUENTE, 10), width=ancho)
    if valores:
        combo.current(0)
    combo.pack(pady=(2, 0))
    return combo


def cargar_hogares():
    ids = []
    nombres = []
    try:
        filas = Conexion.consultar("SELECT id_hogar, numero_hogar, nombre_hogar FROM hogar "
                                   "WHERE estado = 'activo' ORDER BY numero_hogar")
        for fila in filas:
            ids.append(fila[0])
            nombres.append(f"{fila[1]} - {fila[2]}")
    except pymysql.MySQLError as error:
        messagebox.showerror("Base de datos", f"No se pudieron cargar los hogares:\n{error}")
    return ids, nombres

def conectar_direccion(combo_dep, combo_ciudad, combo_zona, combo_calle):
    ids_dep = []
    ids_ciudad = []
    ids_zona = []
    ids_calle = []

    def llenar(combo, lista_ids, sql, datos):
        lista_ids.clear()
        nombres = []
        try:
            filas = Conexion.consultar(sql, datos)
        except pymysql.MySQLError as error:
            messagebox.showerror("Base de datos", f"No se pudieron cargar los datos:\n{error}")
            filas = []
        for fila in filas:
            lista_ids.append(fila[0])
            nombres.append(fila[1])
        combo["values"] = nombres
        combo.set("")

    def vaciar(combo, lista_ids):
        lista_ids.clear()
        combo["values"] = []
        combo.set("")

    def al_elegir_dep(evento):
        id_dep = ids_dep[combo_dep.current()]
        llenar(combo_ciudad, ids_ciudad,
               "SELECT id_ciudad, nombre FROM ciudad WHERE id_departamento = %s ORDER BY nombre", (id_dep,))
        vaciar(combo_zona, ids_zona)
        vaciar(combo_calle, ids_calle)

    def al_elegir_ciudad(evento):
        id_ciudad = ids_ciudad[combo_ciudad.current()]
        llenar(combo_zona, ids_zona,
               "SELECT id_zona, nombre FROM zona WHERE id_ciudad = %s ORDER BY nombre", (id_ciudad,))
        vaciar(combo_calle, ids_calle)

    def al_elegir_zona(evento):
        id_zona = ids_zona[combo_zona.current()]
        llenar(combo_calle, ids_calle,
               "SELECT id_calle, nombre FROM calles WHERE id_zona = %s ORDER BY nombre", (id_zona,))

    combo_dep.bind("<<ComboboxSelected>>", al_elegir_dep)
    combo_ciudad.bind("<<ComboboxSelected>>", al_elegir_ciudad)
    combo_zona.bind("<<ComboboxSelected>>", al_elegir_zona)

    def reiniciar():
        llenar(combo_dep, ids_dep, "SELECT id_departamento, nombre FROM departamentos ORDER BY nombre", ())
        vaciar(combo_ciudad, ids_ciudad)
        vaciar(combo_zona, ids_zona)
        vaciar(combo_calle, ids_calle)

    def obtener():
        if (combo_dep.current() == -1 or combo_ciudad.current() == -1
                or combo_zona.current() == -1 or combo_calle.current() == -1):
            return None
        return (ids_dep[combo_dep.current()], ids_ciudad[combo_ciudad.current()],
                ids_zona[combo_zona.current()], ids_calle[combo_calle.current()])

    reiniciar()
    return obtener, reiniciar
