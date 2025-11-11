def cifrar_atbash(mensaje):
    """
    Objetivo: Cifra un mensaje utilizando el Cifrado Atbash (alfabeto
    invertido) e invirtiendo mayúsculas/minúsculas.
    Autor: Lia Jhong Laos (entrega individual)
    
    Reglas:
    1. Invierte el alfabeto (A->Z, B->Y, ...).
    2. Invierte los dígitos (0->9, 1->8, ...).
    3. Intercambia mayúsculas por minúsculas, y viceversa.
    4. Los espacios y símbolos no se modifican.
    
    >>> cifrar_atbash("HOLA MUNDO")
    'sloz nfmwl'
    >>> cifrar_atbash("sloz nfmwl")
    'HOLA MUNDO'
    >>> cifrar_atbash("12345")
    '87654'
    >>> cifrar_atbash("9876543210")
    '0123456789'
    >>> cifrar_atbash("HolaMundo")
    'sLOZnFMWL'
    >>> cifrar_atbash("¿Esto... es, un Test?")
    '¿vHGL... VH, FM gVHG?'
    >>> cifrar_atbash("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    'zyxwvutsrqponmlkjihgfedcba'
    >>> cifrar_atbash("abcdefghijklmnopqrstuvwxyz")
    'ZYXWVUTSRQPONMLKJIHGFEDCBA'
    >>> cifrar_atbash("Agente 007 (OK?)")
    'zTVMGV 992 (lp?)'
    >>> cifrar_atbash("")
    ''
    """
    
    resultado = ""
    for char in mensaje:
        if 'A' <= char <= 'Z':
            base_ascii = ord('A') + ord('Z')
            inver_ascii = base_ascii - ord(char)
            resultado += chr(inver_ascii).lower()
        elif 'a' <= char <= 'z':
            base_ascii = ord('a') + ord('z')
            inver_ascii = base_ascii - ord(char)
            resultado += chr(inver_ascii).upper()
        elif '0' <= char <= '9':
            base_ascii = ord('0') + ord('9')
            inver_ascii = base_ascii - ord(char)
            resultado += chr(inver_ascii)
        else:
            resultado += char
    return resultado


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())