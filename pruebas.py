import flet as ft

def datos(campo):
    hola = campo.value
    print(hola)

def main(page: ft.Page):
    entry1 = ft.TextField(value="hola")
    entry2 = ft.TextField(value="hola")
    button1 = ft.TextButton(content="Enviar",
                             on_click=lambda e: datos(entry1))

    page.add(ft.Column(controls=[entry1, entry2, button1]))

ft.app(target=main)
