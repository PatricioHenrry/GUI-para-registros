# models/database.py
import sqlite3
from .contacto import Contacto

# -------------------------------
# Clase BaseDatos
# -------------------------------
class BaseDatos:
    def __init__(self, nombre_db="contactos.db"):
        self.conn = sqlite3.connect(nombre_db)
        self.crear_tabla()
        self.cargar_datos_ejemplo()  # Cargar datos de ejemplo si la DB está vacía

    def crear_tabla(self):
        query = """CREATE TABLE IF NOT EXISTS contactos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    email TEXT NOT NULL
                )"""
        self.conn.execute(query)
        self.conn.commit()

    def agregar_contacto(self, contacto):
        query = "INSERT INTO contactos (nombre, apellido, telefono, email) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (contacto.nombre, contacto.apellido, contacto.telefono, contacto.email))
        self.conn.commit()

    def eliminar_contacto(self, contacto_id):
        query = "DELETE FROM contactos WHERE id=?"
        self.conn.execute(query, (contacto_id,))
        self.conn.commit()

    def modificar_contacto(self, contacto_id, contacto):
        query = """UPDATE contactos 
                   SET nombre=?, apellido=?, telefono=?, email=? 
                   WHERE id=?"""
        self.conn.execute(query, (contacto.nombre, contacto.apellido, contacto.telefono, contacto.email, contacto_id))
        self.conn.commit()

    def listar_contactos(self):
        cursor = self.conn.execute("SELECT * FROM contactos")
        return cursor.fetchall()

    def vaciar_lista(self):
        """Elimina todos los contactos de la base de datos"""
        query = "DELETE FROM contactos"
        self.conn.execute(query)
        self.conn.commit()

    def verificar_duplicados(self, email, telefono, contacto_id=None):
        """Verifica si ya existe un contacto con el mismo email o teléfono"""
        # Para modificación, excluir el contacto actual de la búsqueda
        if contacto_id:
            cursor = self.conn.execute(
                "SELECT id, email, telefono FROM contactos WHERE (email=? OR telefono=?) AND id!=?",
                (email, telefono, contacto_id)
            )
        else:
            cursor = self.conn.execute(
                "SELECT id, email, telefono FROM contactos WHERE email=? OR telefono=?",
                (email, telefono)
            )
        
        resultado = cursor.fetchone()
        if resultado:
            if resultado[1] == email:
                return "email"
            elif resultado[2] == telefono:
                return "telefono"
        return None

    def cerrar_conexion(self):
        self.conn.close()

    def cargar_datos_ejemplo(self):
        """Carga 30 contactos de ejemplo si la base de datos está vacía"""
        # Verificar si ya hay contactos
        cursor = self.conn.execute("SELECT COUNT(*) FROM contactos")
        cantidad = cursor.fetchone()[0]
        
        if cantidad > 0:
            return  # Si ya hay contactos, no cargar ejemplos
        
        contactos_ejemplo = [
            ("Ana", "García", "011-1234-5678", "ana.garcia@email.com"),
            ("Carlos", "Rodríguez", "011-2345-6789", "carlos.rodriguez@gmail.com"),
            ("María", "López", "011-3456-7890", "maria.lopez@hotmail.com"),
            ("Juan", "Martínez", "011-4567-8901", "juan.martinez@yahoo.com"),
            ("Laura", "González", "011-5678-9012", "laura.gonzalez@email.com"),
            ("Diego", "Fernández", "011-6789-0123", "diego.fernandez@gmail.com"),
            ("Sofía", "Pérez", "011-7890-1234", "sofia.perez@hotmail.com"),
            ("Miguel", "Sánchez", "011-8901-2345", "miguel.sanchez@email.com"),
            ("Valentina", "Romero", "011-9012-3456", "valentina.romero@gmail.com"),
            ("Alejandro", "Torres", "011-0123-4567", "alejandro.torres@yahoo.com"),
            ("Camila", "Flores", "011-1357-2468", "camila.flores@email.com"),
            ("Mateo", "Morales", "011-2468-1357", "mateo.morales@hotmail.com"),
            ("Isabella", "Herrera", "011-3579-2468", "isabella.herrera@gmail.com"),
            ("Sebastián", "Jiménez", "011-4680-1357", "sebastian.jimenez@email.com"),
            ("Martina", "Ruiz", "011-5791-2468", "martina.ruiz@yahoo.com"),
            ("Nicolás", "Díaz", "011-6802-3579", "nicolas.diaz@hotmail.com"),
            ("Emma", "Vargas", "011-7913-4680", "emma.vargas@gmail.com"),
            ("Lucas", "Castro", "011-8024-5791", "lucas.castro@email.com"),
            ("Mía", "Ortega", "011-9135-6802", "mia.ortega@hotmail.com"),
            ("Tomás", "Ramos", "011-0246-7913", "tomas.ramos@yahoo.com"),
            ("Zoe", "Mendoza", "011-1470-8024", "zoe.mendoza@gmail.com"),
            ("Emilio", "Aguilar", "011-2581-9135", "emilio.aguilar@email.com"),
            ("Alma", "Medina", "011-3692-0246", "alma.medina@hotmail.com"),
            ("Joaquín", "Reyes", "011-4703-1470", "joaquin.reyes@gmail.com"),
            ("Renata", "Guerrero", "011-5814-2581", "renata.guerrero@yahoo.com"),
            ("Gael", "Muñoz", "011-6925-3692", "gael.munoz@email.com"),
            ("Catalina", "Iglesias", "011-7036-4703", "catalina.iglesias@hotmail.com"),
            ("Bautista", "Cortés", "011-8147-5814", "bautista.cortes@gmail.com"),
            ("Delfina", "Rubio", "011-9258-6925", "delfina.rubio@email.com"),
            ("Thiago", "Moreno", "011-0369-7036", "thiago.moreno@yahoo.com")
        ]
        
        # Insertar todos los contactos de ejemplo
        query = "INSERT INTO contactos (nombre, apellido, telefono, email) VALUES (?, ?, ?, ?)"
        self.conn.executemany(query, contactos_ejemplo)
        self.conn.commit()