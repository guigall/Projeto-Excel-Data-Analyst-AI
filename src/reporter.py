"""
reporter.py
-----------
Responsabilidade: Montar e salvar o relatório final de análise.
Recebe as saídas de analyzer.py e validator.py — sem DataFrame, sem leitura de arquivos.
Produz dois formatos: .txt (legível por humanos) e .json (legível por máquina/agente).
"""

import json
import os
from datetime import datetime


# ── Utilitários ───────────────────────────────────────────────────────────────

def _icone_severidade(severidade: str) -> str:
    return {"CRÍTICO": "🔴", "AVISO": "🟡", "INFO": "🔵"}.get(severidade, "⚪")


def _secao(titulo: str, largura: int = 60) -> str:
    linha = "=" * largura
    return f"\n{linha}\n  {titulo}\n{linha}\n"


# ── Relatório em texto ────────────────────────────────────────────────────────

def construir_relatorio_texto(
    nome_arquivo: str,
    analise: dict,
    problemas: list[dict],
) -> str:
    """
    Constrói o relatório legível por humanos a partir dos resultados de análise e validação.
    """
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linhas = []

    linhas.append("=" * 60)
    linhas.append("  EXCEL DATA ANALYST AI — RELATÓRIO DE ANÁLISE")
    linhas.append("=" * 60)
    linhas.append(f"  Arquivo   : {nome_arquivo}")
    linhas.append(f"  Gerado em : {agora}")
    linhas.append("")

    # ── 1. Resumo geral ──
    linhas.append(_secao("1. RESUMO GERAL"))
    linhas.append(f"  Total de registros  : {analise['total_registros']}")
    linhas.append(f"  Total de colunas    : {analise['total_colunas']}")
    linhas.append(f"  Linhas duplicadas   : {analise['linhas_duplicadas']}")
    linhas.append(f"  Total de nulos      : {analise['total_nulos']}")
    linhas.append("")
    linhas.append("  Colunas identificadas:")
    for col, tipo in analise["tipos_dados"].items():
        qtd_nulo = analise["contagem_nulos"].get(col, 0)
        linhas.append(f"    • {col} ({tipo}) — {qtd_nulo} nulo(s)")

    # ── 2. Indicadores numéricos ──
    linhas.append(_secao("2. INDICADORES NUMÉRICOS"))
    if analise["resumo_numerico"]:
        for col, stats in analise["resumo_numerico"].items():
            linhas.append(f"  [{col}]")
            linhas.append(f"    Contagem       : {stats['contagem']}")
            linhas.append(f"    Soma           : {stats['soma']}")
            linhas.append(f"    Média          : {stats['media']}")
            linhas.append(f"    Mínimo         : {stats['minimo']}")
            linhas.append(f"    Máximo         : {stats['maximo']}")
            linhas.append(f"    Desvio Padrão  : {stats['desvio_padrao']}")
            linhas.append("")
    else:
        linhas.append("  Nenhuma coluna numérica encontrada.")

    # ── 3. Distribuição categórica ──
    linhas.append(_secao("3. DISTRIBUIÇÃO CATEGÓRICA"))
    if analise["resumo_categorico"]:
        for col, info in analise["resumo_categorico"].items():
            linhas.append(f"  [{col}] — {info['qtd_unicos']} valor(es) único(s)")
            for val, cnt in info["valores_mais_frequentes"].items():
                linhas.append(f"    • {val}: {cnt}")
            linhas.append("")
    else:
        linhas.append("  Nenhuma coluna categórica encontrada.")

    # ── 4. Qualidade dos dados ──
    linhas.append(_secao("4. QUALIDADE DOS DADOS E INCONSISTÊNCIAS"))
    if problemas:
        for p in problemas:
            icone = _icone_severidade(p["severidade"])
            linhas.append(f"  {icone} [{p['severidade']}] Coluna: {p['coluna']}")
            linhas.append(f"     {p['descricao']}")
            if p.get("detalhe"):
                linhas.append(f"     Detalhe: {p['detalhe']}")
            linhas.append("")
    else:
        linhas.append("  ✅ Nenhum problema encontrado. Os dados parecem consistentes.")

    # ── 5. Insights ──
    linhas.append(_secao("5. INSIGHTS"))
    insights = _gerar_insights(analise, problemas)
    for insight in insights:
        linhas.append(f"  → {insight}")

    # ── 6. Recomendações ──
    linhas.append(_secao("6. RECOMENDAÇÕES"))
    recomendacoes = _gerar_recomendacoes(analise, problemas)
    for rec in recomendacoes:
        linhas.append(f"  ✔ {rec}")

    linhas.append("\n" + "=" * 60)
    linhas.append("  Fim do Relatório")
    linhas.append("=" * 60 + "\n")

    return "\n".join(linhas)


# ── Geradores de insights e recomendações ─────────────────────────────────────

def _gerar_insights(analise: dict, problemas: list[dict]) -> list[str]:
    insights = []

    if analise["linhas_duplicadas"] > 0:
        pct = analise["linhas_duplicadas"] / analise["total_registros"] * 100
        insights.append(
            f"{analise['linhas_duplicadas']} linha(s) duplicada(s) detectada(s) ({pct:.1f}% do total). "
            "Removê-las pode melhorar a precisão das análises."
        )

    if analise["total_nulos"] > 0:
        insights.append(
            f"Há {analise['total_nulos']} valor(es) ausente(s) no conjunto de dados. "
            "Considere estratégias de imputação ou exclusão."
        )

    for col, stats in analise["resumo_numerico"].items():
        if stats["desvio_padrao"] > 0 and stats["media"] != 0:
            cv = stats["desvio_padrao"] / abs(stats["media"])
            if cv > 1:
                insights.append(
                    f"A coluna '{col}' apresenta alta variabilidade (CV={cv:.2f}), "
                    "indicando dados heterogêneos."
                )

    colunas_outlier = [p["coluna"] for p in problemas if "outlier" in p["descricao"].lower()]
    if colunas_outlier:
        insights.append(
            f"Possíveis outliers encontrados em: {', '.join(set(colunas_outlier))}. "
            "Verifique se representam extremos válidos ou erros de digitação."
        )

    if not insights:
        insights.append("O conjunto de dados parece consistente, sem anomalias relevantes.")

    return insights


def _gerar_recomendacoes(analise: dict, problemas: list[dict]) -> list[str]:
    recomendacoes = []

    if analise["linhas_duplicadas"] > 0:
        recomendacoes.append("Remova ou investigue as linhas duplicadas antes de utilizar os dados.")

    colunas_com_nulo = [col for col, n in analise["contagem_nulos"].items() if n > 0]
    if colunas_com_nulo:
        recomendacoes.append(
            f"Trate os valores ausentes em: {', '.join(colunas_com_nulo)}. "
            "Use média/mediana para numéricos ou um valor padrão para categóricos."
        )

    criticos = [p for p in problemas if p["severidade"] == "CRÍTICO"]
    if criticos:
        recomendacoes.append(
            "Resolva os problemas CRÍTICOS antes de utilizar este conjunto de dados em relatórios ou modelos."
        )

    mistos = [p for p in problemas if "misturar" in p["descricao"].lower()]
    if mistos:
        recomendacoes.append(
            "Padronize as colunas com tipos mistos — converta para um único tipo consistente."
        )

    if not recomendacoes:
        recomendacoes.append("Nenhuma ação corretiva necessária. O conjunto de dados está pronto para uso.")

    return recomendacoes


# ── Persistência ──────────────────────────────────────────────────────────────

def salvar_relatorios(
    diretorio_saida: str,
    nome_arquivo: str,
    analise: dict,
    problemas: list[dict],
) -> tuple[str, str]:
    """
    Grava os relatórios .txt e .json no diretório de saída.
    Retorna (caminho_txt, caminho_json).
    """
    os.makedirs(diretorio_saida, exist_ok=True)
    base_nome = os.path.splitext(os.path.basename(nome_arquivo))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"{base_nome}_{timestamp}"

    caminho_txt = os.path.join(diretorio_saida, f"{base}_relatorio.txt")
    caminho_json = os.path.join(diretorio_saida, f"{base}_relatorio.json")

    texto = construir_relatorio_texto(nome_arquivo, analise, problemas)
    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write(texto)

    payload_json = {
        "arquivo": nome_arquivo,
        "gerado_em": datetime.now().isoformat(),
        "analise": analise,
        "problemas": problemas,
        "insights": _gerar_insights(analise, problemas),
        "recomendacoes": _gerar_recomendacoes(analise, problemas),
    }
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(payload_json, f, indent=2, ensure_ascii=False)

    return caminho_txt, caminho_json
