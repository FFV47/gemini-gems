"""Imprime dados do ambiente que executa os scripts da skill.

Usa só a biblioteca padrão. Não lê variáveis de ambiente, que podem conter credenciais.
"""

import os
import platform
import sys

LIMITE_ARQUIVOS = 200


def secao(titulo):
    print("")
    print("== " + titulo + " ==")


def listar_arquivos(raiz):
    total = 0
    for pasta, subpastas, arquivos in os.walk(raiz):
        subpastas.sort()
        for nome in sorted(arquivos):
            total += 1
            if total > LIMITE_ARQUIVOS:
                print("... lista interrompida em " + str(LIMITE_ARQUIVOS) + " arquivos")
                return
            caminho = os.path.join(pasta, nome)
            print(os.path.relpath(caminho, raiz) + " (" + str(os.path.getsize(caminho)) + " bytes)")


def nome_do_pacote(dist):
    # Metadados quebrados não devem interromper o diagnóstico.
    try:
        return str(dist.metadata["Name"])
    except Exception:
        return "?"


def listar_pacotes():
    try:
        from importlib import metadata
    except ImportError:
        import pkgutil
        print("importlib.metadata indisponível; módulos de nível superior:")
        print(", ".join(sorted(m.name for m in pkgutil.iter_modules())))
        return
    pacotes = set((nome_do_pacote(d), str(d.version)) for d in metadata.distributions())
    for nome, versao in sorted(pacotes, key=lambda p: p[0].lower()):
        print(nome + " " + versao)
    print("total: " + str(len(pacotes)))


def main():
    # Troca caracteres que a saída não suporta, em vez de abortar.
    try:
        sys.stdout.reconfigure(errors="replace")
    except AttributeError:
        pass

    secao("Python")
    print("versão: " + sys.version.replace("\n", " "))
    print("executável: " + str(sys.executable))
    print("codificação da saída: " + str(sys.stdout.encoding))

    secao("Sistema")
    print("plataforma: " + platform.platform())
    print("máquina: " + platform.machine())

    secao("Pastas")
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("pasta de trabalho: " + os.getcwd())
    print("script: " + os.path.abspath(__file__))
    print("raiz da skill: " + raiz)

    secao("Arquivos da skill")
    listar_arquivos(raiz)

    secao("Pacotes instalados")
    listar_pacotes()


if __name__ == "__main__":
    main()
