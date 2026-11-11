---
name: diagnosing-bugs
description: Diagnostica bugs difíceis e lentidão em código VBA em seis fases. Constrói com o usuário uma reprodução que ele executa no VBE e que acusa o bug, minimiza o cenário, levanta hipóteses falseáveis, instrumenta uma variável por vez e só então leva a correção ao Fluxo, com teste de regressão e limpeza. Use quando o usuário disser 'diagnostique', 'depure' ou 'debug', ou relatar código que dá erro, trava, devolve resultado errado, parou de funcionar ou ficou lento.
---

## Purpose

Encontrar a causa de um bug difícil ou de uma lentidão em código VBA com disciplina: reproduzir antes de teorizar, provar a causa antes de corrigir e confirmar a correção antes de encerrar.

## Uses

- Agent capabilities: codeInterpreter

## Instructions

Você não executa VBA nem acessa o Excel do usuário. O codeInterpreter lê arquivos anexados, mas não roda macros. Quem executa é o usuário, no VBE.

A **reprodução** é uma `Sub` que o usuário roda com F5 e que imprime, na janela Verificação Imediata (Ctrl+G), `VERMELHO` quando o bug aparece e `VERDE` quando não aparece. Uma **sonda** é uma linha `Debug.Print` temporária que mostra um valor. Uma **rodada** é uma mensagem sua com um pedido de execução e a resposta do usuário com a saída.

Cada rodada custa tempo do usuário. Peça uma execução por rodada, neste formato:

```text
**Execute:** <passos numerados, um por linha>
**Cole de volta:** <o que copiar: saída da Verificação Imediata, número e descrição do erro, valor de célula>
```

Três condições valem em todas as fases:

- **Código de diagnóstico.** A reprodução e as sondas são temporárias: dispensam o plano e a aprovação do **Fluxo** das instruções do agente e o cabeçalho C1. Use nelas só os nomes que o usuário informou. A correção não é código de diagnóstico.
- **Dados em risco.** Se o procedimento sob suspeita altera ou exclui dados ou arquivos, peça ao usuário que rode tudo em uma cópia da pasta de trabalho.
- **Dados sensíveis.** O usuário vai colar código, saídas e dados. Peça que ele troque antes por `<OCULTO>` toda senha, string de conexão, token e dado pessoal. Se ele colar um segredo, não o repita: avise e escreva `<OCULTO>` no lugar. Se o que restou não basta para diagnosticar, diga isso e peça o que falta.

Siga as fases na ordem. Pule uma fase só com justificativa explícita, dita ao usuário.

1. **Construir a reprodução.**
   - **Esta fase é a skill.** O resto é mecânico. Com uma reprodução que fica VERMELHA neste bug, você acha a causa: comparação entre versões, hipóteses e sondas só consomem a reprodução. Sem ela, ler código não resolve. Gaste aqui um esforço desproporcional e não desista na primeira tentativa.
   - Peça o que falta para construí-la: o código do módulo, colado ou anexado em `.txt`; o sintoma exato (número e descrição do erro e a linha que o VBE realça em **Depurar**, ou o valor esperado e o obtido, ou o tempo gasto); a entrada que dispara o bug; se o código já funcionou e o que mudou desde então.
   - Maneiras de construir a reprodução, em ordem de preferência:
     1. **Teste direto.** Chame o procedimento sob suspeita com entrada fixa e compare o resultado com o esperado. Serve quando o cálculo não acessa `Range` (A9).
     2. **Planilha de teste.** A `Sub` grava os dados mínimos em uma planilha nova de uma cópia da pasta, roda a rotina e compara as células de saída com o esperado.
     3. **Dados capturados.** O usuário anexa as linhas reais que falham, em `.xlsx` ou `.csv`. Leia-as com o codeInterpreter, ache o que as distingue das linhas que funcionam e alimente a reprodução com elas.
     4. **Bancada descartável.** Copie o procedimento para um módulo temporário, troque as dependências por valores fixos e chame só o trecho do bug.
     5. **Entradas aleatórias.** Para "às vezes dá errado", rode 1.000 entradas geradas e compare cada resultado com um oráculo: uma função de planilha ou uma versão lenta e óbvia do cálculo. Imprima só as entradas que divergem. Fixe a sequência com `Rnd -1` seguido de `Randomize <semente>`.
     6. **Comparação entre versões.** Se uma versão anterior funcionava, ponha as duas no projeto com nomes distintos, rode a mesma entrada nas duas e compare as saídas. Para achar a mudança culpada, aplique metade das diferenças por vez.
     7. **Roteiro manual.** Último recurso, quando o bug depende de botão, formulário, evento ou seleção. Escreva os passos no formato de rodada e diga o que o usuário observa e cola em cada um.
   - Modelo da reprodução. Troque `a4f2` por quatro caracteres novos a cada diagnóstico, `Variant` pelo tipo real, e compare `Double` com tolerância:

   ```vba
   Option Explicit

   Private Const MARCA As String = "[DEBUG-a4f2]"

   Public Sub ReproduzirBug()
       Dim esperado As Variant
       Dim obtido As Variant

       On Error GoTo TratarErro

       esperado = <resultado que o usuário espera>
       obtido = <chamada ao procedimento sob suspeita, com a entrada que falha>

       If obtido = esperado Then
           Debug.Print MARCA & " VERDE"
       Else
           Debug.Print MARCA & " VERMELHO: esperado=" & CStr(esperado) & "; obtido=" & CStr(obtido)
       End If
       Exit Sub

   TratarErro:
       Debug.Print MARCA & " VERMELHO: erro " & Err.Number & " - " & Err.Description
   End Sub
   ```

   - Se o procedimento trata o próprio erro e exibe uma mensagem, a reprodução não recebe o erro: chame a rotina interna que falha ou compare o efeito (célula, arquivo) com o esperado.
   - Para lentidão, a reprodução mede o tempo com `Timer` e fica VERMELHA acima do limite que o usuário aceita.
   - **Aperte a reprodução.** Depois da primeira versão, pergunte:
     - Dá para ficar mais rápida? Menos linhas de dados, só o trecho do bug.
     - Dá para o sinal ficar mais nítido? Compare o sintoma exato, não "rodou sem erro".
     - Dá para ficar mais determinística? Fixe o que varia: planilha ativa, seleção, filtros, modo de cálculo, data e hora, `Rnd` e variáveis de módulo.
   - **Bug intermitente.** O objetivo é elevar a taxa de reprodução, não obter uma reprodução limpa. Em VBA a causa costuma ser estado, não acaso: `ActiveSheet` e `Selection` (D1), variável de módulo que guarda valor entre execuções, `EnableEvents`, modo de cálculo, filtro ou linha oculta, configuração regional, atualização de consulta em segundo plano. Repita o gatilho 100 vezes em laço, conte os VERMELHOS e varie um estado por vez até a taxa subir. Com 50% dá para depurar; com 1%, não.
   - **Sem reprodução possível.** Pare e diga isso. Liste o que você tentou. Peça ao usuário: (a) uma cópia da pasta de trabalho ou dos dados que reproduzem o bug; (b) evidência capturada: print da mensagem de erro, a linha realçada, a saída da Verificação Imediata; ou (c) permissão para pôr sondas temporárias no código real. Não levante hipóteses sem reprodução.
   - **Critério de saída.** O usuário já rodou a reprodução ao menos uma vez e colou a saída, e ela é:
     - **capaz de ficar VERMELHA:** executa o caminho do bug e compara o sintoma exato que o usuário relatou. Fica VERMELHA neste bug e VERDE depois da correção;
     - **determinística:** o mesmo veredito a cada execução ou, em bug intermitente, uma taxa alta e estável;
     - **rápida:** segundos, não minutos;
     - **de um passo só:** o usuário roda uma `Sub` e cola a saída. Roteiro manual, só como último recurso.
   - Se você se pegar lendo o código para montar uma teoria antes de essa `Sub` existir, pare: pular direto para a hipótese é a falha que esta skill evita. Sem reprodução VERMELHA, não há fase 2.

2. **Reproduzir e minimizar.**
   - Confira, na saída que o usuário colou:
     - a falha é a que o usuário descreveu, não outra falha vizinha. Bug errado, correção errada;
     - a falha se repete em várias execuções ou, em bug intermitente, a uma taxa que permite depurar;
     - o sintoma exato está registrado (mensagem, valor errado, tempo), para as fases seguintes conferirem a correção contra ele.
   - Reduza a reprodução ao menor cenário que ainda fica VERMELHO. Corte entradas, linhas, colunas, chamadores e passos, um por vez, e mantenha só o que sustenta a falha.
   - Para poupar rodadas, a mesma `Sub` pode testar vários cortes em uma execução e imprimir o veredito de cada um.
   - Um cenário mínimo reduz o que a fase 3 precisa suspeitar e vira o teste de regressão da fase 5.
   - A minimização termina quando remover qualquer elemento restante deixa a reprodução VERDE.
   - Não avance sem ter reproduzido e minimizado.

3. **Levantar hipóteses.**
   - Liste de 3 a 5 hipóteses, ordenadas da mais para a menos provável, antes de testar qualquer uma. Uma hipótese só ancora você na primeira ideia plausível.
   - Cada hipótese é falseável. Escreva a previsão que ela faz: "Se `<X>` for a causa, então `<mudar Y>` faz o bug sumir, ou `<mudar Z>` o piora."
   - Hipótese sem previsão é palpite: descarte-a ou refine-a.
   - Mostre a lista ao usuário antes de testar. Ele conhece o domínio e pode reordená-la ("mudei a aba da hipótese 3 ontem") ou eliminar o que já descartou.
   - Não fique parado à espera: na mesma mensagem, envie a sonda da primeira hipótese. Se o usuário reordenar, siga a ordem dele.

4. **Instrumentar.**
   - Cada sonda corresponde a uma previsão da fase 3. Mude uma variável por vez.
   - Preferência de ferramenta:
     1. **Depurador.** Em erro de execução, o usuário clica em **Depurar** e digita `? <expressão>` na Verificação Imediata. Em valor errado, ele põe um ponto de interrupção (F9) na linha que você indicar, avança com F8 e lê a janela Variáveis Locais. Diga a linha e as expressões exatas. Um ponto de interrupção vale mais que dez sondas.
     2. **Sondas** nas fronteiras que distinguem as hipóteses: entrada e saída de cada etapa.
     3. Nunca "imprima tudo e procure": a Verificação Imediata guarda só as últimas 200 linhas, aproximadamente.
   - Toda sonda leva a marca da reprodução (`[DEBUG-a4f2]`). Sonda marcada sai com uma busca na limpeza; sonda sem marca fica no código.
   - **Erro escondido.** Se `On Error Resume Next` ou um tratador esconde a linha que falha, peça ao usuário que marque, no VBE, Ferramentas > Opções > Geral > **Interromper em todos os erros**, e anote a opção anterior para restaurá-la na fase 6.
   - **Hipótese sobre dados.** Número guardado como texto, espaço no fim, data como texto: confira no arquivo anexado com o codeInterpreter ou imprima `TypeName(valor)` e `Len(valor)`.
   - **Lentidão.** Sonda de texto pouco ajuda. Meça primeiro: guarde `Timer` antes e depois de cada etapa (leitura, cálculo, escrita) e imprima os segundos de cada uma. Divida a etapa mais lenta e meça de novo. Corrija só depois de medir.

5. **Corrigir com teste de regressão.**
   - Escreva o teste de regressão antes da correção, mas só se houver um **ponto de teste correto**: um procedimento que o teste chama com entrada fixa e que exercita o padrão real do bug, como ele ocorre na chamada original.
   - Ponto raso dá confiança falsa: testar uma função isolada quando o bug exige a sequência leitura, cálculo e escrita, ou um evento de formulário.
   - Se não há ponto de teste correto, esse é o achado. Registre que a estrutura do código impede fixar o bug em um teste e relate isso na fase 6.
   - Se há:
     1. Transforme a reprodução minimizada em teste: a mesma `Sub`, com nome que diga o que ela testa.
     2. Confirme que ela fica VERMELHA no código atual. Se o VERMELHO veio de alterar código ou dados para forçá-lo, confirme com o usuário que a alteração está no que ele executou.
     3. Leve a correção ao **Fluxo** das instruções do agente: plano com a causa confirmada, aprovação e só então código. O teste entra em **Testes** da Saída.
     4. O usuário aplica a correção e roda o teste: VERDE.
     5. O usuário roda a reprodução da fase 1 no cenário original, não minimizado.

6. **Limpar.**
   - Antes de declarar o bug resolvido, confirme com o usuário, um item por linha:
     - a reprodução original fica VERDE (saída colada);
     - o teste de regressão passa, ou a falta de ponto de teste correto está registrada;
     - nenhuma sonda restou: a busca por `[DEBUG-` no VBE (Ctrl+F, **Projeto atual**) não encontra nada;
     - os módulos temporários foram removidos, ou mantidos com nome que os identifique como teste;
     - a opção de interceptação de erros voltou ao valor anterior, se foi alterada.
   - Declare em uma frase a hipótese que se confirmou, para o usuário registrar junto da alteração. Quem depurar depois aprende com ela.
   - Não declare resolvido um bug cuja reprodução o usuário não rodou depois da correção.

## Parameters

- Sintoma: mensagem de erro, resultado errado ou tempo de execução, descrito na conversa.
- Código do módulo ou do projeto, colado na conversa ou anexado em `.txt`.
- Opcionais: dados que disparam o bug (`.xlsx` ou `.csv`), versão anterior que funcionava e prints.
