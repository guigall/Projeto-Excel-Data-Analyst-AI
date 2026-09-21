"""Testes para reporter.py"""

import json
import os
import pytest
import pandas as pd
from src.analyzer import analisar
from src.validator import validar
from src.reporter import construir_relatorio_texto, salvar_relatorios


@pytest.fixture
def analise_e_problemas():
    df = pd.DataFrame({
        "nome": ["Alice", "Bob", None],
        "pontuacao": [90.0, 85.0, 92.0],
        "categoria": ["A", "B", "A"],
    })
    return analisar(df), validar(df)


def test_relatorio_texto_retorna_string(analise_e_problemas):
    analise, problemas = analise_e_problemas
    relatorio = construir_relatorio_texto("teste.xlsx", analise, problemas)
    assert isinstance(relatorio, str)
    assert len(relatorio) > 0


def test_relatorio_texto_contem_secoes(analise_e_problemas):
    analise, problemas = analise_e_problemas
    relatorio = construir_relatorio_texto("teste.xlsx", analise, problemas)
    for secao in ["RESUMO GERAL", "INDICADORES NUMÉRICOS", "DISTRIBUIÇÃO", "RECOMENDAÇÕES"]:
        assert secao in relatorio


def test_salvar_relatorios_cria_arquivos(tmp_path, analise_e_problemas):
    analise, problemas = analise_e_problemas
    caminho_txt, caminho_json = salvar_relatorios(
        diretorio_saida=str(tmp_path),
        nome_arquivo="teste.xlsx",
        analise=analise,
        problemas=problemas,
    )
    assert os.path.exists(caminho_txt)
    assert os.path.exists(caminho_json)


def test_relatorio_json_valido(tmp_path, analise_e_problemas):
    analise, problemas = analise_e_problemas
    _, caminho_json = salvar_relatorios(
        diretorio_saida=str(tmp_path),
        nome_arquivo="teste.xlsx",
        analise=analise,
        problemas=problemas,
    )
    with open(caminho_json, encoding="utf-8") as f:
        dados = json.load(f)

    assert "analise" in dados
    assert "problemas" in dados
    assert "insights" in dados
    assert "recomendacoes" in dados
