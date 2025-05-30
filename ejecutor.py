import sys
from interpreter import ejecutar_lineas, Entorno

if len(sys.argv) < 2:
    print("Falta el archivo .chapy")
    sys.exit(1)

archivo = sys.argv[1]
with open(archivo, encoding="utf-8") as f:
    codigo = f.read()

try:
    print("✅ ¡Todo chilero! Código válido.")
    lineas = [linea.strip() for linea in codigo.splitlines() if linea.strip()]
    entorno = Entorno()
    ejecutar_lineas(lineas, entorno)
    print("✅ Código ejecutado correctamente")
except Exception as e:
    print("❌ Error al ejecutar:")
    print(e)
