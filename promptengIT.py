import re
#escrever uma função para verificar o endereço de email

def verificar_email(email):
    #pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.search("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        return True
    else:
        return False
    
'''
text to text:
ttt foundation models (FMs) are built for natural language processing tasks
that are developed by the ML reserarch community.

text to embeddings:
are another type of llm that can compare pieces of text (inputs), like what a 
user types into a search bar with indexed data, and makes a connection between
the two.

multimodal:
cad understand and generate different formats, such as text and images. eles conseguem
gerar imagens baseadas em llm prompts, ou seja, instruções em linguagem natural.
input: a photo os an astronaut riding a hors on mars
fm action: create and edit images using natural language prompts
output: an image of an astronaut riding a horse on mars
'''

#GENERATIVE AI USE CASES

