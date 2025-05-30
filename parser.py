class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        while self.position < len(self.tokens):
            self.statement()
        print("✅ Programa valido.")

    def statement(self):
        if self.match("DIGAMOS"):
            self.expect("ID")
            self.expect("ES")
            self.expression()
            self.expect("EXCLAMATION")  # "!"" como separador

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
            self.block()  # ← ahora sí existe este método
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
            self.error("Instruccion invalida")

    def condition(self):
        # Se asume: ID OPERADOR VALOR
        self.expect("ID")
        self.expect("OPERADOR")
        self.expression()

    def expression(self):
        # Acepta cadenas, números, variables y concatenaciones
        if self.match("STRING") or self.match("ID") or self.match("NUMBER"):
            while self.match("OPERADOR_ARIT"):
                if not self.match("STRING") and not self.match("ID") and not self.match("NUMBER"):
                    self.error("Expresion incompleta despues de operador")
            return
        elif self.match("SUMA") or self.match("RESTA") or self.match("MULTIPLICA") or self.match("PARTI"):
            self.expect("PAREN_IZQ")
            
            if not self.match("ID") and not self.match("NUMBER"):
                self.error("Se esperaba ID o NUMBER")

            self.expect("OPERADOR_ARIT")

            if not self.match("ID") and not self.match("NUMBER"):
                self.error("Se esperaba ID o NUMBER")
            
            self.expect("PAREN_DER")



    def list_values(self):
        self.expect("STRING")
        while self.match("COMA"):
            self.expect("STRING")

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
            self.error(f"Se esperaba {kind}")

    def error(self, msg):
        token = self.tokens[self.position] if self.position < len(self.tokens) else ("EOF", "")
        raise SyntaxError(f"{msg} → Token: {token}")
