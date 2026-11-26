from tkinter import messagebox
import pymysql
import Login2_0


def mostrar(contenedor):
    Login2_0.limpiar_contenedor(contenedor)
    Login2_0.crear_titulo(contenedor, "AÑADIR NUEVO HOGAR")

    marco = Login2_0.crear_marco(contenedor)
    entrada_nombre = Login2_0.crear_campo(marco, "NOMBRE DEL HOGAR", 0, 0)
    entrada_ubicacion = Login2_0.crear_campo(marco, "UBICACION", 0, 1)
    entrada_numero = Login2_0.crear_campo(marco, "NUMERO", 1, 0)
    entrada_capacidad = Login2_0.crear_campo(marco, "CAPACIDAD", 1, 1)

    def limpiar():
        entrada_nombre.delete(0, "end")
        entrada_ubicacion.delete(0, "end")
        entrada_numero.delete(0, "end")
        entrada_capacidad.delete(0, "end")

    def registrar():
        nombre = entrada_nombre.get().strip()
        ubicacion = entrada_ubicacion.get().strip()
        numero_texto = entrada_numero.get().strip()
        capacidad_texto = entrada_capacidad.get().strip()

        if nombre == "" or ubicacion == "" or numero_texto == "" or capacidad_texto == "":
            messagebox.showwarning("Datos incompletos", "Completa todos los campos antes de registrar.")
            return
        if len(nombre) > 40:
            messagebox.showwarning("Datos incorrectos", "El nombre del hogar puede tener máximo 40 caracteres.")
            return
        if len(ubicacion) > 50:
            messagebox.showwarning("Datos incorrectos", "La ubicación puede tener máximo 50 caracteres.")
            return

        if not numero_texto.isdigit() or int(numero_texto) <= 0:
            messagebox.showwarning("Datos incorrectos", "El número del hogar debe ser un entero mayor que 0.")
            return
        if not capacidad_texto.isdigit() or int(capacidad_texto) <= 0:
            messagebox.showwarning("Datos incorrectos", "La capacidad debe ser un entero mayor que 0.")
            return
        numero = int(numero_texto)
        capacidad = int(capacidad_texto)

        try:
            con = Login2_0.conectar()
        except pymysql.MySQLError as error:
            messagebox.showerror("Base de datos", f"No se pudo conectar:\n{error}")
            return

        try:
            cursor = con.cursor()
            cursor.execute("INSERT INTO hogar (numero_hogar, nombre_hogar, direccion, capacidad) "
                           "VALUES (%s, %s, %s, %s)", (numero, nombre, ubicacion, capacidad))
            con.commit()
            messagebox.showinfo("Registro exitoso", f"Hogar {numero} - {nombre} registrado.")
            limpiar()
        except pymysql.MySQLError as error:
            con.rollback()
            messagebox.showerror("Error al registrar", Login2_0.mensaje_error(error))
        finally:
            con.close()

    Login2_0.crear_botones(contenedor, limpiar, registrar)
