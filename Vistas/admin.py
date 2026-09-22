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
    producto_en_seleccion = None

    def cambiar_seleccion(e, id):
        nonlocal producto_en_seleccion
        producto_en_seleccion = id
        print(producto_en_seleccion)


    def agregar_stock():
        def confirmar_click():
            lista=[]
            for talle,i in campos_stock.items():
                if i.value:
                     lista.append({"id":producto_en_seleccion,"color":color_seleccionado,"talle": talle, "cantidad":int(i.value)})

            inventario.agregar_stock(lista)
            page.pop_dialog()
            agregar_stock()


        if not producto_en_seleccion:
            ventana_de_alerta(
                "ERROR DE SELECCION",
                "NO SE SELECCIONO EL PRODUCTO PARA AGREGAR STOCK"
            )
            return

        retorno = inventario.listar_stock(producto_en_seleccion)

        colores = retorno["colores"]
        talles = retorno["talles"]
        variantes = retorno["diccionario"]
        color_seleccionado=None

        tabla_talles = ft.Column(visible=False)
        lista_disponibles = ft.Column(visible=False)

        campos_stock = {}

        def seleccionar_color(e, color):

            tabla_talles.controls.clear()
            lista_disponibles.controls.clear()
            campos_stock.clear()
            nonlocal color_seleccionado
            color_seleccionado=color

            variantes_color = [
                v for v in variantes
                if v["color"] == color
            ]

            controles_talles = []

            for talle in talles:

                cantidad = next(
                    (
                        v["cantidad"]
                        for v in variantes_color
                        if v["talle"] == talle
                    ),
                    0
                )

                campo = ft.TextField(
                    width=45,
                    height=40,
                    text_size=12,
                    content_padding=5,
                    keyboard_type=ft.KeyboardType.NUMBER
                )

                campos_stock[talle] = campo

                controles_talles.append(
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[
                            ft.Text(
                                talle,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                str(cantidad),
                                size=12
                            ),
                            campo
                        ]
                    )
                )

            tabla_talles.controls.extend([
                ft.Text(
                    f"Stock de {color}",
                    size=16,
                    weight=ft.FontWeight.BOLD
                ),
                ft.Row(
                    controls=controles_talles,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ])

            disponibles = [
                v for v in variantes_color
                if int(v["cantidad"]) > 0
            ]

            lista_disponibles.controls.append(
                ft.Text(
                    "Talles disponibles:",
                    weight=ft.FontWeight.BOLD
                )
            )

            for variante in disponibles:
                lista_disponibles.controls.append(
                    ft.Text(
                        f'{variante["talle"]} → {variante["cantidad"]}'
                    )
                )

            tabla_talles.visible = True
            lista_disponibles.visible = True

            page.update()

        opciones_colores = [
            ft.MenuItemButton(
                content=color,
                on_click=lambda e, c=color: seleccionar_color(e, c)
            )
            for color in colores
        ]

        menu_colores = ft.SubmenuButton(
            "COLORES",
            controls=opciones_colores
        )

        page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("VENTANA DE STOCK"),
                content=ft.Container(
                    width=350,
                    content=ft.Column(
                        controls=[
                            ft.Text("Seleccione color:"),

                            ft.MenuBar(
                                controls=[
                                    menu_colores
                                ]
                            ),

                            ft.Divider(),

                            tabla_talles,

                            ft.Divider(),

                            lista_disponibles
                        ]
                    )
                ),
                actions=[
                    ft.Button(
                        "CONFIRMAR",
                        on_click=lambda e: confirmar_click()
                    ),
                    ft.Button(
                        "CANCELAR",
                        on_click=lambda e: page.pop_dialog()
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
        )
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

    def ventana_agregar_producto(texto_superior):
        def agregar_clik(texto):
            page.pop_dialog()
            agregar(texto)

        async def seleccionar_archivo(e):
            files = await ft.FilePicker().pick_files(
                allow_multiple=False,
                allowed_extensions=["png"] 
            )
            if files:
                archivo = files[0]
                nombre_archivo = archivo.name
                        
                if nombre_archivo.lower().endswith('.png'):
                    imagen_preview.src=archivo.path
                    imagen_preview.visible=True
                    elementos_seleccionados["imagen"] = archivo.path
                    resultado_texto.value = "Archivo seleccionado con exito"
                    resultado_texto.color = ft.Colors.GREEN_600

                else:
                    elementos_seleccionados["imagen"] = None
                    resultado_texto.value = "Error NO es un archivo PNG."
                    resultado_texto.color = ft.Colors.RED_600
                    ventana_de_alerta("ERROR AL SELECIONAR IMAGEN","LA IMAGEN PROPORCIONADA NO CUMPLE CON EL FORMATO")

                    
            page.update()

        def confirmar_click():
            if elementos_seleccionados["categorias"] == None or elementos_seleccionados["marcas"] == None:
                ventana_de_alerta("ELEMENTOS INCOMPLETOS", "ASEGURESE DE COMPLETAR TODOS LOS ELEMENTOS REQUERIDOS")
            else:
                origen = elementos_seleccionados["imagen"]

                retorno = inventario.agregar_producto(
                    elementos_seleccionados["categorias"],
                    elementos_seleccionados["marcas"],
                    precio.value,
                    origen,
                )
                if isinstance(retorno, tuple):        
                    ventana_de_alerta(*retorno)
                else:                                    
                    page.pop_dialog()
                    if check_stock.value:
                        nonlocal producto_en_seleccion
                        producto_en_seleccion = retorno
                        agregar_stock()
            
        def menu_click(e, clave):
            if clave=="categorias":
                elementos_seleccionados["categorias"]= e.control.content
            elif clave=="marcas":
                elementos_seleccionados["marcas"]= e.control.content
                 

        elementos= inventario.listar_elementos_producto()
        elementos_diccionario={"categorias":elementos[0], "marcas":elementos[1]}
        menu_bar_controles = []
        elementos_seleccionados={"categorias":None, "marcas":None, "imagen": None}
        resultado_texto = ft.Text(value="Ningún archivo seleccionado", size=16, weight=ft.FontWeight.BOLD)
        imagen_preview=ft.Image(
             src="",
             width=200,
             height=200,
             fit=ft.BoxFit.CONTAIN,
             visible=False
        )
        precio=ft.TextField(
             hint_text="Precio"
        )
        check_stock = ft.Checkbox(label="Agregar stock al crear el producto", value=False)

        for clave, lista in elementos_diccionario.items():
            opciones=[]

            for option_text in lista:
                            opciones.append(
                                ft.MenuItemButton(
                                    option_text,
                                    on_click=lambda e, c=clave:menu_click(e,c),
                                )
                            )

            menu_bar_controles.append(
                ft.SubmenuButton(
                    clave.upper(),                  
                    controls=opciones,
                )
            )

        return page.show_dialog(
                    ft.AlertDialog(
                            modal=True,
                            title=ft.Text(texto_superior),
                            content=ft.Column(
                                 controls=[
                                    ft.Button(
                                        content=ft.Text("Seleccionar archivo"),
                                        icon=ft.Icons.UPLOAD_FILE,
                                        on_click=seleccionar_archivo
                                        ),
                                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                                    resultado_texto,
                                    imagen_preview,
                                    ft.MenuBar(
                                        expand=True,
                                        style=ft.MenuStyle(alignment=ft.Alignment.TOP_LEFT),
                                        controls=menu_bar_controles,
                                        ),
                                    precio,
                                    check_stock,
                                    ft.Row(
                                         controls=[
                                                ft.Button(
                                                   content="Agregar categoria",
                                                   on_click=lambda: agregar_clik("categoria")
                                            ),
                                                ft.Button(
                                                   content="Agregar marca",
                                                   on_click=lambda: agregar_clik("marca")
                                            )
                                         ]
                                    )
                                 ]
                            )
                            ,
                            actions=[
                                    ft.Button("CONFIRMAR",on_click=lambda e:confirmar_click()),
                                    ft.Button("CANCELAR", on_click=lambda e: page.pop_dialog())
                                ],
                            actions_alignment=ft.MainAxisAlignment.END,))

    def ventana_con_entradas(texto_superior,tipo, funcion):
        entrada= ft.TextField(
                         hint_text=tipo
                    )
        def confirmar_click():
            valor_entrada=entrada.value
            retorno=funcion(valor_entrada)
            if retorno != None:
                   ventana_de_alerta(*retorno)
            else:
                page.pop_dialog()

        return page.show_dialog(
            ft.AlertDialog(
                    modal=True,
                    title=ft.Text(texto_superior),
                    content=ft.Column(
                            entrada
                    ),
                    actions=[
                            ft.Button("CONFIRMAR",on_click=lambda e:confirmar_click()),
                            ft.Button("CANCELAR", on_click=lambda e: page.pop_dialog())
                        ],
                    actions_alignment=ft.MainAxisAlignment.END,))

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
                                    ft.Text(f"{p.categoria} {p.marca}", weight=ft.FontWeight.BOLD, size=16, max_lines=1),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(p.precio, size=14, color=ft.Colors.GREEN_700, weight=ft.FontWeight.W_600),
                                            ft.Button(
                                                content="Seleccionar",
                                                icon=ft.Icons.ADS_CLICK,
                                                icon_color=ft.Colors.BLUE_600,
                                                tooltip="Agregar al carrito",
                                                data=f"{p.categoria} {p.marca}",
                                                on_click=lambda e, id=p.id: cambiar_seleccion(e, id)
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
            

    def agregar(tipo):
        texto_superior=f"AGREGAR {tipo.upper()}"
        logging.info(f"Se desea agregar {tipo}")
        if tipo=="marca":
            ventana_con_entradas(texto_superior,tipo, inventario.agregar_marca)
        elif tipo=="categoria":
            ventana_con_entradas(texto_superior,tipo, inventario.agregar_categoria)
        elif tipo=="color":
            ventana_con_entradas(texto_superior,tipo, inventario.agregar_color)
        else:
            ventana_agregar_producto(texto_superior)


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
                ft.Button("Agregar productos", on_click=lambda: agregar("producto")),
                ft.Button("Agregar marca", on_click=lambda: agregar("marca")),
                ft.Button("Agregar categoria", on_click=lambda: agregar("categoria")),
                ft.Button("Agregar color", on_click=lambda: agregar("color")),
                #ft.Button("Eliminar productos", on_click=eliminar),
                ft.Button("Mostrar productos", on_click=mostrar),
                #ft.Button("Modificar productos", on_click=modificar),
                ft.Button("Agregar stock", on_click=lambda: agregar_stock()),
                #ft.Button("Consultar estadisticas", on_click=estadisticas),
                #ft.Button("Ver historial de compras productos", on_click=historial),
            ]
        )
    )

    mostrar()

    page.add(
        ft.Row(
            controls=[contenedor_izquierdo, grid_productos],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
    )


ft.app(target=main)