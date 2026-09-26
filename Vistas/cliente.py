import flet as ft
import logging 
import os
import sys
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clases import Inventario  

logging.basicConfig(level=logging.INFO)


def main(page: ft.Page):
    page.title = "Panel de Cliente"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 1500
    page.window.height = 500

    inventario = Inventario()
    producto_seleccionado={"id":None,"color":None,"talle":None, "cantidad":None}

    

    def mostrar():
        lista_productos = inventario.listar_productos()
        contenedor_derecho.content=None
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
                                        ]
                                    )
                                ],
                                spacing=5
                            )
                        )
                    ],
                    spacing=0,
                ),
                border=ft.Border.all(
                    1, ft.Colors.GREY_300
                ),
                border_radius=12,
                bgcolor=ft.Colors.WHITE,
                ink=True, 
                on_click=lambda e, producto=p: mostrar_producto(producto), 
                shadow=ft.BoxShadow(
                    blur_radius=10,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    offset=ft.Offset(0, 4)
                ),
            )
            grid_productos.controls.append(tarjeta_producto)

        contenedor_derecho.content=grid_productos
        page.update()
    
    def mostrar_producto(producto):
        logging.info(f"Click en el producto: {producto.nombre} (ID: {producto.id})")
        stock = inventario.listar_stock(producto.id)
        producto_seleccionado["id"] = producto.id
        contenedor_derecho.content = None
        contenedor_botones = ft.Row(controls=[])
        contenedor_talles = ft.Row(controls=[])

        def seleccionar_producto():
            producto_seleccionado["cantidad"] = int(txt_cantidad.value)
            print(producto_seleccionado)

        def modificar_contador(e, delta: int):
            cantidad_disponible = producto_seleccionado["talle"][1]  
            nuevo_valor = int(txt_cantidad.value) + delta

            if nuevo_valor > cantidad_disponible:
                txt_error_cantidad.value = f"Solo hay {cantidad_disponible} unidades disponibles."
            elif nuevo_valor < 1:
                txt_error_cantidad.value = ""
            else:
                txt_cantidad.value = str(nuevo_valor)
                txt_error_cantidad.value = ""

            page.update()

        def seleccion_talle(e, talle, cantidad_talle):
            nonlocal producto_seleccionado
            producto_seleccionado["talle"] = (talle, cantidad_talle)
            boton_carrito.disabled = False
            stock_color_talle.value = f"Cantidad de stock {cantidad_talle}"
            stock_color_talle.visible = True

            txt_cantidad.value = "1"
            txt_error_cantidad.value = ""
            contador_cantidad.visible = True

            page.update()

        def seleccion_color(e, color, color_datos):
            contenedor_talles.controls.clear()
            nonlocal producto_seleccionado
            boton_carrito.disabled = True
            stock_color_talle.visible = False
            contador_cantidad.visible = False  
            producto_seleccionado["talle"] = None
            producto_seleccionado["color"] = color
            for i in color_datos:
                contenedor_talles.controls.append(
                    ft.Button(
                        content=i[0],
                        on_click=lambda e, t=i[0], ct=i[1]: seleccion_talle(e, t, ct)
                    )
                )
            page.update()

        if not stock["diccionario"]:
            contenedor_botones.controls.append(
                ft.Text("No hay stock disponible de este producto")
            )
        else:
            agrupado = defaultdict(list)
            for items in stock["diccionario"]:
                agrupado[items['color']].append((items['talle'], items['cantidad']))

            for clave, datos in agrupado.items():
                contenedor_botones.controls.append(ft.Button(
                    content=clave,
                    on_click=lambda e, c=clave, d=datos: seleccion_color(e, c, d)
                ))

        txt_cantidad = ft.Text(value="1", size=30, weight=ft.FontWeight.BOLD)
        txt_error_cantidad = ft.Text(value="", color=ft.Colors.RED_400, size=12)
        btn_menos = ft.ElevatedButton("-", on_click=lambda e: modificar_contador(e, -1), width=40)
        btn_mas = ft.ElevatedButton("+", on_click=lambda e: modificar_contador(e, 1), width=40)

        contador_cantidad = ft.Column(
            visible=False,
            controls=[
                ft.Row(controls=[btn_menos, txt_cantidad, btn_mas]),
                txt_error_cantidad,
            ]
        )

        informacion_producto = ft.Column(
            controls=[
                ft.Text(f"{producto.categoria} {producto.marca} {producto.nombre}"),
                ft.Text(f"{producto.precio}"),
                ft.Text("Colores:"),
                contenedor_botones,
                contenedor_talles,
            ]
        )
        imagen = ft.Image(src=producto.imagen, fit=ft.BoxFit.COVER)

        boton_carrito = ft.Button(
            content="Agregar al carrito",
            icon=ft.Icons.SHOP,
            disabled=True,
            on_click=lambda e: seleccionar_producto()
        )

        stock_color_talle = ft.Text(visible=False)

        panel_compra = ft.Column(
            controls=[
                stock_color_talle,
                contador_cantidad,
                boton_carrito,
            ],
            width=250,  
            spacing=10,
        )

        pagina_producto = ft.Row(
            controls=[
                imagen,
                informacion_producto,
                panel_compra,
            ]
        )
        contenedor_derecho.content = ft.Container(
            content=pagina_producto
        )

        page.update()
            
    grid_productos = ft.GridView(
        expand=1,
        max_extent=250,       
        child_aspect_ratio=0.8, 
        spacing=20,
        run_spacing=20,
    )
    contenedor_derecho=ft.Container(
         content=None,
         bgcolor= ft.Colors.GREY,
         expand=True
    )
    
    contenedor_izquierdo = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Panel de Cliente", size=30, weight="bold", color=ft.Colors.BLUE),
                ft.Button("Mostrar productos", on_click=lambda e: mostrar()),
            ]
        )
    )

    mostrar()

    page.add(
        ft.Row(
            controls=[
                contenedor_izquierdo,
                contenedor_derecho,
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
    )

ft.app(target=main)