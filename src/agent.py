"""
agent.py
--------
Responsabilidade: Orquestrar o pipeline completo de análise.
Chama Loader → Analyzer → Validator → Reporter em sequência.

Esta classe é o ponto de integração futura com agentes de IA (LangChain, watsonx, etc.).
Hoje é um orquestrador Python simples — a interface é mantida intencionalmente limpa
para que ferramentas externas possam chamar `executar()` e receber um resultado estruturado
sem conhecer os detalhes internos.
"""

import os
from src.loader import carregar_excel
from src.analyzer import analisar
from src.validator import validar
from src.reporter import salvar_relatorios, construir_relatorio_texto


class AgenteAnalise:
    """
    Coordena o pipeline completo de análise de Excel.

    Parâmetros
    ----------
    diretorio_saida : str
        Diretório onde os relatórios serão gravados. Padrão: 'relatorios/'.
    """

    def __init__(self, diretorio_saida: str = "relatorios"):
        self.diretorio_saida = diretorio_saida

    def executar(self, caminho_arquivo: str, nome_aba: int | str = 0) -> dict:
        """
        Executa o pipeline completo no arquivo Excel informado.

        Parâmetros
        ----------
        caminho_arquivo : str
            Caminho para o arquivo .xlsx a ser analisado.
        nome_aba : int | str
            Índice ou nome da aba. Padrão: primeira aba.

        Retorna
        -------
        dict com as chaves:
            - caminho_arquivo : caminho do arquivo de entrada
            - analise         : saída de analyzer.analisar()
            - problemas       : saída de validator.validar()
            - relatorio_txt   : caminho do relatório .txt gerado
            - relatorio_json  : caminho do relatório .json gerado
            - texto           : relatório completo como string (para exibição)
        """
        print(f"[Agente] Carregando arquivo: {caminho_arquivo}")
        df = carregar_excel(caminho_arquivo, nome_aba=nome_aba)
        print(f"[Agente] Carregado: {len(df)} linhas × {len(df.columns)} colunas.")

        print("[Agente] Executando análise…")
        analise = analisar(df)

        print("[Agente] Executando validação…")
        problemas = validar(df)

        print("[Agente] Gerando relatórios…")
        caminho_txt, caminho_json = salvar_relatorios(
            diretorio_saida=self.diretorio_saida,
            nome_arquivo=caminho_arquivo,
            analise=analise,
            problemas=problemas,
        )

        texto = construir_relatorio_texto(caminho_arquivo, analise, problemas)

        print(f"[Agente] Relatórios salvos:\n  TXT  → {caminho_txt}\n  JSON → {caminho_json}")

        return {
            "caminho_arquivo": caminho_arquivo,
            "analise": analise,
            "problemas": problemas,
            "relatorio_txt": caminho_txt,
            "relatorio_json": caminho_json,
            "texto": texto,
        }
