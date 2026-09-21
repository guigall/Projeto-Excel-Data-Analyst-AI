"""Testes para validator.py"""

import pandas as pd
import pytest
from src.validator import validar, CRITICO, AVISO, INFO


def _filtrar(problemas: list[dict], severidade: str = None, palavra: str = "") -> list[dict]:
    """Filtra problemas por severidade e/ou palavra-chave na descrição."""
    return [
        p for p in problemas
        if (severidade is None or p["severidade"] == severidade)
        and palavra.lower() in p["descricao"].lower()
    ]


# ── Detecção de nulos ─────────────────────────────────────────────────────────

def test_detecta_coluna_completamente_vazia():
    df = pd.DataFrame({"a": [None, None, None], "b": [1, 2, 3]})
    problemas = validar(df)
    assert _filtrar(problemas, CRITICO, "completamente vazia")


def test_detecta_nulos_parciais():
    df = pd.DataFrame({"pontuacao": [1, None, 3, None, 5]})
    problemas = validar(df)
    assert _filtrar(problemas, INFO, "nulo")


# ── Duplicatas ────────────────────────────────────────────────────────────────

def test_detecta_linhas_duplicadas():
    df = pd.DataFrame({"x": [1, 2, 1], "y": ["a", "b", "a"]})
    problemas = validar(df)
    assert _filtrar(problemas, AVISO, "duplicada")


def test_sem_falso_positivo_duplicatas():
    df = pd.DataFrame({"x": [1, 2, 3], "y": ["a", "b", "c"]})
    problemas = validar(df)
    assert not _filtrar(problemas, AVISO, "duplicada")


# ── Outliers ──────────────────────────────────────────────────────────────────

def test_detecta_outliers():
    valores = [10] * 20
    valores.append(10000)  # outlier extremo
    df = pd.DataFrame({"valor": valores})
    problemas = validar(df)
    assert _filtrar(problemas, AVISO, "outlier")


# ── Valores negativos ─────────────────────────────────────────────────────────

def test_detecta_valores_negativos():
    df = pd.DataFrame({"valor": [100, -50, 200]})
    problemas = validar(df)
    assert _filtrar(problemas, INFO, "negativo")


# ── Tipos mistos ──────────────────────────────────────────────────────────────

def test_detecta_tipos_mistos():
    df = pd.DataFrame({"preco": ["10", "20", "N/D", "30", "inválido", "15"]})
    problemas = validar(df)
    assert _filtrar(problemas, AVISO, "misturar")


# ── Coluna constante ──────────────────────────────────────────────────────────

def test_detecta_coluna_constante():
    df = pd.DataFrame({"flag": ["sim", "sim", "sim"]})
    problemas = validar(df)
    assert _filtrar(problemas, INFO, "único")


# ── Dados limpos ──────────────────────────────────────────────────────────────

def test_dados_limpos_sem_criticos():
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "nome": ["Alice", "Bob", "Carol"],
        "pontuacao": [90.0, 85.0, 92.0],
    })
    problemas = validar(df)
    assert not _filtrar(problemas, CRITICO)
