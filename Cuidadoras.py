from tkinter import messagebox
from datetime import date
import pymysql
import Login2_0


def mostrar(contenedor):
    Login2_0.limpiar_contenedor(contenedor)
    Login2_0.crear_titulo(contenedor, "AÑADIR NUEVA CUIDADORA")

    ids_hogares, nombres_hogares = Login2_0.cargar_hogares()

    marco1 = Login2_0.crear_marco(contenedor)
    entrada_nombres = Login2_0.crear_campo(marco1, "NOMBRES", 0, 0)
    entrada_apellidos = Login2_0.crear_campo(marco1, "APELLIDOS", 0, 1)
    entrada_ci = Login2_0.crear_campo(marco1, "CARNET DE IDENTIDAD - CI", 1, 0)
    entrada_nacimiento = Login2_0.crear_campo_fecha(marco1, "FECHA DE NACIMIENTO", 1, 1)

    marco2 = Login2_0.crear_seccion(contenedor, "CONTACTO Y DOMICILIO")
    entrada_telefono = Login2_0.crear_campo(marco2, "TELEFONO", 0, 0)
    entrada_direccion = Login2_0.crear_campo(marco2, "DIRECCION", 0, 1)

    marco3 = Login2_0.crear_seccion(contenedor, "ASIGNACION DE HOGAR")
    entrada_ingreso_hogar = Login2_0.crear_campo_fecha(marco3, "FECHA DE INGRESO AL HOGAR", 0, 0)
    combo_hogar = Login2_0.crear_combo(marco3, "HOGAR ASIGNADO", 0, 1, nombres_hogares)

    def limpiar():
        entrada_nombres.delete(0, "end")
        entrada_apellidos.delete(0, "end")
        entrada_ci.delete(0, "end")
        Login2_0.reiniciar_fecha(entrada_nacimiento)
        entrada_telefono.delete(0, "end")
        entrada_direccion.delete(0, "end")
        Login2_0.reiniciar_fecha(entrada_ingreso_hogar)
        combo_hogar.set("")

    def registrar():
        nombres = entrada_nombres.get().strip()
        apellidos = entrada_apellidos.get().strip()
        ci = entrada_ci.get().strip()
        telefono = entrada_telefono.get().strip()
        direccion = entrada_direccion.get().strip()
        posicion = combo_hogar.current()

        if nombres == "" or apellidos == "" or ci == "" or telefono == "" or direccion == "" or posicion == -1:
            messagebox.showwarning("Datos incompletos", "Completa todos los campos antes de registrar.")
            return

        if len(nombres) > 40 or len(apellidos) > 40:
            messagebox.showwarning("Datos incorrectos", "Nombres y apellidos: máximo 40 caracteres.")
            return
        if len(ci) > 10:
            messagebox.showwarning("Datos incorrectos", "El CI puede tener máximo 10 caracteres.")
            return
        if len(telefono) > 20:
            messagebox.showwarning("Datos incorrectos", "El teléfono puede tener máximo 20 caracteres.")
            return
        if len(direccion) > 75:
            messagebox.showwarning("Datos incorrectos", "La dirección puede tener máximo 75 caracteres.")
            return

        for letra in telefono:
            if not (letra.isdigit() or letra in "+- "):
                messagebox.showwarning("Datos incorrectos", "El teléfono solo puede tener números, espacios, + y -.")
                return

        fecha_nacimiento = Login2_0.validar_fecha(entrada_nacimiento.get())
        fecha_ingreso_hogar = Login2_0.validar_fecha(entrada_ingreso_hogar.get())
        if fecha_nacimiento is None or fecha_ingreso_hogar is None:
            messagebox.showwarning("Fecha incorrecta", "Escribe las fechas con el formato AAAA-MM-DD.")
            return
        if fecha_nacimiento > date.today():
            messagebox.showwarning("Fecha incorrecta", "La fecha de nacimiento no puede ser futura.")
            return
        if fecha_ingreso_hogar < fecha_nacimiento:
            messagebox.showwarning("Fecha incorrecta", "El ingreso al hogar no puede ser anterior al nacimiento.")
            return

        id_hogar = ids_hogares[posicion]

        try:
            con = Login2_0.conectar()
        except pymysql.MySQLError as error:
            messagebox.showerror("Base de datos", f"No se pudo conectar:\n{error}")
            return

        try:
            cursor = con.cursor()
            cursor.execute("INSERT INTO cuidadora (id_hogar, nombres, apellidos, ci, telefono, direccion, "
                           "fecha_de_nacimiento, fecha_ingreso_hogar) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (id_hogar, nombres, apellidos, ci, telefono, direccion,
                            fecha_nacimiento, fecha_ingreso_hogar))
            con.commit()
            messagebox.showinfo("Registro exitoso", f"Cuidadora {nombres} {apellidos} registrada.")
            limpiar()
        except pymysql.MySQLError as error:
            con.rollback()
            messagebox.showerror("Error al registrar", Login2_0.mensaje_error(error))
        finally:
            con.close()

    Login2_0.crear_botones(contenedor, limpiar, registrar)
