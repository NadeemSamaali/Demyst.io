import re

class Tokenizer :
    # Splitting the expression as a list
    def __init__(self, expression : str) :
        self.tokens = re.findall(r'\d+|[+*/()-^]', expression)
        self.current_index = 0
    # Returnts token at current_index and increments the current index by a factor of 1
    def next_token(self) :
        if self.current_index < len(self.tokens) :
            token = self.tokens[self.current_index]
            self.current_index += 1
            return token
        else:
            return None
    # Outputs token at current_index
    def peek_token(self) :
        return self.tokens[self.current_index]

class Node :
    # Initializing node class
    def __init__(self,value, left=None, right=None) :
        self.value = value
        self.left = left
        self.right = right

class Tree : 
    # Initializing tree by using tokenizer as attribute
    def __init__(self, tokenizer) :
        self.tokenizer = tokenizer
        self.char_memory = []
          
    def parse(self) :
        return self.expr()
    
    # Handling addition and substraction
    def expr(self) :
        node = self.term()
        while self.tokenizer.current_index < len(self.tokenizer.tokens) and self.tokenizer.peek_token() in ['+','-'] :
            node = Node(self.tokenizer.next_token(), node, self.term())
        return node
    
    # Handling multiplication and division
    def term(self) :
        node = self.expon()
        while self.tokenizer.current_index < len(self.tokenizer.tokens) and self.tokenizer.peek_token() in ['*','/'] :
            node = Node(self.tokenizer.next_token(), node, self.expon())
        return node
    
    def expon(self) :
        node = self.factor()
        while self.tokenizer.current_index < len(self.tokenizer.tokens) and self.tokenizer.peek_token() in ['^'] :
            node = Node(self.tokenizer.next_token(), node, self.factor())
        return node
    
    # Handling parantheses and lone numbers (setting up nodes)
    def factor(self):
        token = self.tokenizer.next_token()
        if token.isdigit():
            return Node(token)
        elif token == '(':
            node = self.expr()
            self.tokenizer.next_token() 
            return node
        else:
            raise ValueError(f"Unexpected token: {token}")

# Function evaluating the results of the arithmetic expression from the tree
def evaluate(node) :
    
    if node.value.isdigit():
        return float(node.value)
    elif node.value == '+' :
        return evaluate(node.left) + evaluate(node.right)
    elif node.value == '-' :
        return evaluate(node.left) - evaluate(node.right)
    elif node.value == '*' :
        return evaluate(node.left) * evaluate(node.right)
    elif node.value == '/' :
        return evaluate(node.left) / evaluate(node.right)
    elif node.value == '^' :
        return evaluate(node.left) ** evaluate(node.right)
    else :
        raise ValueError(f'The following token is invalid {node.value}')

# Function taking equation as string input and evalutating its result
def parse_and_evaluate(expression : str) :        
    equation = Tokenizer(expression)
    tree = Tree(equation)
    parse_tree = tree.parse()
    return evaluate(parse_tree)
