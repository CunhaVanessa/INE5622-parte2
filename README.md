# Analisador Sintático Preditivo LL(1)

Autores: Vanessa Cunha, Gabriel Terra, Pedro Bressan.

Este projeto implementa um analisador sintático preditivo LL(1) para a linguagem LSI-2024-2. Ele processa um arquivo de entrada contendo código fonte e realiza a análise sintática para verificar se o código está em conformidade com a gramática definida. O analisador utiliza tabelas FIRST e FOLLOW para gerar uma tabela de parsing LL(1) e suporta produções com a derivação vazia (ε).

O projeto contém uma classe principal chamada AnalisadorSintaticoPreditivo, que processa a gramática, calcula os conjuntos FIRST e FOLLOW, constrói a tabela de análise sintática e realiza o parsing dos tokens da entrada com base na gramática.

## Requisitos

É necessário Python 3.7 ou superior para executar o projeto.

## Como utilizar

Para usar o analisador, siga as instruções:

1. Prepare o arquivo de entrada com a extensão .lsi contendo o código que será analisado. Por exemplo, temos o arquivo programa2.lsi que está disponível na pasta de exemplos:

   ```def calcular ( int N , int M ) {
       int Res ;
       if ( N > M ) {
           Res := N - M ;
       } else {
           Res := M - N ;
       }
       return Res ;
   }

   def main ( ) {
       int A , B , C ;
       A := 10 ;
       B := 20 ;
       C := calcular ( A , B ) ;
       print C ;
       return ;
   }
2. Execute o script no terminal fornecendo o caminho para o arquivo como argumento. Por exemplo, use o comando:

   `python3 main.py analise ou setup <caminho_do_arquivo>`

   Um exemplo de execução seria com o argumento setup para gerar as tabelas:

    `python3 main.py setup gramaticas/gramatica.txt`

   Um exemplo de execução seria com o argumento analise para realizar a analise do exemplo:

   `python3 main.py analise exemplos/programa1.lsi`

3. Verifique a saída do programa. O script exibirá o processo de parsing, incluindo cada produção aplicada e tokens consumidos. Em caso de erro, mensagens indicativas serão exibidas para ajudar na correção.

A gramática utilizada no projeto é definida para a linguagem LSI-2024-2. Alguns dos principais elementos incluem declaração de funções, lista de instruções, atribuições, chamadas de função, condicionais e expressões numéricas.

O parsing LL(1) é implementado com uma pilha para os símbolos da gramática e utiliza a tabela de parsing construída a partir dos conjuntos FIRST e FOLLOW. Em caso de erros, mensagens indicam problemas como tokens não consumidos ou produções ausentes na tabela de parsing. 

Possíveis erros incluem mensagens como "list index out of range", que podem ocorrer caso os tokens não terminem com o marcador $ no final da entrada. Outro erro comum é "Erro: sem entrada na tabela", que indica que a entrada não está em conformidade com a gramática.

Por exemplo, a saída do programa pode incluir o seguinte:

Processo de Parsing, exemplo de sucesso:

````
Match: print
EXPR -> NUMEXPR EXPR'
NUMEXPR -> TERM NUMEXPR'
TERM -> FACTOR TERM'
FACTOR -> id FACTOR'
Match: id
FACTOR' -> ε
TERM' -> ε
NUMEXPR' -> ε
EXPR' -> ε
Match: ;
STMTLIST' -> STMT STMTLIST'
STMT -> PRINTST ;
PRINTST -> print EXPR
Match: print
EXPR -> NUMEXPR EXPR'
NUMEXPR -> TERM NUMEXPR'
TERM -> FACTOR TERM'
FACTOR -> id FACTOR'
Match: id
FACTOR' -> ε
TERM' -> ε
NUMEXPR' -> ε
EXPR' -> ε
Match: ;
STMTLIST' -> STMT STMTLIST'
STMT -> RETURNST ;
RETURNST -> return RETURNID
Match: return
RETURNID -> ε
Match: ;
STMTLIST' -> ε
Match: }
FLIST' -> ε
MAIN' -> ε
Match: $
Parsing concluído com sucesso!
Total de Matches: 191
```

Exemplo de erro:


```
ATRIBST -> id := EXPR ATRIBEXPR
Match: id
Match: :=
EXPR -> NUMEXPR EXPR'
NUMEXPR -> TERM NUMEXPR'
TERM -> FACTOR TERM'
FACTOR -> id FACTOR'
Match: id
FACTOR' -> ε
TERM' -> ε
NUMEXPR' -> + TERM NUMEXPR'
Match: +
TERM -> FACTOR TERM'
FACTOR -> id FACTOR'
Match: id
Erro: não há produção para [FACTOR', if].
```
