import flet as ft
import estilos
from Vistas.admin import AdminVista
from Vistas.cliente import ClienteVista
from Vistas.login import LoginVista
from Vistas.compra import CompraVista
from types import SimpleNamespace


def main(page: ft.Page):
    page.title = "Jupiter"
    page.padding = 0
    estilos.aplicar_tema(page)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def mostrar_login(e=None):
        page.clean()
        page.window.maximized = True
        page.end_drawer = None
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.add(*LoginVista(page, mostrar_cliente, mostrar_admin))
        page.update()

    def mostrar_cliente(usuario):
        page.clean()
        page.title = "Panel de Cliente"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.window.maximized = True
        page.add(*ClienteVista(page, mostrar_login, mostrar_compra, usuario))
        page.update()

    def mostrar_compra(usuario):
        page.clean()
        page.end_drawer = None
        page.title = "Finalizar compra"
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.window.maximized = True
        page.add(*CompraVista(page, mostrar_cliente, usuario))
        page.update()

    def mostrar_admin(usuario):
        page.clean()
        page.title = "Panel de Administrador"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.window.maximized = True
        page.add(*AdminVista(page, mostrar_login, usuario))
        page.update()


    mostrar_login()


ft.run(main)