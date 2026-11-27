import tkinter as tk
import Componentes


def crear_tabla(padre, encabezados, anchos, seleccionable=False, al_doble_clic=None):
    marco = tk.Frame(padre, bg="White")
    marco.pack(fill="both", expand=True, padx=20, pady=(0, 18))

    fila_encabezado = tk.Frame(marco, bg=Componentes.COLOR_SECCION)
    fila_encabezado.pack(anchor="w")
    for i in range(len(encabezados)):
        celda = tk.Frame(fila_encabezado, width=anchos[i], height=54, bg=Componentes.COLOR_SECCION,
                         highlightbackground=Componentes.COLOR_BORDE_SECCION, highlightthickness=1)
        celda.pack_propagate(False)
        celda.pack(side="left")
        tk.Label(celda, text=encabezados[i], font=(Componentes.FUENTE, 10, "bold"),
                 bg=Componentes.COLOR_SECCION, fg=Componentes.COLOR_MENU,
                 wraplength=anchos[i] - 8, justify="center").pack(expand=True)

    ancho_total = sum(anchos)
    cuerpo = tk.Frame(marco, bg="White")
    cuerpo.pack(fill="both", expand=True)

    lienzo = tk.Canvas(cuerpo, bg="White", highlightthickness=0, width=ancho_total)
    barra = tk.Scrollbar(cuerpo, orient="vertical", command=lienzo.yview)
    lienzo.configure(yscrollcommand=barra.set)
    lienzo.pack(side="left", fill="y")
    barra.pack(side="left", fill="y")

    filas = tk.Frame(lienzo, bg="White")
    filas._seleccionable = seleccionable
    filas._seleccion_activa = None
    filas._al_doble_clic = al_doble_clic
    lienzo.create_window((0, 0), window=filas, anchor="nw")
    filas.bind("<Configure>", lambda evento: lienzo.configure(scrollregion=lienzo.bbox("all")))

    def rueda(evento):
        if lienzo.winfo_exists():
            lienzo.yview_scroll(int(-1 * (evento.delta / 120)), "units")

    lienzo.bind("<Enter>", lambda evento: lienzo.bind_all("<MouseWheel>", rueda))
    lienzo.bind("<Leave>", lambda evento: lienzo.unbind_all("<MouseWheel>"))
    lienzo.bind("<Destroy>", lambda evento: lienzo.unbind_all("<MouseWheel>"))
    return filas


def vaciar_tabla(filas):
    filas._seleccion_activa = None
    for widget in filas.winfo_children():
        widget.destroy()


def _aplicar_fondo_fila(fila, fondo):
    fila.config(bg=fondo)
    for celda in fila.winfo_children():
        celda.config(bg=fondo)
        for hijo in celda.winfo_children():
            hijo.config(bg=fondo)


def obtener_dato_seleccionado(filas):
    fila = getattr(filas, "_seleccion_activa", None)
    if fila is None or not fila.winfo_exists():
        return None
    return getattr(fila, "_dato", None)


def agregar_fila(filas, valores, anchos, lineas=1, dato=None):
    alto = max(48, lineas * 18 + 16)
    es_par = len(filas.winfo_children()) % 2 == 0
    fondo = "#FFFFFF" if es_par else "#F8FAFC"

    fila = tk.Frame(filas, bg=fondo)
    fila._fondo_base = fondo
    fila._dato = dato
    fila.pack(anchor="w")

    def seleccionar(evento=None):
        anterior = getattr(filas, "_seleccion_activa", None)
        if anterior is not None and anterior.winfo_exists():
            _aplicar_fondo_fila(anterior, anterior._fondo_base)
        filas._seleccion_activa = fila
        _aplicar_fondo_fila(fila, "#DBEAFE")

    def doble_clic(evento=None):
        seleccionar()
        callback = getattr(filas, "_al_doble_clic", None)
        if callback is not None:
            callback(dato)

    es_seleccionable = getattr(filas, "_seleccionable", False)
    if es_seleccionable:
        fila.config(cursor="hand2")
        fila.bind("<Button-1>", seleccionar)
        fila.bind("<Double-Button-1>", doble_clic)

    for i in range(len(valores)):
        texto = str(valores[i])
        color_texto = Componentes.COLOR_TEXTO
        fuente = (Componentes.FUENTE, 10)
        if texto.lower() in ("activo", "exitoso"):
            color_texto = "#15803D"
            fuente = (Componentes.FUENTE, 10, "bold")
        elif texto.lower() in ("egresado", "inactivo", "fallido", "bloqueado"):
            color_texto = "#B91C1C"
            fuente = (Componentes.FUENTE, 10, "bold")

        celda = tk.Frame(fila, width=anchos[i], height=alto, bg=fondo,
                         highlightbackground=Componentes.COLOR_BORDE_CAMPO, highlightthickness=1)
        celda.pack_propagate(False)
        celda.pack(side="left")
        etiqueta = tk.Label(celda, text=texto, font=fuente, bg=fondo, fg=color_texto,
                            wraplength=anchos[i] - 8, justify="center")
        etiqueta.pack(expand=True)
        if es_seleccionable:
            celda.config(cursor="hand2")
            etiqueta.config(cursor="hand2")
            celda.bind("<Button-1>", seleccionar)
            etiqueta.bind("<Button-1>", seleccionar)
            celda.bind("<Double-Button-1>", doble_clic)
            etiqueta.bind("<Double-Button-1>", doble_clic)
