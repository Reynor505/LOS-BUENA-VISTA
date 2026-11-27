import tkinter as tk
from PIL import Image, ImageTk
import pymysql
import Conexion
import Componentes
import Participantes
import Cuidadoras
import Hogares
import Resumen_Hogares
import Resumen_Participantes


COLOR_MENU = "#1F2B3A"
COLOR_SELECCION = "#7CCFF1"
COLOR_TARJETA = "#C8D1D9"

def mostrar_resumen(contenedor):
    Componentes.limpiar_contenedor(contenedor)

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
            numero = Conexion.consultar(consultas[i])[0][0]
        except pymysql.MySQLError:
            numero = "-"

        tarjeta = tk.Frame(contenedor,bg=COLOR_TARJETA,width=190,height=250)
        tarjeta.pack_propagate(False)
        tarjeta.grid(row=1,column=i,padx=10)

        tk.Label(tarjeta,text=titulos[i],font=("Arial",14,"bold"),bg=COLOR_TARJETA).pack(pady=(15,0))
        tk.Label(tarjeta,text=str(numero),font=("Arial",54,"bold"),bg=COLOR_TARJETA).pack(expand=True)


def abrir_panel():
    ventana=tk.Tk()
    ventana.title("Panel Inicial")
    ventana.geometry("1200x800")

    panel_izquierdo=tk.Frame(ventana,bg=COLOR_MENU,width=300)
    panel_izquierdo.pack_propagate(False)
    panel_izquierdo.pack(side="left",fill="y")

    panel_derecho=tk.Frame(ventana,bg="White")
    panel_derecho.pack_propagate(False)
    panel_derecho.pack(fill="both",expand=True)

    tk.Label(panel_izquierdo,text=f"GESTION \n DE HOGARES",font=("Segoe UI",18,"bold"),
             bg=COLOR_MENU,fg="White").pack(pady=18)

    Nombres=["Panel inicial","Participantes","Cuidadoras","Hogares","Resumen - Hogares","Resumen-Participantes"]
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
            case "Resumen - Hogares":
                Resumen_Hogares.mostrar(panel_derecho)
            case "Resumen-Participantes":
                Resumen_Participantes.mostrar(panel_derecho)

    for nombre in Nombres:
        boton=tk.Button(panel_izquierdo,
                        text=nombre.upper(),
                        font=("Arial",14,"bold"),
                        bg=COLOR_MENU,
                        fg="White",
                        height=1,
                        relief="flat",activebackground="#095AAB",
                        activeforeground="white",anchor="w",padx=15,
                        command=lambda n=nombre: seleccionar(n))
        boton.pack(fill="x",pady=(2,0))
        botones.append(boton)

    Abrir_imagen=Image.open("LOGO_NEGATIVO.png").convert("RGBA")
    Imagen_redimensionada=Abrir_imagen.resize((235,86))
    Imagen_logo=ImageTk.PhotoImage(Imagen_redimensionada)
    tk.Label(panel_izquierdo,image=Imagen_logo,bg=COLOR_MENU,fg="White").pack(side="bottom",padx=15)
    
    seleccionar("Panel inicial")

    ventana.mainloop()
