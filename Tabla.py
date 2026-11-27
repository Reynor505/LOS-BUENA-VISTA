import tkinter as tk
import Componentes


def crear_tabla(padre, encabezados, anchos):
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
    for widget in filas.winfo_children():
        widget.destroy()


def agregar_fila(filas, valores, anchos, lineas=1):
    alto = max(48, lineas * 18 + 16)
    es_par = len(filas.winfo_children()) % 2 == 0
    fondo = "#FFFFFF" if es_par else "#F8FAFC"

    fila = tk.Frame(filas, bg=fondo)
    fila.pack(anchor="w")
    for i in range(len(valores)):
        texto = str(valores[i])
        color_texto = Componentes.COLOR_TEXTO
        fuente = (Componentes.FUENTE, 10)
        if texto.lower() == "activo":
            color_texto = "#15803D"
            fuente = (Componentes.FUENTE, 10, "bold")
        elif texto.lower() in ("egresado", "inactivo"):
            color_texto = "#B91C1C"
            fuente = (Componentes.FUENTE, 10, "bold")

        celda = tk.Frame(fila, width=anchos[i], height=alto, bg=fondo,
                         highlightbackground=Componentes.COLOR_BORDE_CAMPO, highlightthickness=1)
        celda.pack_propagate(False)
        celda.pack(side="left")
        tk.Label(celda, text=texto, font=fuente, bg=fondo, fg=color_texto,
                 wraplength=anchos[i] - 8, justify="center").pack(expand=True)
