import flet as ft

def main(page: ft.Page):
    page.title = "Prueba de Vistas Independientes"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#b6b6b4"

    # 1. Instancias separadas para el Login
    email_login = ft.TextField(hint_text="Correo (Login)", width=300)
    pass_login = ft.TextField(hint_text="Contraseña (Login)", password=True, width=300)

    # 2. Instancias separadas para el Registro
    email_reg = ft.TextField(hint_text="Correo (Registro)", width=300)
    pass_reg = ft.TextField(hint_text="Contraseña (Registro)", password=True, width=300)

    def mostrar_alerta():
        def cerrar_alerta(e):
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Datos Incompletos"),
            content=ft.Text("Por favor, rellene todos los campos."),
            actions=[ft.TextButton("Confirmar", on_click=cerrar_alerta)]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def intentar_ingresar(e):
        if not email_login.value or not pass_login.value:
            mostrar_alerta()
        else:
            print("¡Ingreso exitoso!")

    def intentar_registrar(e):
        if not email_reg.value or not pass_reg.value:
            mostrar_alerta()
        else:
            print("¡Registro exitoso!")

    # Vistas independientes
    vista_login = ft.Column([
        ft.Text("Iniciar Sesión", size=20, color=ft.Colors.GREY_800),
        email_login,
        pass_login,
        ft.ElevatedButton("Ingresar", on_click=intentar_ingresar),
        ft.TextButton("¿No tienes cuenta? Regístrate", on_click=lambda e: cambiar_vista(1))
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    vista_registro = ft.Column([
        ft.Text("Registro", size=20, color=ft.Colors.GREY_800),
        email_reg,
        pass_reg,
        ft.ElevatedButton("Registrarse", on_click=intentar_registrar),
        ft.TextButton("¿Ya tienes cuenta? Inicia sesión", on_click=lambda e: cambiar_vista(0))
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    transicion = ft.AnimatedSwitcher(
        content=vista_login,
        duration=400,
        transition=ft.AnimatedSwitcherTransition.SCALE
    )

    def cambiar_vista(indice):
        transicion.content = vista_registro if indice == 1 else vista_login
        transicion.update()

    page.add(transicion)

ft.app(main)