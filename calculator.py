from sys import stdin

class Operator:
    def __init__(self, precedence, associativity, lambdaeq):
        self.precedence = precedence
        self.associativity = associativity
        self.lambdaeq = lambdaeq

class Calculator:
    """Calculator uses defined operators to evaluate infix mathematical expressions"""

    def __init__(self, operators, variables):
        self.operators = operators
        self.variables = variables
    
    def __precedenceAssociativeCheck(self, opstack, tok):
        """Checks whether we need to pop from the operator stack into the output"""
        if len(opstack) <= 0: return False
        elif opstack[-1] not in self.operators: return False
        elif self.operators[opstack[-1]].precedence < self.operators[tok].precedence: return False
        elif self.operators[tok].associativity != 'left': return False
        return True

    def __infixToRPN(self, tokens):
        """Converts infix notation expressions into reverse polish (postfix) notation for easier calculation using the shunting yard algorithm"""
        output = []
        opstack = []

        for tok in tokens:
            if tok == '(':
                opstack.append(tok)
            elif tok == ')':
                while opstack[-1] != '(':
                    output.append(opstack.pop())
                opstack.pop()
            elif tok in self.operators:
                while self.__precedenceAssociativeCheck(opstack, tok):
                    output.append(opstack.pop())
                opstack.append(tok)
            else:
                output.append(tok)
        while opstack:
            output.append(opstack.pop())

        return output

    def calcRPN(self, tokens):
        """Evaluates reverse polish (postfix) notation"""
        stack = []
        for tok in tokens:
            if tok in self.operators:
                op2, op1 = stack.pop(), stack.pop()
                stack.append(self.operators[tok].lambdaeq(op1, op2))
            elif tok in self.variables:
                stack.append(float(self.variables[tok]))
            else:
                stack.append(float(tok))
        return stack.pop()
        
    def calc(self, tokens):
        return self.calcRPN(self.__infixToRPN(tokens))


    
class DefaultCalculator(Calculator):
    """Derived class of Calculator with the default operators +, -, /, *, ^"""
    def __init__(self):
        self.operators = {
            '+': Operator(1, 'left', lambda a,b: a+b),
            '-': Operator(1, 'left', lambda a,b: a-b),
            '*': Operator(2, 'left', lambda a,b: a*b),
            '/': Operator(2, 'left', lambda a,b: a/b),
            '^': Operator(3, 'right', lambda a,b: a**b),
        }

        self.variables = {
            "pi": 3.141592653589793238462643383279502884197169399375105820974,
            "e":  2.718281828459045235360287471352662497757247093699959574966
        }

if __name__ == '__main__':
    print(DefaultCalculator().calc(stdin.readline().strip('\n').split(' ')))
