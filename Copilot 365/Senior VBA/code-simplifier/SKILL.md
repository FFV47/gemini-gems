---
name: code-simplifier
description: Simplifica código VBA sem mudar o comportamento, para ganhar clareza, consistência com as Regras do agente e facilidade de manutenção. Prova a equivalência de cada mudança, apresenta as simplificações como plano e entrega o código só após aprovação, com um teste que compara as duas versões. Por padrão, trabalha no que a última entrega de código do agente criou ou alterou. Use quando o usuário pedir para simplificar, limpar ou refatorar código sem mudar o que ele faz, ou disser 'simplifique', 'refatore', 'code simplifier' ou 'simplifique o que você fez'.
---

## Purpose

Simplificar código VBA sem mudar o que ele faz: deixá-lo mais claro, mais consistente com as **Regras** das instruções do agente e mais fácil de manter, preservando cada resultado, efeito e erro da versão original.

## Uses

- Agent capabilities: codeInterpreter

## Instructions

Uma **simplificação** é uma refatoração: muda como o código faz, nunca o que ele faz. Ela é **equivalente** quando, para toda entrada e todo estado do Excel, a versão simplificada produz os mesmos valores, os mesmos efeitos (células, abas, arquivos, mensagens, seleção e estado do `Application`) e os mesmos erros que a **versão original**, o código antes da simplificação. Equivalência se prova pela leitura, linha a linha.

A **interface** é o que o compilador não confere: o nome de procedimentos e módulos, que botões, formas, faixa de opções, `Application.Run`, `Application.OnTime`, fórmulas de planilha e outras pastas de trabalho podem chamar por texto; o nome dos eventos (`Workbook_Open`, `Worksheet_Change`, `<Controle>_Click`), que o Excel liga pelo nome; e a quantidade, a ordem e o tipo dos parâmetros desses procedimentos. Mudar a interface quebra o chamador sem erro de compilação.

Você não executa VBA nem acessa o Excel do usuário. O codeInterpreter lê arquivos anexados, mas não roda macros. O usuário confirma a equivalência no VBE, com o teste de equivalência do passo 6.

1. **Fixar o escopo.**
   - Por padrão, o escopo é o que a sua última entrega de código nesta conversa criou ou alterou. Compare os módulos entregues com a versão deles que estava na conversa antes da entrega. Módulo criado na entrega entra inteiro.
   - Se o usuário enviar código para simplificar, colado ou anexado em `.txt`, o escopo é esse código ou os procedimentos que ele nomear. Se ele pedir um escopo maior, como o módulo inteiro, use o que ele pediu.
   - Se não der para separar o que a entrega criou do que já existia, pergunte quais procedimentos simplificar e aguarde.
   - Liste os módulos e procedimentos do escopo. O código fora dele fica como está (A7).

2. **Levantar as candidatas.**
   - Percorra cada procedimento do escopo e anote como **candidata** cada mudança que deixe o código mais claro:
     - aninhamento que uma condição invertida, um `ElseIf` ou um `Select Case` achata;
     - lógica duplicada, que vira uma rotina extraída, no módulo que O2 indica;
     - elemento cujo nome não diz o que ele é (N1, N2);
     - código redundante: variável, atribuição ou teste sem efeito, rotina que só repassa a chamada;
     - lógica relacionada espalhada pelo procedimento;
     - comentário que repete o código. Ficam os comentários que as Regras exigem (C1, N4, motivo do `Variant` em E2) e os que explicam por quê;
     - divergência das **Regras**.
   - Escolha clareza em vez de brevidade: prefira `If...ElseIf` ou `Select Case` a `IIf` aninhado, uma instrução por linha (E4) e condição longa quebrada em variáveis `Boolean` com nome. Descarte a candidata que só encurta o código.
   - Mantenha a variável intermediária que dá nome a um valor, onde o usuário o confere na janela Variáveis Locais; a rotina curta que dá nome a um conceito; e a separação que A8 e A9 exigem.

3. **Provar a equivalência.**
   - Confira cada candidata contra estas armadilhas, em que duas formas parecidas se comportam diferente no VBA:
     - **`And` e `Or` avaliam os dois lados.** O VBA não tem curto-circuito: `If Not rng Is Nothing And rng.Value2 > 0` dá erro 91 quando `rng` é `Nothing`. O `If` aninhado que protege o segundo teste continua aninhado ou vira saída antecipada.
     - **`IIf`, `Choose` e `Switch` avaliam todos os argumentos.** `IIf(x = 0, 0, 1 / x)` dá erro de divisão por zero quando `x = 0`, e a função chamada em qualquer argumento roda sempre. Trocar uma delas por `If...Else`, ou o contrário, só é equivalente quando os argumentos não têm efeito colateral nem erro possível.
     - **`= True` só equivale ao teste direto em `Boolean`.** `True` vale `-1`: com `x` igual a `1` em `Integer`, `If x = True` é falso e `If x` é verdadeiro.
     - **Parênteses em volta de um argumento passam uma cópia.** Em `Rotina (x)`, sem `Call`, o VBA avalia `(x)` como expressão, e o parâmetro `ByRef` deixa de alterar `x`. Ao tirar o `Call`, tire também os parênteses: `Rotina x`.
     - **Parâmetro sem `ByVal` é `ByRef`.** Na rotina extraída, declare `ByVal` cada parâmetro que ela não deve devolver ao chamador. Em rotina existente, trocar `ByRef` por `ByVal` muda o resultado quando ela atribui ao parâmetro.
     - **Saída antecipada pula a restauração.** Depois de alterar estado do Excel, como `ScreenUpdating`, `EnableEvents` ou `Calculation`, saia por `GoTo Finalizar` (E7) ou ponha a saída antes da alteração.
     - **`For` avalia os limites uma vez.** `Do While i <= n` relê `n` a cada volta; trocá-lo por `For i = 1 To n` muda o resultado quando o laço altera `n` ou as linhas que percorre.
     - **Referência sem qualificação depende do módulo.** Em módulo de planilha, `Range` e `Cells` sem qualificação apontam para a própria planilha; nos outros módulos, para a planilha ativa. Ao qualificar (D1) ou mover código, mantenha a planilha de cada referência. Ao tirar `Select` e `Activate`, mantenha o posicionamento final que o usuário vê (exceção de D1).
     - **`Option Compare` e `Option Base` valem para o módulo inteiro.** Código movido ou extraído para módulo com outra opção compara texto com outra regra ou cria matrizes com outro índice inicial.
     - **Tipar uma `Variant` muda o comportamento.** Ao separar `Dim a, b As Long` (E2), declare `a As Variant`, com o motivo "mantém o tipo original", até o uso provar que outro tipo dá o mesmo resultado: tipo fixo muda o valor inicial, arredonda decimais e dá erro de tipo onde a `Variant` aceitava o valor.
     - **`Dim x As New` cria o objeto sozinho.** Juntar `Dim x As Classe` e `Set x = New Classe` em `Dim x As New Classe` faz `x Is Nothing` dar sempre falso e recria o objeto no primeiro uso depois de `Set x = Nothing`.
     - **Variável de módulo e `Static` guardam valor entre execuções.** Trocá-las por variável local, ou o contrário, muda o resultado da segunda execução em diante.
     - **Escrita pode mudar a leitura seguinte.** Separar leitura, cálculo e escrita (A9) muda o resultado quando uma escrita altera o que uma leitura posterior vê: fórmula que depende da célula gravada, evento `Worksheet_Change`.
     - **Algumas Regras mudam o comportamento.** Aplicadas a código existente, N6, F1 a F6, D3 a D6, D8, E7 a E9, T1, T2 e A4 nas mensagens mudam valores, tipos, erros ou efeitos.
   - Classifique cada candidata em uma de três listas:
     - **Simplificação:** equivalente, provada pela leitura.
     - **Com premissa:** equivalente se valer um fato que só o usuário pode confirmar: que nada fora do código usa o procedimento ou módulo que a mudança renomeia, remove, move ou cujos parâmetros altera (interface); ou que os dados nunca chegam ao caso em que as duas versões divergem.
     - **Fora desta entrega:** muda o comportamento, inclusive pela aplicação de uma Regra do último item, ou tem equivalência que você não provou. Entram aqui também as divergências fora do escopo e o código morto antigo (A7).
   - O passo termina quando cada candidata está em uma lista, com o motivo.

4. **Apresentar o plano e aguardar.**
   - As listas são o plano do **Fluxo** das instruções do agente. Numere os itens de Simplificações e Com premissa em sequência única, para o usuário aprovar por número. Use este formato:

   ```text
   **Escopo:** <módulos e procedimentos>

   ## Simplificações

   1. `<Procedimento>`: <o que muda>. Equivalente porque <motivo>.

   ## Com premissa

   2. `<Procedimento>`: <o que muda>. Equivalente se <premissa>. Confirma?

   ## Fora desta entrega

   - `<Procedimento>`: <o que é e por que fica de fora, com o ID da Regra quando houver>.
   ```

   - Agrupe em um único item as correções de espaçamento (E1, E5, E6).
   - Lista vazia: escreva `nenhuma`.
   - Na mesma mensagem, peça os dados de C2 que faltarem e a aprovação explícita. Aguarde.
   - Se as listas Simplificações e Com premissa estiverem vazias, diga isso, mostre a lista Fora desta entrega e encerre.

5. **Escrever e conferir.**
   - Escreva os módulos completos (A7) só com os itens aprovados.
   - Com o codeInterpreter, compare a versão original e a simplificada com o `difflib` do Python. Cada diferença corresponde a um item aprovado; desfaça a que não corresponder.
   - Passe cada diferença de novo pelas armadilhas do passo 3. Item aprovado que se mostrar não equivalente fica de fora; diga isso antes do código.
   - Faça a **Verificação** das instruções do agente no que a simplificação mudou. A violação que só some com mudança de comportamento vai para a lista Fora desta entrega.

6. **Entregar.**
   - Entregue conforme a **Saída** das instruções do agente. Em **Testes**, inclua o **teste de equivalência**, que roda as duas versões com as mesmas entradas, incluindo casos-limite:
     - Função de cálculo (A9): entregue a versão original em um módulo temporário, com o sufixo `_Original` em cada procedimento, e uma `Sub` que chama as duas versões e imprime na janela Verificação Imediata (Ctrl+G) `VERDE` quando as saídas coincidem ou `VERMELHO` com a entrada e as duas saídas quando divergem.
     - Procedimento com efeitos (grava em planilha ou arquivo, mostra mensagem): o usuário roda cada versão em uma cópia da pasta de trabalho e compara as saídas.
     - O teste é temporário: dispensa o cabeçalho C1, e o usuário o remove do projeto quando ficar `VERDE`.
   - Em **Riscos**, liste as premissas que o usuário confirmou. Para cada mudança de interface, diga onde o nome pode estar ligado fora do código: botão, forma, faixa de opções, fórmula, `Application.Run`.
   - O item de Fora desta entrega que o usuário quiser segue o Fluxo como alteração separada, depois que o teste de equivalência ficar `VERDE`. Misturado à simplificação, ele faria o teste falhar.

## Parameters

- Código a simplificar. Por padrão, a última entrega de código do agente na conversa.
- Opcionais, colados na conversa ou anexados em `.txt`: código do usuário, versão anterior dos módulos e procedimentos a simplificar.

## Output

- Plano: listas Simplificações, Com premissa e Fora desta entrega, no formato do passo 4.
- Após a aprovação: módulos completos em bloco `vba`, Testes com o teste de equivalência e Riscos com as premissas confirmadas, conforme a Saída das instruções do agente.
