import flet as ft




def main(page: ft.Page):
    page.title = "Contador con función única"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    valor_maximo = 10

    txt_numero = ft.Text(value="1", size=50, weight=ft.FontWeight.BOLD)
    txt_error = ft.Text(value="", color=ft.Colors.RED_400, size=12)

    def modificar_contador(e, numero: int):
        nuevo_valor = int(txt_numero.value) + numero
        if nuevo_valor > valor_maximo:
            txt_error.value = f"Has alcanzado el límite máximo de stock para este producto."
        elif nuevo_valor < 1:
            txt_error.value = f"Has alcanzado el límite mínimo de productos."
        else:
            txt_numero.value = str(nuevo_valor)
            txt_error.value = ""

        page.update()

    btn_menos = ft.ElevatedButton("-", on_click=lambda e: modificar_contador(e, -1), width=60)
    btn_mas = ft.ElevatedButton("+", on_click=lambda e: modificar_contador(e, 1), width=60)

    contenedor = ft.Row(controls=[btn_menos, txt_numero, btn_mas])

    page.add(
        ft.Container(height=10),
        ft.Row([contenedor], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        txt_error,
    )


ft.app(target=main)