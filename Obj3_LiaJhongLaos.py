import tkinter as tk
import manejo_archivos 
from tkinter import messagebox
from tkinter import ttk
from Obj1_LiaJhongLaos import cifrar_cesar
from Obj2_LiaJhongLaos import cifrar_atbash
from validaciones import validar_usuario, validar_clave


USUARIOS_CSV = 'usuarios.csv'
PREGUNTAS_CSV = 'preguntas.csv'
RECUPERACION_CSV = 'recuperacion.csv'
MENSAJES_CSV = 'mensajes.csv'
USUARIOS_CAMPOS = ['Id_usuario', 'clave_usuario', 'id_pregunta', 'respuesta_recuperacion', 'intentos_recuperacion']
RECUPERACION_CAMPOS = ['Id_usuario', 'timestamp']
MENSAJES_CAMPOS = ['destinatario', 'remitente', 'cifrado', 'mensaje-cifrado']


manejo_archivos.inicializar_archivos(
    USUARIOS_CSV, RECUPERACION_CSV, USUARIOS_CAMPOS, RECUPERACION_CAMPOS,
    MENSAJES_CSV, MENSAJES_CAMPOS
)


def _validar_clave_cifrador(entry_clave_widget):
    """Valida la clave numérica para el Cifrado César."""
    try:
        clave = int(entry_clave_widget.get())
        return clave
    except ValueError:
        messagebox.showerror("Error de Clave", "La clave para el Cifrado César debe ser un número entero")
        return None


def handle_cifrar_cesar(entry_msg, entry_key, label_result):
    """Manejador para el botón 'Cifrar César'"""
    clave = _validar_clave_cifrador(entry_key)
    if clave is None:
        return
    mensaje = entry_msg.get()
    resultado = cifrar_cesar(mensaje, clave)
    label_result.config(text=resultado)


def handle_descifrar_cesar(entry_msg, entry_key, label_result):
    """Manejador para 'Descifrar César'."""
    clave = _validar_clave_cifrador(entry_key)
    if clave is None:
        return
    mensaje = entry_msg.get()
    resultado = cifrar_cesar(mensaje, -clave) 
    label_result.config(text=resultado)


def handle_cifrar_atbash(entry_msg, label_result):
    """Manejador para 'Cifrar Atbash'"""
    mensaje = entry_msg.get()
    resultado = cifrar_atbash(mensaje)
    label_result.config(text=resultado)


def handle_descifrar_atbash(entry_msg, label_result):
    """Manejador para 'Descifrar Atbash'."""
    mensaje = entry_msg.get()
    resultado = cifrar_atbash(mensaje)
    label_result.config(text=resultado)


def _descifrar_mensaje_handler(mensaje_cifrado, cifrado_tag):
    """
    Descifra un mensaje basado en su etiqueta ('A' o 'C...').
    Esta función vive en main.py porque tiene acceso a los
    cifradores importados.
    """
    if cifrado_tag == 'A':
        return cifrar_atbash(mensaje_cifrado)
    if cifrado_tag.startswith('C'):
        try:
            clave_str = cifrado_tag[1:]
            clave_int = int(clave_str)
            return cifrar_cesar(mensaje_cifrado, -clave_int)
        except (ValueError, TypeError):
            return "[Error al descifrar clave César]"
    return "[Cifrado desconocido]"


def handle_abrir_registro(ventana_bienvenida):
    """Cierra bienvenida y abre registro"""
    ventana_bienvenida.destroy()
    crear_ventana_registro()


def handle_abrir_ingreso(ventana_bienvenida):
    """Cierra bienvenida y abre ingreso"""
    ventana_bienvenida.destroy()
    crear_ventana_ingreso()


def handle_registro(entry_user, entry_pass, combo_pregunta, entry_resp, ventana_registro):
    """Manejador del botón 'Registrar'"""
    usuario = entry_user.get()
    clave = entry_pass.get()
    pregunta_texto = combo_pregunta.get()
    respuesta = entry_resp.get()
    if not (usuario and clave and pregunta_texto and respuesta):
        messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=ventana_registro)
        return
    if not validar_usuario(usuario):
        messagebox.showerror("Error de Validación", "Usuario inválido. Debe tener 5-15 caracteres (letras, números, _, -, .).", parent=ventana_registro)
        return
    if not validar_clave(clave):
        messagebox.showerror("Error de Validación", "Clave inválida. Debe tener 4-8 caracteres (1 mayús, 1 minús, 1 num, 1 especial: _-#*) y sin repetidos adyacentes.", parent=ventana_registro)
        return
    preguntas_dict = manejo_archivos.cargar_preguntas(PREGUNTAS_CSV)
    id_pregunta = None
    encontrado = False
    claves_preguntas = list(preguntas_dict.keys())
    i = 0
    while i < len(claves_preguntas) and not encontrado:
        id_p = claves_preguntas[i]
        if preguntas_dict[id_p] == pregunta_texto:
            id_pregunta = id_p
            encontrado = True
        i += 1
    if not id_pregunta:
        messagebox.showerror("Error", "Error interno con la pregunta de seguridad.", parent=ventana_registro)
        return
    exito, mensaje = manejo_archivos.registrar_usuario_csv(
        usuario, clave, id_pregunta, respuesta,
        USUARIOS_CSV, USUARIOS_CAMPOS
    )
    if exito:
        messagebox.showinfo("Éxito", mensaje, parent=ventana_registro)
        ventana_registro.destroy()
        crear_ventana_bienvenida()
    else:
        messagebox.showerror("Error de Registro", mensaje, parent=ventana_registro)


def handle_ingreso(entry_user, entry_pass, ventana_ingreso):
    """Manejador del botón 'Ingresar'"""
    usuario = entry_user.get()
    clave = entry_pass.get()
    exito, mensaje = manejo_archivos.validar_ingreso_csv(usuario, clave, USUARIOS_CSV, USUARIOS_CAMPOS)
    if exito:
        ventana_ingreso.destroy()
        crear_ventana_principal(usuario)
    else:
        messagebox.showerror("Error de Ingreso", mensaje, parent=ventana_ingreso)


def handle_buscar_pregunta(entry_user, label_pregunta, entry_respuesta, btn_recuperar):
    """Manejador del botón 'Buscar Pregunta' en recuperación"""
    usuario = entry_user.get()
    pregunta, mensaje = manejo_archivos.obtener_pregunta_csv(usuario, USUARIOS_CSV, PREGUNTAS_CSV)
    if pregunta:
        label_pregunta.config(text=pregunta)
        entry_respuesta.config(state='normal')
        btn_recuperar.config(state='normal')
    else:
        messagebox.showerror("Error", mensaje)


def handle_recuperar_clave(entry_user, entry_respuesta, ventana_recuperacion):
    """Manejador del botón 'Recuperar Clave'"""
    usuario = entry_user.get()
    respuesta = entry_respuesta.get()
    exito, mensaje = manejo_archivos.procesar_recuperacion_csv(usuario, respuesta, USUARIOS_CSV,USUARIOS_CAMPOS, RECUPERACION_CSV, RECUPERACION_CAMPOS)
    if exito:
        messagebox.showinfo("Éxito", f"Recuperación exitosa. Su clave es: {mensaje}", parent=ventana_recuperacion)
        ventana_recuperacion.destroy()
    else:
        messagebox.showerror("Error", mensaje, parent=ventana_recuperacion)


def handle_abrir_envio(remitente, tipo_cifrado, entry_mensaje, entry_clave, ventana_padre):
    """
    Valida el mensaje y la clave (si es César) ANTES de
    abrir la ventana pop-up para pedir el destinatario.
    """
    mensaje_original = entry_mensaje.get()
    clave_int = 0
    if not mensaje_original:
        messagebox.showwarning("Mensaje vacío", "Debe ingresar un mensaje para cifrar y enviar.", parent=ventana_padre)
        return
    if tipo_cifrado == 'cesar':
        clave_obj = _validar_clave_cifrador(entry_clave)
        if clave_obj is None:
            messagebox.showwarning("Clave inválida", "Debe ingresar una clave numérica válida para Cifrado César.", parent=ventana_padre)
            return
        clave_int = clave_obj
    crear_ventana_envio(remitente, tipo_cifrado, mensaje_original, clave_int, ventana_padre)


def handle_enviar_mensaje(remitente, destinatario, tipo_cifrado, mensaje_original, clave, ventana_envio):
    """
    Valida al destinatario, cifra el mensaje y lo guarda en el CSV.
    """
    # 1. Validar destinatario
    destinatario_valido = False
    if destinatario == "*":
        destinatario_valido = True
    else:
        destinatario_valido = manejo_archivos.verificar_usuario_existe(destinatario, USUARIOS_CSV)
    if not destinatario_valido:
        messagebox.showerror("Error", "Destinatario Inexistente.", parent=ventana_envio)
        return
    mensaje_cifrado = ""
    cifrado_tag = ""
    if tipo_cifrado == 'atbash':
        mensaje_cifrado = cifrar_atbash(mensaje_original)
        cifrado_tag = "A"
    else:
        mensaje_cifrado = cifrar_cesar(mensaje_original, clave)
        cifrado_tag = f"C{clave}"
    manejo_archivos.guardar_mensaje_csv(remitente, destinatario, cifrado_tag, mensaje_cifrado, MENSAJES_CSV, MENSAJES_CAMPOS)
    messagebox.showinfo("Éxito", "Mensaje Enviado", parent=ventana_envio)
    ventana_envio.destroy()


def handle_consultar_mensajes(id_usuario, ventana_padre):
    """
    Crea la ventana de "Mensajes Recibidos", llama a la lógica de
    manejo_archivos, descifra y formatea los mensajes.
    """
    # 1. Crear la ventana contenedora
    ventana_mensajes = tk.Toplevel(ventana_padre)
    ventana_mensajes.title(f"Mensajes Recibidos - (Usuario: {id_usuario})")
    ventana_mensajes.geometry("500x400")
    
    frame = tk.Frame(ventana_mensajes, padx=10, pady=10)
    frame.pack(fill="both", expand=True)
    
    label_titulo = tk.Label(frame, text="Lista de Mensajes:", font=("Arial", 12, "bold"))
    label_titulo.pack(anchor="w")
    text_frame = tk.Frame(frame, relief="sunken", borderwidth=1)
    text_frame.pack(fill="both", expand=True, pady=5)
    
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")
    
    text_widget = tk.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set, font=("Arial", 10), state="disabled")
    text_widget.pack(fill="both", expand=True, padx=5, pady=5)
    scrollbar.config(command=text_widget.yview)
    label_total = tk.Label(frame, text="Total de Mensajes: 0", font=("Arial", 10, "italic"))
    label_total.pack(anchor="e", pady=5)
    text_widget.config(state="normal")
    
    separador = "-----------------------------------------------------\n"
    total_mensajes = 0
    mensajes_todos, mensajes_propios = manejo_archivos.obtener_mensajes_csv(id_usuario, MENSAJES_CSV)
    i_todos = 0
    while i_todos < len(mensajes_todos):
        msg = mensajes_todos[i_todos]
        mensaje_descifrado = _descifrar_mensaje_handler(msg['mensaje-cifrado'], msg['cifrado'])
        remitente = msg['remitente']
        
        text_widget.insert("end", separador)
        text_widget.insert("end", f"#{remitente}: {mensaje_descifrado}\n")
        total_mensajes += 1
        i_todos += 1
    i_propios = 0
    while i_propios < len(mensajes_propios):
        msg = mensajes_propios[i_propios]
        mensaje_descifrado = _descifrar_mensaje_handler(msg['mensaje-cifrado'], msg['cifrado'])
        remitente = msg['remitente']
        
        text_widget.insert("end", separador)
        text_widget.insert("end", f"{remitente}: {mensaje_descifrado}\n")
        total_mensajes += 1
        i_propios += 1
    if total_mensajes > 0:
        text_widget.insert("end", separador)
    else:
        text_widget.insert("end", "\nNo tienes mensajes nuevos.")
        
    label_total.config(text=f"Total de Mensajes: {total_mensajes}")
    text_widget.config(state="disabled") # Deshabilitar escritura
    ventana_mensajes.grab_set()
    ventana_mensajes.wait_window()


def crear_ventana_principal(remitente: str):
    """
    La ventana principal del cifrador.
    """
    ventana_principal = tk.Tk()
    ventana_principal.title(f"Cifrado y envío de mensajes - (Usuario: {remitente})")
    ventana_principal.resizable(False, False) 
    
    frame_inputs = tk.Frame(ventana_principal, padx=10, pady=10)
    frame_inputs.grid(row=0, column=0)
    tk.Label(frame_inputs, text="Mensaje:").grid(row=0, column=0, sticky="w", pady=5)
    entry_mensaje = tk.Entry(frame_inputs, width=50)
    entry_mensaje.grid(row=0, column=1, columnspan=2)
    tk.Label(frame_inputs, text="Clave (César):").grid(row=1, column=0, sticky="w", pady=5)
    entry_clave = tk.Entry(frame_inputs, width=10)
    entry_clave.grid(row=1, column=1, sticky="w")
    tk.Label(frame_inputs, text="Resultado:").grid(row=4, column=0, sticky="w", pady=10)
    label_resultado_texto = tk.Label(frame_inputs, text="...", relief="sunken", width=50, anchor="w",wraplength=350, justify="left")
    label_resultado_texto.grid(row=5, column=0, columnspan=3, padx=5, sticky="w")
    tk.Button(frame_inputs, text="Cifrar César", command=lambda: handle_cifrar_cesar(entry_mensaje, entry_clave, label_resultado_texto)).grid(row=2, column=0, pady=10, sticky="ew")
    tk.Button(frame_inputs, text="Cifrar Atbash", command=lambda: handle_cifrar_atbash(entry_mensaje, label_resultado_texto)).grid(row=2, column=1, pady=10, sticky="ew")
    tk.Button(frame_inputs, text="Descifrar César", command=lambda: handle_descifrar_cesar(entry_mensaje, entry_clave, label_resultado_texto)).grid(row=3, column=0, pady=10, sticky="ew")
    tk.Button(frame_inputs, text="Descifrar Atbash", command=lambda: handle_descifrar_atbash(entry_mensaje, label_resultado_texto)).grid(row=3, column=1, pady=10, sticky="ew")
    tk.Button(frame_inputs, text="Enviar mensaje cifrado César", command=lambda: handle_abrir_envio(remitente, 'cesar', entry_mensaje, entry_clave, ventana_principal)).grid(row=6, column=0, pady=10, sticky="ew")
    tk.Button(frame_inputs, text="Enviar mensaje cifrado Atbash", command=lambda: handle_abrir_envio(remitente, 'atbash', entry_mensaje, entry_clave, ventana_principal)).grid(row=6, column=1, pady=10, sticky="ew")
    tk.Button(frame_inputs, text="Consultar mensajes recibidos", font=("Arial", 10, "bold"), command=lambda: handle_consultar_mensajes(remitente, ventana_principal)).grid(row=7, column=0, columnspan=2, pady=15, sticky="ew")
    ventana_principal.mainloop()


def crear_ventana_registro():
    """Ventana para crear un nuevo usuario."""
    ventana_registro = tk.Tk()
    ventana_registro.title("Crear Nuevo Usuario")
    ventana_registro.resizable(False, False)
    frame = tk.Frame(ventana_registro, padx=15, pady=15)
    frame.pack(expand=True)
    tk.Label(frame, text="Usuario:").grid(row=0, column=0, sticky="w", pady=5)
    entry_user = tk.Entry(frame, width=40)
    entry_user.grid(row=0, column=1)
    tk.Label(frame, text="Clave:").grid(row=1, column=0, sticky="w", pady=5)
    entry_pass = tk.Entry(frame, width=40, show="*")
    entry_pass.grid(row=1, column=1)
    tk.Label(frame, text="Pregunta:").grid(row=2, column=0, sticky="w", pady=5)
    preguntas_dict = manejo_archivos.cargar_preguntas(PREGUNTAS_CSV)
    pregunta_seleccionada = tk.StringVar()
    if preguntas_dict:
        pregunta_seleccionada.set(list(preguntas_dict.values())[0])
    combo_pregunta = ttk.Combobox(frame, textvariable=pregunta_seleccionada, values=list(preguntas_dict.values()), width=38, state="readonly")
    combo_pregunta.grid(row=2, column=1)
    tk.Label(frame, text="Respuesta:").grid(row=3, column=0, sticky="w", pady=5)
    entry_resp = tk.Entry(frame, width=40)
    entry_resp.grid(row=3, column=1)
    btn_registrar = tk.Button(frame, text="Registrar", command=lambda: handle_registro(entry_user, entry_pass, combo_pregunta, entry_resp, ventana_registro))
    btn_registrar.grid(row=4, column=0, columnspan=2, pady=15, sticky="ew")
    ventana_registro.mainloop()


def crear_ventana_ingreso():
    """Ventana para ingresar o recuperar clave."""
    ventana_ingreso = tk.Tk()
    ventana_ingreso.title("Identificación para acceso")
    ventana_ingreso.resizable(False, False)
    frame = tk.Frame(ventana_ingreso, padx=15, pady=15)
    frame.pack(expand=True)
    tk.Label(frame, text="Usuario:").grid(row=0, column=0, sticky="w", pady=5)
    entry_user = tk.Entry(frame, width=30)
    entry_user.grid(row=0, column=1, columnspan=2)
    tk.Label(frame, text="Clave:").grid(row=1, column=0, sticky="w", pady=5)
    entry_pass = tk.Entry(frame, width=30, show="*")
    entry_pass.grid(row=1, column=1, columnspan=2)
    btn_ingresar = tk.Button(frame, text="Ingresar", command=lambda: handle_ingreso(entry_user, entry_pass, ventana_ingreso))
    btn_ingresar.grid(row=2, column=0, pady=10, sticky="ew")
    btn_recuperar = tk.Button(frame, text="Recuperar Clave", command=crear_ventana_recuperacion)
    btn_recuperar.grid(row=2, column=1, columnspan=2, pady=10, sticky="ew")
    tk.Label(frame, text="Si no se encuentra registrado debe registrarse previamente\no si olvidaste la clave presiona el botón 'Recuperar Clave'.", font=("Arial", 8), justify="left").grid(row=3, column=0, columnspan=3, pady=5)
    ventana_ingreso.mainloop()


def crear_ventana_recuperacion():
    """Ventana para el proceso de recuperación de clave."""
    ventana_recuperacion = tk.Toplevel()
    ventana_recuperacion.title("Recuperación Clave")
    ventana_recuperacion.resizable(False, False)
    frame = tk.Frame(ventana_recuperacion, padx=15, pady=15)
    frame.pack(expand=True)
    tk.Label(frame, text="Usuario:").grid(row=0, column=0, sticky="w", pady=5)
    entry_user = tk.Entry(frame, width=40)
    entry_user.grid(row=0, column=1)
    btn_buscar = tk.Button(frame, text="Buscar Pregunta")
    btn_buscar.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")
    label_pregunta = tk.Label(frame, text="[Su pregunta aparecerá aquí]", font=("Arial", 9, "italic"), wraplength=250)
    label_pregunta.grid(row=2, column=0, columnspan=2, pady=10)
    tk.Label(frame, text="Respuesta:").grid(row=3, column=0, sticky="w", pady=5)
    entry_respuesta = tk.Entry(frame, width=40, state="disabled")
    entry_respuesta.grid(row=3, column=1)
    btn_recuperar = tk.Button(frame, text="Recuperar Clave", state="disabled", command=lambda: handle_recuperar_clave(entry_user, entry_respuesta, ventana_recuperacion))
    btn_recuperar.grid(row=4, column=0, columnspan=2, pady=15, sticky="ew")
    btn_buscar.config(command=lambda: handle_buscar_pregunta(entry_user, label_pregunta, entry_respuesta, btn_recuperar))
    ventana_recuperacion.grab_set()
    ventana_recuperacion.wait_window()


def crear_ventana_envio(remitente, tipo_cifrado, mensaje_original, clave, ventana_padre):
    """
    Crea la ventana pop-up para solicitar el destinatario.
    """
    ventana_envio = tk.Toplevel(ventana_padre)
    ventana_envio.title("Enviar Mensaje")
    ventana_envio.resizable(False, False)
    frame = tk.Frame(ventana_envio, padx=15, pady=15)
    frame.pack(expand=True)
    tk.Label(frame, text="Destinatario:").grid(row=0, column=0, sticky="w", pady=5)
    entry_destinatario = tk.Entry(frame, width=40)
    entry_destinatario.grid(row=0, column=1, padx=5)
    tk.Label(frame, text=" (Ingrese '*' para enviar a todos)", font=("Arial", 8, "italic")).grid(row=1, column=1, sticky="w")
    btn_enviar = tk.Button(frame, text="Confirmar Envío", command=lambda: handle_enviar_mensaje(remitente, entry_destinatario.get(), tipo_cifrado, mensaje_original, clave, ventana_envio))
    btn_enviar.grid(row=2, column=0, columnspan=2, pady=15, sticky="ew")
    ventana_envio.grab_set()
    ventana_envio.wait_window()


def crear_ventana_bienvenida():
    """Ventana inicial de bienvenida."""
    ventana_bienvenida = tk.Tk()
    ventana_bienvenida.title("TP Grupal - Bienvenida")
    ventana_bienvenida.geometry("400x200")
    ventana_bienvenida.resizable(False, False)
    frame = tk.Frame(ventana_bienvenida, padx=20, pady=20)
    frame.pack(expand=True)
    tk.Label(frame, text="Bienvenido a la aplicación de mensajes secretos.", wraplength=350, pady=10).pack()
    frame_botones = tk.Frame(frame)
    frame_botones.pack(pady=20)
    btn_crear = tk.Button(frame_botones, text="Crear Usuario", command=lambda: handle_abrir_registro(ventana_bienvenida))
    btn_crear.pack(side="left", padx=10)
    btn_ingreso = tk.Button(frame_botones, text="Ingreso Usuario", command=lambda: handle_abrir_ingreso(ventana_bienvenida))
    btn_ingreso.pack(side="right", padx=10)
    ventana_bienvenida.mainloop()


if __name__ == "__main__":
    crear_ventana_bienvenida()