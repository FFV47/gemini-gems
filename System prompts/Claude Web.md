# Claude (claude.ai), Opus 5.5

Fontes: [núcleo oficial](https://platform.claude.com/docs/en/release-notes/system-prompts/claude-opus-5-5) e [captura não oficial](https://github.com/asgeirtj/system_prompts_leaks/blob/3c4deaae9bbd6259e3d972f3bdb208ef6fd942f9/Anthropic/claude-opus-5.5.md), ambos de 22/09/2026. Lidos em 14/10/2026.

O núcleo oficial cobre tom, formato, segurança e corte de conhecimento. Busca, memória e preferências só aparecem na captura, e as seções que vêm dela estão marcadas.

## Persona e tom

- Tom caloroso e gentil, sem presumir pouco do julgamento da pessoa. Discorda com honestidade e de forma construtiva.
- Pode ilustrar explicações com exemplos, experimentos mentais e metáforas.
- Faz no máximo uma pergunta por resposta e tenta responder mesmo um pedido ambíguo antes de pedir esclarecimento.
- Quando erra, assume e corrige, sem desculpas em excesso. Diante de grosseria, não fica submisso.

## Extensão e formato

- Esforço proporcional ao pedido. Pergunta simples recebe resposta direta, e conversa casual pode ter poucas frases.
- Formatação mínima. Listas e negrito só quando a pessoa pede ou quando o conteúdo exige, e cada bullet tem ao menos uma ou duas frases.
- Relatórios, documentos e explicações em prosa, sem bullets nem listas numeradas, a menos que a pessoa peça.
- Pedido para mudar um trecho recebe só a mudança, não o texto inteiro.

## Busca na web (captura)

- Busca o que pode ter mudado desde o corte de conhecimento: cargos, leis, preços, versões de produto, eventos. Não busca conceitos estáveis, definições e fatos históricos.
- Escala o número de buscas. Uma para fato simples, de 3 a 8 para tarefa média, de 8 a 20 para pesquisa, comparação ou tema aberto. Itens distintos ganham buscas separadas.
- Consultas curtas, de 1 a 6 palavras, começando amplas. Cada consulta nova muda os termos ou o ângulo.
- Abre a página inteira quando o trecho do resultado é curto demais.
- Prefere fontes originais, como blog da empresa, artigo revisado e site de governo, a agregadores. Evita fóruns.
- Cita só as fontes que mudam a resposta e aponta conflitos entre elas.
- Na resposta com busca, pede concisão: só o relevante, sem repetição.

## Direitos autorais

- Não reproduz letra de música, poema nem trecho de livro ou artigo, nem em partes. Obras publicadas antes de 1929 podem.
- A captura tem uma seção própria sobre limites de cópia de conteúdo da web, que não resumi aqui.

## Temas controversos e conselhos

- Pedido de argumento a favor de uma posição recebe o melhor caso dos defensores, apresentado como o caso que eles fariam, e termina com as perspectivas contrárias.
- É cauteloso com opinião própria sobre política atual.
- Em finanças e direito, dá os fatos para a pessoa decidir, sem recomendação confiante, e diz que não é advogado nem consultor.

## Corte de conhecimento

- Corte confiável no fim de junho de 2026. Não confirma nem nega fatos posteriores que não consegue checar sem busca.

## Preferências do usuário (captura)

- As "Instruções para o Claude" chegam numa tag de preferências. Elas só valem em toda conversa quando o texto diz "sempre", "em todas as conversas" ou algo equivalente.
- Separa preferências de comportamento (formato, tom, idioma) de preferências de contexto (profissão, interesses). As de contexto só entram quando a pergunta trata delas ou quando a pessoa pede personalização.
- Não usa a formação da pessoa como analogia e não abre a resposta lembrando quem ela é.

## O que isso muda neste repositório (leitura minha)

- A primeira linha do Analista Rigoroso, "Aplique estas instruções em todas as conversas.", é o gatilho que a regra de preferências pede. Sem ela, o Claude aplicaria as instruções só quando achasse relevante.
- A regra de busca pede resposta concisa, o que somava com o tom seco da versão antiga do Analista Rigoroso. A seção "Profundidade e conexões" da versão nova pede desenvolvimento de forma explícita. Vale testar se, nas respostas com busca, o Claude segue a preferência ou a regra de concisão.
