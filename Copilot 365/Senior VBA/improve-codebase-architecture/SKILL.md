---
name: improve-codebase-architecture
description: Procura na arquitetura de um projeto VBA oportunidades de aprofundamento, refatorações que trocam módulos e procedimentos rasos por módulos profundos, de interface pequena, mais fáceis de testar e de percorrer. Entrega um relatório HTML para download, com diagramas antes e depois de cada candidata, e entrevista o usuário sobre a candidata que ele escolher. Não implementa a refatoração. Use quando o usuário pedir para melhorar a arquitetura de um projeto, quiser saber onde o código está difícil de testar ou de alterar, ou disser 'arquitetura', 'aprofunde os módulos' ou 'improve codebase architecture'.
---

## Purpose

Encontrar atrito na arquitetura de um projeto VBA e propor **aprofundamentos**: refatorações que transformam módulos rasos em profundos. O objetivo é código que se testa pela interface e que pessoas e IA percorrem sem saltar de módulo em módulo.

## Uses

- Agent capabilities: codeInterpreter

## Instructions

Você não acessa o projeto do usuário nem executa VBA. O código chega colado na conversa ou anexado em `.txt`; leia os anexos com o codeInterpreter. Esta skill analisa e entrevista; a refatoração sai depois, pelo **Fluxo** das instruções do agente.

**Vocabulário.** Use estes termos, sempre com o mesmo sentido, em cada candidata, no relatório e na entrevista. Termo fixo deixa as candidatas comparáveis.

- **Módulo:** o módulo do VBA, seja padrão, de classe, de formulário, de planilha ou `ThisWorkbook`. Os termos abaixo valem também para um procedimento e para um grupo de módulos: nomeie a escala, como em "o procedimento `X`" ou "o módulo `Y`". Evite: componente, serviço, camada.
- **Interface:** tudo o que o chamador precisa saber para usar o módulo corretamente: nome e parâmetros dos procedimentos `Public`, o que eles leem e gravam em planilhas e arquivos, as variáveis `Public`, a ordem de chamada exigida, os erros que levantam, a configuração de que dependem (nome de planilha, intervalo nomeado, referência de biblioteca) e o custo de desempenho. Vai além da classe-interface de `Implements` e não tem relação com o módulo `Interface` de O2. Evite: API, assinatura.
- **Implementação:** o código dentro do módulo.
- **Profundidade:** alavancagem na interface, ou seja, quanto comportamento o chamador, ou o teste, exercita por unidade de interface que precisa aprender. O módulo é **profundo** quando muito comportamento fica atrás de uma interface pequena, e **raso** quando a interface é quase tão complexa quanto a implementação. Meça pela alavancagem, nunca pela razão entre linhas da implementação e da interface, que premia código inchado.
- **Costura** (_seam_, de Michael Feathers): lugar onde o comportamento muda sem editar ali; é onde fica a interface de um módulo. Onde pôr a costura é uma decisão separada do que fica atrás dela. Em VBA, a costura costuma ser um parâmetro que recebe os dados ou o objeto em vez de buscá-los, ou uma classe-interface usada com `Implements`. Evite: fronteira.
- **Adaptador:** o elemento concreto que ocupa uma costura e satisfaz a interface; em VBA, em geral, uma classe com `Implements`. O termo nomeia o papel, não o conteúdo.
- **Alavancagem:** o que o chamador ganha com a profundidade: mais capacidade por unidade de interface aprendida. Uma implementação serve N chamadores e M testes.
- **Localidade:** o que o mantenedor ganha com a profundidade: mudança, bugs, conhecimento e verificação concentrados em um lugar. Corrigiu uma vez, corrigiu em todo lugar.

**Princípios.**

- A profundidade é da interface, não da implementação. Um módulo profundo pode ser feito, por dentro, de procedimentos `Private` pequenos, cada um com uma responsabilidade (A8); eles só ficam fora da interface.
- **Teste da exclusão:** imagine apagar o módulo. Se a complexidade some, ele só repassava. Se ela reaparece espalhada pelos chamadores, ele se pagava.
- **A interface é a superfície de teste:** chamador e teste cruzam a mesma costura. Teste que precisa passar por baixo da interface indica módulo com formato errado.
- **Um adaptador, costura hipotética; dois adaptadores, costura real.** Crie costura só onde algo varia através dela, em geral produção e teste (A10).
- **Testável em VBA:** o procedimento recebe as dependências (planilha, array, objeto) em vez de buscá-las ou criá-las; o cálculo devolve o resultado e deixa `Range`, `MsgBox` e arquivos nas pontas (A9); interface pequena pede menos testes e preparação mais simples.
- **Testes: substituir, não empilhar.** Os testes na interface do módulo aprofundado substituem os testes dos módulos rasos que ele absorve. O teste confere o resultado observável pela interface, não o estado interno, e sobrevive a refatorações internas: teste que muda junto com a implementação está testando por baixo da interface.

**Categorias de dependência.** A categoria decide como o módulo aprofundado se testa pela costura.

- **Em processo:** cálculo sobre arrays, `Scripting.Dictionary`, `Type` e classes em memória, sem `Range`, arquivo ou rede. Sempre aprofundável: junte os módulos e teste pela nova interface com entradas fixas.
- **Substituível localmente:** a dependência tem um substituto local que roda no teste, como uma planilha criada pela própria `Sub` de teste numa cópia da pasta de trabalho, uma pasta temporária ou um `.csv` no lugar da base. A costura fica interna, sem porta na interface.
- **Portas e adaptadores:** dependência remota que o time mantém, como uma base Access ou SQL Server lida por ADODB ou uma pasta de trabalho na rede. Defina uma porta na costura, uma classe-interface com `Implements`. O módulo profundo guarda a lógica e recebe o transporte como adaptador: ADODB em produção, adaptador em memória no teste.
- **Simulação:** dependência externa que o time não controla, como o Outlook ou um serviço web de terceiros. O módulo aprofundado recebe a dependência como porta, e o teste usa um adaptador de simulação, que registra as chamadas em vez de executá-las.

1. **Reunir o código e delimitar a busca.**
   - Peça o código do projeto, colado ou anexado em `.txt`, com o nome de cada módulo. Inclua módulos de classe, formulários, módulos de planilha e `ThisWorkbook`: a lógica dos eventos faz parte da arquitetura.
   - **Delimite antes de varrer (YAGNI).** Aprofundar um módulo compensa ao facilitar as próximas mudanças nele; por isso, pese mais o que mudou nos últimos meses e o que vai mudar em seguida. Se o usuário indicou uma direção (um módulo, um processo, uma dor), siga-a. Senão, pergunte, junto do pedido de código, quais módulos ele mais alterou nos últimos meses ou vai alterar em seguida. O projeto VBA não tem histórico de commits: complete com a data `Última alteração` do cabeçalho C1 e com os módulos alterados nesta conversa. Sem ponto quente claro, amplie para o projeto inteiro.
   - Se o código trouxer o módulo `Decisoes`, leia-o primeiro: ele registra decisões que esta skill não reabre sem motivo novo. As **Regras** das instruções do agente pesam como decisões registradas: toda candidata as cumpre.
   - Troque por `<OCULTO>` toda senha, string de conexão ou token que o código trouxer, em tudo o que você produzir.
   - O passo termina com o código da área em mãos e os pontos quentes definidos, ou com a decisão de varrer o projeto inteiro.

2. **Explorar.**
   - Se o código veio anexado, monte primeiro, com o codeInterpreter, o mapa do projeto: por módulo, os procedimentos com escopo, parâmetros e número de linhas, as variáveis `Public` e quem chama quem.
   - Percorra o código a partir dos pontos quentes, livremente, e anote onde você sente **atrito**:
     - entender um conceito exige saltar entre muitos módulos ou procedimentos pequenos;
     - módulo ou procedimento **raso**: só repassa a chamada, liga e desliga comportamento por parâmetro `Optional` ou expõe vários procedimentos `Public` que o chamador precisa chamar na ordem certa;
     - funções puras extraídas só para testar, com os bugs em como elas são chamadas, sem **localidade**;
     - módulos acoplados que vazam pela costura: variável `Public` gravada por vários módulos, vários módulos que conhecem o layout da mesma planilha, evento ou formulário que altera outra planilha direto;
     - código sem teste ou difícil de testar pela interface atual: lógica em evento (`Worksheet_Change`, `<Controle>_Click`) ou em formulário, `MsgBox` ou `InputBox` no meio do cálculo, cálculo que lê `Range`.
   - Passe pelo **teste da exclusão** tudo o que parecer raso: apagá-lo concentraria a complexidade ou só a mudaria de lugar? "Concentraria" é o sinal que você procura.
   - Classifique as dependências de cada candidata pelas categorias de dependência.
   - O passo termina quando você leu cada ponto quente e cada suspeita de módulo raso passou pelo teste da exclusão.

3. **Apresentar as candidatas no relatório HTML.**
   - Com o codeInterpreter, grave um arquivo HTML autocontido, `revisao-arquitetura-<aaaammdd-hhmm>.html`, em UTF-8: A5 vale para código VBA, não para o relatório. Entregue o link para download e avise que o arquivo fica disponível só durante esta sessão; o usuário o baixa e abre no navegador.
   - Estilize com Tailwind via CDN e desenhe com Mermaid via CDN o que tem forma de grafo: chamadas, dependências, sequências. Para o resto, desenhe à mão em HTML, CSS e SVG. Cada candidata tem um diagrama antes/depois. Seja visual: o diagrama carrega o peso, e o texto é curto.
   - Estrutura do arquivo:

   ```html
   <!doctype html>
   <html lang="pt-BR">
     <head>
       <meta charset="utf-8" />
       <title>Revisão de arquitetura: {{pasta de trabalho}}</title>
       <script src="https://cdn.tailwindcss.com"></script>
       <script type="module">
         import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11.17.2/dist/mermaid.esm.min.mjs";
         mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
       </script>
       <style>
         .costura { stroke-dasharray: 4 4; }
         .vazamento { stroke: #dc2626; }
         .profundo { background: linear-gradient(135deg, #0f172a, #1e293b); }
       </style>
     </head>
     <body class="bg-stone-50 text-slate-900 font-sans">
       <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
         <header>...</header>
         <section id="candidatas" class="space-y-10">...</section>
         <section id="recomendacao-principal">...</section>
       </main>
     </body>
   </html>
   ```

   - **Cabeçalho:** nome da pasta de trabalho, se o usuário o deu, data e uma legenda compacta: caixa sólida = módulo, linha tracejada = costura, seta vermelha = vazamento, caixa escura de borda grossa = módulo profundo. Vá direto às candidatas, sem parágrafo de introdução.
   - **Cartão de cada candidata**, um `<article>`:
     - **Título:** curto, nomeia o aprofundamento, como "Concentrar a importação do extrato".
     - **Selos:** a força da recomendação, `Forte` (esmeralda), `Vale explorar` (âmbar) ou `Especulativa` (ardósia), e a categoria de dependência.
     - **Módulos:** os módulos e procedimentos envolvidos, em `font-mono text-sm`.
     - **Antes/depois:** o centro do cartão, em duas colunas lado a lado.
     - **Problema:** uma frase, o que dói.
     - **Solução:** uma frase, o que muda.
     - **Ganhos:** tópicos de até seis palavras, nos termos do vocabulário, inclusive o que melhora nos testes, como "localidade: o bug fica em um módulo" ou "a interface encolhe; a implementação absorve os repasses".
     - **Aviso de decisão**, se houver: uma linha numa caixa âmbar.

     Se o diagrama precisa de um parágrafo para ser entendido, redesenhe o diagrama.

   - **Padrões de diagrama.** Escolha o que serve a cada candidata e varie entre os cartões:
     - **Grafo Mermaid** (`flowchart`) para "X chama Y, que chama Z", num cartão `rounded-lg border border-slate-200 bg-white p-4`; `linkStyle` pinta de vermelho a aresta do vazamento, e `classDef`, de escuro o módulo profundo. `sequenceDiagram` serve para "antes, seis idas e voltas; depois, uma".
     - **Caixas e setas à mão:** `<div>`s com borda e setas em SVG sobre um contêiner `relative`, para o "depois" com um módulo profundo de borda grossa e as partes internas esmaecidas.
     - **Corte:** faixas horizontais empilhadas (`h-12 border-l-4`), uma por módulo que a chamada atravessa. Antes, seis faixas finas que nada fazem; depois, uma faixa grossa com a responsabilidade reunida.
     - **Massa:** dois retângulos por módulo, interface e implementação. Raso: a interface quase da altura da implementação. Profundo: interface baixa, implementação alta.
     - **Colapso:** antes, a árvore de chamadas em caixas aninhadas; depois, a mesma árvore dentro de uma caixa só, com as chamadas internas esmaecidas.
   - **Estilo:** editorial, não painel corporativo, com bastante espaço em branco; títulos em `font-serif` combinam com stone e slate. Use um destaque (esmeralda ou índigo), vermelho para vazamento e âmbar para aviso. Diagramas com cerca de 320 px de altura, para antes e depois caberem lado a lado. Rótulos de módulo nos diagramas em `text-xs uppercase tracking-wider`. Os únicos scripts são o Tailwind e o Mermaid; a página é estática.
   - **Recomendação principal:** a última seção, um cartão maior com o nome da candidata que você atacaria primeiro, uma frase sobre o motivo e um link para o cartão dela.
   - **Nomes:** o domínio fala com os nomes do usuário (abas, tabelas, termos do negócio), e a arquitetura, com o vocabulário. Se o usuário chama a aba de `Extrato`, escreva "o módulo de importação do extrato". Frases no tom: "O módulo de importação do extrato é raso: a interface quase iguala a implementação."; "A regra de preço vaza pela costura."; "Dois adaptadores justificam a costura: ADODB em produção, em memória no teste."
   - **Decisão em conflito:** a candidata que contraria uma decisão do módulo `Decisoes` entra só quando o atrito justifica reabrir a decisão, com o aviso "contraria a decisão <n>, mas vale reabrir porque…".
   - Neste passo, descreva o problema e a direção da solução; as interfaces ficam para o passo 4. Depois de entregar o arquivo, pergunte "Qual destas você quer explorar?" e aguarde.
   - Se o usuário não conseguir baixar ou abrir o arquivo, mostre os mesmos cartões no chat, com os diagramas em blocos de texto.
   - O passo termina com o link entregue e a pergunta feita.

4. **Entrevistar sobre a candidata escolhida.**
   - Invoque a skill `grill-me` para percorrer com o usuário a árvore de decisões da candidata: restrições, dependências, o formato do módulo aprofundado, o que fica atrás da costura e quais testes sobrevivem.
   - Aja durante a entrevista, assim que cada decisão se firmar:
     - **Nome novo:** o módulo aprofundado leva o termo de domínio do usuário, conforme N1 e N2; confirme o nome com ele.
     - **Termo vago:** fixe com o usuário um nome único para o conceito e use só esse nome daí em diante.
     - **Código que contradiz o usuário:** se o usuário disser como algo funciona e o código mostrar outra coisa, aponte a divergência e pergunte qual vale.
     - **Candidata rejeitada por motivo duradouro:** pergunte "Quer que eu registre isso no módulo `Decisoes`, para revisões futuras não sugerirem de novo?". Ofereça só quando um revisor futuro precisaria do motivo para não repetir a sugestão; motivo passageiro ("agora não compensa") ou óbvio dispensa o registro. O aceite do usuário aprova o registro: entregue o módulo `Decisoes` completo (A7), com o cabeçalho C1 e a decisão nova no fim, numerada depois da maior existente:

       ```vba
       ' Decisão <n>: <título curto>
       ' <Uma a três frases: o contexto, o que se decidiu e por quê.>
       ```

     - **Interfaces alternativas:** se o usuário quiser comparar desenhos do módulo aprofundado, explique primeiro o espaço do problema: as restrições que qualquer interface nova precisa cumprir e as dependências, com suas categorias. Depois, desenhe três interfaces radicalmente diferentes, uma por restrição:
       1. mínima: de um a três pontos de entrada, com a maior alavancagem por ponto;
       2. otimizada para o chamador mais comum: o caso padrão fica trivial;
       3. com portas e adaptadores, quando uma dependência varia através da costura.

       Para cada uma, mostre a interface (declarações `Public`, sem corpo, com invariantes, ordem de chamada e erros), um exemplo de chamada, o que fica escondido atrás da costura, a estratégia de dependência com os adaptadores e as trocas: onde a alavancagem é alta e onde é fina. Compare as três por profundidade, localidade e posição da costura e recomende uma, ou uma combinação delas. Dê uma leitura forte, não um cardápio.
   - A entrevista termina quando a `grill-me` encerra, com as decisões confirmadas pelo usuário. Para implementar a candidata, retome o **Fluxo** das instruções do agente com essas decisões, sem repetir o que já foi respondido.

## Parameters

- Código do projeto VBA, colado na conversa ou anexado em `.txt`, com o nome de cada módulo.
- Opcionais: direção da análise (módulo, processo ou dor), os módulos mais alterados nos últimos meses e o módulo `Decisoes`.

## Output

- Relatório HTML para download, com um cartão por candidata e a recomendação principal, seguido da pergunta "Qual destas você quer explorar?".
- Após a escolha: a entrevista da skill `grill-me` e, quando o usuário aceitar um registro, o módulo `Decisoes` completo em bloco `vba`.
