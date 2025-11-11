import tkinter as tk
from tkinter import messagebox
from Obj1_LiaJhongLaos import cifrar_cesar
from Obj2_LiaJhongLaos import cifrar_atbash


def _validar_clave(entry_clave_widget):
    """
    Función para obtener y validar la clave César.
    Recibe el widget entry de la clave como parámetro.
    """
    try:
        clave = int(entry_clave_widget.get())
        return clave
    except ValueError:
        messagebox.showerror(
            title="Error de Clave",
            message="La clave para el Cifrado César debe ser un número entero."
        )
        return None


def handle_cifrar_cesar(entry_msg, entry_key, label_result):
    """Manejador para el botón 'Cifrar César'"""
    clave = _validar_clave(entry_key)
    if clave is None:
        return
    mensaje = entry_msg.get()
    resultado = cifrar_cesar(mensaje, clave)
    label_result.config(text=resultado)


def handle_descifrar_cesar(entry_msg, entry_key, label_result):
    """Manejador para 'Descifrar César'."""
    clave = _validar_clave(entry_key)
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


def al_presionar_continuar(ventana_a_destruir):
    """Destruye la ventana actual y abre la principal."""
    ventana_a_destruir.destroy()
    crear_ventana_principal()



def crear_ventana_principal():
    """
    Objetivo: Crea la ventana principal de la aplicación.
    Autor: Lia Jhong Laos
    """
    ventana_principal = tk.Tk()
    ventana_principal.title(f"TP Grupal Parte 1 - Grupo: Lia Jhong Laos")
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
    tk.Button(frame_inputs, text="Descifrar César", command=lambda: handle_descifrar_cesar(entry_mensaje, entry_clave, label_resultado_texto)).grid(row=3, column=0, sticky="ew")
    
    tk.Button(frame_inputs, text="Descifrar Atbash", command=lambda: handle_descifrar_atbash(entry_mensaje, label_resultado_texto)).grid(row=3, column=1, sticky="ew")

    ventana_principal.mainloop()


def crear_ventana_bienvenida():
    """
    Objetivo: Crea la ventana de bienvenida inicial.
    Autor: LiaJhongLaos
    """
    ventana_bienvenida = tk.Tk()
    ventana_bienvenida.title(f"TP Grupal Parte 1 - Grupo: Lia Jhong Laos")
    ventana_bienvenida.geometry("400x300") 
    ventana_bienvenida.resizable(False, False)
    frame = tk.Frame(ventana_bienvenida, padx=20, pady=20)
    frame.pack(expand=True)

    tk.Label(frame, text=f"Bienvenido a la aplicación de mensajes secretos del grupo Lia Jhong Laos.",wraplength=350, pady=10).pack()

    tk.Label(frame, text="Para continuar presione continuar, de lo contrario cierre la ventana.", wraplength=350, pady=10).pack()

    tk.Button(frame, text="Continuar", command=lambda: al_presionar_continuar(ventana_bienvenida)).pack(pady=20)
    ventana_bienvenida.mainloop()


if __name__ == "__main__":
    crear_ventana_bienvenida()
