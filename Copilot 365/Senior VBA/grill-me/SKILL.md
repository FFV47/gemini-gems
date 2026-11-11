---
name: grill-me
description: Entrevista o usuário em rodadas de perguntas numeradas, cada uma com uma resposta recomendada, até resolver todas as decisões de um plano, de uma escolha ou de uma ideia. Use quando o usuário quiser pôr um plano à prova antes de implementar, pedir para ser questionado sobre o desenho de uma solução ou disser 'grill me', 'me sabatine', 'me questione' ou 'me entreviste'.
---

## Purpose

Entrevistar o usuário sem trégua, em rodadas de perguntas com resposta recomendada, até os dois terem o mesmo entendimento do assunto: o plano, a escolha ou a ideia que ele trouxe.

## Uses

- Agent capabilities: codeInterpreter

## Instructions

Trate o assunto como uma **árvore de decisões**: cada decisão abre as decisões que dependem dela. Uma **rodada** é uma mensagem sua com perguntas e a resposta do usuário a ela. A **fronteira** são as decisões cujos pré-requisitos já estão resolvidos: as perguntas que você pode fazer agora sem supor uma resposta que ainda não ouviu.

1. **Montar a árvore de decisões.**
   - Extraia do que o usuário descreveu as decisões que o assunto exige.
   - Registre qual decisão depende de qual.

2. **Separar fatos de decisões.**
   - Decisões são do usuário. Apresente cada uma e aguarde a resposta. Não decida por ele.
   - Fatos são trabalho seu. Antes de perguntar um fato, procure-o na conversa, nos arquivos anexados, lidos com o codeInterpreter, e no seu conhecimento de Excel e VBA. Não pergunte o que você consegue encontrar.
   - Alguns fatos só o usuário tem. Você não acessa os arquivos nem o computador dele. Nomes reais de pastas, arquivos, planilhas, tabelas, colunas e intervalos, o volume de dados e quem usa a solução vêm do usuário.
   - Não invente um nome para destravar uma pergunta.

3. **Calcular a fronteira.**
   - Inclua toda decisão cujos pré-requisitos já estão resolvidos.
   - Uma pergunta cuja resposta depende de outra ainda aberta nesta rodada pertence a uma rodada posterior.
   - Um fato pendente bloqueia só as perguntas que dependem dele. As demais continuam na fronteira.

4. **Perguntar a fronteira inteira em uma única mensagem.**
   - Numere cada pergunta e dê a sua resposta recomendada.
   - Redija cada pergunta de modo que "sim" aceite a resposta recomendada.
   - Peça os fatos que só o usuário tem depois das perguntas, numerados `F1`, `F2`, sem resposta recomendada. Aceite-os colados na conversa ou em arquivo anexado.
   - Use este formato:

   ```text
   ❓ **P1** - **<título da pergunta>**: <corpo da pergunta; pode ter vários parágrafos e alternativas>

   ➡️ <sua resposta recomendada>

   ---

   ❓ **P2** - **<título da pergunta>**: <corpo da pergunta>

   ➡️ <sua resposta recomendada>

   ---

   📎 **F1** - <fato que só o usuário tem>
   ```

5. **Aguardar e atualizar a árvore.**
   - Encerre a mensagem e aguarde as respostas.
   - Cada decisão resolvida avança a fronteira e libera as perguntas que dependiam dela.
   - Volte ao passo 3 enquanto a fronteira tiver perguntas.

6. **Encerrar quando a fronteira ficar vazia.**
   - A entrevista termina com todos os ramos da árvore visitados e nada assumido em silêncio.
   - Liste as decisões tomadas, uma por linha.
   - Pergunte se a lista é o entendimento de vocês dois.
   - Aja só depois da confirmação. Se o resultado for código, retome o **Fluxo** das instruções do agente sem repetir o que já foi respondido. Esta skill não escreve código.

## Parameters

- Plano, escolha ou ideia que o usuário quer pôr à prova, descrito na conversa.
- Arquivos opcionais anexados pelo usuário: código exportado, pasta de trabalho ou prints.
