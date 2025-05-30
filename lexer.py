import re

class Lexer:
    def __init__(self, code):
        self.code = code

    def tokenize(self):
        token_specification = [
            # Palabras clave (primero, para que no se confundan con ID)
            ('DIGAMOS',       r'\bdigamos\b'),
            ('ES',            r'\bes\b'),
            ('PONELE',        r'\bponele\b'),
            ('EN',            r'\ben\b'),
            ('DECI',          r'\bdeci\b'),
            ('YA_ESTUVO',     r'\bya\s*estuvo\b'),
            ('DALE_VUELTAS',  r'\bdale\s*vueltas\b'),
            ('MIENTRAS_QUE',  r'\bmientras\s*que\b'),
            ('SOQUE_HASTA_QUE', r'\bsoque\s*hasta\s*que\b'),
            ('EN_CASO_DE_QUE', r'\ben\s*caso\s*de\s*que\b'),
            ('HAZ',           r'\bhaz\b'),
            ('DE_LO_CONTRARIO', r'\bde\s*lo\s*contrario\b'),
            ('ECHATE',        r'\bechate\b'),
            ('CON',           r'\bcon\b'),
            ('FIN',           r'\bfin\b'),
            ('DEVOLVEME',     r'\bdevolveme\b'),
            ('PEDILE',        r'\bpedile\b'),
            ('LISTAME',       r'\blistame\b'),

            # Operaciones personalizadas
            ('SUMA',          r'\bsuma\b'),
            ('RESTA',         r'\bresta\b'),
            ('MULTIPLICA',    r'\bmultiplica\b'),
            ('PARTI',         r'\bparti\b'),

            # Operadores y símbolos
            ('EXCLAMATION',   r'!'),
            ('PAREN_IZQ',     r'\('),
            ('PAREN_DER',     r'\)'),
            ('OPERADOR_ARIT', r'[\+\-\*/]'),
            ('OPERADOR',      r'[><=]+'),
            ('COMA',          r','),
            ('LLAVES_IZQ',    r'\{'),
            ('LLAVES_DER',    r'\}'),

            # Identificadores y literales
            ('STRING',        r'\"[^\"]*\"'),
            ('NUMBER',        r'\d+'),
            ('ID',            r'[a-zA-Z_][a-zA-Z0-9_]*'),

            # Espacios y errores
            ('SKIP',          r'[ \t\n]+'),
            ('MISMATCH',      r'.')
        ]

        regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
        tokens = []
        for mo in re.finditer(regex, self.code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Illegal character: {value}')
            tokens.append((kind, value))
        return tokens
