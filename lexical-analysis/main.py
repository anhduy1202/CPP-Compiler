from collections import defaultdict
## CONSTANTS
KEYWORDS = ['cout', 'cin', 'endl', 'if', 'else', 'while', 'for', 'int', 'float', 'bool', 'true', 'false', 'void', 'return', 'cout', 'cin', 'char', 'string', 'do', 'switch', 'case', 'break', 'continue', 'default', 'include', 'using', 'namespace', 'std']
SEPARATORS = ['(', ')', '{', '}', '[', ']', ',']
COMMENTS = ['//', '/*', '*/']
PUNCTUATIONS = ['.', ':', ';', ',', '?', '!', '-', '\'']
OPERATORS = ['+', '-', '*']
DIGITS = [str(i) for i in range(10)]
## TOKENS
T_KEYWORD = 'keyword'
T_SEP = 'separator'
T_ID = 'identifier'
T_OPERATOR = 'operator'
T_INT = 'integer'
T_REAL = 'real'
T_PUNC = 'punctuation'
T_STRING = 'string'

class Token:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.value}'

class Lexer:
    def __init__(self):
        self.tokens = defaultdict(list)
        self.keywords = KEYWORDS
        self.separators = SEPARATORS
        self.punctuations = PUNCTUATIONS
        self.operators = OPERATORS
        self.comments = COMMENTS
        self.digits = DIGITS
        self._start = 0
        self._current = 0
        self._linepos = 1
        self.line = ""
    
    # scan if its the end of the line
    def is_at_end(self):
        return self._current >= len(self.line)
    
    # advance next character and return it
    def advance(self):
        self._current += 1
        return self.line[self._current - 1]
    
    # peek next character
    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.line[self._current]
    
    # peek next next character
    def peek_next(self):
        if self._current + 1 >= len(self.line):
            return '\0'
        return self.line[self._current + 1]
    
    # match if next character is expected
    def match(self, expected):
        if self.is_at_end():
            return False
        if self.line[self._current] != expected:
            return False
        self._current += 1
        return True
    
    # scan the string between " " and return it
    def scan_string(self):
        while self.peek() != '"' and not self.is_at_end():
            self.advance()
        if self.is_at_end():
            raise Exception(f'Unterminated string at line {self._linepos}')
        self.advance()
        return self.line[self._start:self._current]

    def scan_real(self):
        while self.peek() in self.digits:
            self.advance()
        if self.peek() == '.':
            self.advance()
        while self.peek() in self.digits:
            self.advance()
        return self.line[self._start:self._current]
    
    def scan_int(self):
        while self.peek() in self.digits:
            self.advance()
        return self.line[self._start:self._current]
    
    # Peek next character and check if whole word is a keyword
    def scan_id(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        id = self.line[self._start:self._current]
        # check if its a keyword
        if id in self.keywords:
            self.tokens[T_KEYWORD].append(id)
        else:
            self.tokens[T_ID].append(id)

    def add_token(self, type, value):
        self.tokens[type].append(Token(value))
    
    def scan_token(self):
        char = self.advance()
        if char in self.separators:
            self.add_token(T_SEP, char)
        # Handle operator with 1 character
        elif char in self.operators:
            self.add_token(T_OPERATOR, char)
        # Handle operator with 2 characters
        elif char == "!":
            if self.match("="):
                self.add_token(T_OPERATOR, "!=")
        elif char == "=":
            if self.match("="):
                self.add_token(T_OPERATOR, "==")
            else:
                self.add_token(T_OPERATOR, "=")
        elif char == "<":
            if self.match("="):
                self.add_token(T_OPERATOR, "<=")
            elif self.match("<"):
                self.add_token(T_OPERATOR, "<<")
            else:
                self.add_token(T_OPERATOR, "<")
        elif char == ">":
            if self.match("="):
                self.add_token(T_OPERATOR, ">=")
            elif self.match(">"):
                self.add_token(T_OPERATOR, ">>")
            else:
                self.add_token(T_OPERATOR, ">")
        elif char == "&":
            if self.match("&"):
                self.add_token(T_OPERATOR, "&&")
        elif char == "|":
            if self.match("|"):
                self.add_token(T_OPERATOR, "||")
        # Handle multiline and single line comments, division operator
        elif char == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            elif self.match('*'):
                while self.peek() != '*' and self.peek() != '/' and not self.is_at_end():
                    self.advance()
                if self.peek() == '*':
                    self.advance()
                    if self.peek() == '/':
                        self.advance()
            else:
                self.tokens[T_OPERATOR].append(char)
        # Handle punctuations
        elif char in self.punctuations:
            self.tokens[T_PUNC].append(char)
        # Handle numbers
        elif char in self.digits:
            while self.peek() in self.digits:
                self.advance()
            if self.peek() == '.' and self.peek_next() in self.digits:
                self.advance()
                while self.peek() in self.digits:
                    self.advance()
                real_number = self.line[self._start:self._current]
                self.add_token(T_REAL, real_number)
            else:
                int_number = self.line[self._start:self._current]
                self.add_token(T_INT, int_number)
        # Handle identifiers
        elif char.isalpha():
            self.scan_id()
        # Handle string literals
        elif char == '"':
            self.add_token(T_STRING, self.scan_string())
        # Handle new line, space, tab, carriage return
        elif char == '\n':
            self._linepos += 1
        elif char == ' ' or char == '\t' or char == '\r':
            pass
        else:
            # Handle invalid characters
            raise Exception(f'Invalid character {char} at position {self._linepos}')

    def tokenize(self, source_code):
        with open(source_code, 'r') as f:
            self.line = f.read()
            while not self.is_at_end():
                # reset start position
                self._start = self._current
                self.scan_token()
                self._linepos += 1

def lexer():
    lexer = Lexer()
    lexer.tokenize('input_sourcecode.txt')
    # Print tokens and lexemes in 2 columns
    print('TOKEN'.ljust(20) + 'LEXEME')
    print('---------------------------')
    for token_type, token_list in lexer.tokens.items():
        token_string = ', '.join([str(token) for token in token_list])
        print(token_type.ljust(20) + token_string)

if __name__ == '__main__':
    lexer()