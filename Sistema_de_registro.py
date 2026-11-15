import tkinter as tk 

import mysql as sqkl

ventana=tk.Tk()

ventana.title("Registro")
ventana.geometry("800x600")
ventana.config(bg="#6eeafd")

login=tk.Frame(ventana,bg="#3A9CFD",height="400",width="400")
login.pack(anchor="s")



ventana.mainloop()