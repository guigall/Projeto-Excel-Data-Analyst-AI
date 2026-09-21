"""Testes para analyzer.py"""

import pandas as pd
import pytest
from src.analyzer import analisar


@pytest.fixture
def df_exemplo():
    return pd.DataFrame({
        "nome": ["Alice", "Bob", "Carol", "Alice", None],
        "idade": [30, 25, 35, 30, 28],
        "salario": [5000.0, 4000.0, 6000.0, 5000.0, 4500.0],
        "departamento": ["RH", "TI", "TI", "RH", "Financeiro"],
    })


def test_total_registros(df_exemplo):
    resultado = analisar(df_exemplo)
    assert resultado["total_registros"] == 5


def test_total_colunas(df_exemplo):
    resultado = analisar(df_exemplo)
    assert resultado["total_colunas"] == 4


def test_nomes_colunas(df_exemplo):
    resultado = analisar(df_exemplo)
    assert resultado["colunas"] == ["nome", "idade", "salario", "departamento"]


def test_contagem_nulos(df_exemplo):
    resultado = analisar(df_exemplo)
    assert resultado["contagem_nulos"]["nome"] == 1
    assert resultado["contagem_nulos"]["idade"] == 0


def test_total_nulos(df_exemplo):
    resultado = analisar(df_exemplo)
    assert resultado["total_nulos"] == 1


def test_linhas_duplicadas(df_exemplo):
    resultado = analisar(df_exemplo)
    # Linha 0 e Linha 3 são idênticas → 1 duplicata
    assert resultado["linhas_duplicadas"] == 1


def test_chaves_resumo_numerico(df_exemplo):
    resultado = analisar(df_exemplo)
    for col in ["idade", "salario"]:
        assert col in resultado["resumo_numerico"]
        stats = resultado["resumo_numerico"][col]
        for chave in ("contagem", "soma", "media", "minimo", "maximo", "desvio_padrao"):
            assert chave in stats


def test_valores_resumo_numerico(df_exemplo):
    resultado = analisar(df_exemplo)
    assert resultado["resumo_numerico"]["idade"]["media"] == pytest.approx(29.6, rel=1e-2)
    assert resultado["resumo_numerico"]["salario"]["minimo"] == 4000.0
    assert resultado["resumo_numerico"]["salario"]["maximo"] == 6000.0


def test_resumo_categorico(df_exemplo):
    resultado = analisar(df_exemplo)
    assert "departamento" in resultado["resumo_categorico"]
    assert resultado["resumo_categorico"]["departamento"]["qtd_unicos"] == 3


def test_dataframe_vazio():
    df = pd.DataFrame()
    resultado = analisar(df)
    assert resultado["total_registros"] == 0
    assert resultado["total_colunas"] == 0
