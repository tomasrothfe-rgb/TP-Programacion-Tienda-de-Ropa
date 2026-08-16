import flet as ft

# Configuración de los entradas de texto con iconos y estilos personalizados
def entry_datos(boolean, texto, icono):
        return ft.Container(
                content=ft.TextField(
                    width=800,
                    prefix_icon=icono,
                    text_style=ft.TextStyle(
                        color=ft.Colors.GREY_800
                    ),
                    hint_text=texto,
                    hint_style=ft.TextStyle(
                        color=ft.Colors.GREY_800,
                        ),
                    password=boolean, 
                    border_color=ft.Colors.TRANSPARENT,
                    can_reveal_password=True,
                    ),
                bgcolor="#bfbfbe",
                border_radius=15,
                border=ft.Border.all(1, "#a0a0a0"),  
                shadow=[
                    ft.BoxShadow(
                    blur_radius=2,
                    spread_radius=0,
                    color=ft.Colors.WHITE,
                    offset=ft.Offset(-1, -1), 
                ),
                    ft.BoxShadow(
                    blur_radius=2,
                    spread_radius=0,
                    color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
                    offset=ft.Offset(1, 1),  
                ),
                ],
            )

def boton_ingresar(texto):
    return ft.Container(
        content=ft.TextButton(
            content=ft.Row(
                controls=[
                   ft.Container(
                        content=ft.Text(texto,
                            color=ft.Colors.WHITE,
                           ),
                        expand=1,
                        alignment=ft.Alignment.CENTER_RIGHT
                   ),
                   ft.Container(
                        content=ft.Icon(ft.Icons.ARROW_RIGHT_ALT_SHARP,
                            color=ft.Colors.WHITE,
                            ),
                        expand=1,
                        alignment=ft.Alignment.CENTER_RIGHT
                    ),
                
                ],
                alignment=ft.Alignment.CENTER
            ), 
            expand=True),
        width=800,
        height=60,
        bgcolor="#2b2b2c",
        border_radius=15,
        border=ft.Border.all(1, "#a0a0a0"),  
        shadow=
            ft.BoxShadow(
            blur_radius=10,
            spread_radius=1,
            color=ft.Colors.with_opacity(0.3,ft.Colors.BLACK),
            offset=ft.Offset(0, 5),
        )
        )
def imagen_inicio():
      return ft.Row(
                      controls=[
                      ft.Container(expand=1),
                      ft.Image(
                          src="Imagenes/nova_prestige_logo_letras.png",
                          height= 350,
                          width = 350, 
                          fit=ft.BoxFit.CONTAIN,
                          color="#2b2b2c",
                          color_blend_mode=ft.BlendMode.SRC_IN,
                          expand=10
                      ),
                      ft.Container(expand=1),
                      ],
                      expand=1
                  )

def main(page: ft.Page):
    page.bgcolor= "#b6b6b4"
    page.padding = 30
    page.window.min_height= 500
    page.window.min_width = 700

    contenido_registro = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            imagen_inicio(),
            ft.Text("Novus Prestige | El arte de la elegancia", color=ft.Colors.GREY_800),
            entry_datos(False,"Ingrese su nombre completo",ft.Icon(ft.Icons.PERSON_2_OUTLINED, 
                                    color=ft.Colors.GREY_800, 
                                    )),
            entry_datos(False,"Ingrese su correo electrónico",ft.Icon(ft.Icons.PERSON_OUTLINE, 
                                    color=ft.Colors.GREY_800, 
                                    )),
            entry_datos(True,"Ingrese su contraseña",ft.Icon(ft.Icons.LOCK_OUTLINE, 
                                    color=ft.Colors.GREY_800,
                                    )),
            entry_datos(True,"Ingrese la clave de administrador",ft.Icon(ft.Icons.LOCK_OUTLINE, 
                                                            color=ft.Colors.GREY_800,
                                                             
                                                            )),
            boton_ingresar("Registrarse"),
            ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("¿Ya estas registrado?", 
                    color=ft.Colors.GREY_800),
                    ft.TextButton("Iniciar sesión", 
                    style=ft.TextStyle(color=ft.Colors.BLACK),
                    on_click=lambda e: cambiar_vista(0))
                    ],
                )
        ]
    )

    contenido_ingreso = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            imagen_inicio(),
            ft.Text("Novus Prestige | El arte de la elegancia", color=ft.Colors.GREY_800),
            entry_datos(False,"Ingrese su nombre de usuario",ft.Icon(ft.Icons.PERSON_2_OUTLINED, 
                                    color=ft.Colors.GREY_800, 
                                    )),
            entry_datos(True,"Ingrese su contraseña",ft.Icon(ft.Icons.LOCK_OUTLINE, 
                                    color=ft.Colors.GREY_800, 
                                    )),
            boton_ingresar("Ingresar"),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text("¿Todavía no tenes una cuenta?", 
                            color=ft.Colors.GREY_800),
                    ft.TextButton("Registrarse", 
                            style=ft.TextStyle(color=ft.Colors.BLACK),
                            on_click=lambda e: cambiar_vista(1))
                ],
            )
            ],
            
        )

    barra_lateral=ft.Container(
        width=85,
        bgcolor="#c2c2c2",
        border_radius=15,
        border=ft.Border.all(1, "#d6d5d4"),
        padding=10,
        shadow=ft.BoxShadow(
                blur_radius=10,
                spread_radius=1,
                color=ft.Colors.with_opacity(0.3,ft.Colors.BLACK),
                offset=ft.Offset(0, 5),
                        ),
        content=ft.Column(
              controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                content=ft.Image(
                                    src="Imagenes/nova_prestige_logo.png",
                                    fit=ft.BoxFit.CONTAIN,
                                    color=ft.Colors.WHITE,
                                    color_blend_mode=ft.BlendMode.SRC_IN,
                                    ),
                                alignment=ft.Alignment.CENTER,
                                ),
                                ft.Container(height=1, 
                                bgcolor=ft.Colors.with_opacity(1,ft.Colors.BLACK), 
                                shadow=ft.BoxShadow(
                                    blur_radius=1,
                                    spread_radius=0,
                                    color=ft.Colors.with_opacity(0.3,ft.Colors.WHITE),
                                    offset=ft.Offset(0, 1),
                                )),
                                ft.IconButton(icon=ft.Icon(ft.Icons.HOUSE, 
                                    color=ft.Colors.WHITE, 
                                    ),
                                    tooltip= "Inicio",
                                    ),
                                ft.IconButton(icon=ft.Icon(ft.Icons.LOGIN, 
                                    color=ft.Colors.WHITE),
                                    tooltip= "Iniciar sesión",
                                    on_click=lambda e: cambiar_vista(0),
                                    ),
                                
                            ],
                            spacing=20,
                        ),
                        bgcolor="#2b2b2c",
                        padding=10, 
                        border_radius=10,
                        border=ft.Border.all(1, "#232324"),
                        shadow=ft.BoxShadow(
                            blur_radius=10,
                            spread_radius=1,
                            color=ft.Colors.with_opacity(0.3,ft.Colors.BLACK),
                            offset=ft.Offset(0, 5),
                        )
                        ),
                    ft.Container(expand=3),
                    ft.Container(
                        height=1,
                        bgcolor=ft.Colors.with_opacity(0.5,ft.Colors.WHITE), 
                        shadow=ft.BoxShadow(
                            blur_radius=1,
                            spread_radius=0,
                            color=ft.Colors.with_opacity(0.3,ft.Colors.BLACK),
                            offset=ft.Offset(0, 1),
                        )
                        ),
                    ft.Container(
                        content=ft.IconButton(icon=ft.Icon(ft.Icons.SETTINGS, 
                                color=ft.Colors.WHITE, 
                                ),
                                tooltip= "Configuración",
                                ),
                        bgcolor="#2b2b2c",
                        padding=10,
                        border_radius=10,
                        aspect_ratio=1,
                        shadow=ft.BoxShadow(
                            blur_radius=10,
                            spread_radius=1,
                            color=ft.Colors.with_opacity(0.3,ft.Colors.BLACK),
                            offset=ft.Offset(0, 5),
                        )
                        )
              ]
        )
    )

    transicion_contenido = ft.AnimatedSwitcher(
            content=contenido_ingreso,
            duration=400, 
            transition=ft.AnimatedSwitcherTransition.SCALE,
            reverse_duration=200,
            switch_in_curve=ft.AnimationCurve.EASE_OUT,
            switch_out_curve=ft.AnimationCurve.EASE_IN,
        )

    def cambiar_vista(indice):
            if indice == 0:
                transicion_contenido.content = contenido_ingreso
            elif indice == 1:
                transicion_contenido.content = contenido_registro
            transicion_contenido.update()
    
    pantalla_central=ft.Container(
        alignment=ft.Alignment.CENTER,
        content=transicion_contenido,
        expand=True,
        bgcolor="#c2c2c2",
        border_radius=15,
        border=ft.Border.all(1, "#d6d5d4"),
        padding=50,
        shadow=ft.BoxShadow(
                blur_radius=10,
                spread_radius=1,
                color=ft.Colors.with_opacity(0.3,ft.Colors.BLACK),
                offset=ft.Offset(0, 5),
        )
    )

    page.add(ft.Row(
        expand=True,
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
                barra_lateral,
                pantalla_central  
                ]
            )
    )

ft.app(main)