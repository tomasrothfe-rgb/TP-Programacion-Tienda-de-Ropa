import flet as ft

def main(page: ft.Page):
    page.title = "Novus Prestige"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    login_correo = ft.TextField(label="Correo electrónico", width=300)
    login_contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)

    def ingresar_tienda(e):
        pass

    btn_ingresar = ft.ElevatedButton("Ingresar", on_click=ingresar_tienda)

    reg_nombre = ft.TextField(label="Nombre completo", width=300)
    reg_correo = ft.TextField(label="Correo electrónico", width=300)
    reg_contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)

    def registrar_usuario(e):
        pass

    btn_registrar = ft.ElevatedButton("Registrarse", on_click=registrar_usuario)

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
            reg_nombre,
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