import flet as ft
import estilos
import conexion_bd
from Vistas.admin import AdminVista
from Vistas.cliente import ClienteVista
from Vistas.login import LoginVista
from Vistas.compra import CompraVista
from types import SimpleNamespace


def main(page: ft.Page):  # Punto de entrada: configura la ventana y arranca en el login
    page.title = "Jupiter"
    page.padding = 0
    estilos.aplicar_tema(page)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def mostrar_login(e=None):  # Limpia la ventana y muestra la pantalla de login/registro
        page.clean()
        page.window.maximized = True
        page.end_drawer = None
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.add(*LoginVista(page, mostrar_cliente, mostrar_admin))
        page.update()

    def mostrar_cliente(usuario):  # Muestra la tienda para el cliente que inició sesión
        page.clean()
        page.title = "Panel de Cliente"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.window.maximized = True
        page.add(*ClienteVista(page, mostrar_login, mostrar_compra, usuario))
        page.update()

    def mostrar_compra(usuario):  # Muestra la pantalla para finalizar la compra del carrito
        page.clean()
        page.end_drawer = None
        page.title = "Finalizar compra"
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.window.maximized = True
        page.add(*CompraVista(page, mostrar_cliente, usuario))
        page.update()

    def mostrar_admin(usuario):  # Muestra el panel de administración
        page.clean()
        page.title = "Panel de Administrador"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.window.maximized = True
        page.add(*AdminVista(page, mostrar_login, usuario))
        page.update()


    mostrar_login()  # Primera pantalla que ve el usuario
    conexion_bd.creacion_bd()  # Crea las tablas y datos iniciales si no existen

ft.run(main)  # Inicia la aplicación Flet