"""
loader.py
---------
Responsabilidade: Ler um arquivo Excel (.xlsx) e retornar um DataFrame do pandas.
Este módulo não faz nada além de leitura — sem análise, sem transformação.
"""

import os
import pandas as pd


class ErroCarregamento(Exception):
    """Lançada quando um arquivo não pode ser carregado."""


def carregar_excel(caminho_arquivo: str, nome_aba: int | str = 0) -> pd.DataFrame:
    """
    Lê um arquivo Excel e retorna seu conteúdo como um DataFrame.

    Parâmetros
    ----------
    caminho_arquivo : str
        Caminho absoluto ou relativo para o arquivo .xlsx.
    nome_aba : int | str
        Índice da aba (base 0) ou nome da aba. Padrão: primeira aba.

    Retorna
    -------
    pd.DataFrame
        DataFrame bruto com os nomes e valores originais das colunas.

    Lança
    -----
    ErroCarregamento
        Se o arquivo não existir, não for .xlsx ou não puder ser lido.
    """
    if not os.path.exists(caminho_arquivo):
        raise ErroCarregamento(f"Arquivo não encontrado: {caminho_arquivo}")

    if not caminho_arquivo.lower().endswith((".xlsx", ".xls")):
        raise ErroCarregamento(
            f"Formato de arquivo não suportado. Esperado .xlsx ou .xls, recebido: {caminho_arquivo}"
        )

    try:
        df = pd.read_excel(caminho_arquivo, sheet_name=nome_aba)
    except Exception as erro:
        raise ErroCarregamento(f"Falha ao ler o arquivo Excel: {erro}") from erro

    if df.empty:
        raise ErroCarregamento("O arquivo Excel está vazio ou a aba não possui dados.")

    return df
