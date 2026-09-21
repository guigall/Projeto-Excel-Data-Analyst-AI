# Excel Data Analyst AI

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas&logoColor=white)
![Pytest](https://img.shields.io/badge/Testes-28%20passed-brightgreen?logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/Licença-MIT-green)

> Assistente em Python que lê qualquer arquivo Excel, analisa os dados automaticamente, detecta inconsistências e gera relatórios prontos para uso — com um único comando.

---

## ✨ Funcionalidades

- 📂 Carregamento de arquivos `.xlsx` por caminho ou nome de aba
- 📊 Análise estrutural automática (linhas, colunas, tipos, nulos, duplicatas)
- 🔢 Indicadores numéricos por coluna (soma, média, mínimo, máximo, desvio padrão)
- 🏷️ Distribuição categórica (valores únicos, top-5 mais frequentes)
- 🔍 Validação de qualidade (outliers via IQR, tipos mistos, colunas vazias, valores negativos)
- 📄 Relatório legível `.txt` + relatório estruturado `.json`
- 🤖 Arquitetura modular pronta para integração com agentes de IA

---

## 🚀 Início Rápido

### 1. Clone o repositório

```bash
git clone https://github.com/guigall/Projeto-Excel-Data-Analyst-AI.git
cd Projeto-Excel-Data-Analyst-AI
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Gere a base fictícia de dados

```bash
python gerar_dados_exemplo.py
```

### 4. Execute a análise

```bash
# Analisar o arquivo de exemplo padrão
python main.py

# Analisar um arquivo personalizado
python main.py caminho/para/seu/arquivo.xlsx

# Analisar uma aba específica pelo nome
python main.py caminho/arquivo.xlsx NomeDaAba
```

Os relatórios são salvos automaticamente na pasta `relatorios/` nos formatos `.txt` e `.json`.

---

## 📋 Exemplo de Output

```
============================================================
  EXCEL DATA ANALYST AI — RELATÓRIO DE ANÁLISE
============================================================
  Arquivo   : data/dados_exemplo.xlsx
  Gerado em : 21/09/2024 18:33:45

============================================================
  1. RESUMO GERAL
============================================================
  Total de registros  : 125
  Total de colunas    : 12
  Linhas duplicadas   : 4
  Total de nulos      : 118

============================================================
  2. INDICADORES NUMÉRICOS
============================================================
  [preco_unitario]
    Média          : 1057.06
    Mínimo         : 9.79
    Máximo         : 99999.99
    Desvio Padrão  : 8922.19

============================================================
  4. QUALIDADE DOS DADOS E INCONSISTÊNCIAS
============================================================
  🟡 [AVISO] Coluna: preco_unitario
     Coluna possui 1 possível(is) outlier(s) (método IQR).

  🟡 [AVISO] Coluna: —
     O conjunto de dados possui 4 linha(s) completamente duplicada(s).

============================================================
  5. INSIGHTS
============================================================
  → 4 linha(s) duplicada(s) detectada(s) (3.2% do total).
  → Possíveis outliers encontrados em: preco_unitario, valor_total.
```

---

## 🧪 Executar os Testes

```bash
pytest tests/ -v
```

```
collected 28 items

tests/test_analyzer.py::test_total_registros         PASSED
tests/test_analyzer.py::test_valores_resumo_numerico PASSED
tests/test_loader.py::test_carregamento_retorna_dataframe PASSED
tests/test_reporter.py::test_relatorio_json_valido   PASSED
tests/test_validator.py::test_detecta_outliers       PASSED
...
28 passed in 0.84s
```

---

## 🗂️ Estrutura do Projeto

```
Projeto-Excel-Data-Analyst-AI/
│
├── data/
│   └── dados_exemplo.xlsx        # Base fictícia de vendas para testes
│
├── src/
│   ├── agent.py                  # Orquestrador do pipeline completo
│   ├── loader.py                 # Leitura do arquivo .xlsx → DataFrame
│   ├── analyzer.py               # Análise estrutural e estatística
│   ├── indicators.py             # Cálculo dos indicadores numéricos e categóricos
│   ├── validator.py              # Detecção de problemas de qualidade
│   └── reporter.py               # Geração dos relatórios .txt e .json
│
├── tests/
│   ├── test_analyzer.py          # 10 testes de análise
│   ├── test_loader.py            # 5 testes de carregamento
│   ├── test_reporter.py          # 4 testes de relatório
│   └── test_validator.py         # 9 testes de validação
│
├── relatorios/                   # Relatórios gerados (ignorados pelo git)
├── gerar_dados_exemplo.py        # Script para criar a base fictícia
├── main.py                       # Ponto de entrada da linha de comando
└── requirements.txt
```

---

## 🏗️ Arquitetura

```
arquivo.xlsx
     │
     ▼
┌─────────────┐
│  loader.py  │  Lê o arquivo → retorna DataFrame bruto
└──────┬──────┘
       │
       ├──────────────────────────┐
       ▼                          ▼
┌─────────────────┐    ┌──────────────────┐
│  analyzer.py    │    │  validator.py    │
│  indicators.py  │    │                  │
│  (estatísticas) │    │  (qualidade)     │
└──────┬──────────┘    └────────┬─────────┘
       │                        │
       └────────────┬───────────┘
                    ▼
           ┌─────────────────┐
           │  reporter.py    │  Gera .txt e .json
           └────────┬────────┘
                    ▼
           ┌─────────────────┐
           │  relatorios/    │
           └─────────────────┘
```

| Módulo | Responsabilidade |
|---|---|
| `loader.py` | Lê `.xlsx` → `DataFrame`. Valida extensão e existência do arquivo. |
| `analyzer.py` | Orquestra os cálculos e consolida o dicionário de análise. |
| `indicators.py` | Funções puras para indicadores numéricos e categóricos. |
| `validator.py` | Detecta outliers, duplicatas, nulos, tipos mistos e valores negativos. |
| `reporter.py` | Monta os relatórios `.txt` e `.json` a partir dos resultados. |
| `agent.py` | Pipeline completo. Ponto de integração futura com IA. |

---

## 🤖 Integração com IA

O `agent.py` foi projetado como ponto de conexão para frameworks de agentes:

```python
from src.agent import AgenteAnalise

agente = AgenteAnalise(diretorio_saida="relatorios")
resultado = agente.executar("meus_dados.xlsx")

print(resultado["texto"])        # relatório legível
print(resultado["analise"])      # dict estruturado para IA consumir
print(resultado["problemas"])    # lista de problemas detectados
```

**Integrações possíveis:**
- **LangChain** — encapsule `AgenteAnalise.executar()` como uma `Tool`
- **IBM watsonx** — exponha como função em um `Assistant`
- **FastAPI** — envolva com uma rota `POST /analisar` para acesso via HTTP

---

## 📦 Dependências

| Biblioteca | Versão mínima | Uso |
|---|---|---|
| `pandas` | 2.0.0 | Manipulação de dados |
| `openpyxl` | 3.1.0 | Leitura de arquivos `.xlsx` |
| `pytest` | 7.4.0 | Testes automatizados |

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja o [CONTRIBUTING.md](CONTRIBUTING.md) para saber como começar.

---

## 📄 Licença

MIT © [Guilherme](https://github.com/guigall)
