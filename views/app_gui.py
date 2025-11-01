# views/app_gui.py
import tkinter as tk
from tkinter import messagebox, ttk
from models import BaseDatos, Contacto

# -------------------------------
# Clase App (Interfaz Gráfica)
# -------------------------------
class App:
    def __init__(self, root):
        self.db = BaseDatos()

        self.root = root
        self.root.title("Libreta de Contactos - ABM")

        # Campos de entrada
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.email_var = tk.StringVar()

        tk.Label(root, text="Nombre").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        tk.Entry(root, textvariable=self.nombre_var).grid(row=0, column=1, padx=5, pady=2)

        tk.Label(root, text="Apellido").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        tk.Entry(root, textvariable=self.apellido_var).grid(row=1, column=1, padx=5, pady=2)

        tk.Label(root, text="Teléfono").grid(row=2, column=0, padx=5, pady=2, sticky="e")
        tk.Entry(root, textvariable=self.telefono_var).grid(row=2, column=1, padx=5, pady=2)

        tk.Label(root, text="Email").grid(row=3, column=0, padx=5, pady=2, sticky="e")
        tk.Entry(root, textvariable=self.email_var).grid(row=3, column=1, padx=5, pady=2)

        # Botones
        tk.Button(root, text="Agregar", command=self.agregar_contacto).grid(row=4, column=0, pady=10, padx=5)
        tk.Button(root, text="Modificar", command=self.modificar_contacto).grid(row=4, column=1, pady=10, padx=5)
        tk.Button(root, text="Eliminar", command=self.eliminar_contacto).grid(row=4, column=2, pady=10, padx=5)
        tk.Button(root, text="Limpiar", command=self.limpiar_campos).grid(row=4, column=3, pady=10, padx=5)
        tk.Button(root, text="Vaciar Lista", command=self.vaciar_lista, bg="red", fg="white").grid(row=4, column=4, pady=10, padx=5)

        # Lista de contactos
        self.tree = ttk.Treeview(root, columns=("ID", "Nombre", "Apellido", "Teléfono", "Email"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Email", text="Email")
        
        # Configurar el ancho de las columnas
        self.tree.column("ID", width=50)
        self.tree.column("Nombre", width=120)
        self.tree.column("Apellido", width=120)
        self.tree.column("Teléfono", width=120)
        self.tree.column("Email", width=200)
        
        self.tree.grid(row=5, column=0, columnspan=5, padx=10, pady=10)

        # Scrollbar para el treeview
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=5, column=5, sticky='ns', pady=10)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.cargar_contactos()

        # Selección de fila
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_contacto)

        self.contacto_id = None
        
        # Manejar el cierre de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    # -------------------------------
    # Funciones de la interfaz
    # -------------------------------
    def validar_campos(self):
        """Valida que todos los campos estén llenos"""
        if not all([self.nombre_var.get().strip(), self.apellido_var.get().strip(),
                   self.telefono_var.get().strip(), self.email_var.get().strip()]):
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return False
        return True

    def validar_email(self, email):
        """Validación básica de formato de email"""
        if "@" not in email or "." not in email:
            messagebox.showwarning("Error", "El formato del email no es válido")
            return False
        return True

    def validar_telefono(self, telefono):
        """Valida que el teléfono solo contenga números, espacios, guiones y paréntesis"""
        # Caracteres permitidos: dígitos, espacios, guiones, paréntesis y el signo +
        caracteres_permitidos = "0123456789 -()+"
        
        if not telefono:
            messagebox.showwarning("Error", "El teléfono no puede estar vacío")
            return False
        
        # Verificar que solo contenga caracteres permitidos
        for caracter in telefono:
            if caracter not in caracteres_permitidos:
                messagebox.showwarning("Error", 
                    f"El teléfono solo puede contener números, espacios, guiones, paréntesis y el signo +\n"
                    f"Caracter no válido encontrado: '{caracter}'")
                return False
        
        # Verificar que tenga al menos algunos dígitos
        if not any(c.isdigit() for c in telefono):
            messagebox.showwarning("Error", "El teléfono debe contener al menos un número")
            return False
        
        # Verificar longitud mínima (al menos 7 dígitos)
        digitos = ''.join(c for c in telefono if c.isdigit())
        if len(digitos) < 7:
            messagebox.showwarning("Error", "El teléfono debe tener al menos 7 dígitos")
            return False
        
        return True

    def limpiar_campos(self):
        """Limpia todos los campos de entrada"""
        self.nombre_var.set("")
        self.apellido_var.set("")
        self.telefono_var.set("")
        self.email_var.set("")
        self.contacto_id = None

    def agregar_contacto(self):
        if not self.validar_campos():
            return
        
        email = self.email_var.get().strip()
        telefono = self.telefono_var.get().strip()
        
        # Validar formato de email
        if not self.validar_email(email):
            return
        
        # Validar formato de teléfono
        if not self.validar_telefono(telefono):
            return
        
        # Verificar duplicados
        duplicado = self.db.verificar_duplicados(email, telefono)
        if duplicado == "email":
            messagebox.showwarning("Error", f"Ya existe un contacto con el email: {email}")
            return
        elif duplicado == "telefono":
            messagebox.showwarning("Error", f"Ya existe un contacto con el teléfono: {telefono}")
            return
            
        contacto = Contacto(self.nombre_var.get().strip(), self.apellido_var.get().strip(),
                            telefono, email)
        self.db.agregar_contacto(contacto)
        self.cargar_contactos()
        self.limpiar_campos()
        messagebox.showinfo("Éxito", "Contacto agregado correctamente")

    def eliminar_contacto(self):
        if self.contacto_id:
            respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este contacto?")
            if respuesta:
                self.db.eliminar_contacto(self.contacto_id)
                self.cargar_contactos()
                self.limpiar_campos()
                messagebox.showinfo("Éxito", "Contacto eliminado")
        else:
            messagebox.showwarning("Error", "Seleccione un contacto")

    def modificar_contacto(self):
        if not self.contacto_id:
            messagebox.showwarning("Error", "Seleccione un contacto")
            return
            
        if not self.validar_campos():
            return
        
        email = self.email_var.get().strip()
        telefono = self.telefono_var.get().strip()
        
        # Validar formato de email
        if not self.validar_email(email):
            return
        
        # Validar formato de teléfono
        if not self.validar_telefono(telefono):
            return
        
        # Verificar duplicados (excluyendo el contacto actual)
        duplicado = self.db.verificar_duplicados(email, telefono, self.contacto_id)
        if duplicado == "email":
            messagebox.showwarning("Error", f"Ya existe otro contacto con el email: {email}")
            return
        elif duplicado == "telefono":
            messagebox.showwarning("Error", f"Ya existe otro contacto con el teléfono: {telefono}")
            return
            
        contacto = Contacto(self.nombre_var.get().strip(), self.apellido_var.get().strip(),
                            telefono, email)
        self.db.modificar_contacto(self.contacto_id, contacto)
        self.cargar_contactos()
        self.limpiar_campos()
        messagebox.showinfo("Éxito", "Contacto modificado")

    def cargar_contactos(self):
        # Limpiar el treeview
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Cargar contactos desde la base de datos
        for fila in self.db.listar_contactos():
            self.tree.insert("", "end", values=fila)

    def seleccionar_contacto(self, event):
        item = self.tree.selection()
        if item:
            contacto = self.tree.item(item)["values"]
            self.contacto_id = contacto[0]
            self.nombre_var.set(contacto[1])
            self.apellido_var.set(contacto[2])
            self.telefono_var.set(contacto[3])
            self.email_var.set(contacto[4])

    def cerrar_aplicacion(self):
        """Cierra la conexión a la base de datos y la aplicación"""
        self.db.cerrar_conexion()
        self.root.destroy()

    def vaciar_lista(self):
        """Elimina todos los contactos de la lista"""
        if not self.db.listar_contactos():
            messagebox.showinfo("Información", "La lista ya está vacía")
            return
            
        respuesta = messagebox.askyesno(
            "Confirmar", 
            "¿Está seguro de eliminar TODOS los contactos?\n\nEsta acción no se puede deshacer."
        )
        if respuesta:
            self.db.vaciar_lista()
            self.cargar_contactos()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Todos los contactos han sido eliminados")