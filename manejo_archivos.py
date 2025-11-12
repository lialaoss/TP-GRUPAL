import csv
import os
import datetime


def inicializar_archivos(usuarios_csv, recuperacion_csv, usuarios_campos, recuperacion_campos, mensajes_csv, mensajes_campos):
    """Crea los archivos CSV con sus cabeceras si no existen."""
    if not os.path.exists(usuarios_csv):
        with open(usuarios_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(usuarios_campos)
            
    if not os.path.exists(recuperacion_csv):
        with open(recuperacion_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(recuperacion_campos)
    if not os.path.exists(mensajes_csv):
        with open(mensajes_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(mensajes_campos)


def cargar_preguntas(preguntas_csv):
    """Lee preguntas.csv y devuelve un diccionario {id: pregunta}."""
    preguntas = {}
    try:
        with open(preguntas_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    preguntas[row[0]] = row[1]
    except FileNotFoundError:
        print(f"Error: {preguntas_csv} no encontrado.")
    return preguntas


def _leer_usuarios(usuarios_csv) -> list:
    """Lee todos los usuarios de CSV y devuelve una lista de diccionarios."""
    if not os.path.exists(usuarios_csv):
        return []
    with open(usuarios_csv, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def _escribir_usuarios(usuarios_lista: list, usuarios_csv, usuarios_campos):
    """Sobrescribe usuarios.csv con la lista de usuarios actualizada."""
    with open(usuarios_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=usuarios_campos)
        writer.writeheader()
        writer.writerows(usuarios_lista)


def _log_intento_fallido(id_usuario: str, recuperacion_csv, recuperacion_campos):
    """Registra un intento fallido en recuperacion.csv."""
    with open(recuperacion_csv, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=recuperacion_campos)
        writer.writerow({
            'Id_usuario': id_usuario,
            'timestamp': datetime.datetime.now().isoformat()
        })


def verificar_usuario_existe(id_usuario, usuarios_csv) -> bool:
    """Verifica si un Id_usuario existe en usuarios.csv."""
    usuarios = _leer_usuarios(usuarios_csv)
    usuario_existente = False
    i = 0
    while i < len(usuarios) and not usuario_existente:
        if usuarios[i]['Id_usuario'] == id_usuario:
            usuario_existente = True
        i += 1
    return usuario_existente


def guardar_mensaje_csv(remitente, destinatario, cifrado, mensaje_cifrado, mensajes_csv, mensajes_campos):
    """Guarda un nuevo mensaje en mensajes.csv (modo append)."""
    nuevo_mensaje = {
        'remitente': remitente,
        'destinatario': destinatario,
        'cifrado': cifrado,
        'mensaje-cifrado': mensaje_cifrado
    }
    with open(mensajes_csv, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=mensajes_campos)
        writer.writerow(nuevo_mensaje)


def registrar_usuario_csv(id_usuario, clave, id_pregunta, respuesta, usuarios_csv, usuarios_campos):
    """
    Intenta registrar un nuevo usuario.
    Devuelve (True, "Mensaje") o (False, "Error").
    """
    usuarios = _leer_usuarios(usuarios_csv)
    usuario_existente = False
    i = 0
    while i < len(usuarios) and not usuario_existente:
        if usuarios[i]['Id_usuario'] == id_usuario:
            usuario_existente = True
        i += 1
            
    if usuario_existente:
        return (False, "Identificador en uso")
    nuevo_usuario = {
        'Id_usuario': id_usuario,
        'clave_usuario': clave,
        'id_pregunta': id_pregunta,
        'respuesta_recuperacion': respuesta.lower(),
        'intentos_recuperacion': 0
    }
    usuarios.append(nuevo_usuario)
    _escribir_usuarios(usuarios, usuarios_csv, usuarios_campos)
    return (True, "Usuario creado exitosamente")


def validar_ingreso_csv(id_usuario, clave, usuarios_csv, usuarios_campos):
    """
    Valida el ingreso de un usuario.
    Devuelve (True, "Mensaje") o (False, "Error").
    """
    usuarios = _leer_usuarios(usuarios_csv)
    usuario_encontrado = None
    i = 0
    encontrado = False
    while i < len(usuarios) and not encontrado:
        if usuarios[i]['Id_usuario'] == id_usuario:
            usuario_encontrado = usuarios[i]
            encontrado = True
        i += 1

    if not usuario_encontrado:
        return (False, "Identificador inexistente o clave errónea")

    if int(usuario_encontrado['intentos_recuperacion']) >= 3:
        return (False, "Usuario bloqueado")

    if usuario_encontrado['clave_usuario'] != clave:
        return (False, "Identificador inexistente o clave errónea")
    if int(usuario_encontrado['intentos_recuperacion']) > 0:
        usuario_encontrado['intentos_recuperacion'] = 0
        _escribir_usuarios(usuarios, usuarios_csv, usuarios_campos)
    return (True, "Ingreso exitoso")


def obtener_pregunta_csv(id_usuario, usuarios_csv, preguntas_csv) -> tuple:
    """
    Obtiene la pregunta de seguridad de un usuario.
    Devuelve (pregunta_texto, "Mensaje") o (None, "Error").
    """
    usuarios = _leer_usuarios(usuarios_csv)
    usuario_encontrado = None
    i = 0
    encontrado = False
    while i < len(usuarios) and not encontrado:
        if usuarios[i]['Id_usuario'] == id_usuario:
            usuario_encontrado = usuarios[i]
            encontrado = True
        i += 1
            
    if not usuario_encontrado:
        return (None, "Usuario no encontrado")
    if int(usuario_encontrado['intentos_recuperacion']) >= 3:
        return (None, "Usuario bloqueado")
    preguntas = cargar_preguntas(preguntas_csv)
    id_pregunta = usuario_encontrado['id_pregunta']
    
    if id_pregunta not in preguntas:
        return (None, "Error: Pregunta no encontrada")
        
    return (preguntas[id_pregunta], "Pregunta encontrada")


def procesar_recuperacion_csv(id_usuario, respuesta_ingresada, usuarios_csv, usuarios_campos, recuperacion_csv, recuperacion_campos) -> tuple:
    """
    Procesa la respuesta de recuperación.
    Devuelve (True, clave_secreta) o (False, "Error").
    """
    usuarios = _leer_usuarios(usuarios_csv)
    usuario_encontrado = None
    indice_usuario = -1
    i = 0
    encontrado = False
    while i < len(usuarios) and not encontrado:
        if usuarios[i]['Id_usuario'] == id_usuario:
            usuario_encontrado = usuarios[i]
            indice_usuario = i
            encontrado = True
        i += 1
            
    if not usuario_encontrado:
        return (False, "Error inesperado: Usuario no encontrado")
    if usuario_encontrado['respuesta_recuperacion'] == respuesta_ingresada.lower():
        usuarios[indice_usuario]['intentos_recuperacion'] = 0
        _escribir_usuarios(usuarios, usuarios_csv, usuarios_campos)
        return (True, usuario_encontrado['clave_usuario'])
    else:
        # Falla: Incrementa intentos, loguea y devuelve error
        _log_intento_fallido(id_usuario, recuperacion_csv, recuperacion_campos)
        intentos_actuales = int(usuarios[indice_usuario]['intentos_recuperacion'])
        intentos_actuales += 1
        usuarios[indice_usuario]['intentos_recuperacion'] = intentos_actuales
        _escribir_usuarios(usuarios, usuarios_csv, usuarios_campos)
        if intentos_actuales >= 3:
            return (False, "Respuesta incorrecta. Usuario bloqueado.")
        else:
            return (False, "Respuesta incorrecta.")


def obtener_mensajes_csv(id_usuario, mensajes_csv) -> tuple:
    """
    Lee mensajes.csv y devuelve dos listas (para_todos, para_mi),
    con los mensajes CIFRADOS.
    """
    mensajes_todos = []
    mensajes_propios = []
    try:
        with open(mensajes_csv, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fila = next(reader, None)
            while fila is not None:
                if fila['destinatario'] == id_usuario:
                    mensajes_propios.append(fila)
                elif fila['destinatario'] == '*':
                    mensajes_todos.append(fila)
                fila = next(reader, None)
    except FileNotFoundError:
        print(f"Error: {mensajes_csv} no encontrado.")
    except Exception as e:
        print(f"Error al leer {mensajes_csv}: {e}")
    mensajes_todos.reverse()
    mensajes_propios.reverse()
    return (mensajes_todos, mensajes_propios)