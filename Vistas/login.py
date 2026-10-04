import flet as ft
import os
import sys
import estilos

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clases import Usuario

def LoginVista(page, ir_a_cliente, ir_a_admin):
    correo_ref = ft.Ref[ft.TextField]()
    contrasena_ref = ft.Ref[ft.TextField]()

    login_correo = estilos.campo_datos("Correo electrónico", "ejemplo@correo.com", ref=correo_ref)
    login_contrasena = estilos.campo_datos("Contraseña", "********", ref=contrasena_ref, password=True, can_reveal_password=True)

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

    def ingresar_tienda(correo, contraseña):
        resultado = Usuario.iniciar_sesion(correo, contraseña)
        if resultado[0] != None:
            ventana_de_alerta(*resultado)
        else:
            usuario = resultado[1]
            if usuario.rol=="admin": 
                ir_a_admin(usuario)
            else:
                ir_a_cliente(usuario)

    btn_ingresar = ft.Button(
        "Ingresar",
        style=estilos.boton_presionado(),
        on_click=lambda e: ingresar_tienda(correo_ref.current.value, contrasena_ref.current.value),
    )

    nombre_ref = ft.Ref[ft.TextField]()
    apellido_ref = ft.Ref[ft.TextField]()
    reg_correo_ref = ft.Ref[ft.TextField]()
    reg_contrasena_ref = ft.Ref[ft.TextField]()

    reg_nombre = estilos.campo_datos("Nombre", "Mario", ref=nombre_ref)
    reg_apellido = estilos.campo_datos("Apellido", "Pérez", ref=apellido_ref)
    reg_correo = estilos.campo_datos("Correo electrónico", "ejemplo@correo.com", ref=reg_correo_ref)
    reg_contrasena = estilos.campo_datos("Contraseña", "********", ref=reg_contrasena_ref, password=True, can_reveal_password=True)

    def registrar_usuario():
        resultado = Usuario.registrar(
            nombre_ref.current.value,
            apellido_ref.current.value,
            reg_correo_ref.current.value,
            reg_contrasena_ref.current.value,
        )
        if resultado != None:
            ventana_de_alerta(*resultado)
        else:
            ingresar_tienda(reg_correo_ref.current.value, reg_contrasena_ref.current.value)

    btn_registrar = ft.Button("Registrarse", style=estilos.boton_presionado(),on_click=lambda e: registrar_usuario())

    login_view = ft.Column(
        [
            login_correo,
            login_contrasena,
            btn_ingresar
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,   
        spacing=15
    )

    register_view = ft.Column(
        [
            ft.Row(
                controls=[
                    ft.Container(reg_nombre, expand=True),
                    ft.Container(reg_apellido, expand=True),
                ],
                spacing=10,
            ),
            reg_correo,
            reg_contrasena,
            btn_registrar
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,   
        spacing=15
    )

    container_contenido = ft.Container(content=login_view, width=700, padding=ft.Padding.only(left=30, right=30))

    def cambiar_pestana(e):
        if e.control.data == 0:
            container_contenido.content = login_view
            texto_superior.value="Inicio de Sesión"
            btn_login_tab.style=estilos.boton_presionado()
            btn_register_tab.style=estilos.boton_no_presionado()
        else:
            container_contenido.content = register_view
            texto_superior.value="Crear Cuenta"
            btn_register_tab.style=estilos.boton_presionado()
            btn_login_tab.style=estilos.boton_no_presionado()
        page.update()

    btn_login_tab = ft.TextButton("INICIAR SESIÓN", data=0, on_click=cambiar_pestana, style=estilos.boton_presionado(), expand=True)
    btn_register_tab = ft.TextButton("REGISTRARSE", data=1, on_click=cambiar_pestana,style=estilos.boton_no_presionado(), expand=True)
    texto_superior=ft.Text("Inicio de Sesión", size=40,font_family=estilos.FUENTE_TITULO, color=estilos.TEXTO, weight=ft.FontWeight.BOLD)
    texto_inferior = ft.Container(
    content=ft.Text("Jupiter Clothes", size=10, font_family=estilos.FUENTE_TEXTO, color=estilos.TEXTO_SUAVE)
    )

    botonera = ft.Container(
    width=700,
    content=estilos.reborde_neu(
        ft.Row([btn_login_tab, btn_register_tab], spacing=0)   
    ),
    padding=ft.Padding.only(left=30, right=30)
        )
    imagen = ft.Image(
    src="Imagenes/Imagenes_UI/imagen_inicio.jpg",
    fit=ft.BoxFit.COVER,
    left=0, top=0, right=0, bottom=0,
)

    tarjeta = estilos.tarjeta_glassmorph("VERSION DE ESCRITORIO","JUPITER, NADA MAS", "El mejor catálogo de ropa de toda Esperanza y zona, \nropa asthetic y vintage")

    imagen_con_tarjeta = ft.Stack(controls=[imagen, tarjeta], expand=True)

    return [ft.Stack(
         expand=True,
         controls=[  
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                texto_superior,
                                botonera,
                                container_contenido,
                                texto_inferior
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20
                        ),
                        expand=True, 
                    ),
                    
                    ft.Container(
                        content=imagen_con_tarjeta,
                        padding=0,
                        expand=True, 
                    )
                ],
                spacing=0,
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.STRETCH
            ),
            estilos.construir_header(),
      ] ) ]
