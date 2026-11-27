import tkinter as tk
from tkinter import messagebox
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

def mostrar_resumen(contenedor):
    Componentes.limpiar_contenedor(contenedor)

    Componentes.crear_titulo(contenedor, "PANEL INICIAL")

    marco_tarjetas = tk.Frame(contenedor, bg="White")
    marco_tarjetas.pack(fill="x", padx=12, pady=12)
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

        tarjeta = tk.Frame(marco_tarjetas, bg=COLOR_TARJETA, height=230,
                           highlightbackground="#CBD5E1", highlightthickness=1)
        tarjeta.pack_propagate(False)
        tarjeta.grid(row=0, column=i, padx=10, pady=8, sticky="nsew")

        tk.Frame(tarjeta, bg=COLORES_ACENTO[i], height=6).pack(fill="x")
        tk.Label(tarjeta, text=titulos[i], font=("Segoe UI", 13, "bold"),
                 bg=COLOR_TARJETA, fg="#1E293B").pack(pady=(22, 0))
        tk.Label(tarjeta, text=str(numero), font=("Segoe UI", 48, "bold"),
                 bg=COLOR_TARJETA, fg=COLORES_ACENTO[i]).pack(expand=True)


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
