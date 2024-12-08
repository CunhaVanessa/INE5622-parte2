import csv
from collections import defaultdict

class AnalisadorSintatico:
    def __init__(self, tokens):
        """
        Inicializa o analisador com os tokens e carrega os arquivos CSV.
        """
        self.tokens = tokens + ['$']
        self.tabela = self._ler_tabela_csv()
        self.simbolo_inicial = next(iter(self.tabela))
        self.nao_terminais = set(self.tabela.keys())

    def _ler_tabela_csv(self):
        """
        Lê a tabela de análise sintática preditiva do arquivo CSV.
        """
        tabela = defaultdict(dict)
        with open('saidas/tabela.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            colunas = next(reader)[1:]
            for linha in reader:
                nao_terminal = linha[0]
                for i, producao in enumerate(linha[1:]):
                    if producao:
                        tabela[nao_terminal][colunas[i]] = producao.split(", ")
        return tabela

    def analisar(self):
        """
        Implementa o parsing preditivo guiado por tabela.
        """
        pilha = ['$']
        pilha.append(self.simbolo_inicial)
        index = 0

        print("\nProcesso de Parsing:")
        while pilha:
            topo = pilha.pop()
            atual = self.tokens[index]

            if topo == atual:
                print(f"Match: {atual}")
                index += 1
            elif topo == 'ε':
                continue
            elif topo in self.nao_terminais:
                if atual in self.tabela[topo]:
                    producao = self.tabela[topo][atual]
                    print(f"{topo} -> {' '.join(producao)}")
                    pilha.extend(reversed(producao))
                else:
                    print(f"Erro: não há produção para [{topo}, {atual}].")
                    return
            else:
                print(f"Erro: esperado '{topo}', mas encontrado '{atual}'.")
                return

        if index < len(self.tokens) - 1:
            print(f"Erro: tokens restantes não consumidos: {self.tokens[index:]}")
        elif len(pilha) > 0:
            print(f"Erro: pilha não vazia: {pilha}")
        else:
            print("Parsing concluído com sucesso!")