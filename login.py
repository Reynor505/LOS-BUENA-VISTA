import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import hashlib
import pymysql

acceso_concedido = False

HOST = "localhost"
USUARIO = "root"
CONTRASENA = "denil"
BASE_DE_DATOS = "aldeas_sos"


def conectar():
    return pymysql.connect(host=HOST,
                           user=USUARIO,
                           password=CONTRASENA,
                           database=BASE_DE_DATOS,
                           charset="utf8mb4")


def probar_conexion():
    try:
        con = conectar()
        con.close()
        return True, "Conexión exitosa con la base de datos aldeas_sos"
    except pymysql.MySQLError as error:
        return False, f"No se pudo conectar:\n{error}"


def consultar(sql, datos=()):
    con = conectar()
    try:
        cursor = con.cursor()
        cursor.execute(sql, datos)
        filas = cursor.fetchall()
        cursor.close()
        return filas
    finally:
        con.close()


def mensaje_error(error):
    codigo = 0
    if len(error.args) > 0 and isinstance(error.args[0], int):
        codigo = error.args[0]

    if codigo == 1062:
        return "Ya existe un registro con esos datos (CI, número o nombre repetido)."
    if codigo in (3819, 4025):
        return "Algún dato no cumple las reglas de la base de datos (revisa fechas, sexo y capacidad)."
    if codigo in (1054, 1048):
        return ("La estructura de la base de datos no coincide con el programa.\n"
                "Ejecuta el archivo cambios_base_datos.sql en MySQL Workbench.\n\n" + str(error))
    return str(error)


def validar_usuario(nombre_usuario, contrasena):
    try:
        con =conectar()
    except pymysql.MySQLError as error:
        return False, f"No se pudo conectar con la base de datos:\n{error}"

    try:
        cursor = con.cursor()
        cursor.execute("SELECT id_usuario, contrasena_hash, intentos_fallidos, bloqueo_hasta, estado "
                       "FROM usuario WHERE nombre_usuario = %s", (nombre_usuario,))
        fila = cursor.fetchone()

        if fila is None:
            # No se guarda en registro_acceso porque esa tabla exige un id_usuario
            return False, "Usuario o contraseña incorrectos."

        id_usuario, hash_guardado, intentos, bloqueo_hasta, estado = fila
        ahora = datetime.now()

        if estado != "activo":
            return False, "El usuario está inactivo. Habla con el administrador."

        # Si todavía está bloqueado no se revisa la contraseña
        if bloqueo_hasta is not None and bloqueo_hasta > ahora:
            segundos = int((bloqueo_hasta - ahora).total_seconds()) + 1
            cursor.execute("INSERT INTO registro_acceso (id_usuario, resultado) VALUES (%s, 'bloqueado')",
                           (id_usuario,))
            con.commit()
            return False, f"Usuario bloqueado. Intenta de nuevo en {segundos} segundos."

        hash_ingresado = hashlib.sha256(contrasena.encode("utf-8")).hexdigest()

        if hash_ingresado == hash_guardado.lower():
            cursor.execute("UPDATE usuario SET intentos_fallidos = 0, bloqueo_hasta = NULL "
                           "WHERE id_usuario = %s", (id_usuario,))
            cursor.execute("INSERT INTO registro_acceso (id_usuario, resultado) VALUES (%s, 'exitoso')",
                           (id_usuario,))
            con.commit()
            return True, "Bienvenido"

        # Contraseña incorrecta
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
        con.commit()
        return False, mensaje

    except pymysql.MySQLError as error:
        return False, f"Error en la base de datos:\n{error}"
    finally:
        con.close()

def abrir_login():
    global acceso_concedido
    acceso_concedido = False

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

    panel_derecho=tk.Frame(ventana,bg="#C3F6FF",width=500,height=20)
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
    
    #PanelDerecho(Inicio de Sesion)

    def iniciar_sesion():
        global acceso_concedido
        usuario = Usuario_Entry.get().strip()
        contra = Contra_Entry.get()

        if usuario == "" or contra == "":
            messagebox.showwarning("Inicio de sesión", "Escribe tu usuario y tu contraseña.")
            return

        correcto, mensaje = validar_usuario(usuario, contra)
        if correcto:
            acceso_concedido = True
            ventana.destroy()         
        else:
            messagebox.showerror("Inicio de sesión", mensaje)
            Contra_Entry.delete(0, "end")

    def conectar_base_de_datos():
        correcto, mensaje =probar_conexion()
        if correcto:
            messagebox.showinfo("Base de datos", mensaje)
        else:
            messagebox.showerror("Base de datos", mensaje)

    def mostrar_contrasena():
        if ver_contra.get():
            Contra_Entry.config(show="")
        else:
            Contra_Entry.config(show="*")

    tk.Label(panel_derecho, text="INICIO DE SESION",font=("Segoe UI",30,"bold"),
             bg="#C3F6FF",fg="Black").pack(padx=15,anchor="nw",pady=(0,20))

    tk.Label(panel_derecho,text="USUARIO",font=("Segoe UI",23,"bold"),
             bg="#C3F6FF",fg="Black").pack(padx=15,anchor="nw")

    Usuario_Entry=tk.Entry(panel_derecho,bg="#D7DCE5",relief="solid",bd=1,font=("Segoe UI",20))
    Usuario_Entry.pack(padx=15,fill="x",ipady=15)

    tk.Label(panel_derecho,text="CONTRASEÑA",font=("Segoe UI",23,"bold"),
             bg="#C3F6FF",fg="Black").pack(padx=15,anchor="nw")

    Contra_Entry=tk.Entry(panel_derecho,bg="#D7DCE5",relief="solid",bd=1,font=("Segoe UI",20),show="*")
    Contra_Entry.pack(padx=15,ipady=15,fill="x")

    ver_contra = tk.BooleanVar(value=False)
    tk.Checkbutton(panel_derecho,text="MOSTRAR",variable=ver_contra,command=mostrar_contrasena,
                   font=("Segoe UI",19,"bold"),bg="#C3F6FF",activebackground="#C3F6FF",
                   fg="Black").pack(anchor="nw",padx=15)

    Iniciar_Sesion=tk.Button(panel_derecho,text="INICIAR SESION",font=("Segoe UI",19,"bold"),bg="#1F2937",
                             fg="White",command=iniciar_sesion)
    Iniciar_Sesion.pack(fill="x",padx=15,pady=(15,0))

    Conectar_Base_De_Datos=tk.Button(panel_derecho,text="CONECTAR CON LA BASE DE DATOS",font=("Segoe UI",15,"bold"),
                                     bg="#1F2937",fg="White",command=conectar_base_de_datos)
    Conectar_Base_De_Datos.pack(fill="x",padx=15,pady=(15,0))

    ventana.bind("<Return>", lambda evento: iniciar_sesion())

    ventana.mainloop()
    return acceso_concedido
