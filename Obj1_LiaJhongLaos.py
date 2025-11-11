def cifrar_cesar(mensaje, clave):
    """
    Objetivo: Cifra un mensaje utilizando el Cifrado César.
    Autor: Lia Jhong Laos (entrega individual)
    
    Consideraciones:
    - Maneja mayúsculas (A-Z)
    - Maneja minúsculas (a-z)
    - Maneja digitos (0-9)
    - Los espacios y símbolos no se modifican.
    
    >>> cifrar_cesar("HOLA MUNDO", 3)
    'KROD PXQGR'
    >>> cifrar_cesar("hola mundo", 3)
    'krod pxqgr'
    >>> cifrar_cesar("Hola Mundo", 3)
    'Krod Pxqgr'
    >>> cifrar_cesar("XYZ", 3)
    'ABC'
    >>> cifrar_cesar("xyz", 3)
    'abc'
    >>> cifrar_cesar("12345", 2)
    '34567'
    >>> cifrar_cesar("7890", 5)
    '2345'
    >>> cifrar_cesar("Esto es... ¡un mensaje! (con simbolos)", 5)
    'Jxyt jx... ¡zs rjsxfoj! (hts xnrgtqtx)'
    >>> cifrar_cesar("Agente 007, ¡misión cumplida! (XYZ)", 1)
    'Bhfouf 118, ¡njtjóo dvnqmjeb! (YZA)'
    >>> cifrar_cesar("No deberia cambiar nada.", 0)
    'No deberia cambiar nada.'
    """
    resultado = ""
    for char in mensaje:
        if 'a' <= char <= 'z':
            base = ord('a')
            offset = (ord(char) - base + clave) % 26
            resultado += chr(base + offset)
        elif 'A' <= char <= 'Z':
            base = ord('A')
            offset = (ord(char) - base + clave) % 26
            resultado += chr(base + offset)
        elif '0' <= char <= '9':
            base = ord('0')
            offset = (ord(char) - base + clave) % 10
            resultado += chr(base + offset)
        else:
            resultado += char
    return resultado


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())

