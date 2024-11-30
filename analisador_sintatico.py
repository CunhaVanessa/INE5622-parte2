from collections import defaultdict

class AnalisadorSintaticoPreditivo:
    def __init__(self, gramatica):
        """
        Inicializa a gramática e estrutura para FIRST, FOLLOW e tabela de análise.
        """
        self.producoes = self.parse_gramatica(gramatica)
        self.first = defaultdict(set)
        self.follow = defaultdict(set)
        self.tabela = defaultdict(dict)
        self.nao_terminais = set(self.producoes.keys())
        self.terminais = self._extrair_terminais()

    def parse_gramatica(self, gramatica):
        """
        Converte gramática no formato string para dicionário.
        Exemplo:
        'E ::= T E'\nE' ::= + T E' | ε\n...' -> {'E': [['T', "E'"]], "E'": [['+', 'T', "E'"], ['ε']], ...}
        """
        producoes = {}
        linhas = gramatica.strip().split('\n')
        for linha in linhas:
            nao_terminal, regras = linha.split('::=')
            nao_terminal = nao_terminal.strip()
            regras = [regra.strip().split() for regra in regras.split('|')]
            # Substituir '' por ε
            regras = [[simbolo if simbolo != "''" else 'ε' for simbolo in regra] for regra in regras]
            producoes[nao_terminal] = regras
        return producoes

    def _extrair_terminais(self):
        """
        Extrai os terminais da gramática a partir das produções.
        """
        terminais = set()
        for producoes in self.producoes.values():
            for producao in producoes:
                for simbolo in producao:
                    if simbolo not in self.producoes and simbolo != 'ε':
                        terminais.add(simbolo)
        return terminais

    def calcular_first(self):
        """
        Calcula os conjuntos FIRST para cada não terminal da gramática.
        """
        alterado = True
        while alterado:
            alterado = False
            for nao_terminal, producoes in self.producoes.items():
                for producao in producoes:
                    for simbolo in producao:
                        if simbolo in self.terminais:
                            if simbolo not in self.first[nao_terminal]:
                                self.first[nao_terminal].add(simbolo)
                                alterado = True
                            break
                        else:
                            novos = self.first[simbolo] - {'ε'}
                            if not novos.issubset(self.first[nao_terminal]):
                                self.first[nao_terminal].update(novos)
                                alterado = True
                            if 'ε' not in self.first[simbolo]:
                                break
                    else:
                        if 'ε' not in self.first[nao_terminal]:
                            self.first[nao_terminal].add('ε')
                            alterado = True

    def calcular_follow(self):
        """
        Calcula os conjuntos FOLLOW para cada não terminal da gramática.
        """
        self.follow[next(iter(self.producoes))].add('$')  # Símbolo inicial
        alterado = True
        while alterado:
            alterado = False
            for nao_terminal, producoes in self.producoes.items():
                for producao in producoes:
                    follow_temp = self.follow[nao_terminal]
                    for simbolo in reversed(producao):
                        if simbolo in self.nao_terminais:
                            if not follow_temp.issubset(self.follow[simbolo]):
                                self.follow[simbolo].update(follow_temp)
                                alterado = True
                            if 'ε' in self.first[simbolo]:
                                follow_temp = follow_temp.union(self.first[simbolo] - {'ε'})
                            else:
                                follow_temp = self.first[simbolo]
                        else:
                            follow_temp = {simbolo}

    def construir_tabela(self):
        """
        Constrói a tabela de análise sintática preditiva.
        """
        for nao_terminal, producoes in self.producoes.items():
            for producao in producoes:
                primeiro = set()
                for simbolo in producao:
                    if simbolo in self.terminais:
                        primeiro.add(simbolo)
                        break
                    primeiro.update(self.first[simbolo] - {'ε'})
                    if 'ε' not in self.first[simbolo]:
                        break
                else:
                    primeiro.add('ε')

                for terminal in primeiro - {'ε'}:
                    if terminal in self.tabela[nao_terminal]:
                        raise ValueError(f"Conflito na tabela para {nao_terminal} -> {producao}")
                    self.tabela[nao_terminal][terminal] = producao

                if 'ε' in primeiro:
                    for terminal in self.follow[nao_terminal]:
                        if terminal in self.tabela[nao_terminal]:
                            raise ValueError(f"Conflito na tabela para {nao_terminal} -> {producao}")
                        self.tabela[nao_terminal][terminal] = producao

    def exibir_tabela(self):
        """
        Exibe a tabela de análise sintática preditiva em formato tabular.
        """
        print("Tabela de Análise Sintática Preditiva:")
        for nao_terminal, entradas in self.tabela.items():
            print(f"{nao_terminal}: {entradas}")

# Exemplo de uso:
gramatica = """
E ::= T E'
E' ::= + T E' | ε
T ::= F T'
T' ::= * F T' | ε
F ::= ( E ) | id
"""

analisador = AnalisadorSintaticoPreditivo(gramatica)
analisador.calcular_first()
analisador.calcular_follow()
analisador.construir_tabela()
analisador.exibir_tabela()

print("\nFIRST:")
for nao_terminal, conjunto in analisador.first.items():
    print(f"{nao_terminal}: {conjunto}")

print("\nFOLLOW:")
for nao_terminal, conjunto in analisador.follow.items():
    print(f"{nao_terminal}: {conjunto}")
