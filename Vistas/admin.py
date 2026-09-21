import flet as ft
import logging 
import os
import sys
import shutil

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
                    origen,
                )
                if retorno != None:
                    ventana_de_alerta(*retorno)
                else:
                    page.pop_dialog()
            
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
        lista_derecha.content.controls.clear()
        for i in lista_productos:
            lista_derecha.content.controls.append(ft.Button(
                content=ft.Column(
                      controls=[
                           ft.Image(src="Imagenes/nova_prestige_logo.png", height=50, width=50),
                           ft.Text(f"{i.nombre}"),
                           ft.Row(
                                controls=[
                                     ft.Text(f"{i.precio}"),
                                     ft.Text(f"{i.stock}")
                                ]
                           )
                      ]
                 )
            ))

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



    lista_derecha = ft.Container(
        content=ft.ListView(expand=1, spacing=10, padding=20),
        bgcolor=ft.Colors.GREY,
        expand=True
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
                #ft.Button("Agregar stock", on_click=agregar_stock),
                #ft.Button("Consultar estadisticas", on_click=estadisticas),
                #ft.Button("Ver historial de compras productos", on_click=historial),
            ]
        )
    )

    page.add(
        ft.Row(
            controls=[contenedor_izquierdo, lista_derecha],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
    )


ft.app(target=main)