"""
main.py
-------
Ponto de entrada da linha de comando para o Excel Data Analyst AI.

Uso
---
    python main.py                           # analisa o arquivo de exemplo padrão
    python main.py caminho/para/arquivo.xlsx # analisa um arquivo personalizado
    python main.py caminho/arquivo.xlsx Aba2 # analisa uma aba específica
"""

import sys
import os
import io

# Força stdout a usar UTF-8 no Windows para suportar caracteres especiais
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Garante que src/ seja importável ao rodar a partir da raiz do projeto
sys.path.insert(0, os.path.dirname(__file__))

from src.agent import AgenteAnalise


def main():
    # Usa o conjunto de dados de exemplo por padrão
    caminho_arquivo = sys.argv[1] if len(sys.argv) > 1 else os.path.join("data", "dados_exemplo.xlsx")
    nome_aba = sys.argv[2] if len(sys.argv) > 2 else 0

    # Converte nome_aba para int se parecer um número
    if isinstance(nome_aba, str) and nome_aba.isdigit():
        nome_aba = int(nome_aba)

    agente = AgenteAnalise(diretorio_saida="relatorios")

    try:
        resultado = agente.executar(caminho_arquivo, nome_aba=nome_aba)
        print("\n" + resultado["texto"])
    except Exception as erro:
        print(f"\n[ERRO] {erro}")
        sys.exit(1)


if __name__ == "__main__":
    main()
