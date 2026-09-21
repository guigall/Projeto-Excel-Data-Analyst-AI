# Excel Data Analyst AI

Um assistente inteligente que lê arquivos Excel, analisa os dados, detecta inconsistências e gera relatórios estruturados — desenvolvido em Python com Pandas.

---

## Funcionalidades

- Carregamento de arquivos `.xlsx` / `.xls`
- Análise estrutural automática (contagem de linhas, tipos de colunas, nulos, duplicatas)
- Indicadores numéricos (soma, média, mínimo, máximo, desvio padrão)
- Distribuição categórica (valores únicos, top-5 frequências)
- Validação de qualidade (outliers, tipos mistos, colunas vazias, valores negativos)
- Relatório legível `.txt` + relatório estruturado `.json`
- Design modular pronto para integração com agentes de IA

---

## Estrutura do Projeto

```
excel-data-analyst-ai/
├── data/
│   └── dados_exemplo.xlsx         # Base fictícia para testes
├── src/
│   ├── loader.py                  # Leitura do arquivo
│   ├── analyzer.py                # Análise estatística
│   ├── validator.py               # Validação de qualidade
│   ├── reporter.py                # Geração de relatórios
│   └── agent.py                   # Orquestrador do pipeline
├── relatorios/                    # Relatórios gerados (conteúdo ignorado pelo git)
├── tests/                         # Testes unitários (pytest)
├── gerar_dados_exemplo.py         # Cria a base fictícia de testes
├── main.py                        # Ponto de entrada da linha de comando
└── requirements.txt
```

---

## Início Rápido

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Gerar a base fictícia de dados

```bash
python gerar_dados_exemplo.py
```

### 3. Executar a análise

```bash
# Analisar o arquivo de exemplo padrão
python main.py

# Analisar um arquivo personalizado
python main.py caminho/para/seu/arquivo.xlsx

# Analisar uma aba específica
python main.py caminho/arquivo.xlsx NomeDaAba
```

Os relatórios são salvos na pasta `relatorios/` nos formatos `.txt` e `.json`.

---

## Executar os Testes

```bash
pytest tests/ -v
```

---

## Arquitetura

| Módulo | Responsabilidade |
|---|---|
| `loader.py` | Lê `.xlsx` → `DataFrame`. Apenas leitura, sem lógica. |
| `analyzer.py` | Calcula indicadores (contagem, soma, média, mín, máx, distribuição). |
| `validator.py` | Detecta problemas de qualidade (nulos, duplicatas, outliers, tipos mistos). |
| `reporter.py` | Monta os relatórios `.txt` e `.json` a partir das saídas de análise e validação. |
| `agent.py` | Orquestra o pipeline completo. Ponto de integração futura com IA. |

---

## Integração Futura com IA

`src/agent.py` foi projetado como ponto de conexão para frameworks de agentes de IA:
- **LangChain**: encapsule `AgenteAnalise.executar()` como uma Tool
- **IBM watsonx**: exponha como função em um Assistant
- **API REST**: envolva com FastAPI para acesso via HTTP

---

## Licença

MIT
