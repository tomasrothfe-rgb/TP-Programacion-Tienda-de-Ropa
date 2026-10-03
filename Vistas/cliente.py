import flet as ft
import logging 
import os
import sys
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clases import Inventario,Usuario,Carrito  


logging.basicConfig(level=logging.INFO)



def ClienteVista(page, ir_a_login, ir_a_compra, usuario):
    inventario = Inventario()
    producto_seleccionado={"id":None,"color":None,"talle":None, "cantidad":None}
    carrito = Carrito(usuario.id) 

    def compra():
        ir_a_compra(usuario)
        
    def ventana_de_alerta(texto_superior, erratas):

        def diseño_entradas(erratas):
                    return ft.Text(
                        erratas,
                    )

        return page.show_dialog(
                    ft.AlertDialog(
                            modal=True,
                            title=ft.Text(texto_superior),
                            content=ft.Column(
                                diseño_entradas(erratas)
                            ),
                            actions=[
                                    ft.Button("CONFIRMAR",on_click=lambda e: page.pop_dialog()),
                                    ft.Button("CANCELAR", on_click=lambda e: page.pop_dialog())
                                ],
                            actions_alignment=ft.MainAxisAlignment.END,))

    def actualizar_carrito():
        columna_carrito.controls.clear()
        lista=carrito.listar_carrito()
        total_carrito.value=0
        lista_controls=[]
        contador=0
        for i in lista:
            contador+=i[5]
        carrito_texto.value=str(contador)
        for i in lista:
            info = inventario.consultar_producto_especifico(i[2])
            lista_controls.append(
                ft.ListTile(
                    leading=ft.Image(src=info["url"]),
                    title=f"{info['categoria']} {info['marca']} {info['nombre']}",
                    subtitle=ft.Column(
                        controls=[
                            ft.Text(f"{i[3]} / Color: {i[4]}", color=ft.Colors.GREY_600, size=12),
                            ft.Text(f"${info['precio']} x {i[5]}")
                        ],
                        spacing=2 
                    ),
                    trailing=ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.RED_400,
                        tooltip="Eliminar del carrito",
                        on_click=lambda e, item=i: eliminar_carrito(e, item) 
                    )
                )
            )
            total_carrito.value+=int(info["precio"]*int(i[5]))

        columna_carrito.controls.extend(lista_controls)
        page.update()

    async def mostrar_carrito(e):
        await page.show_end_drawer()
    
    def eliminar_carrito(e, id):
        carrito.eliminar_carrito(id[0])
        actualizar_carrito()

    def mostrar(producto):
        lista_productos = inventario.listar_productos(producto)
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

        async def seleccionar_producto():
            producto_seleccionado["cantidad"] = int(txt_cantidad.value)
            resultado = carrito.agregar_carrito(producto_seleccionado)
            if resultado !=None:
                ventana_de_alerta(*resultado)
            else:
                actualizar_carrito()
                await page.show_end_drawer() 
            

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
        btn_menos = ft.Button("-", on_click=lambda e: modificar_contador(e, -1), width=40)
        btn_mas = ft.Button("+", on_click=lambda e: modificar_contador(e, 1), width=40)

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
            on_click=seleccionar_producto
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

    def menu_filtro():
        categorias = inventario.listar_elementos_producto()[0]

        opciones = [ft.DropdownOption(key="Todos", text="FILTRAR: TODOS")]
        for c in categorias: 
            opciones += [ft.DropdownOption(key=c, text=f"FILTRAR: {c.upper()}")]

        def al_seleccionar(e):
            seleccion = e.control.value
            mostrar(None if seleccion == "Todos" else seleccion)

        return ft.Dropdown(
            value="Todos",
            options=opciones,
            on_select=al_seleccionar,
        )



    columna_carrito=ft.ListView(
        controls=[]
    )
    total_carrito=ft.Text()
    page.end_drawer = ft.NavigationDrawer(
        controls=[
            ft.Text("CARRITO DE COMPRAS"),
            columna_carrito,
            ft.Divider(thickness=1),
            total_carrito,
            ft.Button(
                content="Comprar",
                on_click=lambda: compra()
            )
        ],
    ) 
    carrito_texto=ft.Text("0")
    filtro = ft.Column(
        controls=[menu_filtro()]
    )

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
                ft.IconButton(icon=ft.Icons.HOME, on_click=lambda: mostrar(None)),
                filtro,
                ft.Row(controls=[carrito_texto, ft.IconButton(icon=ft.Icons.SHOPPING_BAG, on_click=mostrar_carrito)]),
                ft.Button("Cerrar sesión", on_click=ir_a_login),     
            ]
        )
    )
    actualizar_carrito()
    mostrar(None)

    return [
        ft.Row(
            controls=[
                contenedor_izquierdo,
                contenedor_derecho,
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
    ]
