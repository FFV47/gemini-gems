Instruções prontas para colar no campo **Instruções** do Agent Builder. O texto tem **5.880 caracteres** (contados via script), abaixo do limite de 8.000 caracteres para instruções de agentes declarativos. A estrutura segue a orientação da Microsoft: propósito, diretrizes gerais (tom e restrições) e habilidades, mais passo a passo, tratamento de erros e limitações quando relevante, em Markdown, com nomes de ferramentas entre crases e instruções críticas em negrito, e uma etapa final de autoavaliação.

**Nome e descrição sugeridos:** "Engenheiro de Software" — "Escreve, revisa, depura e explica código, com foco em VBA, Power Query, Excel e linguagens gerais."

**Iniciadores de conversa (campo próprio do Agent Builder):**

- _Revisar código_ — "Revise este código e classifique os problemas por gravidade: [cole o código]"
- _Depurar erro_ — "Estou recebendo este erro: [mensagem]. Código: [cole]. Esperado: [x]. Obtido: [y]."
- _Criar macro VBA_ — "Escreva uma macro VBA para Excel que [objetivo]. Minha versão do Excel é [versão]."
- _Explicar código_ — "Explique linha a linha o que este código faz: [cole]"

**Configuração recomendada:**

- **Code interpreter:** ative, para que o agente consiga executar Python e cumprir a regra de não afirmar sem testar. Atenção: capacidades além da busca na web só ficam acessíveis se a organização permitir uso medido ou se o usuário tiver licença do Microsoft 365 Copilot.
- **Conhecimento do modelo:** não ative a opção de desencorajar o conhecimento do modelo. A Microsoft indica a propriedade `discourage_model_knowledge` para agentes que devem responder só com base nas fontes configuradas, o que prejudicaria um agente de programação.
- **SharePoint/OneDrive:** útil para padrões de código da equipe, mas não para esticar as instruções. A Microsoft desaconselha isso porque conteúdo de fonte de conhecimento passa por classificadores de injeção de prompt e linguagem em forma de diretiva pode ser bloqueada, truncada ou sanitizada.
- **Se precisar de mais espaço:** existe o recurso de habilidades personalizadas (skills, em versão prévia), cujas instruções podem ter até 20.000 caracteres e contornam o limite de 8.000.

**Limitações desta resposta:**

- Não testei o agente dentro do Copilot. O comportamento real depende do modelo que a Microsoft usa, e a plataforma troca de modelo periodicamente, o que pode alterar como o agente interpreta as instruções. Teste com os iniciadores e com pedidos fora deles.
- As regras técnicas de VBA, Power Query e Excel vêm do meu conhecimento de treinamento (prática consolidada, confiança alta), não de verificação item a item na web nesta resposta.
- Os nomes exatos de opções da interface (ex.: "Code interpreter" em inglês ou português) podem variar conforme o idioma e a versão do ambiente Microsoft 365 da sua organização.

**Fontes:**

- Microsoft Learn — [Write effective instructions for declarative agents](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-instructions) (atualizado em 11/08/2026)
- Microsoft Learn — [Custom skills in declarative agents (preview)](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-skills)
- Microsoft Learn — [Declarative agent schema 1.8](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-manifest-1.8)
