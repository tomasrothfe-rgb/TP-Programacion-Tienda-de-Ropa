import flet as ft
import flet_color_pickers as fcp
import logging
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import estilos
from clases import Inventario, Usuario

logging.basicConfig(level=logging.INFO)

BORDE_CLARO = ft.Colors.with_opacity(0.6, ft.Colors.WHITE)  # Color de borde claro para tarjetas


def AdminVista(page, ir_a_login, usuario):  # Arma el panel de administración

    inventario = Inventario()
    producto_en_seleccion = None  # Id del producto elegido en la grilla
    tarjeta_seleccionada_ref = None

    def texto(valor, size=14, color=estilos.TEXTO, bold=False, titulo=False, **kwargs):  # Crea un texto con el estilo del panel
        return ft.Text(
            valor,
            size=size,
            color=color,
            weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
            font_family=estilos.FUENTE_TITULO if titulo else estilos.FUENTE_TEXTO,
            **kwargs,
        )

    def etiqueta(valor):  # Texto chico en mayúsculas para secciones
        return texto(valor.upper(), size=11, color=estilos.TEXTO_SUAVE, bold=True)

    def boton(contenido, icono, accion, tipo="secundario"):  # Botón del menú; el tipo cambia el color
        if tipo == "primario":
            fondo, color_texto, borde = estilos.TEXTO, estilos.FONDO, ft.BorderSide(1, estilos.TEXTO)
        elif tipo == "peligro":
            fondo, color_texto, borde = "#FEE2E2", "#DC2626", ft.BorderSide(1, "#FECACA")
        else:
            fondo, color_texto, borde = estilos.BLANCO, estilos.TEXTO, ft.BorderSide(1, estilos.SOMBRA_OSCURA)

        return ft.Button(
            content=ft.Text(
                contenido.upper(),
                size=11,
                weight=ft.FontWeight.W_600,
                font_family=estilos.FUENTE_TEXTO,
            ),
            icon=icono,
            on_click=lambda e: accion(),
            style=ft.ButtonStyle(
                bgcolor=fondo,
                color=color_texto,
                side=borde,
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=ft.Padding.symmetric(horizontal=16, vertical=16),
                overlay_color=ft.Colors.with_opacity(0.08, estilos.TEXTO),
            ),
        )

    def caja_campo(control):  # Caja con fondo para un campo
        return ft.Container(
            content=control,
            bgcolor=estilos.COLOR_CAMPO,
            border_radius=14,
            padding=ft.Padding.symmetric(horizontal=12),
            border=ft.Border.all(1, BORDE_CLARO),
        )

    def campo_texto(titulo, hint="", valor=None, **kwargs):  # Campo de texto con título; devuelve (columna, campo)
        entrada = ft.TextField(
            hint_text=hint,
            value=valor,
            border=ft.InputBorder.NONE,
            text_size=13,
            color=estilos.TEXTO,
            **kwargs,
        )
        return ft.Column(
            controls=[etiqueta(titulo), caja_campo(entrada)],
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ), entrada

    def campo_selector(titulo, opciones, valor, al_elegir):  # Lista desplegable con título
        selector = ft.Dropdown(
            value=valor,
            hint_text="Seleccionar",
            options=[ft.DropdownOption(key=o, text=o.upper()) for o in opciones],
            on_select=lambda e: al_elegir(e.control.value),
            border=ft.InputBorder.NONE,
            text_size=13,
            color=estilos.TEXTO,
        )
        selector.expand = True
        return ft.Column(
            controls=[etiqueta(titulo), caja_campo(ft.Row(controls=[selector]))],
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ), selector

    def mostrar_panel(titulo, controles, subtitulo="Formulario Jupiter"):  # Reemplaza el contenido central por un formulario
        contenedor_principal.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    etiqueta(subtitulo),
                                    texto(titulo.upper(), size=28, bold=True, titulo=True),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            boton("Cancelar", ft.Icons.CLOSE, lambda: mostrar(None)),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    ft.Divider(color=estilos.SOMBRA_OSCURA),
                    *controles,
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=20,
                expand=True,
            ),
            bgcolor=estilos.FONDO,
            shadow=estilos.sombra_neu(12, 24),
            border=ft.Border.all(1, BORDE_CLARO),
            border_radius=32,
            padding=30,
            expand=True,
            margin=ft.Margin.only(right=14, bottom=14),
        )
        page.update()

    def fila_botones(funcion_confirmar, texto_confirmar="Confirmar"):  # Botones Cancelar y Confirmar de los formularios
        return ft.Row(
            controls=[
                boton("Cancelar", None, lambda: mostrar(None)),
                boton(texto_confirmar, ft.Icons.SAVE, funcion_confirmar, "primario"),
            ],
            alignment=ft.MainAxisAlignment.END,
        )

    def ventana_de_alerta(texto_superior, erratas):  # Atajo para mostrar avisos en esta pantalla
        return estilos.ventana_de_alerta(page, texto_superior, erratas)

    def formulario_producto(texto_superior, datos=None):  # Formulario para agregar o modificar un producto
        modificando = datos is not None

        async def seleccionar_archivo(e):  # Abre el selector de archivos para elegir la imagen PNG
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
                    icono_preview.visible=False
                    elementos_seleccionados["imagen"] = archivo.path
                    resultado_texto.value = "Archivo seleccionado con exito"
                    resultado_texto.color = ft.Colors.GREEN_600

                else:
                    elementos_seleccionados["imagen"] = datos["url"] if modificando else None
                    resultado_texto.value = "Error NO es un archivo PNG."
                    resultado_texto.color = ft.Colors.RED_600
                    ventana_de_alerta("ERROR AL SELECIONAR IMAGEN","LA IMAGEN PROPORCIONADA NO CUMPLE CON EL FORMATO")

            page.update()

        def confirmar_click():  # Valida y guarda el producto (nuevo o modificado)
            nonlocal producto_en_seleccion
            if elementos_seleccionados["categorias"] == None or elementos_seleccionados["marcas"] == None:
                ventana_de_alerta("ELEMENTOS INCOMPLETOS", "ASEGURESE DE COMPLETAR TODOS LOS ELEMENTOS REQUERIDOS")
                return

            if modificando:
                if not nombre.value or not nombre.value.strip():
                    ventana_de_alerta("ELEMENTOS INCOMPLETOS", "EL PRODUCTO DEBE TENER UN NOMBRE")
                    return
                retorno = inventario.modificar_producto(
                    datos["id"],
                    elementos_seleccionados["categorias"],
                    elementos_seleccionados["marcas"],
                    nombre.value.strip(),
                    precio.value,
                    elementos_seleccionados["imagen"],
                )
            else:
                retorno = inventario.agregar_producto(
                    elementos_seleccionados["categorias"],
                    elementos_seleccionados["marcas"],
                    nombre.value,
                    precio.value,
                    elementos_seleccionados["imagen"],
                )

            if isinstance(retorno, tuple):
                ventana_de_alerta(*retorno)
                return

            if not modificando and check_stock.value:
                producto_en_seleccion = retorno
                mostrar(None)
                agregar_stock()
            else:
                mostrar(None)

        def elegir(clave, valor):  # Guarda la categoría o marca elegida en el desplegable
            elementos_seleccionados[clave] = valor

        elementos= inventario.listar_elementos_producto()
        elementos_seleccionados={
            "categorias": datos["categoria"] if modificando else None,
            "marcas": datos["marca"] if modificando else None,
            "imagen": datos["url"] if modificando else None,
        }
        resultado_texto = texto(
            "Ningún archivo nuevo seleccionado" if modificando else "Ningún archivo seleccionado",
            size=12, color=estilos.TEXTO_SUAVE,
        )
        imagen_preview=ft.Image(
             src=datos["url"] if modificando else "",
             fit=ft.BoxFit.COVER,
             visible=modificando,
        )
        icono_preview = ft.Icon(ft.Icons.IMAGE, color=estilos.TEXTO_SUAVE, visible=not modificando)
        vista_previa = ft.Container(
            content=ft.Stack(
                controls=[
                    ft.Container(content=icono_preview, alignment=ft.Alignment.CENTER, expand=True),
                    imagen_preview,
                ],
            ),
            width=90,
            height=90,
            bgcolor=estilos.COLOR_CAMPO,
            border_radius=16,
            border=ft.Border.all(1, BORDE_CLARO),
            shadow=estilos.sombra_neu(4, 8),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        columna_nombre, nombre = campo_texto(
            "Nombre del producto *", "Nombre", datos["nombre"] if modificando else None
        )
        columna_precio, precio = campo_texto(
            "Precio *", "Precio", str(datos["precio"]) if modificando else None
        )
        columna_marca, _ = campo_selector(
            "Marca *", elementos[1], datos["marca"] if modificando else None,
            lambda v: elegir("marcas", v),
        )
        columna_categoria, _ = campo_selector(
            "Categoría *", elementos[0], datos["categoria"] if modificando else None,
            lambda v: elegir("categorias", v),
        )
        boton_archivo = boton("Seleccionar archivo", ft.Icons.UPLOAD_FILE, lambda: None)
        boton_archivo.on_click = seleccionar_archivo
        check_stock = ft.Checkbox(
            label="Agregar stock al crear el producto",
            value=False,
            active_color=estilos.TEXTO,
        )

        for columna in (columna_nombre, columna_precio, columna_marca, columna_categoria):
            columna.expand = True

        controles = [
            ft.Row(controls=[columna_nombre, columna_precio], spacing=20),
            ft.Row(controls=[columna_marca, columna_categoria], spacing=20),
            ft.Row(
                controls=[
                    boton("Nueva marca", ft.Icons.ADD, lambda: agregar("marca")),
                    boton("Nueva categoría", ft.Icons.ADD, lambda: agregar("categoria")),
                ],
                spacing=12,
            ),
            ft.Column(
                controls=[
                    etiqueta("Imagen (PNG)"),
                    ft.Row(
                        controls=[
                            vista_previa,
                            ft.Column(
                                controls=[
                                    boton_archivo,
                                    resultado_texto,
                                ],
                                spacing=8,
                            ),
                        ],
                        spacing=20,
                    ),
                ],
                spacing=8,
            ),
        ]
        if not modificando:
            controles.append(check_stock)
        controles.append(ft.Divider(color=estilos.SOMBRA_OSCURA))
        controles.append(fila_botones(confirmar_click, "Guardar producto"))

        mostrar_panel(texto_superior, controles)

    def modificar():  # Abre el formulario con los datos del producto elegido
        if producto_en_seleccion is None:
            ventana_de_alerta("ERROR DE SELECCION", "NO SE SELECCIONO NINGUN PRODUCTO PARA MODIFICAR")
            return
        datos = inventario.consultar_producto_especifico(producto_en_seleccion)
        formulario_producto("MODIFICAR PRODUCTO", datos)

    def eliminar():  # Pide confirmación y elimina el producto elegido
        def confirmar_click():  # Elimina el producto y vuelve a la grilla
             nonlocal producto_en_seleccion
             retorno = inventario.eliminar_producto(producto_en_seleccion)
             if isinstance(retorno, tuple):
                 ventana_de_alerta(*retorno)
                 return
             producto_en_seleccion = None
             mostrar(None)

        if producto_en_seleccion==None:
            ventana_de_alerta("ERROR DE SELECCION", "NO SE SELECCIONO NINGUN PRODUCTO PARA ELIMINAR")
        else:
             nombre_producto = inventario.consultar_producto_especifico(producto_en_seleccion)["nombre"]
             mostrar_panel(
                 "ELIMINAR PRODUCTO",
                 [
                     ft.Container(
                         content=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color="#DC2626", size=36),
                         width=64,
                         height=64,
                         bgcolor="#FEE2E2",
                         border_radius=16,
                         alignment=ft.Alignment.CENTER,
                     ),
                     texto(f"¿ESTA SEGURO DE ELIMINAR \"{nombre_producto}\" DE LA TIENDA?", size=15),
                     ft.Row(
                         controls=[
                             boton("Cancelar", None, lambda: mostrar(None)),
                             boton("Sí, eliminar", ft.Icons.DELETE, confirmar_click, "peligro"),
                         ],
                     ),
                 ],
                 "Confirmación",
             )

    def agregar_stock(color_inicial=None):  # Formulario para cargar stock por color y talle
        if not producto_en_seleccion:
            ventana_de_alerta("ERROR DE SELECCION","NO SE SELECCIONO EL PRODUCTO PARA AGREGAR STOCK")
            return

        nombre_producto = inventario.consultar_producto_especifico(producto_en_seleccion)["nombre"]
        colores = inventario.listar_colores()
        talles = inventario.listar_talles()
        variantes = inventario.listar_stock(producto_en_seleccion)["diccionario"]
        color_seleccionado = None

        tabla_talles = ft.Column(visible=False, spacing=12)
        lista_disponibles = ft.Column(visible=False, spacing=4)
        campos_stock = {}

        def confirmar_click():  # Junta las cantidades ingresadas y las guarda
            if color_seleccionado is None:
                ventana_de_alerta("ERROR DE STOCK","DEBE SELECCIONAR UN COLOR")
                return

            lista = []

            for talle, i in campos_stock.items():
                if i.value:
                    lista.append({"id": producto_en_seleccion,"color": color_seleccionado,"talle": talle,"cantidad": i.value})

            if not lista:
                ventana_de_alerta("ERROR DE STOCK","DEBE INGRESAR AL MENOS UNA CANTIDAD")
                return

            retorno = inventario.agregar_stock(lista)

            if retorno is not None:
                ventana_de_alerta(*retorno)
            else:
                agregar_stock(color_seleccionado)

        def seleccionar_color(color):  # Muestra los talles y el stock actual del color elegido
            nonlocal color_seleccionado
            tabla_talles.controls.clear()
            lista_disponibles.controls.clear()
            campos_stock.clear()
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
                    width=70,
                    text_align=ft.TextAlign.CENTER,
                    text_size=13,
                    color=estilos.TEXTO,
                    cursor_color=estilos.TEXTO,
                    border=ft.InputBorder.NONE,
                    content_padding=8,
                    keyboard_type=ft.KeyboardType.NUMBER,
                )

                campos_stock[talle] = campo

                controles_talles.append(
                    ft.Container(
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=6,
                            controls=[
                                texto(f"Talle {talle}", size=16, bold=True, titulo=True),
                                texto(f"Actual: {cantidad}", size=12, color=estilos.TEXTO_SUAVE),
                                caja_campo(campo),
                            ]
                        ),
                        bgcolor=estilos.BLANCO,
                        border=ft.Border.all(1, estilos.SOMBRA_OSCURA),
                        border_radius=16,
                        padding=14,
                    )
                )

            tabla_talles.controls.extend([
                texto(f"Stock de {color}", size=16, bold=True, titulo=True),
                ft.Row(
                    controls=controles_talles,
                    alignment=ft.MainAxisAlignment.START,
                    wrap=True,
                    spacing=12,
                    run_spacing=12,
                )
            ])

            disponibles = [
                v for v in variantes_color
                if int(v["cantidad"]) > 0
            ]

            lista_disponibles.controls.append(etiqueta("Talles disponibles"))

            for variante in disponibles:
                lista_disponibles.controls.append(
                    texto(f'{variante["talle"]} → {variante["cantidad"]}', size=13)
                )

            tabla_talles.visible = True
            lista_disponibles.visible = True

            page.update()

        columna_color, _ = campo_selector("Color", colores, None, seleccionar_color)
        columna_color.width = 320

        mostrar_panel(
            f"STOCK - {nombre_producto}",
            [
                columna_color,
                tabla_talles,
                lista_disponibles,
                ft.Divider(color=estilos.SOMBRA_OSCURA),
                fila_botones(confirmar_click, "Actualizar stock"),
            ],
            "Ajuste de inventario",
        )

        if color_inicial in colores:
            columna_color.controls[1].content.controls[0].value = color_inicial
            seleccionar_color(color_inicial)

    def ventana_con_entradas(texto_superior,tipo, funcion):  # Formulario simple con un campo (para marca o categoría)
        columna, entrada = campo_texto(f"Nombre de la {tipo} *", tipo)
        columna.width = 420

        def confirmar_click():  # Llama a la función recibida con el valor ingresado
            valor_entrada=entrada.value
            retorno=funcion(valor_entrada)
            if retorno != None:
                   ventana_de_alerta(*retorno)
            else:
                mostrar(None)

        mostrar_panel(texto_superior, [columna, fila_botones(confirmar_click)])

    def ventana_agregar_color(texto_superior):  # Formulario para agregar un color con selector
        color_elegido = {"hex": "#000000"}
        columna_nombre, nombre = campo_texto("Nombre del color *", "color")
        columna_nombre.width = 420
        vista_previa = ft.Container(
            width=40, height=40, border_radius=20,
            bgcolor=color_elegido["hex"],
            border=ft.Border.all(1, ft.Colors.GREY_400),
        )
        texto_hex = texto(color_elegido["hex"], bold=True)

        def al_cambiar_color(e):  # Actualiza la vista previa al cambiar el color
            codigo = e.data
            if codigo is None:
                return
            color_elegido["hex"] = codigo
            vista_previa.bgcolor = codigo
            texto_hex.value = codigo
            page.update()

        selector = fcp.ColorPicker(
            color=color_elegido["hex"],
            enable_alpha=False,
            hex_input_bar=True,
            color_picker_width=300,
            label_text_style=ft.TextStyle(color=estilos.TEXTO, weight=ft.FontWeight.W_600),
            on_color_change=al_cambiar_color,
        )

        def confirmar_click():  # Guarda el color nuevo
            retorno = inventario.agregar_color(nombre.value, color_elegido["hex"])
            if retorno is not None:
                ventana_de_alerta(*retorno)
            else:
                mostrar(None)

        mostrar_panel(
            texto_superior,
            [
                columna_nombre,
                etiqueta("Seleccionar tono"),
                selector,
                ft.Row(controls=[vista_previa, texto_hex], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                fila_botones(confirmar_click),
            ],
        )

    def ver_cuentas():  # Muestra la lista de cuentas registradas
        usuarios = Usuario.listar_usuarios()
        filas = []

        for u in usuarios:
            es_admin = u["rol"] == "admin"
            filas.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.PERSON,
                                    color=estilos.FONDO if es_admin else estilos.TEXTO,
                                    size=20,
                                ),
                                width=40,
                                height=40,
                                bgcolor=estilos.TEXTO if es_admin else estilos.BLANCO,
                                border_radius=12,
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Column(
                                controls=[
                                    texto(f'{u["nombre"]} {u["apellido"]}', bold=True, titulo=True),
                                    texto(u["email"], size=12, color=estilos.TEXTO_SUAVE),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Container(
                                content=texto(
                                    u["rol"].upper(), size=10, bold=True,
                                    color=estilos.FONDO if es_admin else estilos.TEXTO,
                                ),
                                bgcolor=estilos.TEXTO if es_admin else estilos.BLANCO,
                                border=ft.Border.all(1, estilos.SOMBRA_OSCURA),
                                border_radius=20,
                                padding=ft.Padding.symmetric(horizontal=12, vertical=5),
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=14,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.6, estilos.BLANCO),
                    border=ft.Border.all(1, BORDE_CLARO),
                    border_radius=16,
                    padding=14,
                )
            )

        mostrar_panel(
            "CUENTAS DE USUARIOS",
            [
                texto(f"{len(usuarios)} cuentas registradas", size=13, color=estilos.TEXTO_SUAVE),
                *filas,
            ],
            "Usuarios",
        )

    def agregar_administrador():  # Formulario para crear una cuenta de administrador
        columna_nombre, nombre = campo_texto("Nombre *", "Nombre")
        columna_apellido, apellido = campo_texto("Apellido *", "Apellido")
        columna_email, email = campo_texto("Correo *", "Correo")
        columna_clave, clave = campo_texto(
            "Contraseña *", "Contraseña", password=True, can_reveal_password=True
        )
        for columna in (columna_nombre, columna_apellido, columna_email, columna_clave):
            columna.expand = True

        def confirmar_click():  # Crea el admin y vuelve a la lista de cuentas
            retorno = Usuario.registrar_admin(
                nombre.value or "", apellido.value or "", email.value or "", clave.value or ""
            )
            if retorno is not None:
                ventana_de_alerta(*retorno)
            else:
                ver_cuentas()

        mostrar_panel(
            "AGREGAR ADMINISTRADOR",
            [
                ft.Row(controls=[columna_nombre, columna_apellido], spacing=20),
                ft.Row(controls=[columna_email, columna_clave], spacing=20),
                ft.Divider(color=estilos.SOMBRA_OSCURA),
                fila_botones(confirmar_click, "Crear cuenta"),
            ],
            "Cuentas",
        )

    def estilo_tarjeta(tarjeta, activa):  # Resalta o quita el resaltado de una tarjeta
        tarjeta.border = ft.Border.all(2.5 if activa else 1, estilos.TEXTO if activa else BORDE_CLARO)

    def cambiar_seleccion(e, id, tarjeta_container):  # Marca un producto como seleccionado
        nonlocal producto_en_seleccion, tarjeta_seleccionada_ref

        if tarjeta_seleccionada_ref is not None:
            estilo_tarjeta(tarjeta_seleccionada_ref, False)

        producto_en_seleccion = id
        tarjeta_seleccionada_ref = tarjeta_container
        estilo_tarjeta(tarjeta_seleccionada_ref, True)

        page.update()
        print(f"Producto seleccionado ID: {producto_en_seleccion}")

    def pastilla(valor, oscura):  # Etiqueta chica redondeada
        return ft.Container(
            content=texto(
                valor.upper(), size=10, bold=True,
                color=ft.Colors.WHITE if oscura else estilos.TEXTO,
                max_lines=1,
            ),
            bgcolor=ft.Colors.with_opacity(0.7, estilos.OSCURO) if oscura else ft.Colors.with_opacity(0.85, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
            border_radius=20,
            padding=ft.Padding.symmetric(horizontal=12, vertical=4),
        )

    def tarjeta_de_producto(p, stock):  # Tarjeta de producto con imagen, datos y stock
        tarjeta = ft.Container(
            content=ft.Stack(
                controls=[
                    ft.Container(
                        content=ft.Image(src=p.imagen, fit=ft.BoxFit.COVER),
                        left=0, top=0, right=0, bottom=0,
                        border_radius=20,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    ),
                    ft.Container(
                        content=ft.Row(
                            controls=[pastilla(p.categoria, True), pastilla(p.marca, False)],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        left=12, top=12, right=12,
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                texto(p.nombre.upper(), size=14, bold=True, titulo=True, color=ft.Colors.WHITE, max_lines=1),
                                ft.Row(
                                    controls=[
                                        texto(p.precio, size=16, bold=True, titulo=True, color=ft.Colors.WHITE),
                                        texto(
                                            f"Stock: {stock} un.", size=11,
                                            color=ft.Colors.AMBER_200 if stock < 10 else ft.Colors.GREY_300,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                            ],
                            spacing=4,
                            tight=True,
                        ),
                        left=0, right=0, bottom=0,
                        padding=ft.Padding.symmetric(horizontal=16, vertical=14),
                        bgcolor=ft.Colors.with_opacity(0.75, estilos.OSCURO),
                        blur=ft.Blur(16, 16),
                        border_radius=ft.BorderRadius.only(bottom_left=20, bottom_right=20),
                    ),
                ],
            ),
            padding=8,
            bgcolor=estilos.FONDO,
            shadow=estilos.sombra_neu(6, 12),
            border_radius=28,
        )
        estilo_tarjeta(tarjeta, p.id == producto_en_seleccion)
        return tarjeta

    def mostrar(producto):  # Carga la grilla de productos y actualiza los totales
        nonlocal tarjeta_seleccionada_ref, grid_productos
        tarjeta_seleccionada_ref = None
        lista_productos = inventario.listar_productos(producto)
        grid_productos = nueva_grilla()  # Grilla nueva cada vez: reusar la vieja duplicaba tarjetas
        stock_total = 0

        for p in lista_productos:
            stock = sum(int(v["cantidad"]) for v in inventario.listar_stock(p.id)["diccionario"])
            stock_total += stock
            tarjeta_producto = tarjeta_de_producto(p, stock)
            if p.id == producto_en_seleccion:
                tarjeta_seleccionada_ref = tarjeta_producto

            tarjeta_producto.on_click = lambda e, id=p.id, tc=tarjeta_producto: cambiar_seleccion(e, id, tc)
            grid_productos.controls.append(tarjeta_producto)

        elementos = inventario.listar_elementos_producto()
        valor_productos.value = str(len(lista_productos))
        valor_stock.value = str(stock_total)
        valor_marcas.value = str(len(elementos[1]))
        valor_categorias.value = str(len(elementos[0]))

        contenedor_principal.content = grid_productos
        page.update()

    def agregar(tipo):  # Abre el formulario según lo que se quiere agregar
        texto_superior=f"AGREGAR {tipo.upper()}"
        logging.info(f"Se desea agregar {tipo}")
        if tipo=="marca":
            ventana_con_entradas(texto_superior,tipo, inventario.agregar_marca)
        elif tipo=="categoria":
            ventana_con_entradas(texto_superior,tipo, inventario.agregar_categoria)
        elif tipo=="color":
            ventana_agregar_color(texto_superior)
        else:
            formulario_producto(texto_superior)

    def tarjeta_estadistica(icono, titulo, valor, oscuro=False):  # Tarjeta con un número de resumen
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icono, color=estilos.FONDO if oscuro else estilos.TEXTO, size=20),
                        width=40,
                        height=40,
                        bgcolor=estilos.TEXTO if oscuro else estilos.BLANCO,
                        border=ft.Border.all(1, estilos.SOMBRA_OSCURA),
                        border_radius=12,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column(
                        controls=[etiqueta(titulo), valor],
                        spacing=0,
                        tight=True,
                    ),
                ],
                spacing=14,
            ),
            bgcolor=estilos.FONDO,
            shadow=estilos.sombra_neu(6, 14),
            border=ft.Border.all(1, BORDE_CLARO),
            border_radius=20,
            padding=16,
            expand=True,
        )

    def tarjeta_menu(titulo, icono, controles):  # Grupo de botones del menú lateral
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(icono, color=estilos.TEXTO, size=18),
                            ft.Container(
                                content=texto(titulo.upper(), size=13, bold=True, titulo=True),
                                expand=True,
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Divider(color=estilos.SOMBRA_OSCURA, height=10),
                    *controles,
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
            bgcolor=estilos.FONDO,
            shadow=estilos.sombra_neu(8, 16),
            border=ft.Border.all(1, BORDE_CLARO),
            border_radius=24,
            padding=20,
        )

    valor_productos = texto("0", size=20, bold=True, titulo=True)
    valor_stock = texto("0", size=20, bold=True, titulo=True)
    valor_marcas = texto("0", size=20, bold=True, titulo=True)
    valor_categorias = texto("0", size=20, bold=True, titulo=True)

    fila_estadisticas = ft.Row(
        controls=[
            tarjeta_estadistica(ft.Icons.INVENTORY_2, "Total productos", valor_productos, True),
            tarjeta_estadistica(ft.Icons.VIEW_IN_AR, "Stock acumulado", valor_stock),
            tarjeta_estadistica(ft.Icons.COPYRIGHT, "Marcas", valor_marcas),
            tarjeta_estadistica(ft.Icons.LAYERS, "Categorías", valor_categorias),
        ],
        spacing=16,
    )

    def nueva_grilla():  # Crea la grilla de productos vacía
        return ft.GridView(
            expand=1,
            max_extent=300,
            child_aspect_ratio=0.8,
            spacing=20,
            run_spacing=20,
            padding=ft.Padding.only(right=14, bottom=14),
        )

    grid_productos = nueva_grilla()
    contenedor_principal = ft.Container(
        content=grid_productos,
        expand=True,
    )

    tarjeta_productos = tarjeta_menu(
        "Mostrar productos",
        ft.Icons.GRID_VIEW,
        [
            boton("Mostrar productos", ft.Icons.TABLE_ROWS, lambda: mostrar(None), "primario"),
            etiqueta("Catálogo"),
            boton("Agregar producto", ft.Icons.ADD, lambda: agregar("producto")),
            boton("Agregar marca", ft.Icons.COPYRIGHT, lambda: agregar("marca")),
            boton("Agregar categoría", ft.Icons.LAYERS, lambda: agregar("categoria")),
            boton("Agregar color", ft.Icons.PALETTE, lambda: agregar("color")),
            etiqueta("Producto seleccionado"),
            boton("Modificar producto", ft.Icons.EDIT, lambda: modificar()),
            boton("Agregar stock", ft.Icons.INVENTORY, lambda: agregar_stock()),
            boton("Eliminar producto", ft.Icons.DELETE, lambda: eliminar(), "peligro"),
        ],
    )
    tarjeta_cuentas = tarjeta_menu(
        "Mostrar cuentas de usuarios",
        ft.Icons.PEOPLE,
        [
            boton("Ver cuentas", ft.Icons.PERSON_SEARCH, lambda: ver_cuentas(), "primario"),
            boton("Agregar cuenta de administrador", ft.Icons.PERSON_ADD, lambda: agregar_administrador()),
        ],
    )
    tarjeta_estadisticas = tarjeta_menu(
        "Mostrar estadísticas",
        ft.Icons.BAR_CHART,
        [
            texto("Opciones próximamente", size=12, color=estilos.TEXTO_SUAVE),
        ],
    )

    contenedor_izquierdo = ft.Container(
        content=ft.ListView(
            controls=[tarjeta_productos, tarjeta_cuentas, tarjeta_estadisticas],
            spacing=24,
            padding=ft.Padding.only(left=10, top=4, right=18, bottom=18),
        ),
        width=330,
    )

    botones_header = [
        ft.TextButton(
            content=ft.Text("Cerrar Sesión", font_family=estilos.FUENTE_TEXTO, color=estilos.TEXTO_SUAVE),
            on_click=ir_a_login,
        )
    ]
    botones_centro = [
        ft.Container(
            content=texto("ADMIN", size=10, bold=True, color=ft.Colors.WHITE),
            bgcolor=estilos.TEXTO,
            border_radius=20,
            padding=ft.Padding.symmetric(horizontal=12, vertical=4),
        )
    ]
    header = estilos.construir_header(botones_header, botones_centro)

    mostrar(None)  # Carga los productos al abrir el panel

    return [
        ft.Stack(
            expand=True,
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            contenedor_izquierdo,
                            ft.Column(
                                controls=[fila_estadisticas, contenedor_principal],
                                spacing=20,
                                expand=True,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        spacing=20,
                    ),
                    expand=True,
                    padding=ft.Padding.only(top=100, left=20, right=20, bottom=20),
                ),
                header,
            ],
        )
    ]