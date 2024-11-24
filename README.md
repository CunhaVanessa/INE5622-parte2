# INE5622-parte2
---------------------------------------------

### Descrição do Projeto
Este projeto implementa um analisador sintático preditivo para gramáticas LL(1). Ele utiliza os conjuntos **FIRST** e **FOLLOW** para construir uma tabela de análise sintática preditiva, capaz de verificar strings pertencentes à linguagem descrita pela gramática dada.

O programa também lida com gramáticas fatoradas à esquerda e sem recursão à esquerda. Caso a gramática não seja LL(1), o programa identificará conflitos na tabela durante sua construção.

### Estrutura do Código
- **`AnalisadorSintaticoPreditivo`**: Classe principal que realiza todas as operações necessárias.
  - **`calcular_first`**: Calcula os conjuntos FIRST para cada não terminal.
  - **`calcular_follow`**: Calcula os conjuntos FOLLOW para cada não terminal.
  - **`construir_tabela`**: Constrói a tabela de análise sintática preditiva com base nos conjuntos FIRST e FOLLOW.
  - **`exibir_tabela`**: Exibe a tabela de análise sintática no terminal.
- As produções da gramática são configuradas em um dicionário Python.

### Como Configurar
1. **Requisitos:**
   - Python 3.8 ou superior.
   - Um editor de texto ou IDE para rodar o código.

2. **Estrutura de Produções:**
   As produções devem ser fornecidas como um dicionário Python no seguinte formato:
   - Cada não terminal é uma chave.
   - Os valores são listas de produções, onde cada produção é representada por uma lista de símbolos.

   **Exemplo de Produções:**
   ```python
   producoes = {
       "S": [["a", "A"], ["b"]],
       "A": [["b", "S"], ["ε"]]
   }   

3. **Instalação:**
   - Copie o código para um arquivo chamado analisador_sintatico.py.
   - Não é necessário instalar bibliotecas externas.

   **Como executar:**
    1. Abra o terminal no diretório onde o arquivo foi salvo.
    2. Execute o script com o comando: `python analisador_sintatico.py`
    3. Saída Esperada: O programa exibirá:
        - Os conjuntos FIRST e FOLLOW.
        - A tabela de análise sintática preditiva.
   
   **Exemplo de Saída**
    
    - Para a gramática:

                S → aA | b
                A → bS | ε
   
   - O programa exibirá:

            S: {'a': ['a', 'A'], 'b': ['b']}
            A: {'b': ['b', 'S'], '$': ['ε']}

            FIRST:
            S: {'a', 'b'}
            A: {'b', 'ε'}

            FOLLOW:
            S: {'$'}
            A: {'a', 'b', '$'}

 **Notas Importantes**
- Certifique-se de que a gramática fornecida está fatorada e sem recursão à esquerda antes de rodar o programa. 
- Em caso de conflitos na gramática (não LL(1)), o programa exibirá mensagens de erro detalhadas indicando os conflitos.
- Para alterar a gramática analisada, edite a variável producoes no código.

**O que ainda falta**
- Receber a linguagem via linha de comando