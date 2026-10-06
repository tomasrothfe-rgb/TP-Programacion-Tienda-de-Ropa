import flet as ft
import logging 
import os
import sys
import estilos
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clases import Inventario,Usuario,Carrito  
from email_validator import validate_email, EmailNotValidError


logging.basicConfig(level=logging.INFO)

def ClienteVista(page, ir_a_login, ir_a_compra, usuario):
    inventario = Inventario()
    producto_seleccionado={"id":None,"color":None,"talle":None, "cantidad":None}
    carrito = Carrito(usuario.id) 

    def compra():
        ir_a_compra(usuario)
        
    def ventana_de_alerta(texto_superior, erratas):
        return estilos.ventana_de_alerta(page, texto_superior, erratas)

    def tarjeta_item_carrito(item, info):
        return ft.Container(
            padding=14,
            bgcolor="#F8FAFC",
            border=ft.Border.all(1, estilos.SOMBRA_OSCURA),
            border_radius=18,
            content=ft.Row(
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(src=info["url"], width=64, height=64, fit=ft.BoxFit.COVER, border_radius=12),
                    ft.Column(
                        expand=True,
                        spacing=3,
                        controls=[
                            ft.Text(f"{info['nombre']}".upper(), font_family=estilos.FUENTE_TITULO, size=13,
                                    weight=ft.FontWeight.BOLD, color=estilos.TEXTO,
                                    max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                            ft.Text(f"{item[3]} / TALLE {item[4]}".upper(), font_family=estilos.FUENTE_TEXTO,
                                    size=11, color=estilos.TEXTO_SUAVE),
                            ft.Text(f"{formato_precio(info['precio'])} x {item[5]}", font_family=estilos.FUENTE_TEXTO,
                                    size=13, weight=ft.FontWeight.BOLD, color=estilos.TEXTO),
                        ],
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=estilos.TEXTO_SUAVE,
                        tooltip="Eliminar del carrito",
                        on_click=lambda e, it=item: eliminar_carrito(e, it),
                    ),
                ],
            ),
        )

    def actualizar_carrito():
        columna_carrito.controls.clear()
        lista = carrito.listar_carrito()
        total = 0
        unidades = 0

        for i in lista:
            info = inventario.consultar_producto_especifico(i[2])
            columna_carrito.controls.append(tarjeta_item_carrito(i, info))
            total += info["precio"] * int(i[5])
            unidades += int(i[5])

        if not lista:
            columna_carrito.controls.append(
                ft.Container(
                    padding=ft.Padding.only(top=60),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Tu carrito está vacío", font_family=estilos.FUENTE_TEXTO,
                                    size=16, color=estilos.TEXTO_SUAVE),
                )
            )

        carrito_texto.value = str(unidades)
        total_carrito.value = formato_precio(total)
        boton_finalizar_compra.disabled = not lista
        page.update()

    def abrir_carrito(e=None):
        fondo_carrito.visible = True
        panel_carrito.offset = ft.Offset(0, 0)
        page.update()

    def cerrar_carrito(e=None):
        fondo_carrito.visible = False
        panel_carrito.offset = ft.Offset(1, 0)
        page.update()

    def mostrar_carrito(e=None):
        abrir_carrito()

    def iniciar_compra(e=None):
        compra()

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

        def agregar_al_carrito(e=None):
            if agregar():
                abrir_carrito()

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


    def texto_perfil(valor, size=14, color=estilos.TEXTO, bold=False, titulo=False, **kwargs):
        return ft.Text(
            valor,
            size=size,
            color=color,
            weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
            font_family=estilos.FUENTE_TITULO if titulo else estilos.FUENTE_TEXTO,
            **kwargs,
        )

    def pantalla_perfil(controles):
        contenedor_principal.content = ft.Row(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Container(expand=2),
                ft.Container(
                    expand=5,
                    content=ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        controls=[
                            ft.Container(
                                padding=30,
                                content=ft.Column(
                                    spacing=25,
                                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                                    controls=controles,
                                ),
                            )
                        ],
                    ),
                ),
                ft.Container(expand=2),
            ],
        )
        page.update()

    def boton_volver_perfil():
        return ft.TextButton(
            content=ft.Row(
                tight=True,
                spacing=6,
                controls=[
                    ft.Icon(ft.Icons.ARROW_BACK, size=16, color=estilos.TEXTO_SUAVE),
                    texto_perfil("Volver al perfil", color=estilos.TEXTO_SUAVE),
                ],
            ),
            on_click=lambda e: mostrar_perfil(),
        )

    def opcion_perfil(icono, titulo, descripcion, accion):
        tarjeta = estilos.reborde_neu(
            ft.Column(
                spacing=14,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Container(
                        content=ft.Icon(icono, color=estilos.FONDO, size=26),
                        width=56,
                        height=56,
                        bgcolor=estilos.OSCURO,
                        border_radius=16,
                        alignment=ft.Alignment.CENTER,
                    ),
                    texto_perfil(titulo.upper(), size=18, bold=True, titulo=True),
                    texto_perfil(descripcion, size=13, color=estilos.TEXTO_SUAVE),
                ],
            ),
            on_click=lambda e: accion(),
            expand=True,
        )
        tarjeta.height = 220
        return tarjeta

    def mostrar_perfil():
        datos = Usuario.obtener_datos(usuario.id) or {"nombre": "", "apellido": "", "email": ""}
        inicial = (datos["nombre"][:1] or "?").upper()

        tarjeta_datos = estilos.reborde_neu(
            ft.Row(
                spacing=24,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        content=texto_perfil(inicial, size=34, bold=True, titulo=True, color=estilos.FONDO),
                        width=80,
                        height=80,
                        bgcolor=estilos.OSCURO,
                        border_radius=40,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column(
                        spacing=2,
                        controls=[
                            texto_perfil("MI PERFIL", size=12, color=estilos.TEXTO_SUAVE),
                            texto_perfil(f"{datos['nombre']} {datos['apellido']}".upper(), size=30, bold=True, titulo=True),
                            texto_perfil(datos["email"], size=14, color=estilos.TEXTO_SUAVE),
                        ],
                    ),
                ],
            )
        )
        tarjeta_datos.padding = 30

        pantalla_perfil([
            tarjeta_datos,
            ft.Row(
                spacing=25,
                controls=[
                    opcion_perfil(
                        ft.Icons.MANAGE_ACCOUNTS,
                        "Modificar datos de la cuenta",
                        "Cambiá tu nombre, correo o contraseña.",
                        mostrar_modificar_datos,
                    ),
                    opcion_perfil(
                        ft.Icons.RECEIPT_LONG,
                        "Ver compras",
                        "Revisá el historial de tus pedidos.",
                        mostrar_compras,
                    ),
                ],
            ),
        ])

    def mostrar_modificar_datos():
        datos = Usuario.obtener_datos(usuario.id) or {"nombre": "", "apellido": "", "email": ""}
        nombre_ref = ft.Ref[ft.TextField]()
        apellido_ref = ft.Ref[ft.TextField]()
        correo_ref = ft.Ref[ft.TextField]()
        actual_ref = ft.Ref[ft.TextField]()
        nueva_ref = ft.Ref[ft.TextField]()

        def guardar():
            nombre = (nombre_ref.current.value or "").strip()
            apellido = (apellido_ref.current.value or "").strip()
            correo = (correo_ref.current.value or "").strip()
            actual = (actual_ref.current.value or "").strip()
            nueva = (nueva_ref.current.value or "").strip()

            if not nombre or not apellido or not correo:
                ventana_de_alerta("ERROR AL MODIFICAR DATOS", "INGRESE TODOS LOS CAMPOS")
                return
            if not nombre.replace(" ", "").isalpha() or not apellido.replace(" ", "").isalpha():
                ventana_de_alerta("ERROR AL MODIFICAR DATOS", "EL NOMBRE Y EL APELLIDO SOLO PUEDEN CONTENER LETRAS")
                return
            try:
                correo = validate_email(correo, check_deliverability=False).normalized
            except EmailNotValidError:
                ventana_de_alerta("ERROR AL MODIFICAR DATOS", "INGRESE UN CORREO ELECTRÓNICO VÁLIDO")
                return
            if nueva and len(nueva) < 8:
                ventana_de_alerta("ERROR AL MODIFICAR DATOS", "LA CONTRASEÑA DEBE TENER AL MENOS 8 CARACTERES")
                return

            resultado = Usuario.modificar_datos(usuario.id, nombre, apellido, correo, actual, nueva)
            if resultado is not None:
                ventana_de_alerta(*resultado)
                return

            usuario.nombre = nombre
            usuario.apellido = apellido
            usuario.email = correo
            actual_ref.current.value = ""
            nueva_ref.current.value = ""
            ventana_de_alerta("DATOS ACTUALIZADOS", "TUS DATOS SE GUARDARON CORRECTAMENTE")
            page.update()

        formulario = estilos.reborde_neu(
            ft.Column(
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Row(
                        spacing=20,
                        controls=[
                            ft.Container(
                                expand=True,
                                content=estilos.campo_datos("Nombre", "Mario", ref=nombre_ref, value=datos["nombre"]),
                            ),
                            ft.Container(
                                expand=True,
                                content=estilos.campo_datos("Apellido", "Pérez", ref=apellido_ref, value=datos["apellido"]),
                            ),
                        ],
                    ),
                    estilos.campo_datos("Correo electrónico", "ejemplo@correo.com", ref=correo_ref, value=datos["email"]),
                    ft.Divider(color=ft.Colors.with_opacity(0.5, ft.Colors.GREY)),
                    texto_perfil("CAMBIAR CONTRASEÑA (OPCIONAL)", size=13, bold=True, color=estilos.TEXTO_SUAVE),
                    ft.Row(
                        spacing=20,
                        controls=[
                            ft.Container(
                                expand=True,
                                content=estilos.campo_datos(
                                    "Contraseña actual", "********", ref=actual_ref,
                                    password=True, can_reveal_password=True,
                                ),
                            ),
                            ft.Container(
                                expand=True,
                                content=estilos.campo_datos(
                                    "Contraseña nueva", "Mínimo 8 caracteres", ref=nueva_ref,
                                    password=True, can_reveal_password=True,
                                ),
                            ),
                        ],
                    ),
                    ft.Button("Guardar cambios", style=estilos.boton_presionado(), on_click=lambda e: guardar()),
                ],
            )
        )
        formulario.padding = 40

        pantalla_perfil([
            boton_volver_perfil(),
            texto_perfil("MODIFICAR DATOS", size=40, bold=True, titulo=True),
            formulario,
        ])

    def tarjeta_compra(compra):
        filas = []
        for a in compra["articulos"]:
            filas.append(
                ft.Container(
                    padding=ft.Padding.symmetric(vertical=10),
                    border=ft.Border.only(bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.5, estilos.SOMBRA_OSCURA))),
                    content=ft.Row(
                        spacing=14,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Column(
                                expand=True,
                                spacing=2,
                                controls=[
                                    texto_perfil(a["nombre"].upper(), size=14, bold=True, titulo=True),
                                    texto_perfil(
                                        f"{a['categoria']} · {a['marca']} · {a['color']} / TALLE {a['talle']}".upper(),
                                        size=11, color=estilos.TEXTO_SUAVE,
                                    ),
                                ],
                            ),
                            texto_perfil(f"{formato_precio(a['precio'])} x {a['cantidad']}", size=13, bold=True),
                        ],
                    ),
                )
            )

        metodo = "TARJETA" if compra["metodo_pago"] == "tarjeta" else "TRANSFERENCIA"
        envio = "ENVÍO A DOMICILIO" if compra["tipo_envio"] == "envio" else "RETIRO EN LOCAL"

        tarjeta = estilos.reborde_neu(
            ft.Column(
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    texto_perfil(f"ORDEN #{compra['id']}", size=20, bold=True, titulo=True),
                                    texto_perfil(compra["fecha"], size=12, color=estilos.TEXTO_SUAVE),
                                ],
                            ),
                            texto_perfil(formato_precio(compra["total"]), size=24, bold=True, titulo=True),
                        ],
                    ),
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Container(
                                content=texto_perfil(t, size=10, bold=True, color=estilos.TEXTO),
                                bgcolor=estilos.BLANCO,
                                border=ft.Border.all(1, estilos.SOMBRA_OSCURA),
                                border_radius=20,
                                padding=ft.Padding.symmetric(horizontal=12, vertical=4),
                            )
                            for t in (metodo, envio)
                        ],
                    ),
                    *filas,
                ],
            )
        )
        tarjeta.padding = 30
        return tarjeta

    def mostrar_compras():
        compras = Usuario.listar_compras(usuario.id)
        if compras:
            contenido = [tarjeta_compra(c) for c in compras]
        else:
            contenido = [
                ft.Container(
                    padding=ft.Padding.only(top=40),
                    alignment=ft.Alignment.CENTER,
                    content=texto_perfil("Todavía no realizaste compras", size=18, color=estilos.TEXTO_SUAVE),
                )
            ]

        cantidad = len(compras)
        pantalla_perfil([
            boton_volver_perfil(),
            texto_perfil("MIS COMPRAS", size=40, bold=True, titulo=True),
            texto_perfil(f"{cantidad} compra" + ("" if cantidad == 1 else "s"), size=14, color=estilos.TEXTO_SUAVE),
            *contenido,
        ])

    columna_carrito = ft.ListView(expand=True, spacing=14, padding=ft.Padding.all(24))
    total_carrito = ft.Text("$0", font_family=estilos.FUENTE_TITULO, size=26,
                            weight=ft.FontWeight.BOLD, color=estilos.TEXTO)

    boton_finalizar_compra = ft.Button(
        content="INICIAR COMPRA SEGURA",
        disabled=True,
        on_click=iniciar_compra,
        style=ft.ButtonStyle(
            bgcolor={ft.ControlState.DEFAULT: estilos.OSCURO, ft.ControlState.DISABLED: estilos.COLOR_CAMPO},
            color={ft.ControlState.DEFAULT: ft.Colors.WHITE, ft.ControlState.DISABLED: estilos.TEXTO_SUAVE},
            padding=ft.Padding.symmetric(vertical=24),
            shape=ft.RoundedRectangleBorder(radius=30),
            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, letter_spacing=1.5, size=14),
        ),
    )

    encabezado_carrito = ft.Container(
        padding=ft.Padding.symmetric(horizontal=24, vertical=18),
        border=ft.Border.only(bottom=ft.BorderSide(1, estilos.SOMBRA_OSCURA)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("TU CARRITO DE COMPRAS", font_family=estilos.FUENTE_TITULO, size=20,
                        weight=ft.FontWeight.BOLD, color=estilos.TEXTO),
                ft.IconButton(icon=ft.Icons.CLOSE, icon_color=estilos.TEXTO, on_click=cerrar_carrito),
            ],
        ),
    )

    pie_carrito = ft.Container(
        padding=24,
        bgcolor="#F8FAFC",
        border=ft.Border.only(top=ft.BorderSide(1, estilos.SOMBRA_OSCURA)),
        content=ft.Column(
            tight=True,
            spacing=18,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("SUBTOTAL", font_family=estilos.FUENTE_TEXTO, size=12,
                                color=estilos.TEXTO_SUAVE, style=ft.TextStyle(letter_spacing=1)),
                        total_carrito,
                    ],
                ),
                boton_finalizar_compra,
            ],
        ),
    )

    fondo_carrito = ft.Container(
        left=0, right=0, top=0, bottom=0,
        bgcolor=ft.Colors.with_opacity(0.35, ft.Colors.BLACK),
        blur=ft.Blur(8, 8),
        visible=False,
        on_click=cerrar_carrito,
    )

    panel_carrito = ft.Container(
        right=0, top=0, bottom=0,
        width=450,
        bgcolor=ft.Colors.WHITE,
        offset=ft.Offset(1, 0),
        animate_offset=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        content=ft.Column(
            spacing=0,
            controls=[encabezado_carrito, columna_carrito, pie_carrito],
        ),
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

    ALTO_MINIMO_INICIO = 700
    MARGEN_INICIO = 30
    RESERVADO_INICIO = 100 + 20 + 2 * MARGEN_INICIO

    def alto_inicio(alto_ventana):
        return max(ALTO_MINIMO_INICIO, alto_ventana - RESERVADO_INICIO)

    contenido_inicio = ft.Container(
        height=alto_inicio(page.height or 0),
        content=ft.Column(expand=True, spacing=30, controls=[parte_superior, tarjetas_inferiores]),
    )

    inicio = ft.Row(
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Container(expand=2),
            ft.Container(
                expand=5,
                content=ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[ft.Container(padding=MARGEN_INICIO, content=contenido_inicio)],
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

    def ajustar_alto_inicio(e):
        nuevo_alto = alto_inicio(e.height)
        if contenido_inicio.height != nuevo_alto:
            contenido_inicio.height = nuevo_alto
            page.update()

    contenedor_principal.on_size_change = ajustar_alto_inicio

    carrito_boton=[carrito_texto, ft.IconButton(icon=ft.Icons.SHOPPING_BAG, on_click=mostrar_carrito,style=ft.ButtonStyle(color=estilos.TEXTO))]
    botonera_centro=[
    ft.TextButton(content=ft.Text("Inicio", font_family=estilos.FUENTE_TEXTO, color=estilos.TEXTO_SUAVE), on_click=lambda: mostrar_inicio()),                
    ft.TextButton(content=ft.Text("Catálogo", font_family=estilos.FUENTE_TEXTO, color=estilos.TEXTO_SUAVE), on_click=lambda: mostrar_catalogo(None)),
    ft.TextButton(content=ft.Text("Perfil", font_family=estilos.FUENTE_TEXTO, color=estilos.TEXTO_SUAVE), on_click=lambda e: mostrar_perfil()),
    ft.TextButton(content=ft.Text("Cerrar Sesión", font_family=estilos.FUENTE_TEXTO, color=estilos.TEXTO_SUAVE), on_click=ir_a_login)]
    
    header=estilos.construir_header(carrito_boton, botonera_centro)

    def revisar_alerta():
        mensaje = Usuario.revisar_alerta(usuario.id)
        if mensaje:
            ventana_de_alerta("AVISO", mensaje)

    actualizar_carrito()
    mostrar_inicio()
    revisar_alerta()

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
        fondo_carrito,
        panel_carrito,
        ])
    ]