"""
analyzer.py
-----------
Responsabilidade: Orquestrar a análise completa de um DataFrame.

Consolida metadados estruturais e indicadores estatísticos em um único dicionário
de resultado, delegando os cálculos para `indicators.py`.

Sem leitura/escrita de arquivos. Sem mutação de dados.

Estrutura do resultado
----------------------
    {
        "total_registros"  : int,
        "total_colunas"    : int,
        "colunas"          : list[str],
        "tipos_dados"      : {coluna: tipo},
        "contagem_nulos"   : {coluna: int},
        "total_nulos"      : int,
        "linhas_duplicadas": int,
        "resumo_numerico"  : {coluna: {contagem, soma, media, minimo, maximo, desvio_padrao}},
        "resumo_categorico": {coluna: {qtd_unicos, valores_mais_frequentes}},
    }
"""

import pandas as pd

from src.indicators import (
    calcular_resumo_numerico,
    calcular_resumo_categorico,
    contar_nulos_por_coluna,
    contar_linhas_duplicadas,
)


def analisar(df: pd.DataFrame) -> dict:
    """
    Realiza uma análise estrutural e estatística completa do DataFrame.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame a ser analisado. Pode estar vazio.

    Retorna
    -------
    dict
        Dicionário com métricas estruturais e estatísticas (veja docstring do módulo).
    """
    if df.empty:
        return _resultado_vazio()

    contagem_nulos = contar_nulos_por_coluna(df)

    return {
        # Metadados estruturais
        "total_registros"  : len(df),
        "total_colunas"    : len(df.columns),
        "colunas"          : list(df.columns),
        "tipos_dados"      : {col: str(df[col].dtype) for col in df.columns},
        # Qualidade básica
        "contagem_nulos"   : contagem_nulos,
        "total_nulos"      : sum(contagem_nulos.values()),
        "linhas_duplicadas": contar_linhas_duplicadas(df),
        # Indicadores
        "resumo_numerico"  : calcular_resumo_numerico(df),
        "resumo_categorico": calcular_resumo_categorico(df),
    }


# ---------------------------------------------------------------------------
# Auxiliar privado
# ---------------------------------------------------------------------------

def _resultado_vazio() -> dict:
    """Retorna estrutura de resultado padrão para um DataFrame vazio."""
    return {
        "total_registros"  : 0,
        "total_colunas"    : 0,
        "colunas"          : [],
        "tipos_dados"      : {},
        "contagem_nulos"   : {},
        "total_nulos"      : 0,
        "linhas_duplicadas": 0,
        "resumo_numerico"  : {},
        "resumo_categorico": {},
    }
