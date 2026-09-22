import flet as ft


def main(page: ft.Page):
    page.title = "Demo Flet - Tabs con botón"
    page.window.width = 420
    page.window.height = 420
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- Vistas de cada pestaña ---
    vista_inicio = ft.Container(
        content=ft.Text("👋 Bienvenido a la vista de Inicio", size=18),
        alignment=ft.Alignment.CENTER,
        padding=20,
    )

    vista_datos = ft.Container(
        content=ft.Text("📊 Acá irían tus datos o tabla", size=18),
        alignment=ft.Alignment.CENTER,
        padding=20,
    )

    vista_config = ft.Container(
        content=ft.Text("⚙️ Configuración de la app", size=18),
        alignment=ft.Alignment.CENTER,
        padding=20,
    )

    # --- Barra de pestañas (solo encabezados) ---
    tab_bar = ft.TabBar(
        tabs=[
            ft.Tab(label="Inicio"),
            ft.Tab(label="Datos"),
            ft.Tab(label="Config"),
        ],
    )

    # --- Contenido de cada pestaña ---
    tab_view = ft.TabBarView(
        expand=True,
        controls=[vista_inicio, vista_datos, vista_config],
    )

    tabs = ft.Tabs(
        length=3,
        selected_index=0,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[tab_bar, tab_view],
        ),
    )

    # --- Botón: pasa a la siguiente pestaña ---
    async def siguiente_vista(e):
        siguiente = (tabs.selected_index + 1) % tabs.length
        await tabs.move_to(index=siguiente)

    boton_cambiar = ft.Button(
        content="Cambiar de vista ➜",
        icon=ft.Icons.SWAP_HORIZ,
        on_click=siguiente_vista,
    )

    # --- Layout final ---
    page.add(
        ft.Column(
            expand=True,
            controls=[
                tabs,
                ft.Divider(),
                boton_cambiar,
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)