import string
import random
import re

def validate_password(password: str) -> dict:
    errors = []
    if len(password) < 12:
        errors.append("Debe tener al menos 12 caracteres.")
    if not re.search(r'[A-Z]', password):
        errors.append("Debe contener al menos una letra mayúscula.")
    if not re.search(r'[a-z]', password):
        errors.append("Debe contener al menos una letra minúscula.")
    if not re.search(r'[0-9]', password):
        errors.append("Debe contener al menos un número.")
    if not re.search(r'[^A-Za-z0-9]', password):
        errors.append("Debe contener al menos un carácter especial.")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def _ensure_requirements(pwd_chars: list) -> list:
    """Asegura que la lista de caracteres cumpla todos los requisitos."""
    requirements = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]
    # Reemplazar caracteres aleatorios con los requisitos obligatorios
    for i in range(len(requirements)):
        idx = random.randint(0, len(pwd_chars) - 1)
        pwd_chars[idx] = requirements[i]
    return pwd_chars

def generate_from_words(words: str) -> str:
    # Eliminar espacios y juntar todo
    base = "".join(words.split())
    if not base:
        return generate_random()
    
    # Rellenar hasta 12 caracteres si es necesario
    while len(base) < 12:
        base += random.choice(string.ascii_letters + string.digits + string.punctuation)
    
    # Convertir a lista para modificar
    pwd_chars = list(base)
    
    # Asegurar que cumple las reglas
    while not validate_password("".join(pwd_chars))['valid']:
        pwd_chars = _ensure_requirements(pwd_chars)
    
    # Mezclar un poco si las palabras eran muy largas, pero intentaremos mantener la legibilidad
    # si es posible, aunque los requisitos obligan a meter ruido.
    return "".join(pwd_chars)

def generate_random() -> str:
    length = 12 # Generar una de 16 caracteres por seguridad
    all_chars = string.ascii_letters + string.digits + string.punctuation
    
    while True:
        pwd = "".join(random.choice(all_chars) for _ in range(length))
        if validate_password(pwd)['valid']:
            return pwd
