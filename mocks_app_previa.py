import tkinter as tk 

ventana=tk.Tk()
ventana.title("Primer mock app")
ventana.geometry("1000x600")
ventana.config(bg="#0c1515")

GRIS_PANEL = "#555555"
GRIS_CLARO = "#C8D0DA"


separacion=tk.Frame(ventana,bg="#00ffff",width="200",height="50")

panel = tk.Frame(ventana, bg=GRIS_PANEL, width=464, height=430)
panel.place(relx=0.5, rely=0.5, anchor="center")
panel.pack_propagate(False)

tk.Label(panel, text="Inicio de Sesion", bg=GRIS_PANEL, fg=GRIS_CLARO,font=("Pacifico", 28, "bold")).pack(pady=(15, 35))

tk.Label(panel, text="Usuario", bg=GRIS_PANEL, fg=GRIS_CLARO, font=("Pacifico", 16, "bold"), anchor="w").pack(fill="x", padx=28)
entry_usuario = tk.Entry(panel, bg=GRIS_CLARO, fg="black", relief="flat",font=("Pacifico", 14), justify="center")
entry_usuario.pack(fill="x", padx=28, pady=(3, 20), ipady=18)

tk.Label(panel, text="Contraseña", bg=GRIS_PANEL, fg=GRIS_CLARO,font=("Pacifico", 16, "bold"), anchor="w").pack(fill="x", padx=28)

entry_clave = tk.Entry(panel, bg=GRIS_CLARO, fg="black", relief="flat",font=("Pacifico", 14), justify="center", show="*")

entry_clave.pack(fill="x", padx=28, pady=(3, 5), ipady=18)






separacion.pack(fill="y",side="left")


ventana.mainloop()