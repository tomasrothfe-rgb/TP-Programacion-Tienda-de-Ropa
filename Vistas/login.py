import flet as ft
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clases import Usuario

def main(page: ft.Page):
    page.title = "Novus Prestige"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    login_correo = ft.TextField(label="Correo electrónico", width=300)
    login_contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)

    def ventana_de_alerta(texto_superior, erratas):

        def diseño_entradas(erratas):
                    return ft.Text(
                        erratas,
                    )

        return page.show_dialog(
                    ft.AlertDialog(
                            modal=True,
                            title=ft.Text(texto_superior),
                            content=ft.Column(
                                diseño_entradas(erratas)
                            ),
                            actions=[
                                    ft.Button("CONFIRMAR",on_click=lambda e: page.pop_dialog()),
                                    ft.Button("CANCELAR", on_click=lambda e: page.pop_dialog())
                                ],
                            actions_alignment=ft.MainAxisAlignment.END,))

    def ingresar_tienda(correo, contraseña):
        resultado = Usuario.iniciar_sesion(correo, contraseña)
        if resultado[0] != None:
            ventana_de_alerta(*resultado)
        else:
            print(resultado[1].nombre)

    btn_ingresar = ft.Button("Ingresar", on_click=lambda e: ingresar_tienda(login_correo.value, login_contrasena.value))

    reg_nombre = ft.TextField(label="Nombre", width=300)
    reg_apellido = ft.TextField(label="Apellido", width=300)
    reg_correo = ft.TextField(label="Correo electrónico", width=300)
    reg_contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)

    def registrar_usuario():
        resultado = Usuario.registrar(reg_nombre.value, reg_apellido.value, reg_correo.value, reg_contrasena.value)
        if resultado!= None:
            ventana_de_alerta(*resultado)
        else:
            ingresar_tienda(reg_correo.value,reg_contrasena.value)

    btn_registrar = ft.Button("Registrarse", on_click=lambda e: registrar_usuario())

    login_view = ft.Column(
        [
            login_correo,
            login_contrasena,
            btn_ingresar
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )

    register_view = ft.Column(
        [
            ft.Row(controls=[reg_nombre,
            reg_apellido]),
            reg_correo,
            reg_contrasena,
            btn_registrar
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )

    container_contenido = ft.Container(content=login_view)

    def cambiar_pestana(e):
        if e.control.data == 0:
            container_contenido.content = login_view
        else:
            container_contenido.content = register_view
        page.update()

    btn_login_tab = ft.TextButton("Iniciar Sesión", data=0, on_click=cambiar_pestana)
    btn_register_tab = ft.TextButton("Registrarse", data=1, on_click=cambiar_pestana)

    tabs_header = ft.Row([btn_login_tab, btn_register_tab], alignment=ft.MainAxisAlignment.CENTER)

    page.add(
        ft.Column(
            [
                tabs_header,
                container_contenido
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

ft.app(target=main)