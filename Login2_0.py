import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime,timedelta
import hashlib
import pymysql
import Conexion                          

acceso_concedido=False

def validar_usuario(nombre_usuario,contra):
    try:
        conex=Conexion.conectar()
    except pymysql.MySQLError as error:
        return False,f"LA CONEXION CON LA BASE DE DATOS FALLO \n {error}"
    try:
        cursor=conex.cursor()
        cursor.execute("SELECT id_usuario, contrasena_hash, intentos_fallidos, bloqueo_hasta, estado "
                       "FROM usuario WHERE nombre_usuario = %s",(nombre_usuario,))
        fila=cursor.fetchone()

        if fila is None:
            return False, "Usuario o Contraseña Incorrectos"
        
        id_usuario,has_guardado,intentos,bloqueo_hasta,estado=fila
        ahora=datetime.now()

        if estado != "activo":
            return False,"Usuario Inactivo No Puede Realizar Acciones"
        if bloqueo_hasta is not None and bloqueo_hasta > ahora:
            segundos = int((bloqueo_hasta - ahora).total_seconds()) + 1
            cursor.execute("INSERT INTO registro_acceso (id_usuario, resultado) VALUES (%s, 'bloqueado')",
                           (id_usuario,))
            conex.commit()
            return False, f"Usuario bloqueado. Intenta de nuevo en {segundos} segundos."

        hash_ingresado = hashlib.sha256(contra.encode("utf-8")).hexdigest()

        if hash_ingresado == has_guardado.lower():
            cursor.execute("UPDATE usuario SET intentos_fallidos = 0, bloqueo_hasta = NULL "
                           "WHERE id_usuario = %s", (id_usuario,))
            cursor.execute("INSERT INTO registro_acceso (id_usuario, resultado) VALUES (%s, 'exitoso')",
                           (id_usuario,))
            conex.commit()
            return True, "Bienvenido"

        intentos = intentos + 1
        if intentos >= 3:
            nuevo_bloqueo = ahora + timedelta(minutes=1)
            cursor.execute("UPDATE usuario SET intentos_fallidos = 0, bloqueo_hasta = %s "
                           "WHERE id_usuario = %s", (nuevo_bloqueo, id_usuario))
            mensaje = "Contraseña incorrecta. Usuario bloqueado por 1 minuto."
        else:
            cursor.execute("UPDATE usuario SET intentos_fallidos = %s WHERE id_usuario = %s",
                           (intentos, id_usuario))
            mensaje = f"Usuario o contraseña incorrectos. Intento {intentos} de 3."
        cursor.execute("INSERT INTO registro_acceso (id_usuario, resultado) VALUES (%s, 'fallido')",
                       (id_usuario,))
        conex.commit()
        return False, mensaje

    except pymysql.MySQLError as error:
        return False, f"Error en la base de datos:\n{error}"
    finally:
        conex.close()

def conectar_db():
    valor,mensaje=Conexion.comprobar_conexion()
    if valor:
        messagebox.showinfo("CONEXION DE DATOS", mensaje)
    else:
        messagebox.showerror("CONEXION DE DATOS", mensaje)


def abrir_login():
    global acceso_concedido
    acceso_concedido=False

    def mostrar_contra_entry():
        if mostrar_contra.get():
            Contra_Entry.config(show="")
        else:
            Contra_Entry.config(show="*")

    def iniciar_sesion():
        global acceso_concedido
        usuario=Usuario_Entry.get().strip()
        contra=Contra_Entry.get()

        if usuario=="" or contra=="":
            messagebox.showwarning("INICIO DE SESION","Escribe tu usuario y tu contraseña.")
            return

        valor,mensaje=validar_usuario(usuario,contra)
        if valor:
            acceso_concedido=True
            ventana.destroy()
        else:
            messagebox.showerror("INICIO DE SESION",mensaje)
            Contra_Entry.delete(0,"end")

    ventana=tk.Tk()
    ventana.title("Login")
    ventana.geometry("1200x800")
    ventana.config(bg="#0C0606")

    Panel_superior=tk.Frame(ventana,bg="#009FE3",width=20,height=200)
    Panel_superior.pack_propagate(False)
    Panel_superior.pack(fill="x")

    panel_inferior=tk.Frame(ventana,bg="#009FE3",height=90)
    panel_inferior.pack_propagate(False)
    panel_inferior.pack(side="bottom",fill="x")

    panel_derecho=tk.Frame(ventana,bg="#83dbf8",width=500,height=20)
    panel_derecho.pack_propagate(False)
    panel_derecho.pack(side="right",fill="y",padx=(0,29))

    panel_izquierdo=tk.Frame(ventana,bg="#0C0606")
    panel_izquierdo.pack_propagate(False)
    panel_izquierdo.pack(side="left",expand=True,fill="both")

    #Panel Superior

    Abrir_logo_Aldeas_sos=Image.open("LOGO_ALDEAS_SOS.jpg")
    Logo_Aldeas_Redimensionada=Abrir_logo_Aldeas_sos.resize((900,200))

    Logo_Aldeas=ImageTk.PhotoImage(Logo_Aldeas_Redimensionada)

    tk.Label(Panel_superior,image=Logo_Aldeas,bd=0,highlightthickness=0).pack(side="left")

    #Panel_Derecho(Inicio de Sesion)
    tk.Label(panel_derecho, text="INICIO DE SESION",font=("Segoe UI",30,"bold"),
            bg="#83dbf8",fg="Black").pack(padx=15,anchor="nw",pady=(0,20))

    tk.Label(panel_derecho,text="USUARIO",font=("Segoe UI",23,"bold"),
            bg="#83dbf8",fg="Black").pack(padx=15,anchor="nw")

    Usuario_Entry=tk.Entry(panel_derecho,bg="#fdf7f7",relief="solid",bd=1,font=("Segoe UI",20))
    Usuario_Entry.pack(padx=15,fill="x",ipady=15)

    tk.Label(panel_derecho,text="CONTRASEÑA",font=("Segoe UI",23,"bold"),
            bg="#83dbf8",fg="Black").pack(padx=15,anchor="nw")

    Contra_Entry=tk.Entry(panel_derecho,bg="#fdf7f7",relief="solid",bd=1,font=("Segoe UI",20),show="*")
    Contra_Entry.pack(padx=15,ipady=15,fill="x")

    mostrar_contra=tk.BooleanVar(value=False)
    tk.Checkbutton(panel_derecho,variable=mostrar_contra,text="MOSTRAR",font=("Segoe UI",20,"bold"),bg="#83dbf8",
                fg="Black",activebackground="#83dbf8",command=mostrar_contra_entry).pack(anchor="nw",padx=15)

    Iniciar_Sesion=tk.Button(panel_derecho,text="Iniciar Sesion",font=("Segoe UI",19,"bold"),bg="#0A1648",
                            fg="White",command=iniciar_sesion)
    Iniciar_Sesion.pack(fill="x",padx=15,pady=(10,0))

    Conectar_Base_De_Datos=tk.Button(panel_derecho,text="COMPROBAR BASE DE DATOS",font=("Segoe UI",19,"bold"),bg="#0A1648",
                            fg="White",command=conectar_db)

    Conectar_Base_De_Datos.pack(fill="x",padx=15,pady=(15,0))

    ventana.bind("<Return>",lambda evento: iniciar_sesion())

    ventana.mainloop()
    return acceso_concedido 