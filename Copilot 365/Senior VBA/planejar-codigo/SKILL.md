---
name: planejar-codigo
description: Planeja a criação ou a alteração de código VBA antes de qualquer código. Coleta os nomes reais de pastas, arquivos, planilhas, tabelas, colunas e intervalos, avalia se Power Query, fórmula ou tabela dinâmica resolve melhor e apresenta o plano, com passos, entradas, saídas, alterações e riscos, para aprovação explícita do usuário. Use sempre que o usuário pedir para criar ou alterar código VBA e quando outra skill devolver uma correção ou uma implementação ao Fluxo.
---

## Purpose

Planejar uma criação ou alteração de código VBA e obter a aprovação explícita do usuário antes de escrever o código. Esta skill é o passo **Planejar** do **Fluxo** das instruções do agente.

## Uses

- Agent capabilities: codeInterpreter

## Instructions

1. **Coletar:** peça os nomes reais ainda não informados de pastas, arquivos, planilhas, tabelas, colunas e intervalos e, para módulo completo, os dados de C2. Pergunte o volume quando ele mudar a estratégia. Use só nomes dados pelo usuário. Se houver mais de uma leitura, apresente-as. Com os nomes que o código usa, siga.
2. **Alternativa:** se Power Query, fórmula ou tabela dinâmica resolver melhor, diga em uma linha. Se escolhida, explique-a e encerre; senão, siga.
3. **Plano:** liste passos, entradas, saídas, alterações e riscos, destacando o destrutivo. **Escreva código só após aprovação explícita.**

Com a aprovação, siga para o passo **Código** do Fluxo.

## Parameters

- Pedido de criação ou alteração de código, descrito na conversa.
- Opcionais: código existente, colado ou anexado em `.txt`, e arquivos que mostrem os nomes reais.

## Output

- Plano com passos, entradas, saídas, alterações e riscos, com o destrutivo em destaque, seguido do pedido de aprovação explícita.
