---
name: code-review
description: Revisa a última alteração de código VBA que o agente entregou, ou o código que o usuário enviar, em dois eixos relatados em separado. O eixo Padrões confere as Regras do agente e uma base de code smells de Fowler. O eixo Especificação confere se o código faz o que o pedido e o plano aprovado pediram. Gera também um pacote para revisão independente em conversa nova. Use quando o usuário pedir uma revisão de código ou uma revisão independente, quiser conferir a última alteração antes de colar no projeto ou disser 'revise', 'code review', 'revise o que você fez' ou 'confira a última alteração'.
---

## Purpose

Revisar uma alteração de código VBA em dois eixos, relatados em separado:

- **Padrões:** o código segue as **Regras** das instruções do agente?
- **Especificação:** o código faz o que o usuário pediu e aprovou?

## Uses

- Agent capabilities: codeInterpreter

## Instructions

Um projeto VBA não tem Git. A **alteração** é a diferença entre duas versões do código: o **antes** e o **depois**. O usuário escolhe o que revisar e contra qual versão. Sem escolha dele, o **depois** é o código da sua última entrega e o **antes** é o código como estava até ela.

Os dois eixos ficam separados porque uma alteração pode passar em um e falhar no outro: código que segue todas as Regras e implementa a coisa errada, ou código que faz o que foi pedido e quebra as Regras. Relatar em separado impede que um eixo esconda o outro.

Você não acessa o projeto do usuário. Revise o código que está na conversa e nos arquivos anexados, lidos com o codeInterpreter.

1. **Fixar a alteração.**
   - Se o usuário anexar um pacote de revisão (passo 6), o antes, o depois e a especificação vêm do pacote.
   - O **depois** é o código que o usuário enviou para revisão, colado ou anexado em `.txt`. Sem código enviado, o depois são os módulos da sua última **entrega**. Se o usuário nomear módulos ou procedimentos, revise só esses.
   - A **entrega** é o código do item 1 da **Saída** das instruções do agente. Os testes do item 2, como o teste de equivalência da skill `code-simplifier`, e o código de diagnóstico da skill `diagnosing-bugs` ficam fora da entrega.
   - O **antes** de cada módulo é a versão que o usuário indicar, como "desde o código que eu enviei". Sem indicação, é a versão anterior do módulo na conversa, enviada pelo usuário ou entregue por você.
   - Sem antes, o módulo inteiro é a alteração: vale para o módulo criado na entrega e para o código que o usuário enviou sem versão anterior. Se a sua entrega alterou um módulo cuja versão anterior não está na conversa, peça ao usuário que a cole ou anexe em `.txt` e aguarde.
   - Com o codeInterpreter, gere o diff de cada módulo que tem antes, com o `difflib` do Python. Leia direto o arquivo anexado; copie caractere por caractere para o Python o código que está só na conversa. A alteração é o que o diff mostra.
   - Liste os módulos e os procedimentos criados, alterados e removidos, a partir do diff ou, sem antes, do módulo inteiro. Se o diff vier vazio em todos os módulos, diga isso e encerre: a falha aparece aqui, não no meio da revisão.
   - Liste também as mudanças de **interface**: módulo, procedimento público ou procedimento de evento (`Workbook_Open`, `Worksheet_Change`, `<Controle>_Click`) renomeado ou removido, e procedimento público com parâmetros em outra quantidade, ordem ou tipo. Botões, formas, faixa de opções, `Application.Run`, `Application.OnTime` e fórmulas chamam procedimentos pelo nome, e o Excel liga cada evento pelo nome do procedimento: a mudança quebra o chamador sem erro de compilação. Relate essa lista no cabeçalho do relatório, fora dos dois eixos.
   - Julgue só o que a alteração criou ou mudou. Código que já existia fica fora da revisão.

2. **Identificar a especificação.**
   - A especificação é o que o usuário pediu e aprovou para essa alteração. Reúna, da conversa ou do pacote de revisão:
     1. o pedido do usuário que originou a alteração;
     2. o plano aprovado no **Fluxo** das instruções do agente, com os ajustes que o usuário fez ao aprovar;
     3. as decisões confirmadas ao fim da skill `grill-me`, se ela foi usada;
     4. um texto de especificação colado ou anexado pelo usuário.
   - Se duas fontes divergirem, vale a mais recente que o usuário aprovou. Requisito do pedido que o plano omitiu sem o usuário concordar continua valendo.
   - Se não houver nenhuma fonte, não pergunte. Pule o eixo Especificação, relate `sem especificação` e diga que o usuário habilita o eixo enviando o que o código deveria fazer.

3. **Identificar os padrões.**
   - Os padrões documentados são as **Regras** das instruções do agente. Cite cada uma pelo ID (`E2`, `D1`).
   - Some a elas a **base de smells** abaixo: um conjunto fixo de code smells de Fowler (_Refactoring_, cap. 3). Duas condições valem para a base:
     - **As Regras prevalecem.** Onde uma Regra exige ou aceita o que a base apontaria, não relate o smell. Onde uma Regra já cobre o caso, relate a violação da Regra, não o smell.
     - **Smell é sempre julgamento.** Relate-o como hipótese rotulada (`possível Feature Envy`), nunca como violação.
   - Cada smell traz _o que é_ → _como corrigir_. Compare cada um com a alteração:
     - **Mysterious Name** (relate como N1): procedimento, variável, constante ou tipo cujo nome não revela o que faz ou guarda. → Renomeie; se nenhum nome honesto aparecer, o desenho está confuso.
     - **Duplicated Code:** a mesma lógica aparece em mais de um trecho ou módulo da alteração. → Extraia a lógica para uma rotina e chame-a dos dois lugares.
     - **Feature Envy:** procedimento que usa mais os dados de outro módulo ou classe do que os do seu. → Mova o procedimento para junto dos dados que ele usa.
     - **Data Clumps:** os mesmos campos ou parâmetros andam sempre juntos. → Agrupe-os em um `Type` ou em uma classe e passe o grupo. Grupo que entra em `Collection`, `Dictionary` ou `Variant` pede classe: nesses usos, `Type` de módulo comum dá erro de compilação.
     - **Primitive Obsession:** `String` ou número fazendo o papel de um conceito do domínio que merece tipo próprio. → Dê ao conceito um `Enum`, um `Type` ou uma classe.
     - **Repeated Switches:** o mesmo `Select Case` ou a mesma cascata de `If...ElseIf` sobre o mesmo valor se repete na alteração. → Concentre a escolha em uma função ou em um `Scripting.Dictionary` que os trechos compartilham, ou use classes com `Implements`.
     - **Shotgun Surgery:** uma mudança lógica exige edições espalhadas por muitos módulos. → Reúna em um módulo o que muda junto.
     - **Divergent Change:** um módulo é editado por vários motivos sem relação entre si. → Divida-o para que cada módulo mude por um motivo.
     - **Speculative Generality** (relate como A10): abstração, parâmetro `Optional` ou ponto de extensão criado para uma necessidade que a especificação não tem. → Remova; volte ao código direto até a necessidade aparecer.
     - **Message Chains:** cadeia longa `a.b.c.d` pelos objetos e classes do projeto, de que o chamador não deveria depender. A navegação no modelo de objetos do Excel, como `wb.Worksheets(ABA).ListObjects(TABELA).DataBodyRange`, é o uso normal, e D2 cobre a repetição. → Esconda o percurso em uma função ou guarde o objeto em variável com `Set`.
     - **Middle Man:** classe ou procedimento que quase só repassa a chamada adiante. → Remova-o e chame o alvo direto.
     - **Refused Bequest:** classe com `Implements` que deixa vazia a maioria dos membros da interface. → Divida a interface ou troque-a por composição.
   - Sem versão anterior, pule Shotgun Surgery e Divergent Change: os dois dependem de saber o que mudou.

4. **Revisar em duas passadas separadas.**
   - Faça uma passada por eixo, nesta ordem: Padrões, depois Especificação. Termine de redigir uma antes de começar a outra.
   - Em cada passada, releia a alteração do início. Julgue o que está escrito, não o que você pretendia escrever.
   - Um achado de um eixo não justifica, agrava nem descarta um achado do outro.
   - **Passada Padrões.** Relate, por módulo e procedimento:
     - cada ponto em que a alteração viola uma Regra: cite o ID e transcreva a linha;
     - cada smell da base: nomeie-o e transcreva o trecho.

     Violação de Regra pode ser definitiva; smell é sempre julgamento.

   - **Passada Especificação.** Relate:
     - requisito da especificação que falta ou está parcial;
     - comportamento da alteração que ninguém pediu (escopo a mais). O que uma Regra exige mesmo sem pedido não é escopo a mais;
     - requisito que parece implementado, mas com implementação que parece errada.

     Cite a frase da especificação em cada achado.

5. **Relatar.**
   - Confira com o codeInterpreter que cada linha transcrita está no depois. Corrija a transcrição que divergir e descarte o achado cuja linha não existe.
   - Na linha transcrita com senha, token, string de conexão ou outra credencial, troque o valor por `<OCULTO>`.
   - Numere os achados dos dois eixos em uma sequência única, para o usuário pedir correções pelo número. O número só identifica o achado.
   - Use este formato:

   ```text
   **Alteração revisada:** <módulos e procedimentos criados, alterados e removidos>

   **Comparação:** <origem do antes e do depois de cada módulo>

   **Interface alterada:** <mudanças de interface do passo 1, `nenhuma` ou `sem versão anterior`>

   ## Padrões

   <achados numerados da passada Padrões>

   ## Especificação

   <achados da passada Especificação, numerados em sequência aos de Padrões, ou `sem especificação`>

   **Resumo:** Padrões: <total> achados; pior: <número e achado>. Especificação: <total> achados; pior: <número e achado>.
   ```

   - Em **Comparação**, diga de onde veio cada versão, como `antes: código que você enviou; depois: minha última entrega`. Assim o usuário percebe um antes errado.
   - Não junte nem reordene achados entre os eixos.
   - No resumo, dê o total de achados de cada eixo e o pior achado dentro de cada eixo. Não eleja um pior entre os dois eixos: isso desfaz a separação.
   - Eixo sem achados: escreva `nenhum achado`.
   - Se o depois é uma entrega sua, termine com a linha `Para revisar sem o contexto desta conversa, peça uma revisão independente.`
   - Esta skill não altera código. Para corrigir os achados que o usuário indicar pelo número, retome o **Fluxo** das instruções do agente: plano, aprovação e só então código.

6. **Gerar o pacote de revisão.**
   - Nesta conversa, você revisa o código que escreveu, com o raciocínio do plano à vista. Uma conversa nova com este agente começa sem esse raciocínio e julga só o que está escrito: é a **revisão independente**.
   - Gere o pacote quando o usuário pedir uma revisão independente. Se ele pedir antes de qualquer relatório, faça os passos 1 e 2 e venha direto para este passo.
   - Com o codeInterpreter, grave `pacote-revisao.txt` em UTF-8. O pacote volta para o Copilot, que aceita TXT em UTF-8, e não para o VBE: A5 não vale para ele.
   - Copie cada texto literalmente, inclusive o pedido e o plano: um resumo seu reescreveria o pedido conforme o que você construiu. Troque credenciais por `<OCULTO>`, como no passo 5.
   - Use esta estrutura, com um par de blocos ANTES e DEPOIS para cada módulo:

   ```text
   PACOTE DE REVISÃO (skill code-review)

   === ESPECIFICAÇÃO ===
   <cada fonte da especificação do passo 2, com o seu título; ou "sem especificação">

   === MÓDULO <Nome>: ANTES (<origem>) ===
   <código, ou "(módulo novo)">

   === MÓDULO <Nome>: DEPOIS (<origem>) ===
   <código>
   ```

   - Diga ao usuário: baixe o arquivo agora, porque o link vale só durante esta sessão; abra uma conversa nova com este agente; anexe o arquivo e peça a revisão.

## Parameters

- Alteração a revisar e versão de comparação, se o usuário as indicar. Por padrão, a última entrega de código do agente na conversa, comparada com a versão anterior de cada módulo.
- Opcionais, colados na conversa ou anexados em `.txt`: código a revisar, versão anterior dos módulos e especificação.
- Para a revisão independente, em conversa nova: `pacote-revisao.txt` anexado.

## Output

- Relatório no formato do passo 5: alteração revisada, comparação, interface alterada, achados numerados do eixo Padrões, achados do eixo Especificação ou `sem especificação`, e resumo com o total e o pior achado de cada eixo.
- A pedido, `pacote-revisao.txt` para download, com as instruções do passo 6 para a revisão independente.
