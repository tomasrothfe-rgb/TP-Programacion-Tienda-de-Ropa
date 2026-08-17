import flet as ft

def main(page: ft.Page):
    # Crear el TextField deshabilitado por defecto
    mi_textfield = ft.TextField(label="Escribe algo...", disabled=True)

    # Función que se ejecuta al cambiar el estado del Checkbox
    def checkbox_changed(e):
        # El TextField toma el valor contrario al del checkbox en 'disabled'
        # Si el checkbox está marcado (True), disabled será False (activo)
        mi_textfield.disabled = not e.control.value
        mi_textfield.update()

    # Crear el Checkbox con el evento on_change
    mi_checkbox = ft.Checkbox(
        label="Habilitar campo de texto", 
        value=False, 
        on_change=checkbox_changed
    )

    page.add(mi_checkbox, mi_textfield)

ft.app(target=main)
