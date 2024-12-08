import csv
from collections import defaultdict


class GeradorTabela:
    def __init__(self, gramatica):
        """
        Inicializa a gramática, conjuntos FIRST, FOLLOW e a tabela de análise sintática.
        """
        self.gramatica_raw = gramatica.strip()
        self.producoes = self.parse_gramatica(gramatica)
        self.nao_terminais = set(self.producoes.keys())
        self.terminais = self._extrair_terminais()
        self.first = defaultdict(set)
        self.follow = defaultdict(set)
        self.tabela = defaultdict(dict)
        self.simbolo_inicial = next(iter(self.producoes))
        
        print("Inicializando o cálculo dos conjuntos FIRST...")
        self.calcular_first()
        print("Conjuntos FIRST calculados e salvos em 'saidas/first.csv'.")
        
        print("Inicializando o cálculo dos conjuntos FOLLOW...")
        self.calcular_follow()
        print("Conjuntos FOLLOW calculados e salvos em 'saidas/follow.csv'.")
        
        print("Construindo a tabela de análise sintática preditiva...")
        self.construir_tabela()
        print("Tabela de análise sintática preditiva construída e salva em 'saidas/tabela.csv'.")

    def parse_gramatica(self, gramatica):
        """
        Converte a gramática de string para um dicionário de produções.
        """
        producoes = defaultdict(list)
        linhas = gramatica.strip().split('\n')
        for linha in linhas:
            if '::=' in linha:
                nao_terminal, regras = linha.split('::=')
                nao_terminal = nao_terminal.strip()
                regras = [regra.strip().split() for regra in regras.strip().split('|')]
                for regra in regras:
                    regra = ['ε' if simbolo == "''" else simbolo for simbolo in regra]
                    producoes[nao_terminal].append(regra)
        return producoes

    def _extrair_terminais(self):
        """
        Extrai os terminais da gramática.
        """
        terminais = set()
        for regras in self.producoes.values():
            for regra in regras:
                for simbolo in regra:
                    if simbolo not in self.producoes and simbolo != 'ε':
                        terminais.add(simbolo)
        return terminais

    def calcular_first(self):
        """
        Calcula os conjuntos FIRST para todos os não terminais.
        """
        for terminal in self.terminais:
            self.first[terminal] = {terminal}
        
        alterado = True
        while alterado:
            alterado = False
            for nao_terminal in self.nao_terminais:
                for producao in self.producoes[nao_terminal]:
                    tamanho_inicial = len(self.first[nao_terminal])
                    if producao[0] == 'ε':
                        self.first[nao_terminal].add('ε')
                    else:
                        i = 0
                        while i < len(producao):
                            simbolo = producao[i]
                            self.first[nao_terminal].update(self.first[simbolo] - {'ε'})
                            if 'ε' not in self.first[simbolo]:
                                break
                            i += 1
                        else:
                            self.first[nao_terminal].add('ε')
                    if tamanho_inicial != len(self.first[nao_terminal]):
                        alterado = True
        self._first_follow_csv("first")

    def calcular_follow(self):
        """
        Calcula os conjuntos FOLLOW para todos os não terminais.
        """
        self.follow[self.simbolo_inicial].add('$')
        alterado = True
        while alterado:
            alterado = False
            for nao_terminal in self.nao_terminais:
                for producao in self.producoes[nao_terminal]:
                    tamanho = len(producao)
                    for i in range(tamanho):
                        simbolo = producao[i]
                        if simbolo in self.nao_terminais:
                            follow_inicial = self.follow[simbolo].copy()
                            if i + 1 < tamanho:
                                next_simbolo = producao[i + 1]
                                self.follow[simbolo].update(self.first[next_simbolo] - {'ε'})
                                j = i + 1
                                while j < tamanho and 'ε' in self.first[producao[j]]:
                                    if j + 1 < tamanho:
                                        self.follow[simbolo].update(self.first[producao[j + 1]] - {'ε'})
                                    else:
                                        self.follow[simbolo].update(self.follow[nao_terminal])
                                    j += 1
                            else:
                                self.follow[simbolo].update(self.follow[nao_terminal])
                            if follow_inicial != self.follow[simbolo]:
                                alterado = True
        self._first_follow_csv("follow")

    def construir_tabela(self):
        """
        Constrói a tabela de análise sintática preditiva.
        """
        for nao_terminal in self.nao_terminais:
            for producao in self.producoes[nao_terminal]:
                first_producao = self._first_producao(producao)
                for terminal in first_producao - {'ε'}:
                    if terminal in self.tabela[nao_terminal]:
                        raise ValueError(f"Conflito na tabela para [{nao_terminal}, {terminal}]")
                    self.tabela[nao_terminal][terminal] = producao
                if 'ε' in first_producao:
                    for terminal in self.follow[nao_terminal]:
                        if terminal in self.tabela[nao_terminal]:
                            raise ValueError(f"Conflito na tabela para [{nao_terminal}, {terminal}]")
                        self.tabela[nao_terminal][terminal] = ['ε']
        self._tabela_csv()

    def _first_producao(self, producao):
        """
        Calcula o conjunto FIRST para uma produção específica.
        """
        first = set()
        if producao[0] == 'ε':
            first.add('ε')
        else:
            for simbolo in producao:
                first.update(self.first[simbolo] - {'ε'})
                if 'ε' not in self.first[simbolo]:
                    break
            else:
                first.add('ε')
        return first

    def _first_follow_csv(self, conjunto):
        """
        Escreve os conjuntos FIRST/FOLLOW em um arquivo CSV.
        """
        with open(f'saidas/{conjunto}.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Não Terminal', conjunto.upper()])
            for nao_terminal, valores in getattr(self, conjunto).items():
                writer.writerow([nao_terminal, ', '.join(sorted(valores))])

    def _tabela_csv(self):
        """
        Escreve a tabela de análise sintática preditiva em um arquivo CSV.
        """
        with open('saidas/tabela.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            colunas = sorted({t for nao_terminal in self.tabela for t in self.tabela[nao_terminal]})
            writer.writerow(['Não Terminal'] + colunas)
            for nao_terminal, producoes in self.tabela.items():
                linha = [nao_terminal]
                for terminal in colunas:
                    linha.append(', '.join(self.tabela[nao_terminal].get(terminal, [])))
                writer.writerow(linha)
        
        with open('saidas/tabela.csv', mode='r') as infile:
            reader = csv.reader(infile)
            cabecalhos = next(reader)
            linhas = list(reader)

        sorted_rows = sorted(linhas, key=lambda row: list(self.producoes.keys()).index(row[0]))

        with open('saidas/tabela.csv', mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(cabecalhos)
            writer.writerows(sorted_rows)