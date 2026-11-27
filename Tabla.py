import tkinter as tk
import Componentes


def crear_tabla(padre, encabezados, anchos):
    marco = tk.Frame(padre, bg="White")
    marco.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    fila_encabezado = tk.Frame(marco, bg=Componentes.COLOR_SECCION)
    fila_encabezado.pack(anchor="w")
    for i in range(len(encabezados)):
        celda = tk.Frame(fila_encabezado, width=anchos[i], height=60, bg=Componentes.COLOR_SECCION,
                         highlightbackground="Black", highlightthickness=1)
        celda.pack_propagate(False)
        celda.pack(side="left")
        tk.Label(celda, text=encabezados[i], font=("Arial", 11, "bold"), bg=Componentes.COLOR_SECCION,
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
        lienzo.yview_scroll(int(-1 * (evento.delta / 120)), "units")

    lienzo.bind("<Enter>", lambda evento: lienzo.bind_all("<MouseWheel>", rueda))
    lienzo.bind("<Leave>", lambda evento: lienzo.unbind_all("<MouseWheel>"))
    return filas


def vaciar_tabla(filas):
    for widget in filas.winfo_children():
        widget.destroy()


def agregar_fila(filas, valores, anchos, lineas=1):
    alto = max(50, lineas * 16 + 18)
    fila = tk.Frame(filas, bg="White")
    fila.pack(anchor="w")
    for i in range(len(valores)):
        celda = tk.Frame(fila, width=anchos[i], height=alto, bg="White",
                         highlightbackground="Black", highlightthickness=1)
        celda.pack_propagate(False)
        celda.pack(side="left")
        tk.Label(celda, text=str(valores[i]), font=("Arial", 10), bg="White",
                 wraplength=anchos[i] - 8, justify="center").pack(expand=True)
