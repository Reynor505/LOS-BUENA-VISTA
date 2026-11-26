import tkinter as tk
from PIL import Image, ImageTk
import pymysql
import Participantes
import Cuidadoras
import Hogares
import Login2_0

COLOR_MENU = "#1F2937"
COLOR_SELECCION = "#7CCFF1"
COLOR_TARJETA = "#C8D1D9"

def mostrar_resumen(contenedor):
    Login2_0.limpiar_contenedor(contenedor)

    tk.Label(contenedor,text="PANEL INICIAL",font=("Arial",20,"bold"),
             bg="White").grid(row=0,column=0,padx=(15,0),pady=20,columnspan=4,sticky="w")

    for i in range (4):
        contenedor.grid_columnconfigure(i,weight=1,uniform="col")

    titulos = ["PARTICIPANTES\nACTIVOS", "HOGARES\nACTIVOS", "EGRESOS", "SEGUIMIENTOS"]
    consultas = [
        "SELECT COUNT(*) FROM participantes WHERE id_participante NOT IN (SELECT id_participante FROM egreso)",
        "SELECT COUNT(*) FROM hogar WHERE estado = 'activo'",
        "SELECT COUNT(*) FROM egreso",
        "SELECT COUNT(*) FROM seguimiento_egreso"]

    for i in range(4):
        try:
            numero =Login2_0.consultar(consultas[i])[0][0]
        except pymysql.MySQLError:
            numero = "-"

        tarjeta = tk.Frame(contenedor,bg=COLOR_TARJETA,width=200,height=250)
        tarjeta.pack_propagate(False)
        tarjeta.grid(row=1,column=i,padx=10)

        tk.Label(tarjeta,text=titulos[i],font=("Arial",14,"bold"),bg=COLOR_TARJETA).pack(pady=(15,0))
        tk.Label(tarjeta,text=str(numero),font=("Arial",54,"bold"),bg=COLOR_TARJETA).pack(expand=True)


def mostrar_pendiente(contenedor, nombre):
    Login2_0.limpiar_contenedor(contenedor)
    Login2_0.crear_titulo(contenedor, nombre.upper())
    tk.Label(contenedor,text="Esta pantalla todavia no esta desarrollada,MAS TIEMPO PORFA INGE :( ",
             font=("Arial",14),bg="White").pack(anchor="w",padx=15)


def abrir_panel():
    ventana=tk.Tk()
    ventana.title("Panel Inicial")
    ventana.geometry("1200x800")

    panel_izquierdo=tk.Frame(ventana,bg=COLOR_MENU,width=240)   
    panel_izquierdo.pack_propagate(False)
    panel_izquierdo.pack(side="left",fill="y")

    panel_derecho=tk.Frame(ventana,bg="White")                   
    panel_derecho.pack_propagate(False)
    panel_derecho.pack(fill="both",expand=True)

    #Panel Izquierdo

    tk.Label(panel_izquierdo,text=f"GESTION \n DE HOGARES",font=("Segoe UI",18,"bold"),
             bg=COLOR_MENU,fg="White").pack(pady=18)


    Abrir_imagen=Image.open("LOGO_NEGATIVO.png").convert("RGBA")
    Imagen_redimensionada=Abrir_imagen.resize((235,86))
    Imagen_logo=ImageTk.PhotoImage(Imagen_redimensionada)
    tk.Label(panel_izquierdo,image=Imagen_logo,bg=COLOR_MENU,fg="White").pack(side="bottom",padx=15)
    
    Nombres=["Panel inicial","Participantes","Cuidadoras","Hogares","Resumen","Buscar"]
    botones=[]

    def seleccionar(nombre):
        for i in range(len(Nombres)):
            if Nombres[i] == nombre:
                botones[i].config(bg=COLOR_SELECCION)
            else:
                botones[i].config(bg=COLOR_MENU)

        match nombre:
            case "Panel inicial":
                mostrar_resumen(panel_derecho)
            case "Participantes":
                Participantes.mostrar(panel_derecho)
            case "Cuidadoras":
                Cuidadoras.mostrar(panel_derecho)
            case "Hogares":
                Hogares.mostrar(panel_derecho)
            case "Resumen" | "Buscar":
                mostrar_pendiente(panel_derecho, nombre)

    for nombre in Nombres:
        boton=tk.Button(panel_izquierdo,
                        text=nombre.upper(),
                        font=("Arial",16,"bold"),
                        bg=COLOR_MENU,
                        fg="White",
                        height=1,
                        relief="flat",activebackground="#095AAB",
                        activeforeground="white",anchor="w",
                        command=lambda n=nombre: seleccionar(n))
        if nombre == "Buscar":
            boton.pack(side="bottom",fill="x",pady=(0,60))
        else:
            boton.pack(fill="x",pady=(2,0))
        botones.append(boton)

    seleccionar("Panel inicial")

    ventana.mainloop()
