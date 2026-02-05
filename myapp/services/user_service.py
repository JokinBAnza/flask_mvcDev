from myapp import db
from myapp.models.user import Usuario

def crear_usuario(username: str, password: str, is_admin: bool = False) -> Usuario:
    """Crea un usuario nuevo y lo guarda en la base de datos."""
    user = Usuario(username=username, is_admin=is_admin)
    user.set_password(password)  # el hash lo hace el modelo
    db.session.add(user)
    db.session.commit()
    return user

def autenticar_usuario(username: str, password: str) -> Usuario | None:
    """Verifica credenciales y devuelve el usuario si son correctas."""
    user = Usuario.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None

def obtener_usuario_por_id(user_id: int) -> Usuario | None:
    """Devuelve un usuario por su ID."""
    return Usuario.query.get(user_id)

def existe_usuario(username: str) -> bool:
    """Devuelve True si ya existe un usuario con ese username."""
    return Usuario.query.filter_by(username=username).first() is not None
