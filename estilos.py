import flet as ft
FONDO = "#EBF0F5"
TEXTO = "#111827"
TEXTO_SUAVE = "#6B7280"
OSCURO = "#0D1117"
BLANCO = "#FFFFFF"
SOMBRA_OSCURA = "#D1D9E6"
SOMBRA_CLARA = "#FFFFFF"
COLOR_CAMPO = "#E3E9F0"
FUENTE_TEXTO = "Inter"
FUENTE_TITULO = "Space Grotesk"


def aplicar_tema(page: ft.Page):
    page.bgcolor = FONDO
    page.fonts = {
        "Inter": "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
        "Space Grotesk": "https://github.com/google/fonts/raw/main/ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf",
    }
    page.theme = ft.Theme(
        font_family=FUENTE_TEXTO,
        color_scheme=ft.ColorScheme(primary=OSCURO, on_primary=BLANCO, surface=FONDO),
    )

def boton_no_presionado():
    return ft.ButtonStyle(
        color=TEXTO_SUAVE,                      
        bgcolor=FONDO,                    
        padding=20,
        shape=ft.RoundedRectangleBorder(radius=20), 
        overlay_color=ft.Colors.TRANSPARENT, 
    )

def boton_presionado():
    return ft.ButtonStyle(
        color=FONDO,                      
        bgcolor=TEXTO,                    
        padding=20,
        shape=ft.RoundedRectangleBorder(radius=20), 
        overlay_color=ft.Colors.TRANSPARENT,  
    )

def campo_datos(titulo, ejemplo, **kwargs): 
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(titulo.upper(), color=TEXTO_SUAVE),
                reborde_neu(ft.TextField(hint_text=ejemplo, border_color=ft.Colors.TRANSPARENT, color=TEXTO_SUAVE,**kwargs)),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
    )
        

def sombra_neu(distancia=8, blur=16):
    return [
        ft.BoxShadow(blur_radius=blur, offset=ft.Offset(distancia, distancia), color=SOMBRA_OSCURA),
        ft.BoxShadow(blur_radius=blur, offset=ft.Offset(-distancia, -distancia), color=SOMBRA_CLARA),
    ]


def reborde_neu(contenido):
    return ft.Container(
        content=contenido,
        bgcolor=FONDO,
        shadow=sombra_neu(),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.5, ft.Colors.WHITE)),
        border_radius=20,
        padding=5
    )


def tarjeta_glassmorph(titulo_superior, titulo, descripcion):
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

def construir_header():
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Image(src="Imagenes/Imagenes_UI/jupiter_logo.png"),
                ft.Text("JUPITER", font_family=TEXTO, weight=ft.FontWeight.BOLD, color=TEXTO, size=25)
            ],
        ),
        padding=20,
        expand=True,
        height=70,
        blur=ft.Blur(20, 20),
        border=ft.Border.only(bottom=ft.BorderSide(1.5, ft.Colors.with_opacity(0.4, ft.Colors.WHITE))),
        bgcolor=ft.Colors.with_opacity(0.7, FONDO)
    )

def construir_footer():
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