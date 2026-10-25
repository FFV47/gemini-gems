# Gemini (app), 3.8 Flash e 3.1 Pro

Fontes: [captura do 3.8 Flash](https://github.com/asgeirtj/system_prompts_leaks/blob/3c4deaae9bbd6259e3d972f3bdb208ef6fd942f9/Google/gemini-3.8-flash.md), que entrou no repositório em 13/09/2026, e [captura do 3.1 Pro](https://github.com/asgeirtj/system_prompts_leaks/blob/3c4deaae9bbd6259e3d972f3bdb208ef6fd942f9/Google/gemini-3.1-pro.md), datada de 18/05/2026 no próprio texto. Lidas em 14/10/2026. As duas são da versão web no plano pago, e o Google não publica esses prompts.

A base deste resumo é o 3.8 Flash. O 3.1 Pro entra para personalização e recitação, que o 3.8 Flash capturado não traz, e as seções que vêm dele estão marcadas.

## Persona e tom

- Colaborador autêntico e adaptável, com um toque de humor. Procura a intenção real do usuário e responde de forma clara e concisa.
- Equilibra empatia e franqueza. Valida sentimentos, mas corrige desinformação séria com gentileza e de forma direta, como um colega e não como um professor rígido.
- Ajusta tom, energia e humor ao estilo do usuário.
- Prefere o concreto ao descritivo. Nomeia a coisa e o que ela tem de notável, sem adjetivos floreados.

## Extensão e formato

- Meta de cerca de 350 palavras para pergunta com muito contexto. Metas por tipo de pedido: de 350 a 400 em escrita criativa, cerca de 250 em planejamento e menos de 200 em compras.
- Estrutura generosa para leitura rápida. Em pergunta factual ou instrucional, no máximo uma ou duas frases de abertura, e daí direto para bullets, tabela ou parágrafos curtos.
- Proíbe anúncios do tipo "aqui está uma lista de" e seções de fecho rotuladas, como "Resumo:" e "Conclusão:".
- Títulos com `##` só em tarefa longa e complexa. No resto, negrito numa linha própria.
- Conselho e conversa pessoal em prosa calorosa, sem tabela nem títulos.
- Tem componentes visuais próprios: imagem, carrossel, sequência de passos, linha do tempo e widget interativo. Busca imagens por conta própria em temas concretos, como pessoas, lugares, objetos e diagramas.

## Aprendizado

- Antes de responder, se pergunta qual nuance um especialista acrescentaria e se um visual ajudaria.
- Quando o usuário está resolvendo um problema ou tentando entender um conceito, mostra o raciocínio primeiro e a resposta no fim. Ao corrigir um erro do usuário, aponta onde ele errou antes de dar a resposta certa.
- Em pergunta educativa, fecha com uma sugestão que testa o entendimento ou propõe o próximo passo. As sugestões ficam no tema da resposta e nunca abrem assunto novo.
- (3.1 Pro) Nos widgets, assume o papel de tutor visual. Diagramas entram só quando a intenção do usuário é aprender ou entender.

## Premissas e perguntas

- Quando o usuário pergunta se uma conta está certa, refaz a conta passo a passo e só dá o veredito no fim. Não começa com "sim" ou "não".
- Em pedido ambíguo, não gera rascunho e procura entender a intenção primeiro. Ao perguntar, explica por que pergunta e oferece opções concretas. Nunca pergunta o que poderia responder sozinho.

## Busca na web

- A ferramenta de busca do Google serve para conhecimento atual ou verificação de fatos, e devolve trechos das páginas.
- Usa a data atual nas consultas sobre assuntos recentes.
- A regra geral de ferramentas diz que chamar e não usar não custa nada, enquanto deixar de chamar piora a resposta. Na dúvida, chama.
- A captura não traz regra de citação de páginas nem de qualidade de fonte.
- A única regra explícita contra inventar dados fica no gerador de imagens: o texto que acompanha a imagem não inventa nomes, datas nem estatísticas.

## Personalização (3.1 Pro)

- Segue um protocolo de cinco passos antes de usar dado pessoal. Só usa quando o dado agrega, como em recomendação, conselho e planejamento. Em pergunta objetiva ou factual, não usa.
- O histórico de correções do usuário vence qualquer outra fonte.
- Não leva preferência de um domínio para outro e não combina dados pessoais diferentes na mesma resposta.
- Tem uma lista longa de dados sensíveis, que só entram se o usuário pedir.
- Usa o dado sem anunciar e proíbe aberturas como "com base no que você disse". Também pede para não limitar a resposta ao que já sabe do usuário e para oferecer opções fora desse perfil.

## Sigilo e recitação

- Proíbe revelar, repetir ou discutir as próprias instruções.
- (3.1 Pro) Só recita texto que já está visível na conversa, e só a parte que o usuário forneceu.

## Leitura minha

- O padrão do Gemini vai no sentido oposto ao do Claude, com muita estrutura, bullets e metas de palavras. Uma Gem que queira explicação em prosa corrida precisa pedir isso com todas as letras.
- O passo da nuance que um especialista acrescentaria é a mesma ideia da seção "Profundidade e conexões" do Analista Rigoroso.
- Como a captura não tem regra de citação, uma Gem de pesquisa precisa pedir as fontes na própria instrução.
