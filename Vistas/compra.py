import flet as ft
import logging
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clases import Inventario, Carrito
from datetime import datetime

logging.basicConfig(level=logging.INFO)

COSTO_ENVIO = 15000
id_usuario=1


def main(page: ft.Page):
    page.title = "Finalizar compra"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 1500
    page.window.height = 600

    inventario = Inventario()
    carrito = Carrito(id_usuario)


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

    def comprobar_comprar(e):
        campos_envio = [nombre_envio, apellido_envio, correo_envio, direccion_envio, ciudad_envio, codigo_envio]
        if opcion_envio.value == "envio" and any(not c.value.strip() for c in campos_envio):
            ventana_de_alerta("ERROR DE ENVIO", "COMPLETE TODOS LOS DATOS")
            return

        if panel_tarjeta.visible:
            campos_tarjeta = [numero_tarjeta, titular_tarjeta, vencimiento_tarjeta, cvv_tarjeta]
            if any(not c.value.strip() for c in campos_tarjeta):
                ventana_de_alerta("ERROR DE PAGO", "COMPLETE TODOS LOS DATOS DE LA TARJETA")
                return
            metodo = "tarjeta"
        else:
            metodo = "transferencia"

        envio = COSTO_ENVIO if opcion_envio.value == "envio" else 0
        total = sub_total + envio
        fecha = datetime.now().strftime("%d-%m-%Y")

        try:
            resultado = carrito.comprar_carrito({"metodo_pago": metodo, "tipo_envio": opcion_envio.value, "total": total, "fecha": fecha})
        except Exception as ex:
            ventana_de_alerta("ERROR", f"No se pudo registrar la compra: {ex}")
            return

        if resultado:
            boton_comprar.disabled = True
            page.update()
            ventana_de_alerta("COMPRA REALIZADA", f"Tu número de orden es {resultado}")

    lista = carrito.listar_carrito()
    lista_controls = []
    sub_total = 0.0

    for i in lista:
        info = inventario.consultar_producto_especifico(i[2])
        precio = float(info["precio"])
        cantidad = int(i[5])

        lista_controls.append(
            ft.ListTile(
                leading=ft.Image(src=info["url"]),
                title=ft.Text(f"{info['categoria']} {info['marca']} {info['nombre']}"),
                subtitle=ft.Column(
                    controls=[
                        ft.Text(f"{i[3]} / Color: {i[4]}", color=ft.Colors.GREY_600, size=12),
                        ft.Text(f"${precio:.2f} x {cantidad}"),
                    ],
                    spacing=2,
                ),
            )
        )
        sub_total += precio * cantidad

    cantidad_articulos = sum(int(i[5]) for i in lista)

    txt_subtotal = ft.Text()
    txt_envio = ft.Text()
    txt_total = ft.Text(size=20, weight=ft.FontWeight.BOLD)

    boton_comprar = ft.Button(
        content="CONFIRMAR PAGO",
        icon=ft.Icons.SHOPPING_BAG,
        disabled=not lista,
        on_click=lambda e: comprobar_comprar(e),
    )

    def actualizar_totales():
        envio = COSTO_ENVIO if opcion_envio.value == "envio" else 0
        total = sub_total + envio
        
        txt_subtotal.value = f"Subtotal: ${sub_total:.2f}"
        txt_envio.value = "Envío: Gratis" if envio == 0 else f"Envío: ${envio:.2f}"
        txt_total.value = f"Total: ${total:.2f}"
        boton_comprar.content = f"CONFIRMAR PAGO DE ${total:.2f}"
        contenedor_pago_local.visible = (opcion_envio.value == "retiro")  
        contenedor_entradas.disabled = (opcion_envio.value == "retiro")   
        page.update()

    def cambiar_envio(e):
        actualizar_totales()

    if not lista:
        lista_controls = [ft.Text("Tu carrito está vacío", italic=True)]

    contenido_carrito = ft.Column(
        controls=[
            ft.Text(
                f"Resumen de compra      {cantidad_articulos} artículos",
                size=18,
                weight=ft.FontWeight.BOLD,
            ),
            *lista_controls,
            ft.Divider(),
            txt_subtotal,
            txt_envio,
            txt_total,
            boton_comprar,
        ],
        spacing=2,
    )
    contenedor_carrito = ft.Container(content=contenido_carrito, expand=True)
    contenedor_pago_local=ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("ECLIPSIS TIENDA ZONA NORTE"),
                ft.Text("Calle 9 de julio 300, Esperanza (Santa Fe). Horario de atencion de 8:00 a 20:00."),
                ft.Text("El producto se retira presentado el DNI y numero de orden")
            ]
        )
    )
    opcion_envio = ft.RadioGroup(
        value="retiro",
        on_change=cambiar_envio,
        content=ft.Row(
            controls=[
                ft.Radio(value="retiro", label="Retiro en local (gratis)"),
                ft.Radio(value="envio", label=f"Envío a domicilio (${COSTO_ENVIO})"),
            ]
        ),
    )
    nombre_envio = ft.TextField(dense=True)
    apellido_envio = ft.TextField(dense=True)
    correo_envio = ft.TextField(dense=True)
    direccion_envio = ft.TextField(dense=True)
    ciudad_envio = ft.TextField(dense=True)
    codigo_envio = ft.TextField(dense=True)

    contenedor_entradas = ft.Column(
        controls=[
            ft.Text("Direccion de envio"),
            ft.Row(
                controls=[
                    ft.Column(controls=[ft.Text("Nombre"), nombre_envio], spacing=2, expand=True),
                    ft.Column(controls=[ft.Text("Apellido"), apellido_envio], spacing=2, expand=True),
                ],
                spacing=5,
            ),
            ft.Column(controls=[ft.Text("Correo"), correo_envio], spacing=2),
            ft.Column(controls=[ft.Text("Dirección"), direccion_envio], spacing=2),
            ft.Row(
                controls=[
                    ft.Column(controls=[ft.Text("Ciudad"), ciudad_envio], spacing=2, expand=True),
                    ft.Column(controls=[ft.Text("Código postal"), codigo_envio], spacing=2, expand=True),
                ],
                spacing=5,
            ),
        ],
        disabled=True,
    )

    contenido_envio = ft.Column(
        controls=[
            ft.Text("Envío", size=18, weight=ft.FontWeight.BOLD),
            opcion_envio,
            contenedor_pago_local,
            contenedor_entradas
        ]
    )
    contenedor_envio = ft.Container(content=contenido_envio)


    numero_tarjeta = ft.TextField(dense=True)
    titular_tarjeta = ft.TextField(dense=True)
    vencimiento_tarjeta = ft.TextField(dense=True)
    cvv_tarjeta = ft.TextField(dense=True, password=True)

    panel_tarjeta = ft.Column(
        controls=[
            ft.Column(controls=[ft.Text("Número de tarjeta"), numero_tarjeta], spacing=2),
            ft.Column(controls=[ft.Text("Titular"), titular_tarjeta], spacing=2),
            ft.Row(
                controls=[
                    ft.Column(controls=[ft.Text("Vencimiento"), vencimiento_tarjeta], spacing=2, expand=True),
                    ft.Column(controls=[ft.Text("CVV"), cvv_tarjeta], spacing=2, expand=True),
                ],
                spacing=5,
            ),
        ],
        visible=True,
    )

    panel_transferencia = ft.Column(
        controls=[
            ft.Text("Datos para la transferencia"),
            ft.Text("CBU: 0000000000000000000000"),
            ft.Text("Alias: ECLIPSIS.TIENDA"),
            ft.Text("Titular: Eclipsis Tienda"),
        ],
        visible=False,
    )

    def estilo_boton(activo):
        return ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE if activo else ft.Colors.GREY_200,
            color=ft.Colors.WHITE if activo else ft.Colors.BLACK,
        )

    def cambiar_metodo(metodo):
        es_tarjeta = metodo == "tarjeta"
        panel_tarjeta.visible = es_tarjeta
        panel_transferencia.visible = not es_tarjeta
        boton_tarjeta.style = estilo_boton(es_tarjeta)
        boton_transferencia.style = estilo_boton(not es_tarjeta)
        page.update()

    boton_tarjeta = ft.Button(
        content="Tarjeta crédito/débito",
        icon=ft.Icons.CREDIT_CARD,
        style=estilo_boton(True),
        on_click=lambda e: cambiar_metodo("tarjeta"),
    )
    boton_transferencia = ft.Button(
        content="Transferencia",
        icon=ft.Icons.ACCOUNT_BALANCE,
        style=estilo_boton(False),
        on_click=lambda e: cambiar_metodo("transferencia"),
    )

    contenido_pago = ft.Column(
        controls=[
            ft.Text("Pago", size=18, weight=ft.FontWeight.BOLD),
            ft.Row(controls=[boton_tarjeta, boton_transferencia], spacing=10),
            panel_tarjeta,
            panel_transferencia,
        ]
    )
    contenedor_pago = ft.Container(content=contenido_pago)

    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[contenedor_envio, contenedor_pago],
                    expand=True,
                ),
                contenedor_carrito,
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
    )

    actualizar_totales()  


ft.app(target=main)