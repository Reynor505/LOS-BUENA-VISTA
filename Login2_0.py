import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime,timedelta
import hashlib
import pymysql
import Conexion                          

acceso_concedido=False
usuario_actual=None
rol_actual=None

def validar_usuario(nombre_usuario,contra):
    global usuario_actual, rol_actual
    try:
        conex=Conexion.conectar()
    except pymysql.MySQLError as error:
        return False,f"LA CONEXION CON LA BASE DE DATOS FALLO \n {error}"
    try:
        cursor=conex.cursor()
        cursor.execute("SELECT u.id_usuario, u.contrasena_hash, u.intentos_fallidos, u.bloqueo_hasta, u.estado, "
                       "r.nombre, u.nombre, u.apellido "
                       "FROM usuario u JOIN rol r ON r.id_rol = u.id_rol "
                       "WHERE u.nombre_usuario = %s",(nombre_usuario,))
        fila=cursor.fetchone()

        if fila is None:
            return False, "Usuario o Contraseña Incorrectos"
        
        id_usuario,has_guardado,intentos,bloqueo_hasta,estado,nombre_rol,nombre_persona,apellido_persona=fila
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
            usuario_actual = f"{nombre_persona} {apellido_persona}".strip() or nombre_usuario
            rol_actual = nombre_rol
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

def abrir_config_db(padre):
    modal = tk.Toplevel(padre)
    modal.title("Configuración de Base de Datos")
    modal.config(bg="#F1F5F9")
    modal.resizable(False, False)
    modal.transient(padre)
    modal.grab_set()

    modal.update_idletasks()
    x = max(0, padre.winfo_rootx() + (padre.winfo_width() - 440) // 2)
    y = max(0, padre.winfo_rooty() + (padre.winfo_height() - 470) // 2)
    modal.geometry(f"440x470+{x}+{y}")

    tk.Label(modal, text="CONFIGURACIÓN DE BASE DE DATOS", font=("Segoe UI", 14, "bold"),
             bg="#1F2B3A", fg="White", pady=14).pack(fill="x")

    cuerpo = tk.Frame(modal, bg="#F1F5F9")
    cuerpo.pack(fill="both", expand=True, padx=24, pady=16)

    cfg = Conexion.obtener_configuracion()
    campos = {}
    definiciones = [
        ("host", "SERVIDOR (HOST)", cfg["host"], False),
        ("puerto", "PUERTO", str(cfg["puerto"]), False),
        ("usuario", "USUARIO", cfg["usuario"], False),
        ("contra", "CONTRASEÑA", cfg["contra"], True),
        ("base_de_datos", "BASE DE DATOS", cfg["base_de_datos"], False),
    ]

    for clave, etiqueta, valor, ocultar in definiciones:
        tk.Label(cuerpo, text=etiqueta, font=("Segoe UI", 9, "bold"),
                 bg="#F1F5F9", fg="#1E293B").pack(anchor="w", pady=(6, 2))
        entrada = tk.Entry(cuerpo, font=("Segoe UI", 11), relief="flat", bg="#FFFFFF", fg="#1E293B",
                           highlightthickness=1, highlightbackground="#CBD5E1", highlightcolor="#004AAD",
                           show="*" if ocultar else "")
        entrada.insert(0, valor)
        entrada.pack(fill="x", ipady=5)
        campos[clave] = entrada

    def leer_campos():
        host = campos["host"].get().strip()
        puerto_txt = campos["puerto"].get().strip()
        usuario = campos["usuario"].get().strip()
        contra = campos["contra"].get()
        bd = campos["base_de_datos"].get().strip()

        if not host or not puerto_txt or not usuario or not bd:
            messagebox.showwarning("Datos incompletos", "Completa servidor, puerto, usuario y base de datos.", parent=modal)
            return None
        if not puerto_txt.isdigit() or int(puerto_txt) <= 0:
            messagebox.showwarning("Puerto inválido", "El puerto debe ser un número entero positivo.", parent=modal)
            return None
        return host, int(puerto_txt), usuario, contra, bd

    def probar():
        datos = leer_campos()
        if datos is None:
            return
        ok, msg = Conexion.comprobar_conexion_datos(*datos)
        if ok:
            messagebox.showinfo("CONEXIÓN DE DATOS", msg, parent=modal)
        else:
            messagebox.showerror("CONEXIÓN DE DATOS", msg, parent=modal)

    def guardar():
        datos = leer_campos()
        if datos is None:
            return
        try:
            Conexion.guardar_configuracion(*datos)
            messagebox.showinfo("Configuración guardada", "Los datos de conexión se actualizaron correctamente.", parent=modal)
            modal.destroy()
        except OSError as error:
            messagebox.showerror("Error al guardar", f"No se pudo guardar la configuración:\n{error}", parent=modal)

    botones = tk.Frame(modal, bg="#F1F5F9")
    botones.pack(fill="x", padx=24, pady=(0, 18))

    tk.Button(botones, text="PROBAR CONEXIÓN", font=("Segoe UI", 10, "bold"), bg="#1F2B3A", fg="White",
              activebackground="#0F172A", activeforeground="White", relief="flat",
              cursor="hand2", padx=14, pady=8, command=probar).pack(side="left")

    tk.Button(botones, text="GUARDAR", font=("Segoe UI", 10, "bold"), bg="#004AAD", fg="White",
              activebackground="#003A8A", activeforeground="White", relief="flat",
              cursor="hand2", padx=20, pady=8, command=guardar).pack(side="right")


def abrir_login():
    global acceso_concedido, usuario_actual, rol_actual
    acceso_concedido=False
    usuario_actual=None
    rol_actual=None

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
    ventana.title("Inicio de Sesión - Aldeas SOS")
    ventana.minsize(950, 620)
    ventana.update_idletasks()
    x = max(0, (ventana.winfo_screenwidth() - 1150) // 2)
    y = max(0, (ventana.winfo_screenheight() - 740) // 2)
    ventana.geometry(f"1150x740+{x}+{y}")
    ventana.config(bg="#F1F5F9")

    Panel_superior=tk.Frame(ventana,bg="#009FE3",height=170)
    Panel_superior.pack_propagate(False)
    Panel_superior.pack(fill="x")

    panel_inferior=tk.Frame(ventana,bg="#009FE3",height=55)
    panel_inferior.pack_propagate(False)
    panel_inferior.pack(side="bottom",fill="x")

    panel_derecho=tk.Frame(ventana,bg="#D6EBFF",width=460,
                           highlightbackground="#A5D3FB",highlightthickness=1)
    panel_derecho.pack_propagate(False)
    panel_derecho.pack(side="right",fill="y",padx=25,pady=25)

    panel_izquierdo=tk.Frame(ventana,bg="#F1F5F9")
    panel_izquierdo.pack_propagate(False)
    panel_izquierdo.pack(side="left",expand=True,fill="both",padx=(35,10),pady=25)

    #Panel Superior

    Abrir_logo_Aldeas_sos=Image.open("LOGO_ALDEAS_SOS.jpg")
    filtro = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
    Logo_Aldeas_Redimensionada=Abrir_logo_Aldeas_sos.resize((765,170), filtro)

    Logo_Aldeas=ImageTk.PhotoImage(Logo_Aldeas_Redimensionada)

    lbl_logo = tk.Label(Panel_superior,image=Logo_Aldeas,bd=0,highlightthickness=0,bg="#009FE3")
    lbl_logo.image = Logo_Aldeas
    lbl_logo.pack(side="left")

    #Panel Izquierdo (Bienvenida)
    bienvenida = tk.Frame(panel_izquierdo, bg="#F1F5F9")
    bienvenida.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(bienvenida, text="SISTEMA DE GESTIÓN\nDE HOGARES", font=("Segoe UI", 28, "bold"),
             bg="#F1F5F9", fg="#1F2B3A", justify="center").pack(pady=(0, 12))
    tk.Frame(bienvenida, bg="#009FE3", width=120, height=4).pack(pady=(0, 14))
    tk.Label(bienvenida, text="Aldeas Infantiles SOS\nRegistro de Participantes, Cuidadoras y Hogares",
             font=("Segoe UI", 13), bg="#F1F5F9", fg="#475569", justify="center").pack()

    #Panel_Derecho(Inicio de Sesion)
    tk.Label(panel_derecho, text="INICIO DE SESIÓN",font=("Segoe UI",22,"bold"),
            bg="#D6EBFF",fg="#1F2B3A").pack(padx=28,anchor="nw",pady=(28,20))

    tk.Label(panel_derecho,text="USUARIO",font=("Segoe UI",12,"bold"),
            bg="#D6EBFF",fg="#1E293B").pack(padx=28,anchor="nw",pady=(0,4))

    Usuario_Entry=tk.Entry(panel_derecho,bg="#FFFFFF",fg="#1E293B",relief="flat",
                           highlightthickness=1,highlightbackground="#94A3B8",highlightcolor="#004AAD",
                           font=("Segoe UI",14))
    Usuario_Entry.pack(padx=28,fill="x",ipady=8,pady=(0,16))
    Usuario_Entry.focus_set()

    tk.Label(panel_derecho,text="CONTRASEÑA",font=("Segoe UI",12,"bold"),
            bg="#D6EBFF",fg="#1E293B").pack(padx=28,anchor="nw",pady=(0,4))

    Contra_Entry=tk.Entry(panel_derecho,bg="#FFFFFF",fg="#1E293B",relief="flat",
                          highlightthickness=1,highlightbackground="#94A3B8",highlightcolor="#004AAD",
                          font=("Segoe UI",14),show="*")
    Contra_Entry.pack(padx=28,ipady=8,fill="x",pady=(0,10))

    mostrar_contra=tk.BooleanVar(value=False)
    tk.Checkbutton(panel_derecho,variable=mostrar_contra,text="Mostrar contraseña",font=("Segoe UI",11,"bold"),
                   bg="#D6EBFF",fg="#1E293B",activebackground="#D6EBFF",selectcolor="#FFFFFF",
                   cursor="hand2",command=mostrar_contra_entry).pack(anchor="nw",padx=25,pady=(0,18))

    Iniciar_Sesion=tk.Button(panel_derecho,text="INICIAR SESIÓN",font=("Segoe UI",13,"bold"),bg="#004AAD",
                             fg="White",activebackground="#003A8A",activeforeground="White",
                             relief="flat",cursor="hand2",pady=10,command=iniciar_sesion)
    Iniciar_Sesion.pack(fill="x",padx=28,pady=(6,0))

    Conectar_Base_De_Datos=tk.Button(panel_derecho,text="CONFIGURAR BASE DE DATOS",font=("Segoe UI",11,"bold"),bg="#1F2B3A",
                                     fg="White",activebackground="#0F172A",activeforeground="White",
                                     relief="flat",cursor="hand2",pady=9,command=lambda: abrir_config_db(ventana))
    Conectar_Base_De_Datos.pack(fill="x",padx=28,pady=(12,0))

    ventana.bind("<Return>",lambda evento: iniciar_sesion())

    ventana.mainloop()
    return acceso_concedido 