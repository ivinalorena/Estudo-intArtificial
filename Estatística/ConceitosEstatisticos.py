""" algumas informações e códigos que colocarei aqui para estudo, extrai do livro Data Science do Zero"""
import math
import numpy as np

def sum_of_squares(v):
    """Retorna a soma dos quadrados dos valores em v"""
    return sum(x * x for x in v)

def mean(x):
    """Calcula a média de x"""
    return sum(x) / len(x)

def median(v):
    """Encontra o valor mais ao meio de v """
    n = len(v)
    sorted_v = sorted(v)
    midpoint = n//2

    if n % 2 == 1:
        #se for impar, retorna o valor do meio 
        return sorted_v[midpoint]
    else:
        # se for par, retorna a média dos dois valores do meio
        low = midpoint - 1
        high = midpoint
        return (sorted_v[low] + sorted_v[high]) / 2
    #median([1, 2, 3, 4, 5]) # 3

"""Uma generalização da média é o quantil, que representa o valor abaixo do qual uma certa porcentagem dos dados se
encontra ( a mediana representa o valor abaixo do qual 50% dos dados se encontram)"""
def quantile(x, p):
    """Retorna o valor percentual p-ésimo em x"""
    p_index= int(p * len(x))
    return sorted(x)[p_index]
#quantile([1, 2, 3, 4, 5], 0.5) # 3

def mode(x):
    """Retorna o valor mais frequente em x"""
    counts = {}
    for item in x:
        if item not in counts:
            counts[item] = 0
        counts[item] += 1

    max_count = max(counts.values())
    modes = [k for k, v in counts.items() if v == max_count]
    
    return modes[0] if len(modes) == 1 else modes

"""Dispersão se refere à medida de como os nossos dados estão espalhados. Tipicamente:valores
perto de zero significam não estão espalhados, enquanto valores maiores significam que estão mais espalhados."""
#amplitude já possui significado em python
def data_range(x):
    """Retorna a diferença entre o maior e o menor valor em x"""
    return max(x) - min(x)

"""Uma medida de dispersão mais complexa é a variância"""
def de_mean(x):
    """Desloca x ao subtrair a sua média"""
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]
def variance(x):
    """Retorna a variância de x, presume que x tem ao menos dois elementos"""
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n - 1)

"""Desvio padrão é a raiz quadrada da variância, e é uma medida de dispersão mais fácil de interpretar"""
def standard_deviation(x):
    """Retorna o desvio padrão de x"""
    return math.sqrt(variance(x)) #import math

"""alternativa mais robusta computa a diferença entre os percentos (quantos) 75% e 25% do valor"""
def interquartile_range(x):
    """Retorna a diferença entre o quartil 75 e o quartil 25 de x"""
    return quantile(x, 0.75) - quantile(x, 0.25)

"""Covariância mede como duas variáveis variam em conjunto de suas médias"""
def covariance(x,y):
    n = len(x)
    return np.dot(de_mean(x), de_mean(y)) / (n - 1) #import numpy as np
"""quando os elementos correspondentes de x e y estão acima ou abaixo de suas médias, um número positivos entra na soma.
Quando um está acima de sua média e o outro abaixo, um número negativo entra na soma. Na mesma proporção, uma covariância positiva
"grande" significa que x tende a ser grande quando y é grande e pequeno quando y é pequeno, enquanto uma covariância negativa "grande" significa que x tende a ser grande quando y é pequeno e vice-versa.
Uma covariância perto de zero significa que tal relação não existe.
"""
def correlation(x,y):
    stdev_x=standard_deviation(x)
    stdev_y=standard_deviation(y)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(x, y) / stdev_x / stdev_y
    else:
        return 0.0
    
"""* Paradoxo de Simpson"""
"""Correlação e causalidade,  - se x e y possuem forte correlação, isso talvez indique que x causa y ou vice versa, que algum terceiro fator
causa ambos, ou que a correlação é apenas uma coincidência.

-- Para mais esclarecimentos: SciPy, pandas, Statsmodels"""