"""
validator.py
------------
Responsabilidade: Detectar problemas de qualidade de dados e inconsistências no DataFrame.
Retorna uma lista estruturada de problemas — sem leitura/escrita de arquivos, sem mutações.
"""

import pandas as pd


# Níveis de severidade
CRITICO = "CRÍTICO"
AVISO = "AVISO"
INFO = "INFO"


def _problema(severidade: str, coluna: str | None, descricao: str, detalhe: str = "") -> dict:
    return {
        "severidade": severidade,
        "coluna": coluna or "—",
        "descricao": descricao,
        "detalhe": detalhe,
    }


def validar(df: pd.DataFrame) -> list[dict]:
    """
    Executa todas as verificações de qualidade no DataFrame.

    Retorna
    -------
    list[dict]
        Cada item possui as chaves: severidade, coluna, descricao, detalhe.
    """
    problemas = []

    # 1. Colunas completamente vazias
    for col in df.columns:
        if df[col].isnull().all():
            problemas.append(_problema(CRITICO, col, "Coluna completamente vazia (todos os valores são nulos)."))

    # 2. Colunas com mais de 50% de nulos
    for col in df.columns:
        pct_nulo = df[col].isnull().mean()
        if 0 < pct_nulo > 0.50:
            problemas.append(_problema(
                AVISO, col,
                f"Coluna possui {pct_nulo:.0%} de valores nulos (mais de 50%).",
                f"{int(pct_nulo * len(df))} nulos de {len(df)} linhas."
            ))

    # 3. Colunas com algum nulo (informativo)
    for col in df.columns:
        qtd_nulo = df[col].isnull().sum()
        pct_nulo = df[col].isnull().mean()
        if 0 < qtd_nulo <= len(df) * 0.50:
            problemas.append(_problema(
                INFO, col,
                f"Coluna possui {qtd_nulo} valor(es) nulo(s) ({pct_nulo:.1%}).",
            ))

    # 4. Linhas duplicadas
    qtd_duplicadas = df.duplicated().sum()
    if qtd_duplicadas > 0:
        problemas.append(_problema(
            AVISO, None,
            f"O conjunto de dados possui {qtd_duplicadas} linha(s) completamente duplicada(s).",
            "Duplicatas podem distorcer agregações e contagens."
        ))

    # 5. Outliers numéricos (método IQR)
    colunas_numericas = df.select_dtypes(include="number").columns
    for col in colunas_numericas:
        serie = df[col].dropna()
        if len(serie) < 4:
            continue
        q1 = serie.quantile(0.25)
        q3 = serie.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        outliers = serie[(serie < limite_inferior) | (serie > limite_superior)]
        if not outliers.empty:
            problemas.append(_problema(
                AVISO, col,
                f"Coluna possui {len(outliers)} possível(is) outlier(s) (método IQR).",
                f"Faixa esperada: [{limite_inferior:.2f}, {limite_superior:.2f}]. "
                f"Valores encontrados fora da faixa: {outliers.values[:5].tolist()}…"
            ))

    # 6. Valores negativos em colunas numéricas
    for col in colunas_numericas:
        serie = df[col].dropna()
        qtd_negativos = (serie < 0).sum()
        if qtd_negativos > 0:
            problemas.append(_problema(
                INFO, col,
                f"Coluna possui {qtd_negativos} valor(es) negativo(s). Verifique se é esperado.",
            ))

    # 7. Tipos mistos em colunas de texto (ex: números misturados com strings)
    for col in df.select_dtypes(include="object").columns:
        serie = df[col].dropna()
        if len(serie) == 0:
            continue
        parecem_numericos = pd.to_numeric(serie, errors="coerce").notna()
        proporcao_numerica = parecem_numericos.mean()
        if 0 < proporcao_numerica < 1:
            problemas.append(_problema(
                AVISO, col,
                "Coluna parece misturar valores de texto e numéricos.",
                f"~{proporcao_numerica:.0%} dos valores não nulos parecem numéricos."
            ))

    # 8. Colunas constantes (sem variação)
    for col in df.columns:
        if df[col].nunique(dropna=True) == 1:
            problemas.append(_problema(
                INFO, col,
                "Coluna possui apenas um valor único — pode não ter valor analítico.",
            ))

    return problemas
