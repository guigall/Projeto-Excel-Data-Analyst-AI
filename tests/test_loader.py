"""Testes para loader.py"""

import os
import pytest
import pandas as pd
from src.loader import carregar_excel, ErroCarregamento


CAMINHO_EXEMPLO = os.path.join("data", "dados_exemplo.xlsx")


# ── Casos de sucesso ──────────────────────────────────────────────────────────

def test_carregamento_retorna_dataframe():
    df = carregar_excel(CAMINHO_EXEMPLO)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_colunas_corretas():
    df = carregar_excel(CAMINHO_EXEMPLO)
    esperadas = {
        "id_pedido", "data_venda", "regiao", "categoria",
        "vendedor", "quantidade", "preco_unitario", "desconto",
        "valor_total", "status", "avaliacao_cliente", "observacoes",
    }
    assert esperadas.issubset(set(df.columns))


def test_carregamento_por_nome_de_aba():
    df = carregar_excel(CAMINHO_EXEMPLO, nome_aba="Vendas_Bagunca")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


# ── Casos de erro ─────────────────────────────────────────────────────────────

def test_arquivo_inexistente():
    with pytest.raises(ErroCarregamento, match="Arquivo não encontrado"):
        carregar_excel("arquivo_inexistente.xlsx")


def test_extensao_invalida(tmp_path):
    arquivo_txt = tmp_path / "dados.txt"
    arquivo_txt.write_text("olá")
    with pytest.raises(ErroCarregamento, match="Formato de arquivo não suportado"):
        carregar_excel(str(arquivo_txt))
