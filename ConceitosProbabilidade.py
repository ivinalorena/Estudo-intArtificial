"""Probabilidade é uma forma de quantificar a incerteza associada com eventos escolhidos a partir de um
universo deles.
P(E) para signica "a probabilidade de um evento E ocorrer.
1.Teora da probabilidade para contruir modelos 
2.Probabilidade para avaliar modelos


* Dependência e Independência:
A grosso modo:dois eventos E e F são dependentes se soubermos algo sobre se E ocorre nos der informações sobre se F ocorre
(e vice versa). Do contrário são independentes.
Por exemplo: se jogarmos uma moeda honesta duas vezes, o resultado do primeiro lançamento não nos diz nada sobre o resultado do segundo lançamento.
Se E e F são independentes, então P(E e F) = P(E) * P(F).
Se E e F são dependentes, então P(E e F) = P(E) *
----------------------------------------------------------------
Se não são necessariamente independetes (e a probabilidade de F não for 0), logo definimos a probabilidade de E "condicional" a F como:
P(E | F) = P(E e F) / P(F)

Quando E e F são independetes, então P(E | F) = P(E).


* Teorema de Bayes:O teorema de Bayes é uma forma de calcular a probabilidade condicional de um evento
Explica a questão do diagnóstico de um paciente possuir ou não a doença

* Variáeis Aleatórias: é uma variável cujos valores possíveis possuem uma distribuição de probabilidade associada.

* Distribuição contínua: 
Função de densidade para a distribuição uniforme
"""
import math
from random import random
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

def uniform_pdf(x):
    return 1 if x>=0 and x<1 else 0
"""Função de distribuição cumulativa, que fornece a probabilidade de uma variável aleatória ser menor ou igual a um determinado valor"""
def uniform_cdf(x):
    """retorna a probabilidade de uma bariável aleatória uniforme ser <=x"""
    if x<0: return 0
    elif x<1: return x
    else: return 1

"""Distrbuição normal. É determinado por dois parâmetros: a média (mu) e o desvio padrão (sigma). A média indica onde o sino é centralizado
e o desvio padrão indica a largura do sino."""
def normal_pdf(x, mu=0, sigma=1):
    """Retorna a densidade de probabilidade de x para uma distribuição normal com média mu e desvio padrão sigma"""
    sqrt_two_pi = math.sqrt(2 * math.pi)
    return (math.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sqrt_two_pi * sigma))

"""Função de distribuição cumulativa para a distribuição normal não pode ser escrita em termos de funções elementares, mas pode ser escrita
usando math.erf"""
def normal_cdf(x, mu=0, sigma=1):
    return (1 + math.erf((x-mu)/math.sqrt(2) / sigma)) / 2

"""Computar o inverso, no exemplo do livro traz uma busca binária. A função divide em dois intervalos repetidamente até diminuir para um Z próximo
o suficiente da probabilidade desejada"""

""" O teorema do limite central: uma variável aleatória definida como a média de uma grande quantidade de variáveis aleatórias distribuídas
independente e identicamente é ela mesma aproximadamente distribuída normalmente.

variáveis aleatórias
binomiais, as quais possuem dois parâmetros n e p. Uma variável aleatória
Binomial(n,p) é apenas a soma de n variáveis aleatórias independentes
Bernoulli(p), e cada uma delas é igual a 1 com probabilidade p e 0 com
probabilidade 1− p:"""
def bernoulli_trial(p):
    return 1 if random.random() < p else 0
def binomial(n, p):
    return sum(bernoulli_trial(p) for _ in range(n))

def make_hist(p, n, num_points):
    data = [binomial(n, p) for _ in range(num_points)]
    # usa um gráfico de barras para exibir as amostrar binomiais atuais
    histogram = Counter(data)
    plt.bar([x - 0.4 for x in histogram.keys()],
    [v / num_points for v in histogram.values()],
    0.8,
    color='0.75')
    mu = p * n
    sigma = math.sqrt(n * p * (1 - p))
    # usa um gráfico de linhas para exibir uma aproximação da normal
    xs = range(min(data), max(data) + 1)
    ys = [normal_cdf(i + 0.5, mu, sigma) - normal_cdf(i - 0.5, mu, sigma)
    for i in xs]
    plt.plot(xs,ys)
    plt.title("Distribuição Binomial vs. Aproximação Normal" )
    plt.show()

"""Para Mais Esclarecimentos
scipy.stats (http://bit.ly/1L2H0Lj) contém as funções de distribuição
cumulativa e de densidade de probabilidade para a maioria das
distribuições de probabilidade populares.
Lembre-se como, no final do Capítulo 5, eu disse que seria uma boa ideia
estudar com um livro didático de estatística? Também seria uma boa ideia
estudar com um livro didático de probabilidade. O melhor que eu conheço
e está disponível online é o Introduction to Probability
(http://bit.ly/1L2MTYI).


-----------------------CAP 7---------------------------

Hipótese e Inferência
- Teste Estatístico de Hipótese
Exemplo:	Lançar	Uma	Moeda
 Imagine	que	temos	uma	moeda	e	queremos	testar	para	confirmar	se	ela	é
 honesta.	Temos	a	premissa	de	que	a	moeda	possui	a	probabilidade	p	de	cair	cara,
 então	nossa	hipótese	nula	é	que	a	moeda	seja	honesta	—	ou	seja,	que	p	=	0,5.
 Testaremos	novamente	contra	a	hipótese	alternativa	p	≠	0,5.

"""
def normal_approximation_to_binomial(n, p):
    """encontra mi e sigma correspondendo ao Binomial(n, p)"""
    mu = p*n
    sigma = math.sqrt(p*(1-p)*n)
    return mu, sigma

 #	o	cdf	normal	é	a	probabilidade	que	a	variável	esteja	abaixo	de	um	limite
normal_probability_below = normal_cdf
#	está	acima	do	limite	se	não	estiver	abaixo
def normal_probability_above(lo, mu=0, sigma=1):
    return 1 - normal_cdf(lo, mu, sigma)
#	está	entre	se	for	menos	do	que	hi,	mas	não	menor	do	que	lo
def normal_probability_between(lo, hi, mu=0, sigma=1):
    return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)
#	está	fora	se	não	estiver	entre
def normal_probability_outside(lo, hi, mu=0, sigma=1):
    return 1 - normal_probability_between(lo, hi, mu, sigma)

def	normal_upper_bound(probability,	mu=0,	sigma=1):
    """retorna	z	para	que	p(Z	<=	z)	=	probability"""
    return	inverse_normal_cdf(probability,	mu,	sigma)

def	normal_lower_bound(probability,	mu=0,	sigma=1):
    """retorna	z	para	que	p(Z	>=	z)	=	probability"""
    return	inverse_normal_cdf(1	-	probability,	mu,	sigma)
 
def	inverse_normal_cdf(probability,	mu=0,	sigma=1,	tolerance=0.00001):
    """retorna	z	para	que	p(Z	<=	z)	=	probability"""
    #	usa	busca	binária
    low_z = -10.0
    hi_z = 10.0
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2
        if normal_cdf(mid_z, mu, sigma) < probability:
            low_z = mid_z
        else:
            hi_z = mid_z
    return mid_z + mu

def	normal_two_sided_bounds(probability,	mu=0,	sigma=1):
    """retorna	os	limites	simétricos	(sobre	a	média)
    que	contêm	a	probabilidade	específica"""
    tail_probability	=	(1	-	probability)	/	2
    #	limite	superior	deveria	ter	tail_probability	acima
    upper_bound	=	normal_lower_bound(tail_probability,	mu,	sigma)
    #	limite	inferior	deveria	ter	tail_probability	abaixo
    lower_bound	=	normal_upper_bound(tail_probability,	mu,	sigma)
    return	lower_bound,	upper_bound

""" P - VALUES: Uma	outra	maneira	de	pensar	sobre	o	teste	anterior	envolve	p-values.	Em	vez	de
 escolher	limites	com	base	em	alguma	probabilidade	de	corte,	nós	computamos	a
 probabilidade	—	presumindo	que	H0	seja	verdadeiro	—	que	podemos	ver	um
 valor	ao	menos	tão	extremo	quanto	ao	que	realmente	observamos.
 Para	o	nosso	teste	bilateral	para	a	moeda	honesta,	computamos:
"""
def	two_sided_p_value(x,	mu=0,	sigma=1):
    if	x	>=	mu:
        #	se	x	for	maior	do	que	a	média,	a	coroa	será	o	que	for	maior	do	que	x
        return	2	*	normal_probability_above(x,	mu,	sigma)
    else:
        #	se	x	for	menor	do	que	a	média,	a	coroa	será	o	que	for	menor	do	que	x
        return	2	*	normal_probability_below(x,	mu,	sigma)

"""Intervalo de confiança: Temos	testado	hipóteses	sobre	o	valor	da	probabilidade	p,	do	resultado	cara	que
 é	um	parâmetro	da	desconhecida	distribuição	“cara”.	Quando	o	caso	é	esse,	uma
 terceira	abordagem	é	construir	um	intervalo	de	confiança	em	torno	do	valor
 observado	do	parâmetro.
 Por	exemplo,	podemos	estimar	a	probabilidade	de	uma	moeda	viciada	ao
 analisar	o	valor	médio	das	variáveis	Bernoulli	correspondentes	a	cada
 lançamento	—	1	se	cara,	0	se	coroa.	Se	nós	observarmos	525	caras	de	1000
 lançamentos,	logo	estimamos	p	em	0,525"""
