from tkinter import messagebox
import pymysql
import Conexion
import Componentes


def mostrar(contenedor):
    Componentes.limpiar_contenedor(contenedor)
    Componentes.crear_titulo(contenedor, "AÑADIR NUEVO HOGAR")

    marco = Componentes.crear_marco(contenedor)
    entrada_nombre = Componentes.crear_campo(marco, "NOMBRE DEL HOGAR", 0, 0)
    combo_dep = Componentes.crear_combo(marco, "DEPARTAMENTO", 0, 1, [])
    entrada_numero = Componentes.crear_campo(marco, "NUMERO", 1, 0)
    combo_ciudad = Componentes.crear_combo(marco, "CIUDAD", 1, 1, [])
    combo_zona = Componentes.crear_combo(marco, "ZONA", 2, 0, [])
    combo_calle = Componentes.crear_combo(marco, "CALLE", 2, 1, [])
    entrada_capacidad = Componentes.crear_campo(marco, "CAPACIDAD", 3, 0)
##esta cosa e para ese menu de seleccionar para que las direcciones tengas correlacion
    obtener_direccion, reiniciar_direccion = Componentes.conectar_direccion(combo_dep, combo_ciudad,
                                                                            combo_zona, combo_calle)

    def limpiar():
        entrada_nombre.delete(0, "end")
        entrada_numero.delete(0, "end")
        entrada_capacidad.delete(0, "end")
        reiniciar_direccion()

    def registrar():
        nombre = entrada_nombre.get().strip()
        numero_texto = entrada_numero.get().strip()
        capacidad_texto = entrada_capacidad.get().strip()
        direccion = obtener_direccion()
## validacionews para los campos de registros we xdxd
        if nombre == "" or numero_texto == "" or capacidad_texto == "" or direccion is None:
            messagebox.showwarning("Datos incompletos", "Completa todos los campos antes de registrar.")
            return
        if len(nombre) > 40:
            messagebox.showwarning("Datos incorrectos", "El nombre del hogar puede tener máximo 40 caracteres.")
            return

        if not numero_texto.isdigit() or int(numero_texto) <= 0:
            messagebox.showwarning("Datos incorrectos", "El número del hogar debe ser un entero mayor que 0.")
            return
        if not capacidad_texto.isdigit() or int(capacidad_texto) <= 0:
            messagebox.showwarning("Datos incorrectos", "La capacidad debe ser un entero mayor que 0.")
            return
        numero = int(numero_texto)
        capacidad = int(capacidad_texto)
        id_departamento, id_ciudad, id_zona, id_calle = direccion

        try:
            conex = Conexion.conectar()
        except pymysql.MySQLError as error:
            messagebox.showerror("Base de datos", f"No se pudo conectar:\n{error}")
            return

        try:
            cursor = conex.cursor()
            cursor.execute("INSERT INTO hogar (numero_hogar, nombre_hogar, id_departamento, id_ciudad, "
                           "id_zona, id_calle, capacidad) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (numero, nombre, id_departamento, id_ciudad, id_zona, id_calle, capacidad))
            conex.commit()
            messagebox.showinfo("Registro exitoso", f"Hogar {numero} - {nombre} registrado.")
            limpiar()
        except pymysql.MySQLError as error:
            conex.rollback()
            messagebox.showerror("Error al registrar", Conexion.mensaje_error(error))
        finally:
            conex.close()

    Componentes.crear_boton_registrar(contenedor, registrar)