def soma(int a, int b):

    return a + b

def subtracao(double a, double b):
    return a - b

def multiplicacao(double a, double b):
    return a * b

def divisao(double a, double b):
    if b != 0:
        return a / b
    else:
        raise ZeroDivisionError("Erro: divisão por zero!")