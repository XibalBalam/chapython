class Entorno:
    def __init__(self):
        self.variables = {}

    def asignar(self, nombre, valor):
        self.variables[nombre] = valor

    def obtener(self, nombre):
        return self.variables.get(nombre, None)


def ejecutar_lineas(lineas, entorno):
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()

        if linea.startswith("digamos"):
            partes = linea.split()
            nombre = partes[1]
            valor = eval_valor(' '.join(partes[3:])[:-1], entorno)
            entorno.asignar(nombre, valor)

        elif linea.startswith("ponele"):
            partes = linea.split()
            nombre = partes[1]
            valor = eval_valor(' '.join(partes[3:])[:-1], entorno)
            entorno.asignar(nombre, valor)

        elif linea.startswith("deci"):
            contenido = linea[4:].strip()
            if contenido.endswith("!"):
                contenido = contenido[:-1]
            imprimir_valor(contenido, entorno)

        i += 1


def eval_valor(expr, entorno):
    expr = expr.strip()
    if expr.startswith("\"") and expr.endswith("\""):
        return expr.strip('"')
    elif expr.isdigit():
        return int(expr)
    elif expr in entorno.variables:
        return entorno.obtener(expr)
    elif "(" in expr and ")" in expr:
        if "+" in expr:
            partes = expr[1:-1].split("+")
            return eval_valor(partes[0].strip(), entorno) + eval_valor(partes[1].strip(), entorno)
        elif "-" in expr:
            partes = expr[1:-1].split("-")
            return eval_valor(partes[0].strip(), entorno) - eval_valor(partes[1].strip(), entorno)
    return expr


def imprimir_valor(valor, entorno):
    if "+" in valor:
        partes = valor.split("+")
        resultado = ""
        for parte in partes:
            parte = parte.strip()
            if parte.startswith("\"") and parte.endswith("\""):
                resultado += parte.strip('"')
            elif parte in entorno.variables:
                resultado += str(entorno.obtener(parte))
            elif parte.isdigit():
                resultado += parte
            else:
                val = eval_valor(parte, entorno)
                resultado += str(val)
        print(resultado)
    elif valor in entorno.variables:
        print(str(entorno.obtener(valor)))
    else:
        print(str(valor.strip('"')))


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Falta archivo")
        exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        codigo = f.read()

    lineas = [linea.strip() for linea in codigo.splitlines() if linea.strip() and not linea.strip().startswith("#")]
    entorno = Entorno()
    ejecutar_lineas(lineas, entorno)
