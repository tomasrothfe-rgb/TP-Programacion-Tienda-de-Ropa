import flet as ft
import logging 
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from conexion_bd import creacion_bd, agregar_producto, mostrar_productos, modificar_productos, eliminar_productos

logging.basicConfig(level=logging.INFO)




def main(page: ft.Page):
    page.title = "Panel de Administrador "
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 700
    page.window.height = 500

    producto_en_seleccion= None

    def mostrar():
        productos=mostrar_productos()
        lista_derecha.content.controls.clear()
        for producto in productos:
               lista_derecha.content.controls.append(
                      ft.ListTile(title=producto[1], subtitle=(f"Precio: {producto[2]}       Stock: {producto[3]}"), on_click= lambda e, p=producto: producto_seleccionado(e, p))
                    )
        page.update()

    def dialogo_box(lista_entrys,boolean,texto_superior,funcion):
            lista_nueva_entrys=[]
            def entrys(texto):
                return ft.TextField(
                        width=800,
                        hint_text=texto,
                        visible=boolean
            )
            for i in lista_entrys:
                lista_nueva_entrys.append(entrys(i))
    
            def confirmar_click(e):
                valores = [entry.value for entry in lista_nueva_entrys]
                funcion(valores)
                mostrar()
                page.pop_dialog()
    
            return page.show_dialog(
                            ft.AlertDialog(
                            modal=True,
                            title=ft.Text(texto_superior),
                            content=ft.Column(
                                controls=lista_nueva_entrys
                            ),
                            actions=[
                                ft.Button("CONFIRMAR", on_click=confirmar_click),
                                ft.Button("CANCELAR", on_click=lambda e: page.pop_dialog())
                            ],
                            actions_alignment=ft.MainAxisAlignment.END,
                            on_dismiss=lambda e: logging.info("Se cerro la pestaña")))

    def producto_seleccionado(e, producto):
        nonlocal producto_en_seleccion 
        producto_en_seleccion = producto
        logging.info(f"Se selecciono {producto_en_seleccion}")


    def agregar():
            logging.info("Se desea agregar un producto")
            dialogo_box(("Nombre", "Precio", "Stock"),True,"AGREGAR PRODUCTO", lambda valores: (agregar_producto(*valores)))
            
    def modificar():
            logging.info(f"Se desea modificar {producto_en_seleccion}")
            dialogo_box(("Nombre", "Precio"),True,f"MODIFICAR {producto_en_seleccion[1].upper()}", lambda valores: modificar_productos(*valores,producto_en_seleccion[0]))

    def eliminar():
            logging.info(f"Se desea elimnar productos {producto_en_seleccion}")
            dialogo_box((),False,f"ELIMINAR {producto_en_seleccion[1].upper()}", lambda valores: eliminar_productos(producto_en_seleccion[1],producto_en_seleccion[0]))
            
    
    def agregar_stock():
            logging.info("Se desea agregar stock")
    
    def estadisticas():
            logging.info("Se desea ver estadisticas")
    
    def historial():
            logging.info("Se desea ver historial")

    nombre_producto=ft.TextField()
    precio=ft.TextField()
    stock=ft.TextField()

    lista_derecha= ft.Container(
           content=ft.ListView(expand=1, spacing=10, padding=20,),
           bgcolor= ft.Colors.GREY,
           expand=True
    )

    mostrar()

    contenedor_izquierdo=ft.Container(
        content=ft.Column(
               controls=[
                      ft.Text("Panel de Administrador", size=30, weight="bold", color=ft.Colors.BLUE),
                ft.Button(
                    "Agregar productos",
                    on_click=agregar , 
                ),
                ft.Button(
                    "Eliminar productos",
                    on_click=eliminar,
                ),
                ft.Button(
                    "Mostrar productos",
                        on_click= mostrar,
                    ),
                ft.Button(
                    "Modificar productos",
                    on_click=modificar,
                ),
                ft.Button(
                    "Agregar stock",
                        on_click=agregar_stock,
                    ),
                ft.Button(
                    "Consultar estadisticas",
                    on_click=estadisticas,
                ),
                ft.Button(
                    "Ver historial de compras productos",
                        on_click=historial,
                    ),
               ]
        )
    )

    page.add(
        ft.Row(
            controls=[
                   contenedor_izquierdo,
                   lista_derecha
                      ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
        
    )


ft.app(target=main)