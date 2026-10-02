---
name: diagnosticar-sandbox
description: Diagnostica o ambiente que executa os scripts das skills e informa a versão do Python, o sistema operacional, os arquivos da skill e os pacotes instalados. Use quando o usuário pedir diagnóstico do sandbox, quiser testar se scripts de skill rodam ou perguntar quais pacotes Python estão disponíveis.
---

# Diagnosticar o sandbox

1. Execute `scripts/diagnosticar.py`, na pasta desta skill, com Python 3.
2. Mostre a saída completa dentro de um bloco de código, exatamente como o script a imprimiu, linha por linha.
3. Se o script falhar ou não puder ser executado, mostre a mensagem de erro completa e o comando que você usou.

A tarefa termina quando o usuário recebe a saída integral do script ou a mensagem de erro integral.
