class Conta:
    def __init__(self, numero):
        self.__numero = numero
        self.__saldo = 0.0

    def creditar(self, valor):
        self.__saldo += valor
   
    def debitar(self, valor):
        self.__saldo -= valor
   
    def get_numero(self):
        return self.__numero 
   
    def get_saldo(self):
        return self.__saldo

class Poupanca(Conta):
    def __init__(self, numero):
        super().__init__(numero)

    def render_juros(self, taxa):
        self.creditar(self.get_saldo() * taxa)

class Banco:
    def __init__(self):
        self.__contas = []

    def cadastrar(self, conta):
        self.__contas.append(conta)

    def procurar(self, numero):
        for conta in self.__contas:
            if conta.get_numero() == numero:
                return conta
        return None

    def creditar(self, numero, valor):
        conta = self.procurar(numero)
        if conta is not None:
            conta.creditar(valor)

    def debitar(self, numero, valor):
        conta = self.procurar(numero)
        if conta is not None:
            conta.debitar(valor)
   
    def get_saldo(self, numero):
        conta = self.procurar(numero)
        if conta is not None:
            return conta.get_saldo()
        
        return None
   
    def transferir(self, origem, destino, valor):
        conta_origem = self.procurar(origem)
        if conta_origem is not None and conta_origem.get_saldo() >= valor:
            conta_destino = self.procurar(destino)
            if conta_destino is not None:
                conta_origem.debitar(valor)
                conta_destino.creditar(valor)
    
    def render_juros(self, numero, taxa):
        conta = self.procurar(numero)
        if conta is not None:
            if isinstance(conta, Poupanca):
                conta.render_juros(taxa)                