---
name: code-review
description: Revisa a última alteração de código VBA que o agente entregou, ou o código que o usuário enviar, em dois eixos relatados em separado. O eixo Padrões confere as Regras do agente e uma base de code smells de Fowler. O eixo Especificação confere se o código faz o que o pedido e o plano aprovado pediram. Use quando o usuário pedir uma revisão de código, quiser conferir a última alteração antes de colar no projeto ou disser 'revise', 'code review', 'revise o que você fez' ou 'confira a última alteração'.
---

## Purpose

Revisar uma alteração de código VBA em dois eixos, relatados em separado:

- **Padrões:** o código segue as **Regras** das instruções do agente?
- **Especificação:** o código faz o que o usuário pediu e aprovou?

## Uses

- Agent capabilities: codeInterpreter

## Instructions

Um projeto VBA não tem Git. A **alteração** é a diferença entre duas versões do código: o **antes** e o **depois**. O ponto de referência é a última modificação que você fez: o **depois** é o código da sua última entrega e o **antes** é o código como estava até ela.

Os dois eixos ficam separados porque uma alteração pode passar em um e falhar no outro: código que segue todas as Regras e implementa a coisa errada, ou código que faz o que foi pedido e quebra as Regras. Relatar em separado impede que um eixo esconda o outro.

Você não acessa o projeto do usuário. Revise o código que está na conversa e nos arquivos anexados, lidos com o codeInterpreter.

1. **Fixar a alteração.**
   - Localize a sua última entrega de código nesta conversa. Os módulos entregues são o **depois**.
   - O **antes** de cada módulo é a versão anterior dele na conversa: enviada pelo usuário ou entregue por você em resposta anterior. Módulo criado na entrega não tem antes: ele inteiro é a alteração.
   - Se o módulo já existia e a versão anterior não está na conversa, peça ao usuário que a cole ou anexe em `.txt` e aguarde.
   - Se não há entrega sua na conversa, o **depois** é o código que o usuário enviou para revisão. Se ele enviar também a versão anterior, use-a como **antes**; senão, revise o código inteiro.
   - Liste os módulos e os procedimentos criados, alterados e removidos. Se antes e depois forem iguais, diga isso e encerre: a falha aparece aqui, não no meio da revisão.
   - Julgue só o que a alteração criou ou mudou. Código que já existia fica fora da revisão.

2. **Identificar a especificação.**
   - A especificação é o que o usuário pediu e aprovou para essa alteração. Reúna, da conversa:
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
     - **Mysterious Name:** procedimento, variável, constante ou tipo cujo nome não revela o que faz ou guarda. → Renomeie; se nenhum nome honesto aparecer, o desenho está confuso.
     - **Duplicated Code:** a mesma lógica aparece em mais de um trecho ou módulo da alteração. → Extraia a lógica para uma rotina e chame-a dos dois lugares.
     - **Feature Envy:** procedimento que usa mais os dados de outro módulo ou classe do que os do seu. → Mova o procedimento para junto dos dados que ele usa.
     - **Data Clumps:** os mesmos campos ou parâmetros andam sempre juntos. → Agrupe-os em um `Type` ou em uma classe e passe o grupo.
     - **Primitive Obsession:** `String` ou número fazendo o papel de um conceito do domínio que merece tipo próprio. → Dê ao conceito um `Enum`, um `Type` ou uma classe.
     - **Repeated Switches:** o mesmo `Select Case` ou a mesma cascata de `If...ElseIf` sobre o mesmo valor se repete na alteração. → Concentre a escolha em uma função ou em um `Scripting.Dictionary` que os trechos compartilham, ou use classes com `Implements`.
     - **Shotgun Surgery:** uma mudança lógica exige edições espalhadas por muitos módulos. → Reúna em um módulo o que muda junto.
     - **Divergent Change:** um módulo é editado por vários motivos sem relação entre si. → Divida-o para que cada módulo mude por um motivo.
     - **Speculative Generality:** abstração, parâmetro `Optional` ou ponto de extensão criado para uma necessidade que a especificação não tem. → Remova; volte ao código direto até a necessidade aparecer.
     - **Message Chains:** cadeia longa `a.b.c.d` de que o chamador não deveria depender. → Esconda o percurso em uma função ou guarde o objeto em variável com `Set`.
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

     Violação de Regra pode ser definitiva; smell é sempre julgamento. Até 400 palavras.

   - **Passada Especificação.** Relate:
     - requisito da especificação que falta ou está parcial;
     - comportamento da alteração que ninguém pediu (escopo a mais). O que uma Regra exige mesmo sem pedido não é escopo a mais;
     - requisito que parece implementado, mas com implementação que parece errada.

     Cite a frase da especificação em cada achado. Até 400 palavras.

5. **Relatar.**
   - Use este formato:

   ```text
   **Alteração revisada:** <módulos e procedimentos criados, alterados e removidos>

   ## Padrões

   <achados da passada Padrões>

   ## Especificação

   <achados da passada Especificação, ou `sem especificação`>

   **Resumo:** Padrões: <total> achados; pior: <achado>. Especificação: <total> achados; pior: <achado>.
   ```

   - Não junte nem reordene achados entre os eixos.
   - No resumo, dê o total de achados de cada eixo e o pior achado dentro de cada eixo. Não eleja um pior entre os dois eixos: isso desfaz a separação.
   - Eixo sem achados: escreva `nenhum achado`.
   - Esta skill não altera código. Para corrigir um achado, retome o **Fluxo** das instruções do agente: plano, aprovação e só então código.

## Parameters

- Alteração a revisar. Por padrão, a última entrega de código do agente na conversa.
- Opcionais, colados na conversa ou anexados em `.txt`: código a revisar, versão anterior dos módulos e especificação.
