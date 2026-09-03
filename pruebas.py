import customtkinter as ctk
from PIL import Image, ImageTk
import logging
from tkinter import messagebox
import sqlite3 as sql

logging.basicConfig(level=logging.INFO)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Imagen de la empresa >


# Conexion con la bd y creacion de tablas
conexion = sql.connect("Base_de_datos_Tienda_Ropa.db")
cursor = conexion.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (nombre TEXT UNIQUE NOT NULL, contraseña TEXT NOT NULL, rol TEXT NOT NULL)''')


# Clase Usuario
class Usuario():

    def __init__(self, nombre, contraseña, rol):
        self.nombre=nombre
        self.contraseña=contraseña
        self.rol=rol


# Funcion para comprobar si un usuario existe
def comprobar_usuarios(nombre):
    cursor.execute("SELECT * FROM usuarios WHERE nombre = ?", (nombre,))
    fila = cursor.fetchone()
    if fila:
        return Usuario(nombre=fila[0], contraseña=fila[1], rol=fila[2])
    else:
        return None

# Funcion para insertar nuevos usuarios a la base de datos
def ingresar_usuarios(nombre, contraseña, rol):
    cursor.execute("INSERT INTO usuarios VALUES (?, ?, ?)",(nombre, contraseña, rol))
    conexion.commit()


# Ventana de login 
class VentanaLogin(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Tienda de Ropa BOXCLOTHES")
        self.geometry("500x800")
        self.configure(fg_color="black")
        self.resizable(False, False)

        # Fondo más claro
        frame = ctk.CTkFrame(self, fg_color="#141414", border_color="#333333", border_width=1, corner_radius=25)
        frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Variable status para saber en que ventana se está
        self.status_ventana = None

        # Funcion visual de cambio de color de borde login
        def seleccionar_login():
            logging.info("Se ingreso en modo login")
            btn_login.configure(border_color="white", fg_color="#4a1aed")
            lbl_login.configure(text_color="white")
            btn_circular_login.configure(border_color="white", fg_color="white", hover_color="#4a1aed")

            btn_singup.configure(border_color="#828282",fg_color="transparent")
            lbl_singup.configure(text_color="#828282")
            btn_circular_singup.configure(border_color="#828282", fg_color="transparent", hover_color="#333333")

            chk_admin.pack_forget()
            lbl_clave.pack_forget()
            entry_clave.pack_forget()

            self.status_ventana = True
            btn_confirmar.configure(text="Ingresar")

        # Funcion visual de cambio de color de borde singup
        def seleccionar_singup():
            logging.info("Se ingreso en modo singup")
            btn_singup.configure(border_color="white",fg_color="#4a1aed")
            lbl_singup.configure(text_color="white")
            btn_circular_singup.configure(border_color="white", fg_color="white", hover_color="#4a1aed")

            btn_login.configure(border_color="#828282",fg_color="transparent")
            lbl_login.configure(text_color="#828282")
            btn_circular_login.configure(border_color="#828282", fg_color="transparent", hover_color="#333333")

            chk_admin.pack(anchor="w", padx=25, pady=(30,5)) 
            lbl_clave.pack(anchor="w", padx=25, pady=(20, 5)) 
            entry_clave.pack(fill="x", padx=15, pady=(5, 5)) 

            self.status_ventana = False
            btn_confirmar.configure(text="Registrarse")
        # Se checkea si esta puesto el tick, para dejar escribir o no en el entry
        def no_escribir_clave():
            if chk_admin.get() == 1:
                entry_clave.configure(state="normal")
            else:
                entry_clave.configure(state="disabled")

        # Funcion que permite el ingreso de la ventana principal
        def ingresar_tienda():
            posible_usuario = comprobar_usuarios(entry_nombre.get())
            # Comprobar si los campos estan vacios
            if entry_nombre.get() == "" or entry_contraseña.get() == "":
                logging.warning("Campos incompletos")
                messagebox.showwarning( title="Campo incompleto" ,message="Ingrese todos los datos")
            else:
            # login
                if self.status_ventana== True:
                    # Se comprueba si existe o no, caso negativo mensaje de error
                    if posible_usuario:
                        logging.info("El usuario existe")
                        # Confirmar contraseña
                        if posible_usuario.contraseña == entry_contraseña.get():
                            logging.info("Usuario y contraseña correctos")
                            if posible_usuario.rol == "Administrador":
                                self.abrir_tienda_administrador(posible_usuario)
                            else:
                                self.abrir_tienda_cliente(posible_usuario)
                        else:
                            logging.warning("Contraseña incorrecta")
                            messagebox.showwarning( title="Contraseña Incorrecta", message="La contraseña no coindice con la del ususario")
                    else:
                        logging.warning("El usuario no existe")
                        messagebox.showwarning( title="Usuario Inexistente" ,message="El usuario ingresado NO existe en el sistema")
            # singup      
                else:
                    # Comprobamos si existe el usuario para evitar duplicados
                    if posible_usuario:
                        logging.warning("Ya existe un usuario con ese nombre")
                        messagebox.showwarning( title="Usuario ya existente" ,message="Este nombre usuario ingresado ya existe en el sistema")
                    else:
                        # registro como admin
                        if chk_admin.get() == 1:
                            if entry_clave.get() == "23452":
                                logging.info("Clave correcta")
                                ingresar_usuarios(entry_nombre.get(), entry_contraseña.get(), "Administrador")
                            else:
                                logging.warning("Clave incorrecta")
                                messagebox.showwarning( title="Clave Incorrecta" ,message="La clave de administrador ingresada NO es correcta o el campo esta VACIO")
                        # usuario común
                        else:
                            logging.info("No Admin")
                            ingresar_usuarios(entry_nombre.get(), entry_contraseña.get(), "Cliente")


        # Botón de Login
        btn_login = ctk.CTkFrame(frame, fg_color="transparent", border_color="#828282", border_width=1, corner_radius=25, height=70)
        btn_login.pack_propagate(False)
        btn_login.pack(padx=15, pady=(15, 0), fill="x")
        lbl_login = ctk.CTkLabel(btn_login, text="Login", fg_color="transparent", font=("Arial", 24, "normal"), text_color="#828282")
        lbl_login.pack(side="left", padx=20)
        btn_circular_login = ctk.CTkButton(btn_login, text="", width=32, height=32, corner_radius=10, border_width=1, fg_color="transparent", border_color="#828282", hover_color="#333333", command=seleccionar_login)
        btn_circular_login.pack(side="right", padx=20)

        # Botón de Signup
        btn_singup = ctk.CTkFrame(frame, fg_color="#141414", border_color="#828282", border_width=1, corner_radius=25, height=70)
        btn_singup.pack_propagate(False)
        btn_singup.pack(padx=15, pady=(10, 15), fill="x")
        lbl_singup = ctk.CTkLabel(btn_singup, text="Singup", fg_color="transparent", font=("Arial", 24, "normal"), text_color="#828282")
        lbl_singup.pack(side="left", padx=20)
        btn_circular_singup = ctk.CTkButton(btn_singup, text="", width=32, height=32, corner_radius=10, border_width=1, fg_color="transparent", border_color="#828282", hover_color="#333333", command=seleccionar_singup)
        btn_circular_singup.pack(side="right", padx=20)

        # Nombre
        lbl_nombre = ctk.CTkLabel(frame, text="Nombre", text_color="#828282", font=("Arial", 24, "normal"))
        lbl_nombre.pack(anchor="w", padx=25, pady=(5, 5))  

        entry_nombre = ctk.CTkEntry(frame, fg_color="#333333", border_width=0, corner_radius=16, height=50, font=("Arial", 16, "normal"))
        entry_nombre.pack(fill="x", padx=15, pady=(5, 5))

        # Contraseña
        lbl_contraseña = ctk.CTkLabel(frame, text="Contraseña", text_color="#828282", font=("Arial", 24, "normal"))
        lbl_contraseña.pack(anchor="w", padx=25, pady=(20, 5))  

        entry_contraseña = ctk.CTkEntry(frame, fg_color="#333333", border_width=0, corner_radius=16, height=50, show="*", font=("Arial", 16, "normal"))
        entry_contraseña.pack(fill="x", padx=15, pady=(5, 5))

        # Clave Administrador + Checkout administrador
        chk_admin = ctk.CTkCheckBox(frame, text="¿Desea registrarse como administrador?",font=("Arial", 20, "normal"),text_color="#828282",checkmark_color="#828282", fg_color="#828282", hover_color="#828282", border_color="#828282", command=no_escribir_clave)
        chk_admin.pack(anchor="w", padx=25, pady=(30,5)) 

        lbl_clave = ctk.CTkLabel(frame, text="Clave del Administrador", text_color="#828282", font=("Arial", 24, "normal"))
        lbl_clave.pack(anchor="w", padx=25, pady=(20, 5))  

        entry_clave = ctk.CTkEntry(frame, fg_color="#333333", border_width=0, corner_radius=16, height=50, show="*", font=("Arial", 16, "normal"))
        entry_clave.pack(fill="x", padx=15, pady=(5, 5))

        # Frame de Decoracion 
        fr_decoracion= ctk.CTkFrame(frame,fg_color="#4a1aed", border_width=0, height=5, corner_radius=25) 
        fr_decoracion.pack(side="bottom", fill="x",padx=25)


        # Boton de Confirmar
        btn_confirmar= ctk.CTkButton(frame, text="Ingresar", fg_color="#4a1aed", border_width=0, height=70, corner_radius=25,font=("Arial", 24, "normal"),hover_color="#2c1e5c", command= ingresar_tienda)
        btn_confirmar.pack(side="bottom", fill="x", pady=30,padx=25)

        # Botones apretados por default
        btn_circular_login.invoke()
        chk_admin.select()

    # Oculta el login y abre la ventana del admin
    def abrir_tienda_administrador(self, usuario):
        self.withdraw()   
        VentanaTiendaAdministrador(self, usuario)

    # Oculta el login y abre la ventana del cliente
    def abrir_tienda_cliente(self, usuario):
        self.withdraw()   
        VentanaTiendaCliente(self, usuario)


# Ventana de la tienda cliente
class VentanaTiendaCliente(ctk.CTkToplevel):

    def __init__(self, ventana_login, usuario):
        super().__init__(ventana_login)

        self.ventana_login = ventana_login
        self.usuario = usuario

        self.title(f"Tienda de Ropa BOXCLOTHES - cliente {usuario.nombre}")
        self.geometry("1000x1000")   
        self.configure(fg_color="black")

        # Si el usuario cierra esta ventana, se cierra todo
        self.protocol("WM_DELETE_WINDOW", self.cerrar_todo)

        frame = ctk.CTkFrame(self, fg_color="#141414", border_color="#333333", border_width=1, corner_radius=25)
        frame.pack(pady=10, padx=10, fill="both", expand=True)

        lbl_bienvenida = ctk.CTkLabel(frame, text=f"Bienvenido cliente {usuario.nombre}", text_color="white", font=("Arial", 24, "normal"))
        lbl_bienvenida.pack(anchor="w", padx=25, pady=(20, 5))


    # Cierra la ventana de tienda Y la app entera 
    def cerrar_todo(self):
        self.destroy()
        self.ventana_login.destroy()

# Ventana de la tienda administrador
class VentanaTiendaAdministrador(ctk.CTkToplevel):
    def __init__(self, ventana_login, usuario):
        super().__init__(ventana_login)

        self.ventana_login = ventana_login
        self.usuario = usuario

        self.title(f"Tienda de Ropa BOXCLOTHES - admin {usuario.nombre}")
        self.geometry("1000x1000")   
        self.configure(fg_color="black")

        # Si el usuario cierra esta ventana, se cierra todo
        self.protocol("WM_DELETE_WINDOW", self.cerrar_todo)

        frame = ctk.CTkFrame(self, fg_color="#141414", border_color="#333333", border_width=1, corner_radius=25)
        frame.pack(pady=10, padx=10, fill="both", expand=True)

        lbl_bienvenida = ctk.CTkLabel(frame, text=f"Bienvenido admin {usuario.nombre}", text_color="white", font=("Arial", 24, "normal"))
        lbl_bienvenida.pack(anchor="w", padx=25, pady=(20, 5))


    # Cierra la ventana de tienda Y la app entera 
    def cerrar_todo(self):
        self.destroy()
        self.ventana_login.destroy()
    

app = VentanaLogin()
app.mainloop()
conexion.close()