"""O gradiente é o vetor de derivadas parciais de uma função multivariada.
Ele aponta na direção de maior crescimento da função.
Para minimizar uma função, andar aos poucos na direção oposta ao gradiente."""

def difference_quotient(f,x,h):
    """Retorna a taxa de variação média de f entre x e x + h."""
    return (f(x + h) - f(x)) / h

def	derivative(x):
    return	2	*	x
derivative_estimate	=	partial(difference_quotient,	square,	h=0.00001)
 #	planeja	mostrar	que	são	basicamente	o	mesmo
import	matplotlib.pyplot	as	plt
x	=	range(-10,10)
plt.title("Actual	Derivatives	vs.	Estimates")
plt.plot(x,	map(derivative,	x),	'rx',	label='Actual')												
#	vermelho	x
plt.plot(x,	map(derivative_estimate,	x),	'b+',	label='Estimate')	#	azul	+
plt.legend(loc=9)
plt.show()

def	partial_difference_quotient(f,	v,	i,	h):
    """computa	o	i-ésimo	quociente	diferencial	parcial	de	f	em	v"""
    w	=	[v_j	+	(h	if	j	==	i	else	0)	#	adiciona	h	ao	elemento	i-ésimo	de	v
        for	j,	v_j	in	enumerate(v)]
    return	(f(w)	-	f(v))	/	h

"""Estimar o gradiente do mesmo jeito"""
def	estimate_gradient(f,	v,	h=0.00001):
    return	[partial_difference_quotient(f,	v,	i,	h)
        for	i,	_	in	enumerate(v)]

"""A	maior	desvantagem	da	abordagem	“estimar	usando	os	quocientes
 diferenciais”	é	sair	caro	em	termos	de	computação.	Se	v	tem	o	tamanho	n,
 estimate_gradient	tem	que	avaliar	f	em	2n	entradas	diferentes.	Se	você	está
 estimando	gradientes	um	após	o	outro,	está	fazendo	muito	mais	trabalho	extra"""

"""Pegaremos um ponto inicial aleatório e andaremos a pequenos passos na direção oposta do gradiente, até chegarmos em
um ponto onde o gradiente seja muito pequeno:"""

def	step(v,	direction,	step_size):
    """move	step_size	na	direção	a	partir	de	v"""
    return	[v_i	+	step_size	*	direction_i
        for	v_i,	direction_i	in	zip(v,	direction)]
def	sum_of_squares_gradient(v):
    return	[2	*	v_i	for	v_i	in	v]
#	escolhe	um	ponto	inicial	aleatório
v	=	[random.randint(-10,10)	for	i	in	range(3)]
tolerance	=	0.0000001
while	True:
    gradient	=	sum_of_squares_gradient(v)		#	computa	o	gradiente	em	v
    next_v	=	step(v,	gradient,	-0.01)	#	pega	um	passo	gradiente	negativo								
    
    if	distance(next_v,	v)	<	tolerance:	#	para	se	estivermos	convergindo						
        break
    v	=	next_v	 #	continua	se	não	estivermos																												

"""ele	sempre	termina	com	um	v	muito	próximo	a
[0,0,0].	Quanto	menor	for	a	tolerance,	mais	próximo	ele	será
 

* ESCOLHENDO O TAMANHO DO PRÓXIMO PASSO:
1. Usar	um	passo	de	tamanho	fixo
2. Diminuir	gradualmente	o	tamanho	do	passo	a	cada	vez
3. A	cada	passo,	escolher	o	tamanho	do	passo	que	minimize	o	valor	da função	objetiva

A terceira opção parece ser a mais perfeita, mas na prática é uma computação muito custosa.

criar uma função “aplicação segura” que retorna infinito (que nunca deveria ser o mínimo de nada) para
entradas inválidas:
"""
def	safe(f):
    """retorna	uma	nova	função	que	é	igual	a	f,
    exceto	que	ele	exibe	infinito	como	saída	toda	vez	que	f	produz	um	erro"""
    def	safe_f(*args,	**kwargs):
        try:
            return	f(*args,	**kwargs)
        except:
            return	float('inf') #isso significa "infinito" em Python						
    return	safe_f

"""temos	alguma	target_fn	que	queremos	minimizar,	e	também	temos	o	seu
 gradient_fn.	Por	exemplo,	target_fn	poderia	representar	erros	em	um	modelo	como
 uma	função	dos	seus	parâmetros,	e	talvez	queiramos	encontrar	os	parâmetros
 que	produzem	os	menores	erros	possíveis.
 Além	do	mais,	digamos	que	escolhemos	(de	alguma	forma)	um	valor	inicial	para
 os	parâmetros	theta_0.	Logo,	podemos	implementar	o	gradiente	descendente
 como:"""

def	minimize_batch(target_fn,	gradient_fn,	theta_0,	tolerance=0.000001):
    """usa	o	gradiente	descendente	para	encontrar	theta	que	minimize	a	função	alvo"""
    step_sizes	=	[100,	10,	1,	0.1,	0.01,	0.001,	0.0001,	0.00001]
    theta	=	theta_0	#	ajusta	theta	para	o	valor	inicial
    target_fn	=	safe(target_fn)	#	versão	segura	de	target_fn
    value	=	target_fn(theta)	#	valor	que	estamos	minimizando
    while	True:
        gradient	=	gradient_fn(theta)
        next_thetas	=	[step(theta,	gradient,	-step_size)
                        for	step_size	in	step_sizes]
        #	escolhe	aquele	que	minimiza	a	função	de	erro
        next_theta	=	min(next_thetas,	key=target_fn)
        next_value	=	target_fn(next_theta)
                                    #	para	se	estivermos	“convergindo”
        if	abs(value	-	next_value)	<	tolerance:
            return	theta
        else:
            theta,	value	=	next_theta,	next_value
""" Chamamos	de	minimize_batch	porque,	para	cada	passo	do	gradiente,	ele	considera	o
 conjunto	inteiro	de	dados.

Às	vezes	vamos	querer	maximizar	uma	função	e	podemos	fazê-la	ao	minimizar seu	negativo	(que	possui	um	gradiente	negativo	correspondente)
"""
def	negate(f):
    """retorna	uma	função	que,	para	qualquer	entrada,	x	retorna	-f(x)"""
    return	lambda	*args,	**kwargs:	-f(*args,	**kwargs)

def	negate_all(f):
    """o	mesmo	quando	f	retorna	uma	lista	de	números"""
    return	lambda	*args,	**kwargs:	[-y	for	y	in	f(*args,	**kwargs)]

def	maximize_batch(target_fn,	gradient_fn,	theta_0,	tolerance=0.000001):
    return	minimize_batch(negate(target_fn),
    negate_all(gradient_fn),
    theta_0,
    tolerance)

"""Gradiente Descendente Estocástico: Ao usar o grupo de abordagens anteriores, cada passo
 gradiente requer que nós façamos uma previsão e computemos o gradiente para
 o conjunto de dados inteiro, fazendo com que cada passo leve mais tempo. Normalmente, essas funções de erro são aditivas, o que significa que o erro
 previsto no 	conjunto de dados inteiro é simplesmente a soma dos erros preditivos
 para cada ponto. Quando o caso é esse, podemos aplicar uma técnica chamada gradiente
 descendente estocástico, que computa o gradiente (e anda um passo) apenas um
 ponto de cada vez. Ele circula sobre nossos dados repetidamente até alcançar um
 ponto de parada

 Durante cada ciclo, vamos querer iterar sobre nossos dados em ordem aleatória:"""

def	in_random_order(data):
    """gerador	retorna	os	elementos	do	dado	em	ordem	aleatória"""
    indexes	=	[i	for	i,	_	in	enumerate(data)]#	cria	uma	lista	de	índices
    random.shuffle(indexes)		#	os	embaralha
    for	i	in	indexes:	#	retorna	os	dados	naquela	ordem
        yield	data[i]

""" Andaremos um passo gradiente para cada ponto de dados. Esse método deixa a
 possibilidade de circularmos próximos a um mínimo para sempre, então quando
 pararmos de obter melhorias, diminuiremos o tamanho do passo e,
 eventualmente, pararemos:"""

def	minimize_stochastic(target_fn,	gradient_fn,	x,	y,	theta_0,	alpha_0=0.01):
    data	=	zip(x,	y)
    theta	=	theta_0	#	palpite	inicial																											
    alpha	=	alpha_0	#	tamanho	do	passo	inicial																											
    min_theta,	min_value	=	None,	float("inf")		#	o	mínimo	até	agora
    iterations_with_no_improvement	=	0
    #	se	formos	até	100	iterações	sem	melhorias,	paramos
    while	iterations_with_no_improvement	<	100:
        value	=	sum(	target_fn(x_i,	y_i,	theta)	for	x_i,	y_i	in	data	)
    if	value	<	min_value:
        #	se	achou	um	novo	mínimo,	lembre-se
        #	e	volte	para	o	tamanho	do	passo	original
        min_theta,	min_value	=	theta,	value
        iterations_with_no_improvement	=	0
        alpha	=	alpha_0
    else:
        #	do	contrário,	não	estamos	melhorando,	portanto	tente
        #	diminuir	o	tamanho	do	passo
        iterations_with_no_improvement	+=	1
        alpha	*=	0.9
 #	e	ande	um	passo	gradiente	para	todos	os	pontos	de	dados
    for	x_i,	y_i	in	in_random_order(data):
        gradient_i	=	gradient_fn(x_i,	y_i,	theta)
        theta	=	vector_subtract(theta,	scalar_multiply(alpha,	gradient_i))
    return	min_theta

""" A	versão	estocástica	será	tipicamente	mais	rápida	do	que	a	versão	batch.
 Naturalmente,	vamos	querer	uma	versão	que	maximize	da	mesma	forma:"""
def	maximize_stochastic(target_fn,	gradient_fn,	x,	y,	theta_0,	alpha_0=0.01):
    return	minimize_stochastic(negate(target_fn),
    negate_all(gradient_fn),
    x,
    y,
    theta_0,
    alpha_0)
"""
 scikit-learn	possui	um	módulo	de	Gradiente	Descendente	Estocástico
 (http://scikit-learn.org/stable/modules/sgd.html).	Não	é	tão	geral	quanto	o
 nosso	em	alguns	pontos	e	mais	geral	em	outros.	Apesar	de	que,	na	maioria
 das	situações	do	mundo	real,	você	usará	bibliotecas	nas	quais	a	otimização
 já	estará	pronta,	então	você	não	terá	que	se	preocupar	com	elas	(exato
 quando	não	funcionar	corretamente,	o	que,	um	dia,	inevitavelmente,
 acontecerá)
"""
