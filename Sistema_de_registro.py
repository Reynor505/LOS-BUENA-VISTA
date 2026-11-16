import tkinter as tk 

import os
from PIL import Image, ImageTk

def ingresar():
    nombre = entry_usuario.get().strip()
    clave = entry_clave.get()

    if nombre == "" or clave == "":
        mostrar_error("Completa usuario y contraseña.")
        return

def mostrar_error(texto):
    lbl_error.config(text=texto)
    marco_error.pack(fill="x", 
                     pady=(10, 0),
                     before=btn_ingresar)


ventana = tk.Tk()
ventana.title("Aldeas Infantiles SOS Bolivia")
ventana.geometry("1100x700")
ventana.configure(bg="black")
ventana.resizable(False, False)

banda = tk.Frame(ventana, bg="#1FCDF9", height=205)
banda.place(x=0, y=253, relwidth=1)

ruta_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Aldeas SOS.png")

img_logo = Image.open(ruta_logo).convert("RGBA").resize((170, 170), Image.LANCZOS)
logo_tk = ImageTk.PhotoImage(img_logo)
lbl_logo = tk.Label(banda, image=logo_tk, bg="#00AEEF", bd=0)
lbl_logo.image = logo_tk
lbl_logo.place(x=50, y=17)
    

tk.Label(banda, text="ALDEAS\nINFANTILES SOS", 
         bg="#00AEEF", fg="white",
         font=("Arial", 24, "bold"), 
         justify="left").place(x=780, y=30)

tk.Label(banda, text="BOLIVIA", 
         bg="#00AEEF", 
         fg="#CFEFFB",
         font=("Arial", 24, "bold")).place(x=780, y=120)

panel = tk.Frame(ventana, 
                 bg="#CDEBF8", 
                 width=505, 
                 height=465)


panel.place(x=260, y=103)
panel.pack_propagate(False)

tk.Label(panel, text="Ingreso al sistema", 
         bg="#CDEBF8", 
         fg="#5087D4",
         font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=44, pady=(35, 15))

tarjeta = tk.Frame(panel, 
                   bg="white", 
                   padx=20, 
                   pady=20)

tarjeta.pack(padx=44, fill="x")

tk.Label(tarjeta, text="Usuario", bg="white", fg="#4B5563",
         font=("Segoe UI", 10)).pack(anchor="w")
entry_usuario = tk.Entry(tarjeta, font=("Segoe UI", 12), relief="solid", bd=1)
entry_usuario.pack(fill="x", ipady=8, pady=(4, 12))

tk.Label(tarjeta, text="Contraseña", bg="white", fg="#4B5563",
         font=("Segoe UI", 10)).pack(anchor="w")
entry_clave = tk.Entry(tarjeta, font=("Segoe UI", 12), relief="solid", bd=1, show="•")
entry_clave.pack(fill="x", ipady=8, pady=(4, 0))

# Mensaje de error (se muestra solo cuando hace falta)
marco_error = tk.Frame(tarjeta, bg="#FDE8E6")
lbl_error = tk.Label(marco_error, text="", bg="#FDE8E6", fg="#B42318",
                     font=("Segoe UI", 10), anchor="w", padx=10, pady=8)
lbl_error.pack(fill="x")

btn_ingresar = tk.Button(tarjeta, text="Ingresar", bg="#0B6BCB", fg="white",
                         font=("Segoe UI", 11), relief="flat", cursor="hand2",
                         activebackground="#095AAB", activeforeground="white",
                         command=ingresar)
btn_ingresar.pack(fill="x", ipady=8, pady=(15, 0))

tk.Label(tarjeta, text="Al llegar a 3 intentos fallidos la cuenta se bloquea 1 minuto.",
         bg="white", 
         fg="#374151", 
         font=("Segoe UI", 9),
         wraplength=380, 
         justify="left").pack(anchor="w", pady=(12, 0))

tk.Label(panel, text="Tablas: USUARIO (intentos_fallidos, bloqueo_hasta), REGISTRO_ACCESO",
         bg="#CDEBF8", 
         fg="#6B7280", 
         font=("Segoe UI", 8)).pack(anchor="w", padx=44, pady=(12, 0))

ventana.bind("<Return>", lambda e: ingresar())

ventana.mainloop()