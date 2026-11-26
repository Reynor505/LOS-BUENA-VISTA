import tkinter as tk
from tkinter import messagebox
from datetime import date
import pymysql
import Login2_0


def mostrar(contenedor):
    Login2_0.limpiar_contenedor(contenedor)
    Login2_0.crear_titulo(contenedor, "AÑADIR NUEVO PARTICIPANTE")

    ids_hogares, nombres_hogares = Login2_0.cargar_hogares()

    marco1 = Login2_0.crear_marco(contenedor)
    entrada_nombres = Login2_0.crear_campo(marco1, "NOMBRES", 0, 0)
    entrada_apellidos = Login2_0.crear_campo(marco1, "APELLIDOS", 0, 1)
    entrada_ci = Login2_0.crear_campo(marco1, "CARNET DE IDENTIDAD - CI", 1, 0)
    entrada_nacimiento = Login2_0.crear_campo_fecha(marco1, "FECHA DE NACIMIENTO", 1, 1)
    combo_sexo = Login2_0.crear_combo(marco1, "SEXO", 2, 0, ["M - Masculino", "F - Femenino"])

    marco2 = Login2_0.crear_seccion(contenedor, "ASIGNACION DE HOGAR")
    entrada_ingreso_sistema = Login2_0.crear_campo_fecha(marco2, "FECHA DE INGRESO-SISTEMA", 0, 0)
    entrada_ingreso_hogar = Login2_0.crear_campo_fecha(marco2, "FECHA DE INGRESO AL HOGAR", 0, 1)
    combo_hogar = Login2_0.crear_combo(marco2, "HOGAR ASIGNADO", 1, 0, nombres_hogares)

    marco3 = Login2_0.crear_seccion(contenedor, "SITUACION PREVIA")
    texto_situacion = tk.Text(marco3, height=5, font=("Arial", 12), relief="flat")
    texto_situacion.grid(row=0, column=0, columnspan=2, sticky="ew", padx=15, pady=10)

    def limpiar():
        entrada_nombres.delete(0, "end")
        entrada_apellidos.delete(0, "end")
        entrada_ci.delete(0, "end")
        Login2_0.reiniciar_fecha(entrada_nacimiento)
        Login2_0.reiniciar_fecha(entrada_ingreso_sistema)
        Login2_0.reiniciar_fecha(entrada_ingreso_hogar)
        combo_sexo.set("")
        combo_hogar.set("")
        texto_situacion.delete("1.0", "end")

    def registrar():
        nombre = entrada_nombres.get().strip()
        apellido = entrada_apellidos.get().strip()
        ci = entrada_ci.get().strip()
        sexo_texto = combo_sexo.get()
        posicion = combo_hogar.current()
        situacion = texto_situacion.get("1.0", "end").strip()

        if nombre == "" or apellido == "" or ci == "" or sexo_texto == "" or posicion == -1 or situacion == "":
            messagebox.showwarning("Datos incompletos", "Completa todos los campos antes de registrar.")
            return

        if len(nombre) > 40 or len(apellido) > 40:
            messagebox.showwarning("Datos incorrectos", "Nombres y apellidos: máximo 40 caracteres.")
            return
        if len(ci) > 10:
            messagebox.showwarning("Datos incorrectos", "El CI puede tener máximo 10 caracteres.")
            return
        if len(situacion) > 350:
            messagebox.showwarning("Datos incorrectos", "La situación previa puede tener máximo 350 caracteres.")
            return

        fecha_nacimiento = Login2_0.validar_fecha(entrada_nacimiento.get())
        fecha_ingreso = Login2_0.validar_fecha(entrada_ingreso_sistema.get())
        fecha_inicio_hogar = Login2_0.validar_fecha(entrada_ingreso_hogar.get())
        if fecha_nacimiento is None or fecha_ingreso is None or fecha_inicio_hogar is None:
            messagebox.showwarning("Fecha incorrecta", "Escribe las fechas con el formato AAAA-MM-DD.")
            return
        if fecha_nacimiento > date.today():
            messagebox.showwarning("Fecha incorrecta", "La fecha de nacimiento no puede ser futura.")
            return
        if fecha_ingreso < fecha_nacimiento:
            messagebox.showwarning("Fecha incorrecta", "La fecha de ingreso no puede ser anterior al nacimiento.")
            return

        sexo = sexo_texto[0]
        id_hogar = ids_hogares[posicion]

        try:
            con = Login2_0.conectar()
        except pymysql.MySQLError as error:
            messagebox.showerror("Base de datos", f"No se pudo conectar:\n{error}")
            return

        try:
            cursor = con.cursor()

            cursor.execute("SELECT capacidad FROM hogar WHERE id_hogar = %s", (id_hogar,))
            capacidad = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM asignacion_hogar WHERE id_hogar = %s AND fecha_fin IS NULL",
                           (id_hogar,))
            ocupados = cursor.fetchone()[0]
            if ocupados >= capacidad:
                messagebox.showwarning("Hogar lleno", f"Ese hogar ya tiene {ocupados} de {capacidad} cupos ocupados.")
                return

            cursor.execute("INSERT INTO participantes (nombre, apellido, fecha_de_nacimiento, ci, sexo, "
                           "fecha_de_ingreso, situacion_inicial) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (nombre, apellido, fecha_nacimiento, ci, sexo, fecha_ingreso, situacion))
            id_participante = cursor.lastrowid

            cursor.execute("INSERT INTO asignacion_hogar (id_participante, id_hogar, fecha_inicio) "
                           "VALUES (%s, %s, %s)", (id_participante, id_hogar, fecha_inicio_hogar))

            con.commit()
            messagebox.showinfo("Registro exitoso", f"Participante {nombre} {apellido} registrado.")
            limpiar()
        except pymysql.MySQLError as error:
            con.rollback()
            messagebox.showerror("Error al registrar", Login2_0.mensaje_error(error))
        finally:
            con.close()

    Login2_0.crear_botones(contenedor, limpiar, registrar)
