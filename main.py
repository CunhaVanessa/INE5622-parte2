import sys
from gerador_tabela import GeradorTabela
from analisador_sintatico_preditivo import AnalisadorSintatico

def main():
    if len(sys.argv) < 3:
        print("Uso:")
        print("  Para gerar tabelas: python3 main.py setup <caminho_gramatica>")
        print("  Para análise preditiva: python3 main.py analise <caminho_programa>")
        sys.exit(1)

    comando = sys.argv[1]
    caminho_arquivo = sys.argv[2]

    if comando == "setup":
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as file:
                gramatica = file.read()
            GeradorTabela(gramatica)
            print(f"Tabelas geradas com sucesso para a gramática em '{caminho_arquivo}'.")
        except FileNotFoundError:
            print(f"Erro: Arquivo de gramática '{caminho_arquivo}' não encontrado.")
        except Exception as e:
            print(f"Erro ao gerar tabelas: {e}")

    elif comando == "analise":
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as file:
                tokens = file.read().replace(';', ' ; ').replace(',', ' , ').replace('(', ' ( ').replace(')', ' ) ').replace('{', ' { ').replace('}', ' } ').replace(':=', ' := ').split()
                tokens = ['num' if t.isdigit() else 'id' if t.isidentifier() else t for t in tokens]
            analisador = AnalisadorSintatico(tokens)
            analisador.analisar()
        except FileNotFoundError:
            print(f"Erro: Arquivo de programa '{caminho_arquivo}' não encontrado.")
        except Exception as e:
            print(f"Erro na análise preditiva: {e}")

    else:
        print(f"Comando desconhecido: {comando}")
        print("Uso:")
        print("  Para gerar tabelas: python3 main.py setup <caminho_gramatica>")
        print("  Para análise preditiva: python3 main.py analise <caminho_programa>")
        sys.exit(1)

if __name__ == "__main__":
    main()
