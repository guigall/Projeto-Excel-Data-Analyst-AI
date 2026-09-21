"""
indicators.py
-------------
Responsabilidade: Calcular indicadores estatísticos de um DataFrame.

Funções puras — sem efeitos colaterais, sem I/O.
"""

import pandas as pd


def contar_nulos_por_coluna(df: pd.DataFrame) -> dict:
    """Retorna {coluna: quantidade_de_nulos} para todas as colunas."""
    return {col: int(df[col].isna().sum()) for col in df.columns}


def contar_linhas_duplicadas(df: pd.DataFrame) -> int:
    """Retorna o número de linhas duplicadas (excluindo a primeira ocorrência)."""
    return int(df.duplicated().sum())


def calcular_resumo_numerico(df: pd.DataFrame) -> dict:
    """
    Retorna resumo estatístico das colunas numéricas.

    Estrutura por coluna:
        {contagem, soma, media, minimo, maximo, desvio_padrao}
    """
    resultado = {}
    for col in df.select_dtypes(include="number").columns:
        serie = df[col].dropna()
        resultado[col] = {
            "contagem"     : int(serie.count()),
            "soma"         : float(serie.sum()),
            "media"        : float(serie.mean()),
            "minimo"       : float(serie.min()),
            "maximo"       : float(serie.max()),
            "desvio_padrao": float(serie.std()),
        }
    return resultado


def calcular_resumo_categorico(df: pd.DataFrame) -> dict:
    """
    Retorna resumo das colunas não-numéricas (object, category, bool, etc.).

    Estrutura por coluna:
        {qtd_unicos, valores_mais_frequentes: [{valor, frequencia}, ...]}
    """
    resultado = {}
    for col in df.select_dtypes(exclude="number").columns:
        serie = df[col].dropna()
        top = serie.value_counts().head(5)
        resultado[col] = {
            "qtd_unicos"             : int(serie.nunique()),
            "valores_mais_frequentes": [
                {"valor": str(v), "frequencia": int(f)}
                for v, f in top.items()
            ],
        }
    return resultado
