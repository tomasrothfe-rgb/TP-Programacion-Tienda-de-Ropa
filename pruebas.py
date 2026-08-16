import flet as ft

def main(page: ft.Page):
    page.title = "Login y Registro con Animación"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 1. Vista de Iniciar Sesión
    def vista_login():
     return   ft.Container(
        content=ft.Column([
            ft.Text("Iniciar Sesión", size=20, weight=ft.FontWeight.BOLD),
            ft.TextField(label="Correo electrónico"),
            ft.TextField(label="Contraseña", password=True),
            ft.ElevatedButton("Entrar"),
            ft.Divider(),
            ft.TextButton(
                "¿No tienes cuenta? Regístrate aquí",
                on_click=lambda e: cambiar_vista(1)
            )
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.Alignment.CENTER,
        padding=20
    )

    # 2. Vista de Registrarse
    def vista_registro():
        return ft.Container(
        content=ft.Column([
            ft.Text("Crea una cuenta nueva", size=20, weight=ft.FontWeight.BOLD),
            ft.TextField(label="Nombre completo"),
            ft.TextField(label="Correo electrónico"),
            ft.TextField(label="Contraseña", password=True),
            ft.ElevatedButton("Registrarse"),
            ft.Divider(),
            ft.TextButton(
                "¿Ya tienes cuenta? Inicia sesión",
                on_click=lambda e: cambiar_vista(0)
            )
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.Alignment.CENTER,
        padding=20
    )

    # 3. AnimatedSwitcher para manejar la transición suave entre vistas
    transicion_vista = ft.AnimatedSwitcher(
        content=vista_login(),
        duration=400, # Duración de la animación en milisegundos
        transition=ft.AnimatedSwitcherTransition.SCALE, # Tipo de transición (FADE o SCALE)
        reverse_duration=200,
        switch_in_curve=ft.AnimationCurve.EASE_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN,
    )

    # Contenedor principal que envuelve al switcher
    contenedor_principal = ft.Container(
        content=transicion_vista, 
        expand=True, 
        alignment=ft.Alignment.CENTER
    )

    # Función para alternar las vistas de manera animada
    def cambiar_vista(indice):
        if indice == 0:
            transicion_vista.content = vista_login()
        else:
            transicion_vista.content = vista_registro()
        transicion_vista.update() # Actualizamos el switcher para ejecutar la animación

    page.add(contenedor_principal)

ft.app(target=main)