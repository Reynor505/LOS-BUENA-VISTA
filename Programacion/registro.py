import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

import pymysql

conexion_datos = dict(host="localhost", port=3306, user="root", password="112367", database="aldeas_sos")

AZUL = "#d9d9d9"
GRIS = "#1f2937"


def obtener_hogares():
    try:
        con = pymysql.connect(**conexion_datos)
        cursor = con.cursor()
        cursor.execute("SELECT id_hogar, numero_hogar, nombre_hogar FROM hogar "
                       "WHERE estado = 'activo' ORDER BY numero_hogar")
        lista = cursor.fetchall()
        con.close()
        return list(lista)
    except pymysql.MySQLError:
        return []


def guardar():
    nombres = entry_nombres.get().strip()
    apellidos = entry_apellidos.get().strip()
    nacimiento = entry_nacimiento.get().strip()
    sexo = combo_sexo.get()
    ingreso = entry_ingreso.get().strip()
    inicio = entry_inicio.get().strip()
    situacion = texto_situacion.get("1.0", tk.END).strip()
    pos_hogar = combo_hogar.current()

    if nombres == "" or apellidos == "" or nacimiento == "" or ingreso == "" or inicio == "" or situacion == "":
        messagebox.showwarning("Falta información", "Completa todos los campos.")
        return
    if sexo == "":
        messagebox.showwarning("Falta información", "Elige el sexo.")
        return
    if pos_hogar == -1:
        messagebox.showwarning("Falta información", "Elige el hogar.")
        return
    
    try:
        f_nacimiento = datetime.strptime(nacimiento, "%Y-%m-%d")
        f_ingreso = datetime.strptime(ingreso, "%Y-%m-%d")
        f_inicio = datetime.strptime(inicio, "%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("Fecha incorrecta", "Usa el formato AAAA-MM-DD (ejemplo: 2012-05-30).")
        return


    hoy = datetime.now()

    if f_nacimiento > hoy:
        messagebox.showwarning("Fecha incorrecta", "La fecha de nacimiento no puede ser futura.")
        return

    edad = hoy.year - f_nacimiento.year
    if (hoy.month, hoy.day) < (f_nacimiento.month, f_nacimiento.day):
        edad = edad - 1

    if edad >= 18:
        messagebox.showwarning(f"Edad incorrecta", "\nSolo se pueden registrar menores de 18 años.")
        return

    if f_ingreso < f_nacimiento:
        messagebox.showwarning("Fecha incorrecta", "\nLa fecha de ingreso no puede ser anterior al nacimiento.")
        return

    if f_inicio < f_ingreso:
        messagebox.showwarning("Fecha incorrecta", "\nLa fecha de inicio no puede ser anterior a la fecha de ingreso.")
        return

    id_hogar = hogares[pos_hogar][0]

    try:
        con = pymysql.connect(**conexion_datos)
        cursor = con.cursor()

        cursor.execute("INSERT INTO participantes "
                       "(nombre, apellido, fecha_de_nacimiento, sexo, fecha_de_ingreso, situacion_inicial) "
                       "VALUES (%s, %s, %s, %s, %s, %s)",
                       (nombres, apellidos, nacimiento, sexo, ingreso, situacion))
        id_participante = cursor.lastrowid

        cursor.execute("INSERT INTO asignacion_hogar (id_participante, id_hogar, fecha_inicio) "
                       "VALUES (%s, %s, %s)",
                       (id_participante, id_hogar, inicio))

        con.commit()
        con.close()
    except pymysql.MySQLError as error:
        messagebox.showerror("Error", f"No se pudo guardar:\n{error}")
        return

    messagebox.showinfo("Guardado", "Participante registrado correctamente.")

    entry_nombres.delete(0, tk.END)
    entry_apellidos.delete(0, tk.END)
    entry_nacimiento.delete(0, tk.END)
    combo_sexo.set("")
    entry_ingreso.delete(0, tk.END)
    combo_hogar.set("")
    entry_inicio.delete(0, tk.END)
    texto_situacion.delete("1.0", tk.END)


def abrir_registro():
    global entry_nombres, entry_apellidos, entry_nacimiento, combo_sexo
    global entry_ingreso, combo_hogar, entry_inicio, texto_situacion, hogares

    ventana = tk.Tk()
    ventana.title("Nuevo participante - Aldeas Infantiles SOS")
    ventana.geometry("1100x700")
    ventana.configure(bg=AZUL)
    ventana.resizable(False, False)

    fuente = ("Arial", 13, "bold")

    lateral = tk.Frame(ventana, bg=GRIS)
    lateral.place(x=0, y=0, width=302, height=700)

    tk.Label(ventana, text="NUEVO PARTICIPANTE", bg=AZUL, fg="white",
             font=("Arial", 14, "bold")).place(x=319, y=8)
    tk.Label(ventana, text="DATOS DEL PARTICIPANTE", bg=AZUL, fg="white",
             font=("Arial", 14, "bold")).place(x=321, y=50)

    tk.Label(ventana, text="NOMBRES", bg=AZUL, fg="white", font=fuente).place(x=319, y=120)
    entry_nombres = tk.Entry(ventana, font=("Segoe UI", 12), bd=0)
    entry_nombres.place(x=311, y=162, width=329, height=47)

    tk.Label(ventana, text="APELLIDOS", bg=AZUL, fg="white", font=fuente).place(x=708, y=120)
    entry_apellidos = tk.Entry(ventana, font=("Segoe UI", 12), bd=0)
    entry_apellidos.place(x=708, y=162, width=354, height=47)

    tk.Label(ventana, text="FECHA DE NACIMIENTO", bg=AZUL, fg="white", font=fuente).place(x=317, y=246)
    entry_nacimiento = tk.Entry(ventana, font=("Segoe UI", 12), bd=0)
    entry_nacimiento.place(x=311, y=290, width=253, height=47)

    tk.Label(ventana, text="SEXO", bg=AZUL, fg="white", font=fuente).place(x=614, y=246)
    combo_sexo = ttk.Combobox(ventana, values=["M", "F"], state="readonly", font=("Segoe UI", 12))
    combo_sexo.place(x=614, y=290, width=186, height=47)

    tk.Label(ventana, text="FECHA INGRESO", bg=AZUL, fg="white", font=fuente).place(x=847, y=246)
    entry_ingreso = tk.Entry(ventana, font=("Segoe UI", 12), bd=0)
    entry_ingreso.place(x=847, y=290, width=216, height=47)

    tk.Label(ventana, text="ASIGNACION HOGAR", bg=AZUL, fg="white", font=fuente).place(x=310, y=358)
    hogares = obtener_hogares()
    nombres_hogares = []
    for h in hogares:
        nombres_hogares.append(f"Hogar {h[1]} - {h[2]}")
    combo_hogar = ttk.Combobox(ventana, values=nombres_hogares, state="readonly", font=("Segoe UI", 12))
    combo_hogar.place(x=311, y=392, width=256, height=47)

    tk.Label(ventana, text="FECHA INICIO", bg=AZUL, fg="white", font=fuente).place(x=847, y=358)
    entry_inicio = tk.Entry(ventana, font=("Segoe UI", 12), bd=0)
    entry_inicio.place(x=847, y=392, width=216, height=47)

    tk.Label(ventana, text="Fechas: AAAA-MM-DD", bg=AZUL, fg="#CFE0FF",
             font=("Segoe UI", 9)).place(x=614, y=400)

    tk.Label(ventana, text="SITUACION INICIAL", bg=AZUL, fg="white", font=fuente).place(x=318, y=462)
    texto_situacion = tk.Text(ventana, font=("Segoe UI", 12), bd=0, wrap="word")
    texto_situacion.place(x=319, y=496, width=766, height=107)

    tk.Button(ventana, text="Guardar", bg="white", fg=AZUL,
              font=("Arial", 12, "bold"), relief="flat", cursor="hand2",
              command=guardar).place(x=965, y=625, width=120, height=40)

    

    ventana.mainloop()