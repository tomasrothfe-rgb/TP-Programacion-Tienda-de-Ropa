import flet as ft

def main(page: ft.Page):
    page.title = "Visor de Productos"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Lista de datos de ejemplo (Simulación de una base de datos)
    productos = [
        {"nombre": "Laptop Gamer", "precio": "$1,200", "imagen": "https://picsum.photos"},
        {"nombre": "Auriculares Bluetooth", "precio": "$85", "imagen": "https://picsum.photos"},
        {"nombre": "Teclado Mecánico", "precio": "$45", "imagen": "https://picsum.photos"},
        {"nombre": "Mouse Inalámbrico", "precio": "$30", "imagen": "https://picsum.photos"},
        {"nombre": "Monitor 4K", "precio": "$350", "imagen": "https://picsum.photos"},
        {"nombre": "Silla Ergonómica", "precio": "$180", "imagen": "https://picsum.photos"},
    ]

    # Función que se ejecuta al presionar el botón de carrito
    def agregar_al_carrito(e):
        producto_nombre = e.control.data
        print(producto_nombre)
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"¡{producto_nombre} agregado al carrito!"),
            action="OK"
        )
        page.snack_bar.open = True
        page.update()

    # Contenedor GridView para mostrar los productos en filas y columnas
    grid_productos = ft.GridView(
        expand=1,
        max_extent=250,        # Ancho máximo de cada tarjeta de producto
        child_aspect_ratio=0.8, # Relación de aspecto (más alto que ancho)
        spacing=20,
        run_spacing=20,
    )

    # Creamos las tarjetas para cada producto
    for p in productos:
        tarjeta_producto = ft.Container(
            content=ft.Column(
                controls=[
                    # Imagen del producto
                    ft.Image(
                        src=p["imagen"],
                        border_radius=10,
                        fit="cover",
                        expand=True 
                    ),
                    # Información del producto (Texto y Botón)
                    ft.Container(
                        padding=10,
                        content=ft.Column(
                            controls=[
                                ft.Text(p["nombre"], weight=ft.FontWeight.BOLD, size=16, max_lines=1),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(p["precio"], size=14, color=ft.Colors.GREEN_700, weight=ft.FontWeight.W_600),
                                        ft.IconButton(
                                            icon=ft.Icons.ADD_SHOPPING_CART_ROUNDED,
                                            icon_color=ft.Colors.BLUE_600,
                                            tooltip="Agregar al carrito",
                                            data=p["nombre"],
                                            on_click=agregar_al_carrito
                                        )
                                    ]
                                )
                            ],
                            spacing=5
                        )
                    )
                ],
                spacing=0
            ),
            # Estilo del recuadro del producto (Corregido con ft.Border)
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
            )
        )
        
        # Agregamos la tarjeta al GridView
        grid_productos.controls.append(tarjeta_producto)

    # Añadir el GridView a la página
    page.add(
        ft.Text("Nuestros Productos", size=28, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        grid_productos
    )

ft.app(target=main)