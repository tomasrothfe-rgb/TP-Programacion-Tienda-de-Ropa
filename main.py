import flet as ft



# Página de login
def login(page: ft.Page):
    page.title = "Tienda de Ropa - TP Programación"
    page.bgcolor = "Black"
    page.padding = 10
    page.spacing = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH 

# Funcion para los contenedores de la grilla
    def contenedores_grilla(ocupa,contenido):
        return ft.Container(
            content=ft.Row(
            [contenido],
            alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=ocupa,  
        )

# Funcion para transformar contenedor a efecto glass
    def contenedroes_efecto_glass(ancho, contenido):
        return ft.Container(
            content=contenido,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREY),
            border_radius=25,
            aspect_ratio=ancho,
            expand=True,
            blur=(20, 20),
            border=ft.Border.all(0.3, ft.Colors.WHITE),
            padding=25
        )

    parte_superior_login = ft.Row(
        [ft.Container(
                content=ft.Column(
                [ft.Image(
                src="Tienda de Ropa - TP Programacion/Imagenes/login.png",
                fit=ft.BoxFit.CONTAIN,
                opacity=0.8,
                expand=True,)],
            ),
                alignment=ft.Alignment.CENTER,
                expand=True,
            ),
            ft.Container(
                content=ft.Column(
                [ft.Image(
                src="Tienda de Ropa - TP Programacion/Imagenes/sujeto.png",
                fit=ft.BoxFit.CONTAIN,
                opacity=0.8,
                expand=True,)],
            ),
                alignment=ft.Alignment.TOP_RIGHT,
                expand=True,
            ),
        ],
        expand=True,
        spacing=10,
    )

    parte_centro_login =  ft.Row(
        [ft.Column([
            ft.Text("Nombre de usuario", size=56),
            ft.TextField( hint_text="Jane Doe"),
            ft.Text("Contraseña", size=56),
            ft.TextField( hint_text="Jane Doe")
        ]
        ),
        ft.Button(content="",icon=ft.Icons.ARROW_RIGHT)
        ],
        expand=True,
        spacing=10,
    )

    parte_inferior_login =  ft.Row(
        [ft.Column(
        [   contenedores_grilla(1,ft.Container()),
            contenedores_grilla(2,ft.Container(
                            content=ft.Column(
                            [ft.Image(
                            src="Tienda de Ropa - TP Programacion/Imagenes/logo_SW_letras.png",
                            fit=ft.BoxFit.CONTAIN,
                            opacity=0.8,
                            expand=True,)],
                        ),
                            alignment=ft.Alignment.BOTTOM_LEFT,
                            expand=True,
                        ))
        ],
        expand=True,
        spacing=10,
        ),
            ft.Container(
                content=ft.Column(
                [ft.Image(
                src="Tienda de Ropa - TP Programacion/Imagenes/Logo_SW_imagen.png",
                fit=ft.BoxFit.CONTAIN,
                opacity=0.8,
                expand=True,)],
            ),
                alignment=ft.Alignment.TOP_RIGHT,
                expand=True,
            ),
        ],
        expand=True,
        spacing=10,
    )

    grilla_login = ft.Column(
            [
                contenedores_grilla(10,parte_superior_login),
                ft.Container(bgcolor=ft.Colors.with_opacity(0.8,ft.Colors.WHITE),alignment=ft.Alignment.CENTER, height=1),
                contenedores_grilla(40,parte_centro_login),
                contenedores_grilla(5,parte_inferior_login),
            ],
            expand=True,
            spacing=10,
        )
    
    recuadro_centro = contenedroes_efecto_glass(1, grilla_login)
    recuadro_centro2 = contenedroes_efecto_glass(0.3, ft.Container())

    fondo = ft.Container(
        content=ft.Row(
            [
            contenedores_grilla(6,ft.Container()),
            contenedores_grilla(1,recuadro_centro2),
            contenedores_grilla(1,ft.Container()),
            contenedores_grilla(12,recuadro_centro),
            contenedores_grilla(6,ft.Container())
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        image=ft.DecorationImage(
            src="Tienda de Ropa - TP Programacion/Imagenes/Fondo_Gradiente.png",
            fit=ft.BoxFit.COVER,
            opacity=1,
        ),
        border_radius=20,
        padding=25,
    )

    page.add(fondo)


ft.run(login)