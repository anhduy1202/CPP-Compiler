from dataclasses import dataclass
from enum import Enum

class TokenType(Enum):
	INTEGER   = 0
	PLUS      = 1
	MINUS     = 2
	MULTIPLY  = 3
	DIVIDE    = 4
	LPAREN    = 5
	RPAREN    = 6

@dataclass
class IntNode:
	value: any

	def __repr__(self):
		return f"{self.value}"

@dataclass
class AddNode:
	left: any
	right: any

	def __repr__(self):
		return f"({self.left}+{self.right})"

@dataclass
class SubtractNode:
	left: any
	right: any

	def __repr__(self):
		return f"({self.left}-{self.right})"

@dataclass
class MultiplyNode:
	left: any
	right: any

	def __repr__(self):
		return f"({self.left}*{self.right})"

@dataclass
class DivideNode:
	left: any
	right: any

	def __repr__(self):
		return f"({self.left}/{self.right})"

@dataclass
class PositiveNode:
	node: any

	def __repr__(self):
		return f"(+{self.node})"
	
@dataclass
class NegativeNode:
	node: any

	def __repr__(self):
		return f"(-{self.node})"

@dataclass
class Integer:
    value: int

    def __repr__(self):
        return f"{self.value}" 

@dataclass
class Token:
	type: TokenType
	value: any = None

	def __repr__(self):
		return self.type.name + (f":{self.value}" if self.value != None else "")

class Lexer:
    def __init__(self, text):
        self.text = iter(text)
        self.advance()

    def error(self):
        raise Exception('Entered expression is invalid!')

    def advance(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def skip_whitespace(self):
        # Skip whitespace characters in the input
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def generate_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            elif self.current_char.isdigit():
                yield self.generate_integer()
            elif self.current_char == '+':
                self.advance()
                yield Token(TokenType.PLUS)
            elif self.current_char == '-':
                self.advance()
                yield Token(TokenType.MINUS)
            elif self.current_char == '*':
                self.advance()
                yield Token(TokenType.MULTIPLY)
            elif self.current_char == '/':
                self.advance()
                yield Token(TokenType.DIVIDE)
            elif self.current_char == '(':
                self.advance()
                yield Token(TokenType.LPAREN)
            elif self.current_char == ')':
                self.advance()
                yield Token(TokenType.RPAREN)
            else:
                self.error()
    
    def generate_integer(self):
        number = self.current_char
        self.advance()
        while self.current_char is not None and self.current_char.isdigit():
            number += self.current_char
            self.advance()
        return Token(TokenType.INTEGER, int(number))

class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.advance()
    
    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None
    
    def error(self):
        raise Exception('Entered expression is invalid!')
    
    def parse(self):
        if self.current_token == None:
            return None
        result = self.expression()
        if self.current_token != None:
            self.error()
        return result

    def expression(self):
        result = self.term()
        try:
            while self.current_token != None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
                if self.current_token.type == TokenType.PLUS:
                    self.advance()
                    result = AddNode(result, self.term())
                elif self.current_token.type == TokenType.MINUS:
                    self.advance()
                    result = SubtractNode(result, self.term())
            return result
        except:
            self.error()
    
    def term(self):
        result = self.factor()
        while self.current_token != None and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            if self.current_token.type == TokenType.MULTIPLY:
                self.advance()
                result = MultiplyNode(result, self.factor())
            elif self.current_token.type == TokenType.DIVIDE:
                self.advance()
                result = DivideNode(result, self.factor())
        return result
    
    def factor(self):
        token = self.current_token
        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.expression()
            if self.current_token.type != TokenType.RPAREN:
                self.error()
            self.advance()
            return result
        elif token.type == TokenType.INTEGER:
            self.advance()
            return IntNode(token.value)
        elif token.type == TokenType.PLUS:
            self.advance()
            return PositiveNode(self.factor())
        elif token.type == TokenType.MINUS:
            self.advance()
            return NegativeNode(self.factor())
        else:
            self.error()

class Interpreter:
    def __init__(self, tree):
        self.tree = tree
    
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)
    
    def visit_AddNode(self, node):
        return Integer(self.visit(node.left).value + self.visit(node.right).value)
    
    def visit_SubtractNode(self, node):
        return Integer(self.visit(node.left).value - self.visit(node.right).value)
    
    def visit_MultiplyNode(self, node):
        return Integer(self.visit(node.left).value * self.visit(node.right).value)
    
    def visit_DivideNode(self, node):
        try:
            return Integer(self.visit(node.left).value // self.visit(node.right).value)
        except ZeroDivisionError:
            raise Exception('Division by zero is not allowed!')
    
    def visit_IntNode(self, node):
        return Integer(node.value)
    
    def visit_PositiveNode(self, node):
        return Integer(+self.visit(node.node).value)

    def visit_NegativeNode(self, node):
        return Integer(-self.visit(node.node).value)
    
    def interpret(self):
        return self.visit(self.tree)

# Main
def main():
    while True:
        try:
            text = input('Enter the expression \n')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        token = lexer.generate_token()
        parser = Parser(token)
        tree = parser.parse()
        interpreter = Interpreter(tree)
        result = interpreter.interpret()
        print('Result = ', result.value, '\n')

if __name__ == "__main__":
    main()
