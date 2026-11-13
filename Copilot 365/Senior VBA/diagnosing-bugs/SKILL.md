---
name: diagnosing-bugs
description: Diagnostica bugs difíceis e lentidão em código VBA em seis fases. Constrói com o usuário uma reprodução que ele executa no VBE e que acusa o bug, minimiza o cenário, levanta hipóteses falseáveis, instrumenta uma variável por vez e só então leva a correção ao Fluxo, com teste de regressão e limpeza. Use quando o usuário disser 'diagnostique', 'depure' ou 'debug', ou relatar código que não compila, dá erro, trava, devolve resultado errado, parou de funcionar ou ficou lento.
---

## Purpose

Encontrar a causa de um bug difícil ou de uma lentidão em código VBA com disciplina: reproduzir antes de teorizar, provar a causa antes de corrigir e confirmar a correção antes de encerrar.

## Uses

- Agent capabilities: codeInterpreter

## Instructions

Você não executa VBA nem acessa o Excel do usuário. Quem executa é o usuário, no VBE, e só o código dele rodando lá reproduz o bug. O codeInterpreter roda Python: com ele, você lê arquivos anexados e compara versões de código. Uma tradução do VBA para Python muda o comportamento, como o estouro de `Integer` acima de 32.767, a conversão automática de `Variant` e a vírgula decimal de `CStr` no pt-BR.

A **reprodução** é uma `Sub` que o usuário roda com F5 e que imprime, na janela Verificação Imediata (Ctrl+G), `VERMELHO` quando o bug aparece e `VERDE` quando não aparece. Uma **sonda** é uma linha `Debug.Print` temporária que mostra um valor. A **marca** é o texto `[DEBUG-<id>]`, com quatro caracteres novos em `<id>` a cada diagnóstico; ela identifica a saída e o código temporário do diagnóstico. Uma **rodada** é uma mensagem sua com um pedido de execução e a resposta do usuário com a saída.

Cada rodada custa tempo do usuário. Peça uma execução por rodada. Vários testes cabem em uma execução se cada um partir do mesmo estado inicial e imprimir o próprio veredito. A conversa é o único registro do diagnóstico: abra cada rodada com a linha de estado e feche com o pedido, neste formato:

```text
**Diagnóstico:** fase <n> de 6 · marca [DEBUG-<id>] · sintoma: <sintoma exato> · a desfazer: <módulos temporários, sondas, arquivos e opções do VBE alterados, ou "nada">

<análise e código da rodada>

**Execute:** <passos numerados, um por linha>
**Cole de volta:** <o que copiar: saída da Verificação Imediata, número e descrição do erro, valor de célula>
```

A primeira linha que a reprodução imprime traz a marca e o número da rodada. O primeiro passo de **Execute** manda limpar a Verificação Imediata (clicar nela, Ctrl+A, Delete): a janela acumula a saída das execuções anteriores, e quem copia tudo cola vereditos antigos junto com o novo.

Quatro condições valem em todas as fases:

- **Código de diagnóstico.** A reprodução e as sondas são temporárias. Elas dispensam o plano e a aprovação do **Fluxo** das instruções do agente, as seções Testes e Riscos da **Saída** e as Regras C1, O1 e O2: a marca e as rotinas auxiliares ficam dentro da própria reprodução. D1 também não vale quando a reprodução fixa de propósito a planilha ativa ou a seleção. Use nelas só os nomes que o usuário informou. A correção não é código de diagnóstico.
- **Colagem.** O usuário cola a reprodução no fim do módulo do procedimento sob suspeita, onde ela alcança também procedimentos `Private`. Por isso a reprodução declara tudo dentro da `Sub`, sem `Option Explicit` nem declarações de módulo, que depois de um procedimento não compilam. Se o módulo é de classe ou de formulário, onde F5 não roda a `Sub`, ela vai para um módulo novo (Inserir > Módulo) e chama só membros públicos. Cada nova versão substitui a anterior, porque duas `Sub` com o mesmo nome no módulo não compilam. Para rodar, o usuário clica dentro da `Sub` e tecla F5.
- **Dados em risco.** Se o procedimento sob suspeita altera ou exclui dados, peça ao usuário que rode tudo em uma cópia da pasta de trabalho. A cópia protege só a própria pasta. Se o procedimento grava, move ou exclui arquivos (`Kill`, `Name`, `SaveAs`), salva outras pastas, envia e-mail ou grava em banco de dados, a reprodução troca esse efeito por um valor fixo (bancada descartável) ou o aponta para uma pasta de teste que o usuário indicar, e o pedido de execução diz qual das duas. Um laço que repete o gatilho repete o efeito a cada volta.
- **Dados sensíveis.** O usuário vai colar código, saídas e dados. Peça que ele troque antes por `<OCULTO>` toda senha, string de conexão e token, e cada dado pessoal por um valor fictício de mesmo formato (tamanho, tipo, espaços, acentos), que preserva o que dispara o bug. Se ele colar um segredo, não o repita: avise e escreva `<OCULTO>` no lugar. Se o que restou não basta para diagnosticar, diga isso e peça o que falta.

Siga as fases na ordem. Pule uma fase só com justificativa explícita, dita ao usuário.

1. **Construir a reprodução.**
   - **Esta fase é a skill.** O resto é mecânico. Com uma reprodução que fica VERMELHA neste bug, você acha a causa: comparação entre versões, hipóteses e sondas só consomem a reprodução. Sem ela, ler código não resolve. Gaste aqui um esforço desproporcional e não desista na primeira tentativa.
   - Peça o que falta para construí-la: o código do módulo, com o nome e o tipo dele (comum, de planilha, de classe ou de formulário), colado ou anexado em `.txt`; o sintoma exato (número e descrição do erro e a linha que o VBE realça em **Depurar**, ou o valor esperado e o obtido, ou o tempo gasto); a entrada que dispara o bug; se o código já funcionou e o que mudou desde então.
   - Maneiras de construir a reprodução, em ordem de preferência:
     1. **Teste direto.** Chame o procedimento sob suspeita com entrada fixa e compare o resultado com o esperado. Serve quando o cálculo não acessa `Range` (A9).
     2. **Planilha de teste.** A `Sub` grava os dados mínimos em uma planilha nova de uma cópia da pasta, roda a rotina e compara as células de saída com o esperado.
     3. **Dados capturados.** O usuário anexa as linhas reais que falham, de preferência em `.xlsx`, que guarda o tipo de cada célula: o `.csv` grava tudo como texto e apaga a diferença entre número e texto. Leia-as com o codeInterpreter, ache o que as distingue das linhas que funcionam e alimente a reprodução com elas.
     4. **Bancada descartável.** Copie o procedimento, com outro nome, para um módulo novo, troque as dependências por valores fixos e chame só o trecho do bug.
     5. **Entradas aleatórias.** Para "às vezes dá errado", rode 1.000 entradas geradas e compare cada resultado com um oráculo: uma função de planilha ou uma versão lenta e óbvia do cálculo. Imprima o total de divergências e só as 20 primeiras, que cabem na Verificação Imediata. Fixe a sequência com `Rnd -1` seguido de `Randomize <semente>`.
     6. **Comparação entre versões.** Se uma versão anterior funcionava, ponha as duas no projeto com nomes distintos, rode a mesma entrada nas duas e compare as saídas. Para achar a mudança culpada, liste as diferenças entre as versões com o `difflib` no codeInterpreter e aplique metade delas por vez.
     7. **Evento disparado pelo código.** Quando o bug depende de evento, seleção ou botão, a reprodução faz o que o usuário faria: gravar na célula dispara `Worksheet_Change`, selecionar um intervalo dispara `Worksheet_SelectionChange`, e chamar a macro atribuída ao botão percorre o caminho do clique, salvo quando ela lê `Application.Caller`. Os eventos só disparam com `EnableEvents` ligado.
     8. **Roteiro manual.** Último recurso, quando o código não alcança o gatilho, como um clique em formulário. Escreva os passos no formato de rodada e diga o que o usuário observa e cola em cada um.
   - Modelo da reprodução. Troque `a4f2` pelo `<id>` deste diagnóstico, `<n>` pelo número da rodada e `Variant` pelo tipo real, e compare `Double` com tolerância:

   ```vba
   Public Sub ReproduzirBug()
       Const MARCA As String = "[DEBUG-a4f2]"
       Dim esperado As Variant
       Dim obtido As Variant

       On Error GoTo TratarErro

       Debug.Print MARCA & " rodada <n>"
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
   - **Travamento ou fechamento do Excel.** A reprodução não volta para imprimir o veredito, e a Verificação Imediata some quando o Excel fecha. Grave cada linha de saída no arquivo `Environ$("TEMP") & "\DEBUG-<id>.txt"`, abrindo e fechando o arquivo a cada linha (`Open ... For Append`, `Print #`, `Close`): a última linha mostra até onde o código chegou. O usuário salva tudo antes de rodar e, se o Excel parar de responder, tenta Esc ou Ctrl+Break antes de encerrá-lo. Depois, ele abre `%TEMP%\DEBUG-<id>.txt` com Win+R e cola o conteúdo ou anexa o arquivo.
   - **Erro de compilação.** O VBE acusa o erro antes de rodar, e `On Error` não o captura. A reprodução é **Depurar > Compilar VBAProject**: um passo, que mostra a mensagem e realça a linha sem executar nada. Na fase 2, o cenário mínimo é a linha realçada e as declarações de que ela depende.
   - **Aperte a reprodução.** Depois da primeira versão, pergunte:
     - Dá para ficar mais rápida? Menos linhas de dados, só o trecho do bug.
     - Dá para o sinal ficar mais nítido? Compare o sintoma exato, não "rodou sem erro".
     - Dá para ficar mais determinística? Fixe o que varia: planilha ativa, seleção, filtros, modo de cálculo, data e hora, `Rnd` e variáveis de módulo.
   - **Bug intermitente.** O objetivo é elevar a taxa de reprodução, não obter uma reprodução limpa. Em VBA a causa costuma ser estado, não acaso: `ActiveSheet` e `Selection` (D1), variável de módulo que guarda valor entre execuções, `EnableEvents`, modo de cálculo, filtro ou linha oculta, configuração regional, atualização de consulta em segundo plano. Repita o gatilho 100 vezes em laço, conte os VERMELHOS e varie um estado por vez até a taxa subir. Com 50% dá para depurar; com 1%, não.
   - **Sem reprodução possível.** Pare e diga isso. Liste o que você tentou. Peça ao usuário: (a) os dados que reproduzem o bug, em `.xlsx`, e o código do projeto inteiro em `.txt`, que você lê com o codeInterpreter; (b) evidência capturada: print da mensagem de erro, a linha realçada, a saída da Verificação Imediata; ou (c) permissão para pôr sondas temporárias no código real. Não levante hipóteses sem reprodução.
   - **Critério de saída.** O usuário já rodou a reprodução ao menos uma vez e colou a saída, e ela é:
     - **capaz de ficar VERMELHA:** executa o caminho do bug e compara o sintoma exato que o usuário relatou. Fica VERMELHA neste bug e VERDE depois da correção;
     - **determinística:** o mesmo veredito a cada execução ou, em bug intermitente, uma taxa alta e estável;
     - **rápida:** segundos, não minutos;
     - **de um passo só:** o usuário roda uma `Sub`, ou compila o projeto, e cola a saída. Roteiro manual, só como último recurso.
   - Se você se pegar lendo o código para montar uma teoria antes de essa `Sub` existir, pare: pular direto para a hipótese é a falha que esta skill evita. Sem reprodução VERMELHA, não há fase 2.

2. **Reproduzir e minimizar.**
   - Confira, na saída que o usuário colou:
     - a falha é a que o usuário descreveu, não outra falha vizinha. Bug errado, correção errada;
     - a falha se repete em várias execuções ou, em bug intermitente, a uma taxa que permite depurar;
     - o sintoma exato está registrado (mensagem, valor errado, tempo), para as fases seguintes conferirem a correção contra ele.
   - Reduza a reprodução ao menor cenário que ainda fica VERMELHO. Corte entradas, linhas, colunas, chamadores e passos, um por vez, e mantenha só o que sustenta a falha.
   - Para poupar rodadas, teste vários cortes na mesma execução.
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
   - Cada sonda corresponde a uma previsão da fase 3. Sondas só leem valores, e várias cabem em uma execução; teste que muda entrada, estado ou código muda uma variável por vez.
   - Preferência de ferramenta:
     1. **Depurador.** Em erro de execução, o usuário clica em **Depurar**; em valor errado, ele põe um ponto de interrupção (F9) na linha que você indicar e roda a reprodução. Na parada, ele digita na Verificação Imediata as expressões que você escrever, todas em uma linha (`? "total=" & total, "linha=" & i`), e copia a saída. Peça as leituras sempre assim: a janela Variáveis Locais e os passos com F8 obrigariam o usuário a transcrever à mão. Um ponto de interrupção vale mais que dez sondas.
     2. **Sondas** nas fronteiras que distinguem as hipóteses: entrada e saída de cada etapa. Diga depois de qual linha cada sonda entra.
     3. Nunca "imprima tudo e procure": a Verificação Imediata guarda só as últimas 200 linhas, aproximadamente.
   - Toda sonda escreve a marca como texto literal, como em `Debug.Print "[DEBUG-a4f2] total=" & total`: a constante `MARCA` só existe dentro da reprodução, e a busca da fase 6 procura o texto. Sonda marcada sai com uma busca na limpeza; sonda sem marca fica no código.
   - **Erro escondido.** Se `On Error Resume Next` ou um tratador esconde a linha que falha, peça ao usuário que marque, no VBE, Ferramentas > Opções > Geral > **Interromper em todos os erros**, e anote a opção anterior para restaurá-la na fase 6. A opção vale para todo o VBE e interrompe também as linhas em que o código espera erro (E8). Quando a parada cair numa delas, peça a linha realçada e avise o usuário de que ela não é o bug.
   - **Hipótese sobre dados.** Número guardado como texto, espaço no fim, data como texto: confira no `.xlsx` anexado com o codeInterpreter ou imprima `TypeName(valor)` e `Len(valor)`.
   - **Lentidão.** Sonda de texto pouco ajuda. Meça primeiro: guarde `Timer` antes e depois de cada etapa (leitura, cálculo, escrita) e imprima os segundos de cada uma. Divida a etapa mais lenta e meça de novo. Corrija só depois de medir.

5. **Corrigir com teste de regressão.**
   - Escreva o teste de regressão antes da correção, mas só se houver um **ponto de teste correto**: um procedimento que o teste chama com entrada fixa e que exercita o padrão real do bug, como ele ocorre na chamada original.
   - Ponto raso dá confiança falsa: testar uma função isolada quando o bug exige a sequência leitura, cálculo e escrita, ou um evento de formulário.
   - Se não há ponto de teste correto, esse é o achado. Registre que a estrutura do código impede fixar o bug em um teste e relate isso na fase 6.
   - Se há:
     1. Transforme a reprodução minimizada em teste: a mesma `Sub`, com nome que diga o que ela testa e a marca `[TESTE]` no lugar de `[DEBUG-<id>]`, que a busca da fase 6 contaria como sonda.
     2. Na mesma mensagem do teste, leve a correção ao **Fluxo** das instruções do agente: invoque a skill `planejar-codigo` com a causa confirmada e inclua o plano e os pedidos dela. O usuário roda o teste e responde aos pedidos na mesma resposta.
     3. Confirme que o teste ficou VERMELHO no código atual. Se o VERMELHO veio de alterar código ou dados para forçá-lo, prove que a alteração está no que o usuário executou: peça o procedimento como está no VBE, ou os dados como estão, e compare-os com a versão anterior à alteração usando o `difflib` no codeInterpreter. A única diferença deve ser a alteração.
     4. Com a aprovação e o VERMELHO confirmado, escreva a correção. O teste entra em **Testes** da Saída.
     5. O usuário aplica a correção e roda o teste: VERDE.
     6. O usuário roda a reprodução da fase 1 no cenário original, não minimizado.

6. **Limpar.**
   - Antes de declarar o bug resolvido, confirme com o usuário cada item abaixo e cada item de `a desfazer` da linha de estado, um por linha:
     - a reprodução original fica VERDE (saída colada);
     - o teste de regressão passa, ou a falta de ponto de teste correto está registrada;
     - nenhuma sonda restou: a busca por `DEBUG-` no VBE (Ctrl+F, **Projeto atual**) não encontra nada;
     - os módulos temporários foram removidos, ou mantidos com nome que os identifique como teste;
     - o arquivo `%TEMP%\DEBUG-<id>.txt` foi apagado, se foi criado;
     - a opção de interceptação de erros voltou ao valor anterior, se foi alterada.
   - Declare em uma frase a hipótese que se confirmou, para o usuário registrar junto da alteração. Quem depurar depois aprende com ela.
   - Não declare resolvido um bug cuja reprodução o usuário não rodou depois da correção.

## Parameters

- Sintoma: mensagem de erro, resultado errado, travamento ou tempo de execução, descrito na conversa.
- Código do módulo ou do projeto, com o nome e o tipo de cada módulo, colado na conversa ou anexado em `.txt`.
- Opcionais: dados que disparam o bug (`.xlsx` ou `.csv`), versão anterior que funcionava e prints.

## Output

- Em cada rodada: a linha de estado, o código de diagnóstico em bloco `vba` e o pedido no formato **Execute** e **Cole de volta**.
- Na fase 3: de 3 a 5 hipóteses ordenadas, cada uma com a previsão que a falseia, e a sonda da primeira.
- Na fase 5: o teste de regressão e o plano da skill `planejar-codigo`; após a aprovação, a correção conforme a **Saída** das instruções do agente, com o teste em **Testes**.
- Na fase 6: a lista de conferência e a frase com a hipótese confirmada.
