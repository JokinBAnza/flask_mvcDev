# Sistema de Gestión de Biblioteca Web

## Descripción

Esta es una aplicación web desarrollada con **Flask**, **SQLite** y **Flask-WTF**, que permite gestionar libros y socios de una biblioteca.  
La aplicación permite crear, listar, buscar, prestar y devolver libros, así como gestionar los socios que tienen préstamos activos.

---

## Tecnologías utilizadas

- Python 3
- Flask
- SQLite
- Flask-WTF
- SQLAlchemy
- Flask-Login (opcional para autenticación)
- Jinja2 (templates HTML)

---

## Estructura del proyecto

myapp/
│
├─ controllers/
│ ├─ libros_controller.py  # Rutas y lógica de libros
│ └─ socios_controller.py  # Rutas y lógica de socios
│
├─ models/
│ ├─ libro.py
│ ├─ socio.py
│ └─ prestamo.py
│
├─ services/
│ └─ libros_service.py  # Funciones para CRUD de libros
│
├─ forms/
│ ├─ libro_form.py
│ └─ socio_form.py
│
├─ decorators/
│ └─ libro_disponible.py  # Decorador para verificar disponibilidad de libros
│
├─ templates/
│ ├─ base.html
│ ├─ paginas/
│ │ ├─ libros/  # Templates de libros (listado, detalle, prestar, devolver)
│ │ └─ socios/  # Templates de socios (listado, crear, préstamos)
│
└─ run.py  # Archivo principal para iniciar la app

---

## Funcionalidades

### Libros

- Listar todos los libros y su estado (disponible/prestado)
- Listar solo los libros disponibles
- Buscar libros por título (no distingue mayúsculas/minúsculas)
- Crear nuevos libros
- Editar libros existentes
- Prestar un libro a un socio (verifica que el libro esté disponible y que el socio no tenga otro libro)
- Devolver un libro mediante el socio que lo tiene prestado
- Visualizar todos los libros prestados junto con el socio que los tiene

### Socios

- Crear socios
- Listar todos los socios
- Ver socios que tienen actualmente un libro prestado

### Formularios (Flask-WTF)

- Formulario de búsqueda de libros
- Formulario de creación/edición de libros
- Formulario de préstamo de libros
- Formulario de devolución de libros
- Todos los formularios validan la entrada y muestran mensajes de error claros

### Decoradores

- `@libro_disponible`: Verifica si un libro está disponible antes de prestarlo  
- Evita duplicación de lógica y asegura reglas de negocio en un solo lugar

### Autenticación (opcional)

- Se recomienda utilizar Flask-Login para la gestión de usuarios
- Las operaciones de préstamos, devoluciones y creación requieren autenticación

---

## API (JSON)

- `GET /api/libros` → Devuelve todos los libros  
- `GET /api/libros/disponibles` → Devuelve solo libros disponibles  
- `GET /api/libros/buscar/<titulo>` → Libros cuyo título contenga `<titulo>`  
- `GET /api/libros/socios/prestamos` → Listado de socios con libros prestados  

---

## Instalación y ejecución

Crear y activar el entorno virtual, instalar dependencias, inicializar la base de datos y ejecutar la aplicación:

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Inicializar base de datos
# Si tienes un script para poblar datos iniciales
python seed.py  # opcional

# Crear tablas en SQLite
python -c "from myapp import db; db.create_all()"

# Ejecutar la aplicación
python run.py

Abrir en el navegador:

http://127.0.0.1:5000/
```
Posibles mejoras futuras

Añadir autenticación de usuarios con roles más complejos

Añadir categorías o géneros a los libros

Mejorar el diseño de la interfaz con CSS/Bootstrap

Integrar notificaciones para libros vencidos

Exportar listado de libros o socios a CSV/PDF