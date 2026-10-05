import flet as ft
import logging 
import os
import sys
import estilos
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

    def generar_tarjetas_incio(lista):
        tarjetas = ft.Row(
            controls=[],
            expand=True,                                      
            spacing=25,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        )
        for imagen, filtro in lista:
            tarjeta = estilos.reborde_neu(
                ft.Image(src=imagen, fit=ft.BoxFit.CONTAIN),
                on_click=lambda e, f=filtro: mostrar_catalogo(f),
                expand=True,
            )
            tarjeta.padding = 20    
            tarjetas.controls.append(tarjeta)
        return tarjetas

    def generar_tarjetas_superior(lista):
        tarjetas = ft.Row(
            controls=[],
            expand=True,                                     
            spacing=25,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,  
        )
        for i in lista:
            tarjetas.controls.append(
                ft.Container(
                    expand=True,                               
                    content=ft.Image(src=i, fit=ft.BoxFit.CONTAIN),
                    bgcolor=ft.Colors.WHITE,
                    padding=20,
                    border_radius=20,
                    border=ft.Border.all(1, ft.Colors.with_opacity(0.5, ft.Colors.GREY)),
                )
            )
        return tarjetas
    
    def mostrar_inicio():
        contenedor_principal.content=inicio
        page.update()

    def formato_precio(valor):
        return "$" + f"{valor:,.0f}".replace(",", ".")

    def crear_tarjeta_producto(p):
        etiqueta = ft.Container(
            left=20, top=20,
            padding=ft.Padding.symmetric(horizontal=16, vertical=6),
            bgcolor=ft.Colors.with_opacity(0.35, ft.Colors.BLACK),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
            border_radius=20,
            content=ft.Text(f"{p.categoria} · {p.marca}".upper(), font_family=estilos.FUENTE_TEXTO,
                            size=12, color=ft.Colors.WHITE, style=ft.TextStyle(letter_spacing=1.5)),
        )

        panel_inferior = ft.Container(
            left=0, right=0, bottom=0,
            padding=20,
            bgcolor=ft.Colors.with_opacity(0.55, ft.Colors.BLACK),
            blur=ft.Blur(20, 20),
            content=ft.Column(
                tight=True,
                spacing=12,
                controls=[
                    ft.Text(p.nombre.upper(), font_family=estilos.FUENTE_TITULO, size=18,
                            weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE,
                            max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(formato_precio(p.precio), font_family=estilos.FUENTE_TITULO, size=24,
                                    weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Row(
                                tight=True,
                                spacing=6,
                                controls=[
                                    ft.Text("VER DETALLES", font_family=estilos.FUENTE_TEXTO, size=14,
                                            weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE,
                                            style=ft.TextStyle(letter_spacing=1)),
                                    ft.Icon(ft.Icons.ARROW_FORWARD, size=16, color=ft.Colors.WHITE),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        )

        return ft.Container(
            border_radius=25,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,   
            shadow=estilos.sombra_neu(),
            bgcolor=estilos.OSCURO,
            on_click=lambda e, prod=p: mostrar_producto(prod),
            content=ft.Stack(
                controls=[
                    ft.Image(src=p.imagen, fit=ft.BoxFit.COVER, left=0, top=0, right=0, bottom=0),
                    etiqueta,
                    panel_inferior,
                ],
            ),
        )

    def mostrar_catalogo(categoria):
        lista_productos = inventario.listar_productos(categoria)
        grid_productos.controls.clear()

        for p in lista_productos:
            grid_productos.controls.append(crear_tarjeta_producto(p))

        dropdown_filtro.value = categoria if categoria else "Todos"
        titulo_catalogo.value = categoria.upper() if categoria else "CATÁLOGO"
        cantidad = len(lista_productos)
        contador_catalogo.value = f"{cantidad} producto" + ("" if cantidad == 1 else "s")

        zona_productos.content = grid_productos if lista_productos else texto_vacio
        contenedor_principal.content = catalogo
        page.update()

    def mostrar_producto(producto):
        logging.info(f"Click en el producto: {producto.nombre} (ID: {producto.id})")
        stock = inventario.listar_stock(producto.id)
        producto_seleccionado.update({"id": producto.id, "color": None, "talle": None, "cantidad": None})

        agrupado = defaultdict(list)          
        hex_colores = {}                     
        for items in stock["diccionario"]:
            agrupado[items["color"]].append((items["talle"], items["cantidad"]))
            hex_colores[items["color"]] = items["hex"]

        fila_colores = ft.Row(spacing=10)
        fila_talles = ft.Row(spacing=14, run_spacing=14, wrap=True)
        txt_color = ft.Text("—", font_family=estilos.FUENTE_TEXTO, size=15, color=estilos.TEXTO_SUAVE)
        txt_talle = ft.Text("—", font_family=estilos.FUENTE_TEXTO, size=15, color=estilos.TEXTO_SUAVE)
        txt_cantidad = ft.Text("1", font_family=estilos.FUENTE_TITULO, size=22, weight=ft.FontWeight.BOLD,
                               color=estilos.TEXTO, width=40, text_align=ft.TextAlign.CENTER)
        txt_stock = ft.Text("", font_family=estilos.FUENTE_TEXTO, size=13, color=estilos.TEXTO_SUAVE)
        txt_error_cantidad = ft.Text("", font_family=estilos.FUENTE_TEXTO, size=12, color=ft.Colors.RED_400)

        def dibujar_colores():
            fila_colores.controls.clear()
            for color in agrupado:
                elegido = producto_seleccionado["color"] == color
                fila_colores.controls.append(
                    ft.Container(
                        width=56, height=56, border_radius=28, padding=5,
                        border=ft.Border.all(2, estilos.TEXTO if elegido else ft.Colors.TRANSPARENT),
                        tooltip=color,
                        on_click=lambda e, c=color: seleccion_color(c),
                        content=ft.Container(
                            border_radius=23,
                            bgcolor=hex_colores.get(color) or estilos.COLOR_CAMPO,
                            border=ft.Border.all(1, estilos.SOMBRA_OSCURA),
                        ),
                    )
                )

        def dibujar_talles():
            fila_talles.controls.clear()
            talles = agrupado.get(producto_seleccionado["color"], [])
            for talle, cantidad in talles:
                elegido = producto_seleccionado["talle"] is not None and producto_seleccionado["talle"][0] == talle
                fila_talles.controls.append(
                    ft.Container(
                        width=90, height=58, border_radius=18, alignment=ft.Alignment.CENTER,
                        bgcolor=estilos.OSCURO if elegido else estilos.BLANCO,
                        border=ft.Border.all(1, estilos.OSCURO if elegido else estilos.SOMBRA_OSCURA),
                        on_click=lambda e, t=talle, c=cantidad: seleccion_talle(t, c),
                        content=ft.Text(talle, font_family=estilos.FUENTE_TEXTO, size=15,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE if elegido else estilos.TEXTO),
                    )
                )

        def seleccion_color(color):
            producto_seleccionado["color"] = color
            producto_seleccionado["talle"] = None
            txt_color.value = color.upper()
            txt_talle.value = "—"
            panel_cantidad.visible = False
            boton_carrito.disabled = True
            boton_comprar.disabled = True
            dibujar_colores()
            dibujar_talles()
            page.update()

        def seleccion_talle(talle, cantidad_talle):
            producto_seleccionado["talle"] = (talle, cantidad_talle)
            txt_talle.value = talle
            txt_cantidad.value = "1"
            txt_error_cantidad.value = ""
            txt_stock.value = f"Stock disponible: {cantidad_talle}"
            panel_cantidad.visible = True
            boton_carrito.disabled = False
            boton_comprar.disabled = False
            dibujar_talles()
            page.update()

        def modificar_contador(delta: int):
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

        def agregar():
            producto_seleccionado["cantidad"] = int(txt_cantidad.value)
            resultado = carrito.agregar_carrito(producto_seleccionado)
            if resultado is not None:
                ventana_de_alerta(*resultado)
                return False
            actualizar_carrito()
            return True

        async def agregar_al_carrito(e=None):
            if agregar():
                await page.show_end_drawer()

        def comprar_ahora(e=None):
            if agregar():
                compra()

        def estilo_boton(fondo, texto, borde=None):
            return ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT: fondo, ft.ControlState.DISABLED: estilos.COLOR_CAMPO},
                color={ft.ControlState.DEFAULT: texto, ft.ControlState.DISABLED: estilos.TEXTO_SUAVE},
                padding=ft.Padding.symmetric(vertical=26),
                shape=ft.RoundedRectangleBorder(radius=22),
                side=ft.BorderSide(1, borde) if borde else None,
                text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, letter_spacing=1.5, size=15),
            )

        boton_carrito = ft.Button(
            content="AGREGAR AL CARRITO",
            icon=ft.Icons.SHOPPING_BAG_OUTLINED,
            disabled=True,
            on_click=agregar_al_carrito,
            style=estilo_boton(estilos.OSCURO, ft.Colors.WHITE),
        )
        boton_comprar = ft.Button(
            content="COMPRAR AHORA",
            disabled=True,
            on_click=comprar_ahora,
            style=estilo_boton(estilos.BLANCO, estilos.TEXTO, estilos.SOMBRA_OSCURA),
        )

        panel_cantidad = ft.Row(
            visible=False,
            spacing=15,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    bgcolor=estilos.BLANCO,
                    border_radius=18,
                    border=ft.Border.all(1, estilos.SOMBRA_OSCURA),
                    padding=ft.Padding.symmetric(horizontal=6),
                    content=ft.Row(
                        tight=True,
                        spacing=0,
                        controls=[
                            ft.IconButton(icon=ft.Icons.REMOVE, icon_color=estilos.TEXTO,
                                          on_click=lambda e: modificar_contador(-1)),
                            txt_cantidad,
                            ft.IconButton(icon=ft.Icons.ADD, icon_color=estilos.TEXTO,
                                          on_click=lambda e: modificar_contador(1)),
                        ],
                    ),
                ),
                ft.Column(spacing=2, controls=[txt_stock, txt_error_cantidad]),
            ],
        )

        etiqueta_negrita = lambda t: ft.Text(t, font_family=estilos.FUENTE_TEXTO, size=15,
                                             weight=ft.FontWeight.BOLD, color=estilos.TEXTO)
        divisor = ft.Divider(height=30, color=ft.Colors.with_opacity(0.5, ft.Colors.GREY))

        if not agrupado:
            boton_carrito.disabled = True
            boton_comprar.disabled = True
            bloque_opciones = ft.Text("No hay stock disponible de este producto",
                                      font_family=estilos.FUENTE_TEXTO, size=16, color=estilos.TEXTO_SUAVE)
        else:
            dibujar_colores()
            bloque_opciones = ft.Column(
                spacing=18,
                controls=[
                    ft.Row(tight=True, spacing=8, controls=[etiqueta_negrita("COLOR:"), txt_color]),
                    fila_colores,
                    ft.Row(tight=True, spacing=8, controls=[etiqueta_negrita("TALLE:"), txt_talle]),
                    fila_talles,
                    panel_cantidad,
                ],
            )

        informacion_producto = ft.Column(
            expand=1,
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text(f"{producto.categoria} · {producto.marca}".upper(), font_family=estilos.FUENTE_TEXTO,
                        size=14, color=estilos.TEXTO_SUAVE, style=ft.TextStyle(letter_spacing=2)),
                ft.Text(producto.nombre.upper(), font_family=estilos.FUENTE_TITULO, size=52,
                        weight=ft.FontWeight.BOLD, color=estilos.TEXTO, style=ft.TextStyle(height=0.95)),
                ft.Text(formato_precio(producto.precio), font_family=estilos.FUENTE_TITULO, size=36,
                        weight=ft.FontWeight.BOLD, color=estilos.TEXTO),
                divisor,
                bloque_opciones,
                ft.Divider(height=30, color=ft.Colors.with_opacity(0.5, ft.Colors.GREY)),
                boton_carrito,
                boton_comprar,
            ],
        )

        etiqueta_marca = ft.Container(
            left=24, top=24,
            padding=ft.Padding.symmetric(horizontal=16, vertical=6),
            bgcolor=ft.Colors.with_opacity(0.35, ft.Colors.BLACK),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
            border_radius=20,
            content=ft.Text(producto.marca.upper(), font_family=estilos.FUENTE_TEXTO, size=12,
                            color=ft.Colors.WHITE, style=ft.TextStyle(letter_spacing=1.5)),
        )
        imagen = ft.Container(
            expand=1,
            aspect_ratio=1,
            border_radius=25,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            bgcolor=estilos.OSCURO,
            content=ft.Stack(
                controls=[
                    ft.Image(src=producto.imagen, fit=ft.BoxFit.COVER, left=0, top=0, right=0, bottom=0),
                    etiqueta_marca,
                ],
            ),
        )

        tarjeta = estilos.reborde_neu(
            ft.Row(
                spacing=50,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[imagen, informacion_producto],
            )
        )
        tarjeta.padding = 40

        contenedor_principal.content = ft.Row(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Container(expand=1),
                ft.Container(
                    expand=6,
                    content=ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        controls=[ft.Container(padding=30, content=tarjeta)],   
                    ),
                ),
                ft.Container(expand=1),
            ],
        )
        page.update()

    def menu_filtro():
        categorias = inventario.listar_elementos_producto()[0]

        estilo_opcion = ft.ButtonStyle(color=estilos.TEXTO)   
        opciones = [ft.DropdownOption(key="Todos", text="FILTRAR: TODOS", style=estilo_opcion)]
        for c in categorias: 
            opciones += [ft.DropdownOption(key=c, text=f"FILTRAR: {c.upper()}", style=estilo_opcion)]

        def al_seleccionar(e):
            seleccion = e.control.value
            mostrar_catalogo(None if seleccion == "Todos" else seleccion)

        return ft.Dropdown(
            value="Todos",
            options=opciones,
            on_select=al_seleccionar,
            width=260,
            border_radius=15,
            border_color=estilos.SOMBRA_OSCURA,     
            border_width=1,
            filled=True,
            fill_color=estilos.FONDO,             
            bgcolor=estilos.FONDO,                 
            menu_style=ft.MenuStyle(bgcolor=estilos.FONDO),
            color=estilos.TEXTO,                  
            text_style=ft.TextStyle(color=estilos.TEXTO, font_family=estilos.FUENTE_TEXTO),
            text_size=14,
            trailing_icon=ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=estilos.TEXTO),
            selected_trailing_icon=ft.Icon(ft.Icons.ARROW_DROP_UP, color=estilos.TEXTO),
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
    carrito_texto=ft.Text("0", color=estilos.TEXTO)
    dropdown_filtro = menu_filtro()

    tarjetas_inferiores = ft.Container(
        expand=1,    
        content=generar_tarjetas_incio((
            ("Imagenes/Imagenes_UI/ui_remeras.png", "Remera"),
            ("Imagenes/Imagenes_UI/ui_pantalones.png", "Pantalón"),
            ("Imagenes/Imagenes_UI/ui_camperas.png", "Campera"),
        )),
    )

    parte_superior_izquierda = ft.Container(content=ft.Image(src="Imagenes/Imagenes_UI/letras_inicio.png", fit=ft.BoxFit.COVER), expand=True)
    parte_superior_derecha = ft.Container(content=ft.Image(src="Imagenes/Imagenes_UI/imagen_inicio.jpg", fit=ft.BoxFit.COVER, border_radius=20), expand=True)
    parte_superior_inferior = ft.Container(content=generar_tarjetas_superior(
        (
            ("Imagenes/Imagenes_UI/primeras_marcas.png"),
            ("Imagenes/Imagenes_UI/atencion.png"),
            ("Imagenes/Imagenes_UI/algodon.png"),
            ("Imagenes/Imagenes_UI/sucursales.png"),
        )
    ), expand=True)

    parte_superior = estilos.reborde_neu(
        ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    expand=4,                    
                    spacing=40,
                    controls=[parte_superior_izquierda, parte_superior_derecha],
                ),
                ft.Divider(color=ft.Colors.with_opacity(0.5, ft.Colors.GREY)),
                parte_superior_inferior,          
            ],
        ),
        expand=3,                                 
    )

    parte_superior.padding=50

    inicio = ft.Row(
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,   
        controls=[
            ft.Container(expand=2),                         
            ft.Container(
                expand=5,                                    
                content=ft.Column(
                    expand=True,
                    spacing=30,
                    controls=[parte_superior, tarjetas_inferiores],
                ),
            ),
            ft.Container(expand=2),                          
        ],
    )


    grid_productos = ft.GridView(
        expand=True,
        max_extent=320,
        child_aspect_ratio=0.8,
        spacing=30,
        run_spacing=30,
        padding=30,          
    )

    titulo_catalogo = ft.Text("CATÁLOGO", font_family=estilos.FUENTE_TITULO, size=40,
                              weight=ft.FontWeight.BOLD, color=estilos.TEXTO)
    contador_catalogo = ft.Text("", font_family=estilos.FUENTE_TEXTO, size=14, color=estilos.TEXTO_SUAVE)

    barra_catalogo = estilos.reborde_neu(
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(spacing=0, controls=[titulo_catalogo, contador_catalogo]),
                dropdown_filtro,
            ],
        )
    )

    zona_productos = ft.Container(expand=True)
    texto_vacio = ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        content=ft.Text("No hay productos en esta categoría", font_family=estilos.FUENTE_TEXTO,
                        size=20, color=estilos.TEXTO_SUAVE),
    )

    catalogo = ft.Row(
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Container(expand=1),
            ft.Container(
                expand=6,
                content=ft.Column(expand=True, spacing=10, controls=[barra_catalogo, zona_productos]),
            ),
            ft.Container(expand=1),
        ],
    )

    contenedor_principal = ft.Container(
        content=None,
        expand=True,
        padding=ft.Padding.only(top=100, left=20, right=20, bottom=20)
    )

    carrito_boton=[carrito_texto, ft.IconButton(icon=ft.Icons.SHOPPING_BAG, on_click=mostrar_carrito,style=ft.ButtonStyle(color=estilos.TEXTO))]
    botonera_centro=[
    ft.TextButton(content=ft.Text("Inicio", font_family=estilos.FUENTE_TEXTO, color=estilos.TEXTO_SUAVE), on_click=lambda: mostrar_inicio()),                
    ft.TextButton(content=ft.Text("Catálogo", font_family=estilos.FUENTE_TEXTO, color=estilos.TEXTO_SUAVE), on_click=lambda: mostrar_catalogo(None)),
    ft.TextButton(content=ft.Text("Cerrar Sesión", font_family=estilos.FUENTE_TEXTO, color=estilos.TEXTO_SUAVE), on_click=ir_a_login)]
    
    header=estilos.construir_header(carrito_boton, botonera_centro)

    actualizar_carrito()
    mostrar_inicio()

    return [ft.Stack(
        expand=True,
        controls=[
        ft.Row(
            controls=[
                contenedor_principal,
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        ),
        header,
        ])
    ]