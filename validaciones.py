import doctest


def validar_usuario(usuario: str) -> bool:
    """
    Objetivo: Valida que el ID de usuario cumpla las reglas.
    Autor: [Tu Nombre]

    Reglas:
    - Longitud: 5 a 15 caracteres.
    - Caracteres permitidos: letras (a-z, A-Z), números (0-9), '_', '-', '.'

    >>> # --- Casos Válidos ---
    >>> # 1. Caso simple
    >>> validar_usuario("usuario1")
    True
    >>> # 2. Caso con todos los permitidos
    >>> validar_usuario("user.1-2_3")
    True
    >>> # 3. Caso de longitud mínima (5)
    >>> validar_usuario("abc_1")
    True
    >>> # 4. Caso de longitud máxima (15)
    >>> validar_usuario("12345.6789-0_12")
    True
    
    >>> # --- Casos Inválidos ---
    >>> # 5. Inválido (muy corto)
    >>> validar_usuario("usr")
    False
    >>> # 6. Inválido (muy largo)
    >>> validar_usuario("un_usuario_muy_largo_123")
    False
    >>> # 7. Inválido (caracter '!')
    >>> validar_usuario("user!")
    False
    >>> # 8. Inválido (caracter '@')
    >>> validar_usuario("user@123")
    False
    >>> # 9. Inválido (espacio)
    >>> validar_usuario("user 123")
    False
    >>> # 10. Inválido (vacío)
    >>> validar_usuario("")
    False
    """
    if not 5 <= len(usuario) <= 15:
        return False
    caracteres_permitidos = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-"
    for char in usuario:
        if char not in caracteres_permitidos:
            return False
    return True


def validar_clave(clave: str) -> bool:
    """
    Objetivo: Valida que la clave de usuario cumpla las reglas.
    Autor: [Tu Nombre]

    Reglas:
    - Longitud: 4 a 8 caracteres.
    - 1+ mayúscula, 1+ minúscula, 1+ número.
    - 1+ caracter especial ('_', '-', '#', '*').
    - No hay caracteres adyacentes repetidos.

    >>> # --- Casos Válidos ---
    >>> # 1. Caso simple (longitud mínima 4)
    >>> validar_clave("A_b1")
    True
    >>> # 2. Caso complejo (longitud 7)
    >>> validar_clave("#aB7*c")
    True
    >>> # 3. Caso simple (longitud máxima 8)
    >>> validar_clave("-Test#12")
    True
    
    >>> # --- Casos Inválidos ---
    >>> # 4. Inválido (muy corta)
    >>> validar_clave("A_1")
    False
    >>> # 5. Inválido (muy larga)
    >>> validar_clave("Abc_12345")
    False
    >>> # 6. Inválido (sin mayúscula)
    >>> validar_clave("a_b1")
    False
    >>> # 7. Inválido (sin minúscula)
    >>> validar_clave("A_B1")
    False
    >>> # 8. Inválido (sin número)
    >>> validar_clave("A_b*")
    False
    >>> # 9. Inválido (sin especial)
    >>> validar_clave("AaB1")
    False
    >>> # 10. Inválido (adyacente letra)
    >>> validar_clave("AA_b1")
    False
    >>> # 11. Inválido (adyacente número)
    >>> validar_clave("A_b11")
    False
    >>> # 12. Inválido (adyacente especial)
    >>> validar_clave("A__b1")
    False
    """
    if not 4 <= len(clave) <= 8:
        return False
    for i in range(len(clave) - 1):
        if clave[i] == clave[i+1]:
            return False
    tiene_mayus, tiene_minus, tiene_num, tiene_especial = False, False, False, False
    especiales_permitidos = "_-#*"
    for char in clave:
        if 'a' <= char <= 'z':
            tiene_minus = True
        elif 'A' <= char <= 'Z':
            tiene_mayus = True
        elif '0' <= char <= '9':
            tiene_num = True
        elif char in especiales_permitidos:
            tiene_especial = True
    return all([tiene_mayus, tiene_minus, tiene_num, tiene_especial])


if __name__ == "__main__":
    doctest.testmod(verbose=True)


