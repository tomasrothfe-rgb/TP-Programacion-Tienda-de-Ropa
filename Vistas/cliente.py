import flet as ft
import logging 
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clases import Inventario  

logging.basicConfig(level=logging.INFO)


def main(page: ft.Page):
    page.title = "Panel de Administrador "
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 700
    page.window.height = 500

    inventario = Inventario()

    def mostrar():
        lista_productos=inventario.listar_productos()
        grid_productos.controls.clear()
        for p in lista_productos:
            tarjeta_producto = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Image(
                            src=p.imagen,
                            border_radius=10,
                            fit="cover",
                            expand=True 
                        ),
                        ft.Container(
                            padding=10,
                            content=ft.Column(
                                controls=[
                                    ft.Text(p.nombre, weight=ft.FontWeight.BOLD, size=16, max_lines=1),
                                    ft.Text(f"{p.categoria} · {p.marca}", size=12, color=ft.Colors.GREY_700, max_lines=1),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(p.precio, size=14, color=ft.Colors.GREEN_700, weight=ft.FontWeight.W_600),
                                            ft.Button(
                                                content="Seleccionar",
                                                icon=ft.Icons.ADS_CLICK,
                                                icon_color=ft.Colors.BLUE_600,
                                                tooltip="Agregar al carrito",
                                                data=p.nombre,
                                                on_click=lambda e, id=p.id: print(e, id)
                                            )
                                        ]
                                    )
                                ],
                                spacing=5
                            )
                        )
                    ],
                    spacing=0,
                ),
                border=ft.Border(
                    top=ft.BorderSide(1, ft.Colors.GREY_300),
                    bottom=ft.BorderSide(1, ft.Colors.GREY_300),
                    left=ft.BorderSide(1, ft.Colors.GREY_300),
                    right=ft.BorderSide(1, ft.Colors.GREY_300)
                ),
                border_radius=12,
                bgcolor=ft.Colors.WHITE,
                shadow=ft.BoxShadow(
                    blur_radius=10,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                ),
            )
            
            grid_productos.controls.append(tarjeta_producto)

        page.update()
            
    
    grid_productos = ft.GridView(
        expand=1,
        max_extent=250,       
        child_aspect_ratio=0.8, 
        spacing=20,
        run_spacing=20,
    )
    contenedor_izquierdo = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Panel de Administrador", size=30, weight="bold", color=ft.Colors.BLUE),
                ft.Button("Mostrar productos", on_click=lambda: mostrar()),

            ]
        )
    )

    
    page.add(
        ft.Row(
            controls=[
                contenedor_izquierdo,
                grid_productos,
                      ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
        
    )


ft.app(target=main)