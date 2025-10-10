'''O Algoritmo de Luhn é amplamente utilizado para verificação de erros em 
diversas aplicações, como a verificação de números de cartão de crédito.
Ao construir este projeto, você ganhará experiência trabalhando com cálculos
numéricos e manipulação de strings.
----------------------------------------------------------------------------------------------------
O algoritmo de Luhn é o seguinte:
Da direita para a esquerda, dobre o valor de cada segundo dígito; se o produto for maior que 9, 
some os dígitos dos produtos.
Calcule a soma de todos os dígitos.
Se a soma de todos os dígitos for um múltiplo de 10, o número é válido; caso contrário, não é válido.
Exemplo: 
Account number      7   9  9  2  7  3  9   8  7  1  x
Double every other  7  18  9  4  7  6  9  16  7  2  x
Sum 2-char digits   7   9  9  4  7  6  9   7  7  2  x
----------------------------------------------------------------------------------------------------
- informação relevante para se ter na mente:
string[start:stop:step]
'''
def verify_card_number(card_number):
    sum_of_odd_digits = 0
    card_number_reversed = card_number[::-1]
    odd_digits = card_number_reversed[::2]

    for digit in odd_digits:
        sum_of_odd_digits += int(digit)

    sum_of_even_digits = 0
    even_digits = card_number_reversed[1::2]
    for digit in even_digits:
        number = int(digit) * 2
        if number >= 10:
            number = (number // 10) + (number % 10)
        sum_of_even_digits += number
    total = sum_of_odd_digits + sum_of_even_digits
    return total % 10 == 0

def main():
    card_number = '4111-1111-4555-1142'
    card_translation = str.maketrans({'-': '', ' ': ''})
    translated_card_number = card_number.translate(card_translation)

    if verify_card_number(translated_card_number):
        print('VALID!')
    else:
        print('INVALID!')

main()