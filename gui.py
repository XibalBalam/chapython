import tkinter as tk
from tkinter import ttk
from lexer import Lexer
from parser import Parser

# Validación de código
def validar_codigo():
    codigo = entrada.get("1.0", tk.END).strip()
    if not codigo:
        resultado.set("❌ No se ingresó ningún código.")
        etiqueta_resultado.config(fg="red")
        return
    try:
        tokens = Lexer(codigo).tokenize()
        Parser(tokens).parse()
        resultado.set("✅ Código válido")
        etiqueta_resultado.config(fg="green")
    except Exception as e:
        resultado.set(f"❌ Error: {str(e)}")
        etiqueta_resultado.config(fg="red")

# Ventana principal
ventana = tk.Tk()
ventana.title("NarrativaLang – Validador de Código")
ventana.geometry("700x450")
ventana.configure(bg="#f0f0f0")

# Título
titulo = tk.Label(ventana, text="PROYECTO", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333")
titulo.pack(pady=(10, 0))

subtitulo = tk.Label(ventana, text="Validador de Lenguaje Experimental", font=("Arial", 12), bg="#f0f0f0", fg="#555")
subtitulo.pack(pady=(0, 10))

# Frame para el editor de texto
frame_editor = tk.Frame(ventana, bg="#ffffff", bd=2, relief="groove")
frame_editor.pack(padx=20, pady=10, fill="both", expand=True)

entrada = tk.Text(frame_editor, height=10, font=("Consolas", 12), bg="#ffffff", fg="#000000", wrap="word")
entrada.pack(padx=10, pady=10, fill="both", expand=True)

# Botón de validación
boton_validar = tk.Button(ventana, text="Validar Código", command=validar_codigo, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=20, pady=5)
boton_validar.pack(pady=10)

# Resultado
resultado = tk.StringVar()
etiqueta_resultado = tk.Label(ventana, textvariable=resultado, font=("Arial", 12), bg="#f0f0f0")
etiqueta_resultado.pack(pady=(0, 10))

ventana.mainloop()
