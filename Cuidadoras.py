from tkinter import messagebox
from datetime import date
import pymysql
import Conexion
import Componentes


def mostrar(contenedor):
    Componentes.limpiar_contenedor(contenedor)
    Componentes.crear_titulo(contenedor, "AÑADIR NUEVA CUIDADORA")

    ids_hogares, nombres_hogares = Componentes.cargar_hogares()

    marco1 = Componentes.crear_marco(contenedor)
    entrada_nombres = Componentes.crear_campo(marco1, "NOMBRES", 0, 0)
    entrada_apellidos = Componentes.crear_campo(marco1, "APELLIDOS", 0, 1)
    entrada_ci = Componentes.crear_campo(marco1, "CARNET DE IDENTIDAD - CI", 1, 0)
    entrada_nacimiento = Componentes.crear_campo_fecha(marco1, "FECHA DE NACIMIENTO", 1, 1)

    marco2 = Componentes.crear_seccion(contenedor, "CONTACTO Y DOMICILIO")
    entrada_telefono = Componentes.crear_campo(marco2, "TELEFONO", 0, 0)
    combo_dep = Componentes.crear_combo(marco2, "DEPARTAMENTO", 0, 1, [])
    combo_ciudad = Componentes.crear_combo(marco2, "CIUDAD", 1, 0, [])
    combo_zona = Componentes.crear_combo(marco2, "ZONA", 1, 1, [])
    combo_calle = Componentes.crear_combo(marco2, "CALLE", 2, 0, [])

    obtener_direccion, reiniciar_direccion = Componentes.conectar_direccion(combo_dep, combo_ciudad,
                                                                            combo_zona, combo_calle)

    marco3 = Componentes.crear_seccion(contenedor, "ASIGNACION DE HOGAR")
    entrada_ingreso_hogar = Componentes.crear_campo_fecha(marco3, "FECHA DE INGRESO AL HOGAR", 0, 0)
    combo_hogar = Componentes.crear_combo(marco3, "HOGAR ASIGNADO", 0, 1, nombres_hogares)

    def limpiar():
        entrada_nombres.delete(0, "end")
        entrada_apellidos.delete(0, "end")
        entrada_ci.delete(0, "end")
        Componentes.reiniciar_fecha(entrada_nacimiento)
        entrada_telefono.delete(0, "end")
        reiniciar_direccion()
        Componentes.reiniciar_fecha(entrada_ingreso_hogar)
        combo_hogar.set("")

    def registrar():
        nombres = entrada_nombres.get().strip()
        apellidos = entrada_apellidos.get().strip()
        ci = entrada_ci.get().strip()
        telefono = entrada_telefono.get().strip()
        direccion = obtener_direccion()
        posicion = combo_hogar.current()

        if nombres == "" or apellidos == "" or ci == "" or telefono == "" or direccion is None or posicion == -1:
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

        for letra in telefono:
            if not (letra.isdigit() or letra in "+- "):
                messagebox.showwarning("Datos incorrectos", "El teléfono solo puede tener números, espacios, + y -.")
                return

        fecha_nacimiento = Componentes.validar_fecha(entrada_nacimiento.get())
        fecha_ingreso = Componentes.validar_fecha(entrada_ingreso_hogar.get())
        if fecha_nacimiento is None or fecha_ingreso is None:
            messagebox.showwarning("Fecha incorrecta", "Escribe las fechas con el formato AAAA-MM-DD.")
            return
        if fecha_nacimiento > date.today():
            messagebox.showwarning("Fecha incorrecta", "La fecha de nacimiento no puede ser futura.")
            return
        if fecha_ingreso < fecha_nacimiento:
            messagebox.showwarning("Fecha incorrecta", "El ingreso al hogar no puede ser anterior al nacimiento.")
            return

        id_hogar = ids_hogares[posicion]
        id_departamento, id_ciudad, id_zona, id_calle = direccion

        try:
            conex = Conexion.conectar()
        except pymysql.MySQLError as error:
            messagebox.showerror("Base de datos", f"No se pudo conectar:\n{error}")
            return

        try:
            cursor = conex.cursor()
            cursor.execute("SELECT COUNT(*) FROM cuidadora WHERE id_hogar = %s AND estado = 'activo'", (id_hogar,))
            cantidad = cursor.fetchone()[0]
            if cantidad >= Componentes.MAX_CUIDADORAS:
                messagebox.showwarning("Hogar completo",
                                       f"Ese hogar ya tiene {cantidad} de {Componentes.MAX_CUIDADORAS} cuidadoras.")
                return

            cursor.execute("INSERT INTO cuidadora (id_hogar, nombres, apellidos, ci, telefono, fecha_nacimiento, "
                           "fecha_ingreso, id_departamento, id_ciudad, id_zona, id_calle) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (id_hogar, nombres, apellidos, ci, telefono, fecha_nacimiento, fecha_ingreso,
                            id_departamento, id_ciudad, id_zona, id_calle))
            conex.commit()
            messagebox.showinfo("Registro exitoso", f"Cuidadora {nombres} {apellidos} registrada.")
            limpiar()
        except pymysql.MySQLError as error:
            conex.rollback()
            messagebox.showerror("Error al registrar", Conexion.mensaje_error(error))
        finally:
            conex.close()

    Componentes.crear_boton_registrar(contenedor, registrar)
