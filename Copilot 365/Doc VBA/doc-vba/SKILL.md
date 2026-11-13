---
name: doc-vba
description: Invoque quando o usuário fornecer o código completo de um projeto VBA e quiser criar, em duas etapas, um mapa técnico para o autor e um manual Word voltado a usuários sem conhecimento de programação.
---

## Purpose

Analisar um projeto VBA a partir do código e de materiais visuais opcionais, conduzir a validação com o autor e produzir documentação clara para dois públicos: usuários finais e responsáveis pela manutenção que ainda não conhecem o código.

## Uses

- Agent capabilities: codeInterpreter

## Instructions

1. **Reunir as entradas.**
   - Leia o arquivo `.txt` anexado com todo o código do projeto, incluindo módulos, classes, formulários e eventos.
   - Considere prints anexados de formulários, abas, botões e mensagens.
   - Extraia da mensagem do usuário os dados do projeto, público, finalidade, responsáveis e contexto operacional.
   - Marque dados ausentes como `[CONFIRMAR]`; não invente valores.
   - Nunca reproduza senhas, tokens, strings de conexão ou credenciais. Informe apenas que o recurso é protegido quando isso for relevante.

2. **Mapear a experiência de uso.**
   - Identifique pontos de entrada: procedimentos públicos sem argumentos, eventos ao abrir, salvar, fechar ou alterar, botões de formulários, comandos da faixa de opções, atalhos e agendamentos.
   - Registre interações visíveis: mensagens, pedidos de entrada, barra de status, rótulos definidos no código e janelas de escolha de arquivo ou pasta.
   - Copie mensagens visíveis exatamente, substituindo somente trechos dinâmicos por descrições entre colchetes.
   - Levante pré-requisitos, validações, formatos aceitos, dependências da tela ou seleção atual, saídas, arquivos criados ou sobrescritos, PDFs, impressões, novas abas e integrações externas.
   - Para e-mails, diferencie envio automático de abertura para revisão.
   - Identifique ações sem volta, falhas tratadas, falhas silenciosas, configurações que podem permanecer alteradas após erro e trechos potencialmente demorados.

3. **Mapear a arquitetura e a manutenção do código.**
   - Catalogue módulos, classes, formulários, planilhas e `ThisWorkbook`, informando a responsabilidade de cada componente.
   - Para cada rotina relevante, registre: finalidade, gatilho ou chamador, parâmetros, retorno, variáveis globais usadas, objetos alterados, arquivos ou sistemas acessados, efeitos colaterais e rotinas chamadas.
   - Construa um fluxo de chamadas legível, mostrando os principais caminhos desde a ação do usuário ou evento até a saída final.
   - Explique regras de negócio, constantes, nomes definidos, intervalos, tabelas, planilhas ocultas, referências de biblioteca e dependências externas.
   - Destaque pontos frágeis: caminhos fixos, referências por índice, `On Error Resume Next`, variáveis sem declaração, código duplicado, dependências implícitas, credenciais e riscos de alteração.
   - Inclua orientações práticas para manutenção: onde alterar cada comportamento, como testar com segurança, como fazer backup, como validar regressões e como reverter uma mudança.
   - Explique o VBA em linguagem acessível a um novo funcionário, preservando os nomes reais de módulos, rotinas, planilhas e controles para facilitar a localização no editor.
   - Não afirme relações que o código não prove; marque incertezas como `[CONFIRMAR]`.

4. **Entregar somente a Etapa 1 e aguardar.**
   - Apresente: resumo da ferramenta; tabela `Como o usuário aciona | O que acontece | Rotina no código`; inventário técnico `Componente | Responsabilidade | Dependências`; principais fluxos de chamada; perguntas pendentes.
   - Peça ao autor para confirmar ou corrigir as pendências antes de gerar os documentos finais.
   - Se o autor pedir para seguir sem responder, mantenha todas as lacunas como `[CONFIRMAR]`.

5. **Gerar a documentação final.**
   - Produza um documento Word com duas partes claramente separadas: `Manual do usuário` e `Guia técnico de manutenção`.
   - No manual do usuário, inclua visão geral, pré-requisitos, tarefas passo a passo, mensagens, cuidados, solução de problemas e pendências.
   - No guia técnico, inclua visão arquitetural, inventário de componentes, fluxo de execução, catálogo das rotinas principais, regras de negócio, dependências, pontos de configuração, riscos conhecidos, procedimento seguro de alteração, testes recomendados e glossário VBA.
   - Use títulos, listas, tabelas e diagramas textuais simples para consulta rápida.
   - A documentação deve ser bela, com tipografia e layout limpos e legíveis, já que o usuário voltará a ela mais tarde para revisar. Pense em Tufte.
   - Gere o arquivo `.docx` usando o codeInterpreter e forneça um link para download.
   - Fonte do texto deve ser Arial. Para os textos, tabelas e diagramas o tamanho mínimo é 12. Os títulos devem ser maiores que 12 para manter a hieraquia visual.
   - Não utilize cabeçalhos e rodapés.

6. **Validar antes de concluir.**
   - Confirme que cada componente relevante do projeto aparece no inventário.
   - Confirme que cada rotina pública ou acionável está ligada a um gatilho ou marcada como não localizada.
   - Confirme que riscos, dependências externas e ações sem volta estão destacados.
   - Confirme que termos técnicos são explicados para alguém sem experiência prévia no projeto.
   - Confirme que nenhuma credencial foi exposta.

## Parameters

- Código completo do projeto VBA, preferencialmente em `.txt`.
- Prints opcionais de formulários, abas, botões e mensagens.

## Output

- Etapa 1: resumo da ferramenta, as tabelas e os fluxos de chamada do passo 4 e as perguntas pendentes, seguidos do pedido de confirmação ao autor.
- Etapa 2: link para download do `.docx` com as partes `Manual do usuário` e `Guia técnico de manutenção`.
