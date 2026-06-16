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

def _truncate_and_fix(pwd_str: str, max_length: int = 12) -> str:
    """Trunca a max_length caracteres y asegura que cumpla los requisitos."""
    # Rellenar hasta max_length si es necesario
    while len(pwd_str) < max_length:
        pwd_str += random.choice(string.ascii_letters + string.digits + string.punctuation)
    # Truncar a max_length
    pwd_str = pwd_str[:max_length]
    # Asegurar requisitos
    pwd_chars = list(pwd_str)
    while not validate_password("".join(pwd_chars))['valid']:
        pwd_chars = _ensure_requirements(pwd_chars)
    return "".join(pwd_chars)


def generate_from_words(words: str) -> str:
    # Validar longitud máxima de la cadena
    if len(words) > 75:
        raise ValueError("La entrada no puede exceder los 75 caracteres.")

    # Validar máximo 3 palabras
    word_list = words.split()
    if len(word_list) > 3:
        raise ValueError("Se permiten máximo 3 palabras.")

    # Eliminar espacios y juntar todo
    base = "".join(word_list)
    if not base:
        return generate_random()
    
    return _truncate_and_fix(base)

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
    """Genera múltiples contraseñas diferentes a partir de palabras base.
    Máximo 3 palabras y máximo 75 caracteres. Todas las contraseñas tienen exactamente 12 caracteres."""
    # Validar longitud máxima de la cadena
    if len(words) > 75:
        raise ValueError("La entrada no puede exceder los 75 caracteres.")

    word_list = words.split()
    if len(word_list) > 3:
        raise ValueError("Se permiten máximo 3 palabras.")

    base = "".join(word_list)
    passwords = []

    # --- Tipo 1: Basada en palabras (estrategia original mejorada) ---
    pwd1 = generate_from_words(words)
    passwords.append(pwd1)

    # --- Tipo 2: Leet Speak ---
    leet_base = _leet_speak(base)
    passwords.append(_truncate_and_fix(leet_base))

    # --- Tipo 3: CamelCase + Símbolos ---
    camel_base = _camel_case_with_symbols(word_list)
    passwords.append(_truncate_and_fix(camel_base))

    # --- Tipo 4: Aleatoria (12 caracteres) ---
    passwords.append(generate_random(length=12))

    return passwords
