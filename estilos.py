import flet as ft
FONDO = "#EBF0F5"  # Color de fondo general
TEXTO = "#111827"  # Color de texto principal
TEXTO_SUAVE = "#6B7280"  # Color de texto secundario (gris)
OSCURO = "#0D1117"  # Color oscuro para botones y detalles
BLANCO = "#FFFFFF"  # Blanco
SOMBRA_OSCURA = "#D1D9E6"  # Sombra oscura del efecto neumórfico
SOMBRA_CLARA = "#FFFFFF"  # Sombra clara del efecto neumórfico
COLOR_CAMPO = "#E3E9F0"  # Fondo de los campos de texto
FUENTE_TEXTO = "Inter"  # Fuente para textos comunes
FUENTE_TITULO = "Space Grotesk"  # Fuente para títulos


def aplicar_tema(page: ft.Page):  # Aplica colores y fuentes a toda la app
    page.bgcolor = FONDO
    page.fonts = {
        "Inter": "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
        "Space Grotesk": "https://github.com/google/fonts/raw/main/ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf",
    }
    page.theme = ft.Theme(
        font_family=FUENTE_TEXTO,
        color_scheme=ft.ColorScheme(primary=OSCURO, on_primary=BLANCO, surface=FONDO),
    )

def boton_no_presionado():  # Estilo de botón inactivo (claro)
    return ft.ButtonStyle(
        color=TEXTO_SUAVE,                      
        bgcolor=FONDO,                    
        padding=20,
        shape=ft.RoundedRectangleBorder(radius=20), 
        overlay_color=ft.Colors.TRANSPARENT, 
    )

def boton_presionado():  # Estilo de botón activo (oscuro)
    return ft.ButtonStyle(
        color=FONDO,                      
        bgcolor=TEXTO,                    
        padding=20,
        shape=ft.RoundedRectangleBorder(radius=20), 
        overlay_color=ft.Colors.TRANSPARENT,  
    )

def campo_datos(titulo, ejemplo, **kwargs):  # Campo de texto con título arriba y estilo neumórfico
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(titulo.upper(), color=TEXTO_SUAVE),
                reborde_neu(ft.TextField(hint_text=ejemplo, border_color=ft.Colors.TRANSPARENT, color=TEXTO_SUAVE,**kwargs)),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
    )
        

def sombra_neu(distancia=8, blur=16):  # Devuelve las dos sombras del efecto neumórfico
    return [
        ft.BoxShadow(blur_radius=blur, offset=ft.Offset(distancia, distancia), color=SOMBRA_OSCURA),
        ft.BoxShadow(blur_radius=blur, offset=ft.Offset(-distancia, -distancia), color=SOMBRA_CLARA),
    ]


def reborde_neu(contenido, on_click=None, expand=False):  # Envuelve un control en una caja con sombra neumórfica
    return ft.Container(
        content=contenido,
        bgcolor=FONDO,
        shadow=sombra_neu(),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.5, ft.Colors.WHITE)),
        border_radius=20,
        padding=20,
        expand=expand,
        ink=on_click is not None,  
        on_click=on_click,
    )


def tarjeta_glassmorph(titulo_superior, titulo, descripcion):  # Tarjeta translúcida (efecto vidrio) sobre una imagen
    return  ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        titulo_superior,
                        size=12,
                        font_family=FUENTE_TEXTO,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        style=ft.TextStyle(letter_spacing=1.5),
                    ),
                    padding=ft.Padding.symmetric(horizontal=16, vertical=6),
                    bgcolor=ft.Colors.with_opacity(0.25, ft.Colors.WHITE),
                    border=ft.Border.all(1, ft.Colors.with_opacity(0.5, ft.Colors.WHITE)),
                    border_radius=20,
                ),
                ft.Text(
                    titulo,
                    font_family=FUENTE_TITULO,
                    size=34,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Text(
                    descripcion,
                    font_family=FUENTE_TEXTO,
                    size=15,
                    color=ft.Colors.with_opacity(0.85, ft.Colors.WHITE),
                ),
            ],
            spacing=14,
            tight=True,
        ),
        padding=40,
        bgcolor=ft.Colors.with_opacity(0.25, ft.Colors.WHITE),  
        blur=ft.Blur(20, 20),                                   
        border=ft.Border.all(1, ft.Colors.with_opacity(0.4, ft.Colors.WHITE)),
        border_radius=30,
            
        left=40, right=40, bottom=60,                            
    )


def construir_header(botones=None, botones_centro=None):  # Barra superior con logo y botones a la izquierda, centro y derecha
    izquierda = ft.Row(
        controls=[
            ft.Image(src="Imagenes/Imagenes_UI/jupiter_logo.png"),
            ft.Text("JUPITER", font_family=FUENTE_TEXTO, weight=ft.FontWeight.BOLD, color=TEXTO, size=20),
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
    )

    centro = ft.Row(
        controls=botones_centro,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    derecha = ft.Row(
        controls=botones,
        expand=True,
        alignment=ft.MainAxisAlignment.END,
    )

    return ft.Container(
        content=ft.Row(
            controls=[izquierda, centro, derecha],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
        expand=True,
        height=80,
        blur=ft.Blur(20, 20),
        border=ft.Border.only(bottom=ft.BorderSide(1.5, ft.Colors.with_opacity(0.4, ft.Colors.WHITE))),
        bgcolor=ft.Colors.with_opacity(0.7, FONDO),
    )

def construir_footer():  # Barra inferior con el copyright
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("© 2026 JUPITER", size=12, color=TEXTO_SUAVE, font_family=FUENTE_TEXTO),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        height=50,
        bgcolor=BLANCO,
        border=ft.Border.only(top=ft.BorderSide(1, SOMBRA_OSCURA)),
        bottom=0, left=0, right=0,   
    )


def ventana_de_alerta(page, titulo, descripcion, texto_boton="ACEPTAR", al_cerrar=None):  # Muestra un aviso emergente; el ícono cambia según sea error, éxito o info
    mayusculas = titulo.upper()
    if "ERROR" in mayusculas:
        icono, fondo_icono, color_icono = ft.Icons.ERROR_OUTLINE, "#FEE2E2", "#DC2626"
    elif any(p in mayusculas for p in ("ACTUALIZADO", "REALIZADA", "REENVIADO", "EXITO", "ÉXITO")):
        icono, fondo_icono, color_icono = ft.Icons.CHECK_CIRCLE_OUTLINE, "#DCFCE7", "#16A34A"
    else:
        icono, fondo_icono, color_icono = ft.Icons.INFO_OUTLINE, COLOR_CAMPO, TEXTO

    def cerrar(e):  # Cierra el aviso y ejecuta la acción opcional al cerrar
        page.pop_dialog()
        if al_cerrar:
            al_cerrar()

    page.show_dialog(
        ft.AlertDialog(
            modal=True,
            bgcolor=FONDO,
            shape=ft.RoundedRectangleBorder(radius=28),
            content_padding=ft.Padding.all(32),
            content=ft.Container(
                width=380,
                content=ft.Column(
                    tight=True,
                    spacing=14,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    content=ft.Icon(icono, color=color_icono, size=32),
                                    width=64,
                                    height=64,
                                    bgcolor=fondo_icono,
                                    border_radius=20,
                                    alignment=ft.Alignment.CENTER,
                                )
                            ],
                        ),
                        ft.Text(
                            titulo,
                            font_family=FUENTE_TITULO,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=TEXTO,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            descripcion,
                            font_family=FUENTE_TEXTO,
                            size=14,
                            color=TEXTO_SUAVE,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=6),
                        ft.Button(texto_boton, style=boton_presionado(), on_click=cerrar),
                    ],
                ),
            ),
        )
    )