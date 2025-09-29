"""Igualmente,	este	script	conta	as	palavras	em	sua	entrada	e	exibe	as	mais	comuns:"""
 #	most_common_words.py
import	sys
import re
from collections import	Counter
#	passa o	número	de	palavras como primeiro argumento
try:
    num_words= int(sys.argv[1])
except:
    print("usage:most_common_words.py num_words")
sys.exit(1)
word = 'teste'  #para armazenar a palavra atual

#código	de	saída	não-zero	indica	erro
counter	=	Counter(word.lower())#	palavras	em	minúsculas
for	line in	sys.stdin:
    for	word in	line.strip().split(): #	se	separam	por	espaços
        if word:  # se linha estiver vazia, não conta
            counter[word.lower()] += 1

for word, count in counter.most_common(num_words):
        sys.stdout.write(str(count))
        sys.stdout.write("\t")
        sys.stdout.write(word)
        sys.stdout.write("\n")

""" depois	disso,	você	poderia	fazer	algo	como:
 C:\DataScience>type	the_bible.txt	|	python	most_common_words.py	10
 64193			the
 51380			and
 34753			of
 13643			to
 12799			that
 12560			in
 10263			he
 9840				shall
 8987				unto
 8836				for
 
 
* Lendo arquivos, o básico de arquivos texto
r = somente leitura
w = escrita (sobrescreve o arquivo existente)
a = anexar (adiciona ao final do arquivo existente)
b = modo binário (para arquivos binários, como imagens)
#	não	se	esqueça	de	fechar	os	arquivos	ao	terminar
file_for_writing.close()
para não se preocupar com o fechamento do arquivo poderá ser codificado da segunte maneira:
with open('file.txt', 'w') as file_for_writing:
    file_for_writing.write('Hello, World!')


Se	você	precisar	ler	um	arquivo	de	texto	inteiro,	você	pode	apenas	iterar	sobre	as linhas	do	arquivo	usando	for:"""

starts_with_hash	=	0
with	open('input.txt','r')	as	f:
	for	line	in	f:
		if	re.match("^#",line):
			#	observe	cada	linha	do	arquivo
			#	use	um	regex	para	ver	se	começa	com	'#'
			starts_with_hash	+=	1		#	se	começar,	adicione	1	à	contagem

"""pegar apenas o dominio de um email:"""
def	get_domain(email_address):
    """separa	no	'@'	e	retorna	na	última	parte"""
    return	email_address.lower().split("@")[-1]
with	open('email_addresses.txt',	'r')	as	f:
    domain_counts	=	Counter(get_domain(line.strip())
                                    for	line	in	f
                                    if	"@"	in	line)

"""Arqvuivos delimitados
Tais	arquivos	são	separados	por	vírgula	(comma-separated)	ou
 por	tabulação	(tab-separated).	Cada	linha	possui	diversos	campos,	com	uma
 vírgula	(ou	uma	tabulação)	indicando	onde	um	campo	termina	e	o	outro	começa.
 Começa	a	ficar	complicado	quando	você	tem	campos	com	vírgulas,	tabulações	e
 newlines	neles	(inevitavelmente	você	terá).	Por	esse	motivo,	é	quase	sempre	um
 erro	tentar	analisar	sozinho.	Em	vez	disso,	você	deveria	usar	o	modulo	csv	do
 Python	(ou	as	bibliotecas	pandas).


Exempolo: um arquivo delimitado por tabulaão de preçõs de ações:
6/20/2014			AAPL						90.91
 6/20/2014			MSFT						41.68
 6/20/2014			FB			64.5
 6/19/2014			AAPL						91.86
 6/19/2014			MSFT						41.51
 6/19/2014			FB			64.34
Poderíamos processar como:	
"""
import	csv
with	open('tab_delimited_stock_prices.txt',	'rb')	as	f:
    reader	=	csv.reader(f,	delimiter='\t')
    for	row	in	reader:
        date	=	row[0]
        symbol	=	row[1]
        closing_price	=	float(row[2])
        process(date,	symbol,	closing_price)
# se tiver cabeçalho,  você	pode	pular	a	linha	(com	uma	chamada	inicial	para	reader.next())	ou	obter	cada
#linha	como	um	dict	(com	os	cabeçalhos	como	chaves)	usando	csv.DictReader
with	open('colon_delimited_stock_prices.txt',	'rb')	as	f:
    reader	=	csv.DictReader(f,	delimiter=':')
    for	row	in	reader:
        date	=	row["date"]
        symbol	=	row["symbol"]
        closing_price	=	float(row["closing_price"])
        process(date,	symbol,	closing_price)


"""EXTRAINDO DADOS DA INTERNET
1. Para extrair dados do HTML é necessário a biblioteca BeautifulSoup:ela	constrói	uma	árvore
 a	partir	de	vários	elementos	de	uma	página	e	fornece	uma	simples	interface	para
 acessá-los.
2. Biblioteca de pedidos (pip install requests) que	é	uma	maneira	mais
 simpática	de	fazer	pedidos	(http://docs.python-requests.org/en/latest/)	ao	HTTP
 do	que	para	qualquer	coisa	construída	dentro	de	Python
O interpretador de HTML em python não é tão flexível, será necessário instalar (pip install html5lib)
"""
from	bs4	import	BeautifulSoup
import	requests
html	=	requests.get("http://www.example.com").text
soup	=	BeautifulSoup(html,	'html5lib')

"""Por exemplo, para encontrar a primeira tag <p> no HTML, você pode fazer:"""
first_paragraph	=	soup.find('p')#ou	somente	soup.p
first_paragraph_text=soup.p.text.split()


"""USANDO APIS
 Muitos	websites	e	serviços	web	fornecem	interfaces	de	programação	de
 aplicativos	(APIs),	permitindo	que	você	solicite	os	dados	em	formato
 estruturado.

JSON	(e	XML)
 Como	o	HTTP	é	um	protocolo	para	a	transferência	de	texto,	os	dados	que	você
 solicita	por	meio	de	uma	API	da	web	deve	ser	serializada	em	formato	de	string.
 Geralmente,	essa	serialização	usa	o	JavaScript	Object	Notation	(JSON).	Os
 objetos	JavaScript	se	parecem	bastante	com	os	dicts	do	Python,	o	que	facilita	a
 interpretação	de	suas	strings:
 {	"title":"Data Science Book",
			"author":"Joel Grus",
			"publicationYear":2014,
			"topics":["data","science","data science"]}"""
import	json
serialized	=	"""{	
"title"	:	"Data	Science	Book",
"author"	:	"Joel	Grus",
"publicationYear"	:	2014,
"topics"	:	[	"data",	"science",	"data	science"]	}"""
#	analisa	o	json	para	criar	um	dict	do	Python
deserialized	=	json.loads(serialized)
if	"data	science"	in	deserialized["topics"]:
    print(deserialized)

"""as vezes, um provedor api fornece apenas respostas em XML, nesse caso utiliza-se BeautifulSoup para analisar o XML, da mesma forma como usamos para obter do HTML
"""