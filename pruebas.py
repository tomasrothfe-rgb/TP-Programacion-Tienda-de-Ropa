import flet as ft

BG = "#AEAEAE"
CARD = "#808080"
DARK = "#222222"

def main(page: ft.Page):
    page.bgcolor = BG
    page.padding = 30
    page.window_width = 1400
    page.window_height = 900

    sidebar = ft.Container(
        width=85,
        bgcolor=DARK,
        border_radius=25,
        padding=20,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.AC_UNIT, color="white"),
                        ft.Divider(color="#555"),
                        ft.Icon(ft.Icons.HOME, color="white70"),
                        ft.Icon(ft.Icons.PUBLIC, color="white70"),
                        ft.Icon(ft.Icons.STAR_BORDER, color="white70"),
                        ft.Icon(ft.Icons.SHARE, color="white70"),
                    ]
                ),
                ft.Icon(ft.Icons.SETTINGS, color="white70")
            ]
        )
    )

    login = ft.Container(
        expand=True,
        bgcolor=CARD,
        border_radius=30,
        padding=60,
        shadow=ft.BoxShadow(
            blur_radius=40,
            spread_radius=0,
            color="#868686",
            offset=ft.Offset(8, 8),
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=70,
                    height=70,
                    bgcolor=DARK,
                    border_radius=35,
                    content=ft.Icon(ft.Icons.AC_UNIT,
                                    color="white")
                ),

                ft.Text(
                    "Reagle",
                    size=40,
                    weight=ft.FontWeight.W_600,
                ),

                ft.Text(
                    "All Your Workflows, One Place",
                    color="grey"
                ),

                ft.Container(height=25),

                ft.TextField(
                    label="Email",
                    width=500,
                    border_radius=15,
                    filled=True,
                    bgcolor="#A3A3A3",
                    border_color="transparent",
                    prefix_icon=ft.Icons.PERSON,
                ),

                ft.Container(height=10),

                ft.TextField(
                    label="Password",
                    password=True,
                    can_reveal_password=True,
                    width=500,
                    border_radius=15,
                    filled=True,
                    bgcolor="#EFEFEF",
                    border_color="transparent",
                    prefix_icon=ft.Icons.LOCK,
                ),

                ft.Container(height=25),

                ft.ElevatedButton(
                    "Sign In",
                    width=500,
                    height=55,
                    style=ft.ButtonStyle(
                        bgcolor=DARK,
                        color="white",
                        shape=ft.RoundedRectangleBorder(radius=15)
                    )
                ),

                ft.Container(height=20),



                ft.Container(height=20),

            ]
        )
    )

    page.add(
        ft.Row(
            expand=True,
            controls=[
                sidebar,
                login
            ]
        )
    )

ft.app(main)