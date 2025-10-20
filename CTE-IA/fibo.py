# Módulo de números de Fibonacci

def fib_print(n):
    """Escreve a série de Fibonacci até n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

def fib_build(n):
    """Retorna a série de Fibonacci até n."""
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a+b
    return result