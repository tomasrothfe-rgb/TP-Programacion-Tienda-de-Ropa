import flet as ft
import logging
import os
import sys
import estilos

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clases import Inventario, Carrito
from datetime import datetime

logging.basicConfig(level=logging.INFO)

COSTO_ENVIO = 15000
TEXTO_GARANTIA = "GARANTÍA DE DEVOLUCIÓN JUPITER POR 30 DÍAS"
VERDE = "#16A34A"
ALTO_MAXIMO_LISTA = 340


def CompraVista(page, ir_a_cliente, usuario):
    inventario = Inventario()
    carrito = Carrito(usuario.id)
    estado = {"envio": "retiro", "pago": "tarjeta"}

    def formato_precio(valor):
        return "$" + f"{valor:,.0f}".replace(",", ".")

    def ventana_de_alerta(texto_superior, erratas):
        return estilos.ventana_de_alerta(page, texto_superior, erratas)

    def etiqueta(texto):
        return ft.Text(texto.upper(), font_family=estilos.FUENTE_TEXTO, size=12,
                       weight=ft.FontWeight.W_600, color=estilos.TEXTO)

    def campo_texto(**kwargs):
        return ft.TextField(
            bgcolor=ft.Colors.WHITE,
            filled=True,
            border_radius=16,
            border_color=estilos.SOMBRA_OSCURA,
            focused_border_color=estilos.TEXTO,
            color=estilos.TEXTO,
            cursor_color=estilos.TEXTO,
            text_size=15,
            content_padding=ft.Padding.symmetric(horizontal=20, vertical=16),
            **kwargs,
        )

    def campo_con_etiqueta(texto, campo, expand=False):
        return ft.Column(spacing=6, expand=expand, horizontal_alignment=ft.CrossAxisAlignment.STRETCH, controls=[etiqueta(texto), campo])

    def titulo_seccion(numero, titulo, paso):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=32, height=32, border_radius=16, bgcolor=estilos.OSCURO,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Text(str(numero), font_family=estilos.FUENTE_TEXTO, size=13,
                                            weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ),
                        ft.Text(titulo, font_family=estilos.FUENTE_TITULO, size=24,
                                weight=ft.FontWeight.BOLD, color=estilos.TEXTO),
                    ],
                ),
                ft.Text(paso, font_family=estilos.FUENTE_TEXTO, size=11, color=estilos.TEXTO_SUAVE,
                        style=ft.TextStyle(letter_spacing=1)),
            ],
        )

    def divisor():
        return ft.Divider(height=10, color=ft.Colors.with_opacity(0.5, ft.Colors.GREY))

    def crear_selector(opciones, inicial, al_cambiar):
        botones = {}

        def pintar(actual):
            for valor, (contenedor, icono, texto) in botones.items():
                activo = valor == actual
                contenedor.bgcolor = estilos.OSCURO if activo else ft.Colors.WHITE
                contenedor.border = ft.Border.all(1, estilos.OSCURO if activo else estilos.SOMBRA_OSCURA)
                icono.color = ft.Colors.WHITE if activo else estilos.TEXTO
                texto.color = ft.Colors.WHITE if activo else estilos.TEXTO

        def elegir(valor):
            pintar(valor)
            al_cambiar(valor)

        for valor, titulo, nombre_icono in opciones:
            icono = ft.Icon(nombre_icono, size=16)
            texto = ft.Text(titulo, font_family=estilos.FUENTE_TEXTO, size=12,
                            weight=ft.FontWeight.BOLD, style=ft.TextStyle(letter_spacing=1))
            contenedor = ft.Container(
                expand=True,
                height=44,
                border_radius=14,
                alignment=ft.Alignment.CENTER,
                on_click=lambda e, v=valor: elegir(v),
                content=ft.Row(tight=True, spacing=10, alignment=ft.MainAxisAlignment.CENTER,
                               controls=[icono, texto]),
            )
            botones[valor] = (contenedor, icono, texto)

        pintar(inicial)
        return ft.Row(spacing=12, controls=[b[0] for b in botones.values()])

    def caja_info(controles):
        return ft.Container(
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, estilos.SOMBRA_OSCURA),
            border_radius=16,
            content=ft.Column(spacing=6, horizontal_alignment=ft.CrossAxisAlignment.STRETCH, controls=controles),
        )

    def texto_info(texto, negrita=False):
        return ft.Text(texto, font_family=estilos.FUENTE_TEXTO, size=14, color=estilos.TEXTO,
                       weight=ft.FontWeight.BOLD if negrita else None)

    def comprobar_comprar(e):
        campos_envio = [nombre_envio, apellido_envio, correo_envio, direccion_envio, ciudad_envio, codigo_envio]
        if estado["envio"] == "envio" and any(not c.value.strip() for c in campos_envio):
            ventana_de_alerta("ERROR DE ENVIO", "COMPLETE TODOS LOS DATOS")
            return

        if estado["pago"] == "tarjeta":
            campos_tarjeta = [numero_tarjeta, titular_tarjeta, vencimiento_tarjeta, cvv_tarjeta]
            if any(not c.value.strip() for c in campos_tarjeta):
                ventana_de_alerta("ERROR DE PAGO", "COMPLETE TODOS LOS DATOS DE LA TARJETA")
                return
            metodo = "tarjeta"
        else:
            metodo = "transferencia"

        envio = COSTO_ENVIO if estado["envio"] == "envio" else 0
        total = sub_total + envio
        fecha = datetime.now().strftime("%d-%m-%Y")

        try:
            resultado = carrito.comprar_carrito({"metodo_pago": metodo, "tipo_envio": estado["envio"], "total": total, "fecha": fecha})
        except Exception as ex:
            ventana_de_alerta("ERROR", f"No se pudo registrar la compra: {ex}")
            return

        if resultado:
            boton_comprar.disabled = True

            estilos.ventana_de_alerta(
                page,
                "COMPRA REALIZADA",
                f"Tu número de orden es {resultado}",
                "VOLVER A LA TIENDA",
                al_cerrar=lambda: ir_a_cliente(usuario),
            )

    lista = carrito.listar_carrito()
    lista_controls = []
    sub_total = 0.0

    for i in lista:
        info = inventario.consultar_producto_especifico(i[2])
        precio = float(info["precio"])
        cantidad = int(i[5])

        lista_controls.append(
            ft.Container(
                padding=12,
                bgcolor=ft.Colors.WHITE,
                border_radius=16,
                content=ft.Row(
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src=info["url"], width=52, height=60, fit=ft.BoxFit.COVER, border_radius=10),
                        ft.Column(
                            expand=True,
                            spacing=3,
                            controls=[
                                ft.Text(f"{info['categoria']} {info['marca']} {info['nombre']}".upper(),
                                        font_family=estilos.FUENTE_TITULO, size=12, weight=ft.FontWeight.BOLD,
                                        color=estilos.TEXTO, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(f"{i[3]} • TALLE {i[4]}".upper(), font_family=estilos.FUENTE_TEXTO,
                                        size=10, color=estilos.TEXTO_SUAVE),
                                ft.Text(f"{formato_precio(precio)} x {cantidad}", font_family=estilos.FUENTE_TEXTO,
                                        size=12, weight=ft.FontWeight.BOLD, color=estilos.TEXTO),
                            ],
                        ),
                        ft.Text(formato_precio(precio * cantidad), font_family=estilos.FUENTE_TEXTO, size=12,
                                weight=ft.FontWeight.BOLD, color=estilos.TEXTO),
                    ],
                ),
            )
        )
        sub_total += precio * cantidad

    cantidad_articulos = sum(int(i[5]) for i in lista)

    txt_subtotal = ft.Text(font_family=estilos.FUENTE_TEXTO, size=14, color=estilos.TEXTO)
    txt_envio = ft.Text(font_family=estilos.FUENTE_TEXTO, size=13, weight=ft.FontWeight.BOLD)
    txt_total = ft.Text(font_family=estilos.FUENTE_TITULO, size=30, weight=ft.FontWeight.BOLD, color=estilos.TEXTO)

    boton_comprar = ft.Button(
        content="CONFIRMAR PAGO",
        icon=ft.Icons.LOCK_OUTLINE,
        disabled=not lista,
        on_click=comprobar_comprar,
        style=ft.ButtonStyle(
            bgcolor={ft.ControlState.DEFAULT: estilos.OSCURO, ft.ControlState.DISABLED: estilos.COLOR_CAMPO},
            color={ft.ControlState.DEFAULT: ft.Colors.WHITE, ft.ControlState.DISABLED: estilos.TEXTO_SUAVE},
            padding=ft.Padding.symmetric(vertical=24),
            shape=ft.RoundedRectangleBorder(radius=30),
            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, letter_spacing=1.5, size=14),
        ),
    )

    def actualizar_totales():
        envio = COSTO_ENVIO if estado["envio"] == "envio" else 0
        total = sub_total + envio

        txt_subtotal.value = formato_precio(sub_total)
        txt_envio.value = "GRATIS" if envio == 0 else formato_precio(envio)
        txt_envio.color = VERDE if envio == 0 else estilos.TEXTO
        txt_total.value = formato_precio(total)
        boton_comprar.content = f"CONFIRMAR PAGO DE {formato_precio(total)}  →"
        contenedor_pago_local.visible = estado["envio"] == "retiro"
        contenedor_entradas.visible = estado["envio"] == "envio"
        page.update()

    def cambiar_envio(valor):
        estado["envio"] = valor
        actualizar_totales()

    def cambiar_metodo(valor):
        estado["pago"] = valor
        panel_tarjeta.visible = valor == "tarjeta"
        panel_transferencia.visible = valor == "transferencia"
        page.update()

    nombre_envio = campo_texto()
    apellido_envio = campo_texto()
    correo_envio = campo_texto()
    direccion_envio = campo_texto()
    ciudad_envio = campo_texto()
    codigo_envio = campo_texto()

    contenedor_entradas = ft.Column(
        spacing=14,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        visible=False,
        controls=[
            ft.Text("DIRECCIÓN DE DESTINO", font_family=estilos.FUENTE_TEXTO, size=11, weight=ft.FontWeight.BOLD,
                    color=estilos.TEXTO, style=ft.TextStyle(letter_spacing=1)),
            ft.Row(spacing=16, controls=[
                campo_con_etiqueta("Nombre", nombre_envio, expand=True),
                campo_con_etiqueta("Apellido", apellido_envio, expand=True),
            ]),
            campo_con_etiqueta("Correo electrónico", correo_envio),
            campo_con_etiqueta("Dirección", direccion_envio),
            ft.Row(spacing=16, controls=[
                campo_con_etiqueta("Ciudad", ciudad_envio, expand=True),
                campo_con_etiqueta("Código postal", codigo_envio, expand=True),
            ]),
        ],
    )

    contenedor_pago_local = caja_info([
        texto_info("JUPITER TIENDA ZONA NORTE", negrita=True),
        texto_info("Calle 9 de julio 300, Esperanza (Santa Fe). Horario de atencion de 8:00 a 20:00."),
        texto_info("El producto se retira presentado el DNI y numero de orden"),
    ])

    selector_envio = crear_selector(
        [("envio", "ENVÍO A DOMICILIO", ft.Icons.LOCAL_SHIPPING),
         ("retiro", "RETIRO EN LOCAL", ft.Icons.STOREFRONT)],
        estado["envio"],
        cambiar_envio,
    )

    numero_tarjeta = campo_texto()
    vencimiento_tarjeta = campo_texto()
    cvv_tarjeta = campo_texto(password=True)
    titular_tarjeta = campo_texto()

    panel_tarjeta = ft.Column(
        spacing=14,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        visible=True,
        controls=[
            campo_con_etiqueta("Número de tarjeta", numero_tarjeta),
            ft.Row(spacing=16, controls=[
                campo_con_etiqueta("Expiración", vencimiento_tarjeta, expand=True),
                campo_con_etiqueta("CVV / CVC", cvv_tarjeta, expand=True),
            ]),
            campo_con_etiqueta("Nombre en la tarjeta", titular_tarjeta),
        ],
    )

    panel_transferencia = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        visible=False,
        controls=[
            caja_info([
                texto_info("Datos para la transferencia", negrita=True),
                texto_info("CBU: 0000000000000000000000"),
                texto_info("Alias: JUPITER.TIENDA"),
                texto_info("Titular: Jupiter Tienda"),
            ]),
        ],
    )

    selector_pago = crear_selector(
        [("tarjeta", "TARJETA CRÉDITO/DÉBITO", ft.Icons.CREDIT_CARD),
         ("transferencia", "TRANSFERENCIA", ft.Icons.ACCOUNT_BALANCE)],
        estado["pago"],
        cambiar_metodo,
    )

    tarjeta_entrega = estilos.reborde_neu(
        ft.Column(
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                titulo_seccion(1, "MÉTODO DE ENTREGA", "PASO 1 DE 2"),
                divisor(),
                selector_envio,
                contenedor_pago_local,
                contenedor_entradas,
            ],
        )
    )
    tarjeta_entrega.padding = 32
    tarjeta_entrega.border_radius = 30

    tarjeta_pago = estilos.reborde_neu(
        ft.Column(
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                titulo_seccion(2, "MÉTODO DE PAGO", "PASO 2 DE 2"),
                divisor(),
                selector_pago,
                panel_tarjeta,
                panel_transferencia,
            ],
        )
    )
    tarjeta_pago.padding = 32
    tarjeta_pago.border_radius = 30

    alto_lista = min(ALTO_MAXIMO_LISTA, max(1, len(lista)) * 96 - 12)
    lista_resumen = ft.Column(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        height=alto_lista,
        controls=lista_controls or [
            ft.Text("Tu carrito está vacío", font_family=estilos.FUENTE_TEXTO, size=14,
                    color=estilos.TEXTO_SUAVE, italic=True)
        ],
    )

    texto_articulos = f"{cantidad_articulos} ARTÍCULO" + ("" if cantidad_articulos == 1 else "S")

    tarjeta_resumen = estilos.reborde_neu(
        ft.Column(
            spacing=18,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("RESUMEN DE COMPRA", font_family=estilos.FUENTE_TITULO, size=22,
                                weight=ft.FontWeight.BOLD, color=estilos.TEXTO),
                        ft.Container(
                            padding=ft.Padding.symmetric(horizontal=14, vertical=6),
                            bgcolor=estilos.OSCURO,
                            border_radius=20,
                            content=ft.Text(texto_articulos, font_family=estilos.FUENTE_TEXTO, size=11,
                                            weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ),
                    ],
                ),
                divisor(),
                lista_resumen,
                divisor(),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Subtotal de prendas", font_family=estilos.FUENTE_TEXTO, size=14,
                                color=estilos.TEXTO_SUAVE),
                        txt_subtotal,
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Costo de envío", font_family=estilos.FUENTE_TEXTO, size=14,
                                color=estilos.TEXTO_SUAVE),
                        txt_envio,
                    ],
                ),
                divisor(),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Total final", font_family=estilos.FUENTE_TITULO, size=18,
                                weight=ft.FontWeight.BOLD, color=estilos.TEXTO),
                        txt_total,
                    ],
                ),
                boton_comprar,
                ft.Text(TEXTO_GARANTIA, font_family=estilos.FUENTE_TEXTO, size=10, color=estilos.TEXTO_SUAVE,
                        text_align=ft.TextAlign.CENTER, style=ft.TextStyle(letter_spacing=1)),
            ],
        )
    )
    tarjeta_resumen.padding = 32
    tarjeta_resumen.border_radius = 30

    actualizar_totales()

    boton_volver = ft.TextButton(
        content=ft.Row(
            tight=True,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.ARROW_BACK, size=18, color=estilos.TEXTO_SUAVE),
                ft.Text("Volver a la tienda", font_family=estilos.FUENTE_TEXTO, color=estilos.TEXTO_SUAVE),
            ],
        ),
        on_click=lambda e: ir_a_cliente(usuario),
    )

    header = estilos.construir_header([boton_volver], [])

    cuerpo = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Container(height=20),
            ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Container(expand=3),
                    ft.Container(
                        expand=10,
                        content=ft.Row(
                            spacing=34,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            controls=[
                                ft.Column(expand=7, spacing=34, horizontal_alignment=ft.CrossAxisAlignment.STRETCH, controls=[tarjeta_entrega, tarjeta_pago]),
                                ft.Column(expand=5, horizontal_alignment=ft.CrossAxisAlignment.STRETCH, controls=[tarjeta_resumen]),
                            ],
                        ),
                    ),
                    ft.Container(expand=3),
                ],
            ),
            ft.Container(height=40),
        ],
    )

    return [
        ft.Stack(
            expand=True,
            controls=[
                ft.Container(expand=True, padding=ft.Padding.only(top=100), content=cuerpo),
                header,
            ],
        )
    ]