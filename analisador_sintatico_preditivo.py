# analisador_sintatico_preditivo.py
# Autores: Vanessa Cunha, Gabriel Terra, Pedro Bressan
# Implementação de um analisador sintático preditivo LL(1) para a linguagem LSI-2024-2

import sys
from collections import defaultdict

class AnalisadorSintaticoPreditivo:
    def __init__(self, gramatica, tokens):
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
        self.tokens = tokens
        self.calcular_first()
        self.calcular_follow()
        self.construir_tabela()

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
                        while True:
                            simbolo = producao[i]
                            self.first[nao_terminal].update(self.first[simbolo] - {'ε'})
                            if 'ε' not in self.first[simbolo]:
                                break
                            i += 1
                            if i == len(producao):
                                self.first[nao_terminal].add('ε')
                                break
                    if tamanho_inicial != len(self.first[nao_terminal]):
                        alterado = True

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

    def analisar(self):
        """
        Implementa o parsing preditivo guiado por tabela.
        """
        self.tokens.append('$')  # Adiciona o marcador de fim de entrada
        self.pilha = ['$']
        self.pilha.append(self.simbolo_inicial)
        index = 0
        sucesso = True

        print("\nProcesso de Parsing:")
        while len(self.pilha) > 0:
            if index >= len(self.tokens):  # Verifica se o índice está fora do limite
                print("Erro: índice fora do limite ao consumir tokens.")
                sucesso = False
                break

            topo = self.pilha.pop()
            atual = self.tokens[index]

            if topo == atual:
                print(f"Match: {atual}")
                index += 1
            elif topo == 'ε':
                continue
            elif topo in self.terminais:
                print(f"Erro: esperado '{topo}', mas encontrado '{atual}'")
                sucesso = False
                break
            elif topo in self.nao_terminais:
                if atual in self.tabela[topo]:
                    producao = self.tabela[topo][atual]
                    print(f"{topo} -> {' '.join(producao)}")
                    for simbolo in reversed(producao):
                        self.pilha.append(simbolo)
                else:
                    print(f"Erro: sem entrada na tabela para [{topo}, {atual}]")
                    sucesso = False
                    break
            else:
                print(f"Erro: símbolo desconhecido '{topo}'")
                sucesso = False
                break

        # Validação final
        if sucesso and len(self.pilha) == 0 and atual == '$' and index == len(self.tokens) - 1:
            print("Parsing concluído com sucesso!")
        else:
            if len(self.pilha) > 1 or self.pilha[0] != '$':
                print(f"Erro: pilha não vazia. Conteúdo da pilha: {self.pilha}")
            if index < len(self.tokens) - 1:
                print(f"Erro: tokens não consumidos. Tokens restantes: {self.tokens[index:]}")
            print("Erro: a entrada não foi completamente consumida.")



def main():
    if len(sys.argv) != 2:
        print("Uso: python analisador_sintatico_preditivo.py <caminho_do_arquivo>")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]

    try:
        with open(caminho_arquivo, 'r') as arquivo:
            conteudo = arquivo.read()

        tokens = conteudo.replace(';', ' ; ').replace(',', ' , ').replace('(', ' ( ').replace(')', ' ) ').replace('{', ' { ').replace('}', ' } ').replace(':=', ' := ').split()
        tokens = ['num' if token.isdigit() else 'id' if token.isidentifier() and token not in ['def', 'int', 'print', 'return', 'if', 'else'] else token for token in tokens]

        gramatica = """
                    MAIN ::= FLIST MAIN'
                    MAIN' ::= STMT
                    MAIN' ::= ''

                    FLIST ::= FDEF FLIST'
                    FLIST' ::= FDEF FLIST'
                    FLIST' ::= ''

                    FDEF ::= def id ( PARLIST ) { STMTLIST }

                    PARLIST ::= int id PARLIST'
                    PARLIST ::= ''
                    PARLIST' ::= , int id PARLIST'
                    PARLIST' ::= ''

                    VARLIST ::= id VARLIST'
                    VARLIST' ::= , id VARLIST'
                    VARLIST' ::= ''

                    STMT ::= int VARLIST ;
                    STMT ::= ATRIBST ;
                    STMT ::= PRINTST ;
                    STMT ::= RETURNST ;
                    STMT ::= IFSTMT
                    STMT ::= { STMTLIST }
                    STMT ::= ;

                    ATRIBST ::= id := EXPR ATRIBEXPR
                    ATRIBEXPR ::= FCALL
                    ATRIBEXPR ::= ''

                    FCALL ::= id ( PARLISTCALL )

                    PARLISTCALL ::= id PARLISTCALL'
                    PARLISTCALL' ::= , id PARLISTCALL'
                    PARLISTCALL' ::= ''

                    PRINTST ::= print EXPR

                    RETURNST ::= return RETURNID
                    RETURNID ::= id
                    RETURNID ::= ''

                    IFSTMT ::= if ( EXPR ) STMT ELSEPART
                    ELSEPART ::= else STMT ELSEBODY
                    ELSEBODY ::= ε

                    STMTLIST ::= STMT STMTLIST'
                    STMTLIST' ::= STMT STMTLIST'
                    STMTLIST' ::= ''

                    EXPR ::= NUMEXPR EXPR'
                    EXPR' ::= < NUMEXPR
                    EXPR' ::= <= NUMEXPR
                    EXPR' ::= > NUMEXPR
                    EXPR' ::= >= NUMEXPR
                    EXPR' ::= == NUMEXPR
                    EXPR' ::= <> NUMEXPR
                    EXPR' ::= ''

                    NUMEXPR ::= TERM NUMEXPR'
                    NUMEXPR' ::= + TERM NUMEXPR'
                    NUMEXPR' ::= - TERM NUMEXPR'
                    NUMEXPR' ::= ''

                    TERM ::= FACTOR TERM'
                    TERM' ::= * FACTOR TERM'
                    TERM' ::= / FACTOR TERM'
                    TERM' ::= ''

                    FACTOR ::= num
                    FACTOR ::= ( EXPR )
                    FACTOR ::= id FACTOR'
                    FACTOR' ::= ( PARLISTCALL )
                    FACTOR' ::= ''
                    """

        analisador = AnalisadorSintaticoPreditivo(gramatica, tokens)
        analisador.analisar()

    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho_arquivo}' não encontrado.")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()