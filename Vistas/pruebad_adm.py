import flet as ft

def main(page: ft.Page):
    page.title = "Verificador de Archivos PNG"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Texto donde se mostrará el resultado
    resultado_texto = ft.Text(value="Ningún archivo seleccionado", size=16, weight=ft.FontWeight.BOLD)

    # Función asíncrona moderna para invocar el FilePicker
    async def seleccionar_archivo(e):
        files = await ft.FilePicker().pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg"] 
        )
        
        # Validamos si el usuario seleccionó un archivo o canceló
        if files:
            archivo = files[0] # Tomamos el primer archivo seleccionado de la lista
            nombre_archivo = archivo.name
            
            # Verificamos si termina en .png
            if nombre_archivo.lower().endswith('.png'):
                resultado_texto.value = f"✅ ¡Correcto! '{nombre_archivo}' es un archivo PNG."
                resultado_texto.color = ft.Colors.GREEN_600
            else:
                resultado_texto.value = f"❌ Error: '{nombre_archivo}' NO es un archivo PNG."
                resultado_texto.color = ft.Colors.RED_600
        else:
            resultado_texto.value = "Selección cancelada."
            resultado_texto.color = ft.Colors.ORANGE_600
        
        page.update()

    
    page.add(
        ft.Column(
            controls=[
                ft.Text("Validador de Formato PNG", size=24, weight=ft.FontWeight.BOLD),
                ft.Button(
                    content=ft.Text("Seleccionar archivo"),
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=seleccionar_archivo
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                resultado_texto
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

# Ejecutar la aplicación de forma estándar
ft.run(main)
