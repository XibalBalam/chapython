import tkinter as tk
from lexer import Lexer
from parser import Parser
import re

class Tooltip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None

    def show(self, message, x, y):
        self.hide()
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=message, background="lightyellow", borderwidth=1, relief="solid", font=("Arial", 10))
        label.pack()

    def hide(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

# Validación de código
def validar_codigo():
    entrada.tag_remove("errorline", "1.0", tk.END)
    tooltip.hide()
    codigo = entrada.get("1.0", tk.END)
    if not codigo.strip():
        resultado.set("❌ Esta en blanco Vos!")
        etiqueta_resultado.config(fg="red")
        return
    try:
        tokens = Lexer(codigo).tokenize()
        parser = Parser(tokens)
        parser.code = codigo
        parser.parse()
        resultado.set("✅ Código válido")
        etiqueta_resultado.config(fg="green")
    except SyntaxError as e:
        resultado.set(f"❌ Error: {str(e)}")
        etiqueta_resultado.config(fg="red")
        tooltip.hide()
        entrada.tag_remove("errorline", "1.0", tk.END)

        match = re.search(r"En: \('(.+?)', '(.+?)'\)", str(e))
        if match:
            tipo, palabra = match.groups()
            contenido = entrada.get("1.0", tk.END)
            for m in re.finditer(re.escape(palabra), contenido):
                start = m.start()
                end = m.end()
                linea = contenido.count("\n", 0, start) + 1
                col = start - contenido.rfind("\n", 0, start)
                inicio = f"{linea}.{col - 1 if col > 0 else 0}"
                fin = f"{linea}.{col + len(palabra)}"
                entrada.tag_add("errorline", inicio, fin)
                bbox = entrada.bbox(inicio)
                if bbox:
                    x, y, _, _ = bbox
                    x += entrada.winfo_rootx()
                    y += entrada.winfo_rooty() + 20
                    tooltip.show(str(e), x, y)
                break

# Resaltado de sintaxis
def resaltar_sintaxis(event=None):
    entrada.tag_remove("keyword", "1.0", tk.END)
    entrada.tag_remove("string", "1.0", tk.END)
    entrada.tag_remove("number", "1.0", tk.END)
    entrada.tag_remove("operator", "1.0", tk.END)
    entrada.tag_remove("variable", "1.0", tk.END)
    entrada.tag_remove("endkeyword", "1.0", tk.END)
    entrada.tag_remove("bool", "1.0", tk.END)
    entrada.tag_remove("null", "1.0", tk.END)
    entrada.tag_remove("errorline", "1.0", tk.END)
    tooltip.hide()

    code = entrada.get("1.0", tk.END)

    simple_keywords = [
        "digamos", "es", "ponele", "en", "deci", "haz", "con", "fin",
        "devolveme", "pedile", "listame", "suma", "resta", "multiplica", "parti"
    ]

    compound_token_parts = {
        "dale vueltas": ["dale", "vueltas"],
        "mientras que": ["mientras", "que"],
        "soque hasta que": ["soque", "hasta", "que"],
        "en caso de que": ["en", "caso", "de", "que"],
        "de lo contrario": ["de", "lo", "contrario"]
    }

    booleanos = ["verdadero", "falso"]
    nulos = ["null"]

    all_keywords = set(simple_keywords + list(compound_token_parts.keys()) + ["ya estuvo"])

    string_zones = []
    for match in re.finditer(r'"[^"\n]*"', code):
        start = match.start()
        end = match.end()
        string_zones.append((start, end))
        entrada.tag_add("string", f"1.0+{start}c", f"1.0+{end}c")

    def esta_en_string(pos):
        return any(start <= pos < end for start, end in string_zones)

    for match in re.finditer(r'\bya estuvo\b', code):
        if esta_en_string(match.start()):
            continue
        entrada.tag_add("endkeyword", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

    for phrase, parts in compound_token_parts.items():
        pattern = r'\b' + r'\s+'.join(parts) + r'\b'
        for match in re.finditer(pattern, code):
            if esta_en_string(match.start()):
                continue
            start_index = match.start()
            for part in parts:
                part_match = re.search(r'\b' + re.escape(part) + r'\b', code[start_index:])
                if part_match:
                    real_start = start_index + part_match.start()
                    real_end = start_index + part_match.end()
                    entrada.tag_add("keyword", f"1.0+{real_start}c", f"1.0+{real_end}c")
                    start_index = real_end

    for word in simple_keywords:
        for match in re.finditer(r'\b' + re.escape(word) + r'\b', code):
            if esta_en_string(match.start()):
                continue
            entrada.tag_add("keyword", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

    for b in booleanos:
        for match in re.finditer(r'\b' + re.escape(b) + r'\b', code):
            if esta_en_string(match.start()):
                continue
            entrada.tag_add("bool", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

    for n in nulos:
        for match in re.finditer(r'\b' + re.escape(n) + r'\b', code):
            if esta_en_string(match.start()):
                continue
            entrada.tag_add("null", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

    for match in re.finditer(r'\b\d+\b', code):
        if esta_en_string(match.start()):
            continue
        entrada.tag_add("number", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

    for match in re.finditer(r'[+\-*/=<>!]+', code):
        if esta_en_string(match.start()):
            continue
        entrada.tag_add("operator", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

    for match in re.finditer(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code):
        word = match.group()
        if word in all_keywords or esta_en_string(match.start()):
            continue
        entrada.tag_add("variable", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

# GUI
ventana = tk.Tk()
ventana.title("NarrativaLang – Validador de Código")
ventana.geometry("700x450")
ventana.configure(bg="#f0f0f0")

titulo = tk.Label(ventana, text="ChaPython", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333")
titulo.pack(pady=(10, 0))

subtitulo = tk.Label(ventana, text="Validador de Lenguaje Experimental", font=("Arial", 12), bg="#f0f0f0", fg="#555")
subtitulo.pack(pady=(0, 10))

frame_editor = tk.Frame(ventana, bg="#ffffff", bd=2, relief="groove")
frame_editor.pack(padx=20, pady=10, fill="both", expand=True)

entrada = tk.Text(frame_editor, height=10, font=("Consolas", 12), bg="#ffffff", fg="#000000", wrap="word", undo=True)
entrada.pack(padx=10, pady=10, fill="both", expand=True)

entrada.tag_configure("keyword", foreground="#0077cc", font=("Consolas", 12, "bold"))
entrada.tag_configure("string", foreground="#cc0000")
entrada.tag_configure("number", foreground="#009900")
entrada.tag_configure("operator", foreground="#aa00aa")
entrada.tag_configure("variable", foreground="#E69129")
entrada.tag_configure("endkeyword", foreground="#990099", font=("Consolas", 12, "bold"))
entrada.tag_configure("bool", foreground="#0099CC", font=("Consolas", 12, "italic"))
entrada.tag_configure("null", foreground="#999999", font=("Consolas", 12, "italic"))
entrada.tag_configure("errorline", underline=True, underlinefg="red")

entrada.bind("<KeyRelease>", resaltar_sintaxis)
entrada.bind("<Key>", lambda e: tooltip.hide())
entrada.bind("<Button-1>", lambda e: tooltip.hide())

boton_validar = tk.Button(ventana, text="Compilar", command=validar_codigo, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=20, pady=5)
boton_validar.pack(pady=10)

import subprocess
import os

def ejecutar_codigo():
    validar_codigo()
    if "✅" in resultado.get():
        with open("temp.chapy", "w", encoding="utf-8") as f:
            f.write(entrada.get("1.0", tk.END))
        ruta_ejecutor = "ejecutor.py"
        subprocess.Popen(["start", "cmd", "/k", f"python {ruta_ejecutor} temp.chapy"], shell=True)

boton_ejecutar = tk.Button(ventana, text="Ejecutar", command=ejecutar_codigo, bg="#2196F3", fg="white", font=("Arial", 12, "bold"), padx=20, pady=5)
boton_ejecutar.pack(pady=(0, 10))

resultado = tk.StringVar()
etiqueta_resultado = tk.Label(ventana, textvariable=resultado, font=("Arial", 12), bg="#f0f0f0")
etiqueta_resultado.pack(pady=(0, 10))

tooltip = Tooltip(entrada)
ventana.mainloop()