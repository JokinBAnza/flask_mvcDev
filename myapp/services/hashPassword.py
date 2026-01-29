from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    """Devuelve el hash seguro de la contraseña."""
    return generate_password_hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verifica si la contraseña coincide con el hash."""
    return check_password_hash(hashed, password)
