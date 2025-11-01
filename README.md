   **💻GUI PARA REGISTROS💻** 

  Aplicación de escritorio con interfaz gráfica hecha en **Tkinter** (Python) para realizar operaciones **CRUD** (Crear, Leer, Actualizar y Eliminar) sobre una base de datos SQLite.

  Este proyecto forma parte de mi aprendizaje en desarrollo de software y gestión de datos. Es un ejercicio académico desarrollado con estructura modular y buenas prácticas para que pueda crecer y usarse en entornos reales.




  🎯 **Objetivos del proyecto**

1.  Desarrollar interfaces gráficas en Python.
2.  Hacer uso de SQLite embebido sin dependencias externas.
3.  Separar por capas la estructura (GUI / Lógica / Modelo).




⚙️ ⚙️ **Funcionalidades**

-  Crear nuevos registros
-  Listar registros existentes
-  Editar registros
-  Eliminar registros
-  Base de datos generada automáticamente al ejecutar el programa





🛠 🛠  **Tecnologías utilizadas**

-  Lenguaje  Python 3.x 
-  GUI con Tkinter 
-  Base de datos con SQLite (nativa en Python) 
-  Arquitectura  MVC simplificado (models / views / main)




  
📂 📂 **Estructura del proyecto**

**GUI PARA REGISTROS**

    ├├── main.py # Punto de entrada de la app


    ├├── views/

       ├── app_gui.py # Ventanas / interfaz Tkinter
 
       ├── init.py

    ├├── models/
 
       ├── contacto.py # Modelo de datos (clase)

       ├── database.py # Conexión + CRUD
     
       ├── init.py
    


 ▶️ **Cómo ejecutar el proyecto**

1. Clonar el repositorio:

```bash```

    git clone https://github.com/tu-usuario/Interfaz-para-registros.git

    cd Interfaz-para-registros

2. Ejecutar el programa:

```bash```

    python main.py

No requiere instalación de dependencias externas, solo Python 3.x.






🛠️ 🛠️ **Mejoras futuras**

-  Validaciones de entrada más robustas

-  Exportar datos a CSV / Excel

-  Tema visual más moderno (ttkbootstrap / customtkinter)

-  Soporte para múltiples tablas y modelos

-  Conversión futura a aplicación ejecutable (.exe con PyInstaller)





👨‍💻 👨‍💻 **Autores**

 Desarrollado por:
-  Bergagna, Gabriela
-  Palacios, Fabricio 
-  Barboza, Mariano 
-  Giraudo, Ana Laura
-  Henrry, Patricio
  
Estudiantes de Ciencia de Datos e Inteligencia Artificial.
