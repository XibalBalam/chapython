class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.code = ""

    def parse(self):
        while self.position < len(self.tokens):
            self.statement()
        print("✅ ¡Todo chilero! Código válido.")

    def statement(self):
        if self.match("DIGAMOS"):
            self.expect("ID")
            self.expect("ES")
            self.expression()
            self.expect("EXCLAMATION")

        elif self.match("PONELE"):
            self.expect("ID")
            self.expect("EN")
            self.expression()
            self.expect("EXCLAMATION")

        elif self.match("DECI"):
            self.expression()
            self.expect("EXCLAMATION")

        elif self.match("YA_ESTUVO"):
            self.expect("EXCLAMATION")

        elif self.match("DALE_VUELTAS"):
            self.expect("MIENTRAS_QUE")
            self.condition()
            self.expect("HAZ")
            self.block()
            self.expect("SOQUE_HASTA_QUE")
            self.condition()
            self.expect("EXCLAMATION")

        elif self.match("EN_CASO_DE_QUE"):
            self.condition()
            self.expect("HAZ")
            self.block()
            if self.match("DE_LO_CONTRARIO"):
                self.expect("HAZ")
                self.block()

        elif self.match("ECHATE"):
            self.expect("ID")
            self.expect("CON")
            self.expect("ID")
            self.expect("LLAVES_IZQ")
            while not self.match("FIN"):
                self.statement()
            self.expect("EXCLAMATION")
        # Aceptar cierre con } si está
            if self.match("LLAVES_DER"):
                pass

        elif self.match("DEVOLVEME"):
            self.expression()
            self.expect("EXCLAMATION")

        elif self.match("PEDILE"):
            self.expect("ID")
            self.expect("EXCLAMATION")

        elif self.match("LISTAME"):
            self.expect("ID")
            self.expect("CON")
            self.list_values()
            self.expect("EXCLAMATION")

        else:
            self.error("😵 Esa instrucción no la conozco, revisá bien lo que escribiste.")

    def condition(self):
        self.expect("ID")
        self.expect("OPERADOR")
        self.expression()

    def expression(self):
        if self.match("STRING") or self.match("ID") or self.match("NUMBER"):
            while self.match("OPERADOR_ARIT"):
                if not self.match("STRING") and not self.match("ID") and not self.match("NUMBER"):
                    self.error("😬 Después del operador hace falta un número o variable")
            return
        elif self.match("SUMA") or self.match("RESTA") or self.match("MULTIPLICA") or self.match("PARTI"):
            self.expect("PAREN_IZQ")
            if not self.match("ID") and not self.match("NUMBER"):
                self.error("👀 Se esperaba un número o variable después del paréntesis de apertura")
            self.expect("OPERADOR_ARIT")
            if not self.match("ID") and not self.match("NUMBER"):
                self.error("👀 Después del operador falta un número o variable")
            self.expect("PAREN_DER")
        else:
            self.error("🤔 No entendí esa expresión, revisá bien.")

    def list_values(self):
        if not self.match("STRING") and not self.match("NUMBER"):
            self.error("📦 Se esperaba un valor para la lista")
        while self.match("COMA"):
            if not self.match("STRING") and not self.match("NUMBER"):
                self.error("📦 Se esperaba otro valor después de la coma")

    def block(self):
        self.expect("LLAVES_IZQ")
        while not self.match("LLAVES_DER"):
            self.statement()

    def match(self, kind):
        if self.position < len(self.tokens) and self.tokens[self.position][0] == kind:
            self.position += 1
            return True
        return False

    def expect(self, kind):
        if not self.match(kind):
            token = self.tokens[self.position] if self.position < len(self.tokens) else ("EOF", "")
            linea = self.code_line(token)
            descripcion = self.token_descripcion(kind)
            self.error(f"👀 Te faltó {descripcion} en la línea {linea}, pero encontré '{token[1]}'")

    def code_line(self, token):
        try:
            before = self.code.find(token[1])
            if before == -1:
                return '?'
            return self.code[:before].count('\n') + 1
        except:
            return '?'

    def token_descripcion(self, kind):
        descripciones = {
            "EXCLAMATION": "el signo de cierre (!) al final de la instrucción",
            "PAREN_IZQ": "un paréntesis de apertura (",
            "PAREN_DER": "un paréntesis de cierre )",
            "LLAVES_IZQ": "una llave de apertura {",
            "LLAVES_DER": "una llave de cierre }",
            "ID": "un nombre válido (variable, función, etc.)",
            "STRING": "una cadena entre comillas",
            "NUMBER": "un número",
            "OPERADOR": "un operador como <, > o ==",
            "OPERADOR_ARIT": "un operador aritmético como + o -",
            "FIN": "la palabra clave 'fin'"
        }
        return descripciones.get(kind, f"'{kind}'")

    def error(self, msg):
        token = self.tokens[self.position] if self.position < len(self.tokens) else ("EOF", "")
        raise SyntaxError(f"❌ {msg} → En: {token}")
