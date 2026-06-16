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

def generate_random(length: int = 12) -> str:
    all_chars = string.ascii_letters + string.digits + string.punctuation
    
    while True:
        pwd = "".join(random.choice(all_chars) for _ in range(length))
        if validate_password(pwd)['valid']:
            return pwd


def validate_password_detailed(password: str) -> dict:
    """Retorna el estado individual de cada requisito de seguridad."""
    return {
        'valid': all([
            len(password) >= 12,
            bool(re.search(r'[A-Z]', password)),
            bool(re.search(r'[a-z]', password)),
            bool(re.search(r'[0-9]', password)),
            bool(re.search(r'[^A-Za-z0-9]', password)),
        ]),
        'checks': {
            'length': len(password) >= 12,
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'lowercase': bool(re.search(r'[a-z]', password)),
            'number': bool(re.search(r'[0-9]', password)),
            'special': bool(re.search(r'[^A-Za-z0-9]', password)),
        }
    }


def _leet_speak(text: str) -> str:
    """Aplica sustituciones leet speak al texto."""
    leet_map = {
        'a': '@', 'A': '@',
        'e': '3', 'E': '3',
        's': '$', 'S': '$',
        'o': '0', 'O': '0',
        'i': '!', 'I': '!',
        't': '7', 'T': '7',
    }
    return "".join(leet_map.get(c, c) for c in text)


def _camel_case_with_symbols(words: list) -> str:
    """Capitaliza cada palabra e intercala números y símbolos."""
    symbols = list("!@#$%&*")
    result = ""
    for i, word in enumerate(words):
        if word:
            result += word.capitalize()
            if i < len(words) - 1:
                result += random.choice(symbols)
                result += str(random.randint(0, 9))
    return result


def generate_multiple_from_words(words: str, count: int = 4) -> list:
    """Genera múltiples contraseñas diferentes a partir de palabras base."""
    word_list = words.split()
    base = "".join(word_list)
    passwords = []

    # --- Tipo 1: Basada en palabras (estrategia original mejorada) ---
    pwd1 = generate_from_words(words)
    passwords.append(pwd1)

    # --- Tipo 2: Leet Speak ---
    leet_base = _leet_speak(base)
    while len(leet_base) < 12:
        leet_base += random.choice(string.ascii_letters + string.digits + string.punctuation)
    leet_chars = list(leet_base)
    while not validate_password("".join(leet_chars))['valid']:
        leet_chars = _ensure_requirements(leet_chars)
    passwords.append("".join(leet_chars))

    # --- Tipo 3: CamelCase + Símbolos ---
    camel_base = _camel_case_with_symbols(word_list)
    while len(camel_base) < 12:
        camel_base += random.choice(string.ascii_letters + string.digits + string.punctuation)
    camel_chars = list(camel_base)
    while not validate_password("".join(camel_chars))['valid']:
        camel_chars = _ensure_requirements(camel_chars)
    passwords.append("".join(camel_chars))

    # --- Tipo 4: Aleatoria (16 caracteres) ---
    passwords.append(generate_random(length=16))

    return passwords
