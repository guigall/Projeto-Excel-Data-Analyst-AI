"""
gerar_dados_exemplo.py
----------------------
Cria um conjunto de dados fictício de vendas (data/dados_exemplo.xlsx) para fins de teste.
Nenhum dado real ou confidencial é utilizado.

Execução:
    python gerar_dados_exemplo.py
"""

import os
import random
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)

# ── Configuração ──────────────────────────────────────────────────────────────
TOTAL_LINHAS = 120
CAMINHO_SAIDA = os.path.join(os.path.dirname(__file__), "data", "dados_exemplo.xlsx")

REGIOES = ["Norte", "Sul", "Leste", "Oeste", "Centro"]
CATEGORIAS = ["Eletrônicos", "Vestuário", "Alimentos", "Móveis", "Livros"]
STATUS = ["Concluído", "Pendente", "Cancelado", "Reembolsado"]
VENDEDORES = [f"Vendedor_{i:02d}" for i in range(1, 11)]

# ── Intervalo de datas ────────────────────────────────────────────────────────
DATA_INICIO = datetime(2023, 1, 1)

def data_aleatoria(inicio: datetime, dias: int = 365) -> datetime:
    return inicio + timedelta(days=random.randint(0, dias))

# ── Construção das linhas ─────────────────────────────────────────────────────
linhas = []
for i in range(1, TOTAL_LINHAS + 1):
    data_venda = data_aleatoria(DATA_INICIO)
    quantidade = random.randint(1, 50)
    preco_unitario = round(random.uniform(5.0, 500.0), 2)
    desconto = round(random.uniform(0, 0.30), 2)
    valor_total = round(quantidade * preco_unitario * (1 - desconto), 2)

    linhas.append({
        "id_pedido": f"PED-{i:04d}",
        "data_venda": data_venda.strftime("%Y-%m-%d"),
        "regiao": random.choice(REGIOES),
        "categoria": random.choice(CATEGORIAS),
        "vendedor": random.choice(VENDEDORES),
        "quantidade": quantidade,
        "preco_unitario": preco_unitario,
        "desconto": desconto,
        "valor_total": valor_total,
        "status": random.choice(STATUS),
        "avaliacao_cliente": random.choice([1, 2, 3, 4, 5, None]),  # alguns nulos
        "observacoes": random.choice(["", "", "", "Pedido prioritário", "Entrega atrasada", None]),
    })

df = pd.DataFrame(linhas)

# ── Injeção intencional de problemas de qualidade (para demonstração) ─────────

# 1. Adiciona 5 linhas completamente duplicadas
duplicadas = df.sample(5, random_state=1)
df = pd.concat([df, duplicadas], ignore_index=True)

# 2. Define alguns valores de valor_total como nulos
indices_nulos = random.sample(range(len(df)), 8)
df.loc[indices_nulos, "valor_total"] = None

# 3. Injeta um outlier em preco_unitario
df.loc[0, "preco_unitario"] = 99999.99
df.loc[0, "valor_total"] = 99999.99

# 4. Adiciona uma linha com quantidade negativa (erro de digitação)
df.loc[1, "quantidade"] = -5

# 5. Cria uma aba alternativa com tipo misto para demonstração
df_bagunca = df.copy()
df_bagunca.loc[2, "preco_unitario"] = "N/D"  # tipo misto

# ── Salvar ────────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(CAMINHO_SAIDA), exist_ok=True)

with pd.ExcelWriter(CAMINHO_SAIDA, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Vendas", index=False)
    df_bagunca.to_excel(writer, sheet_name="Vendas_Bagunca", index=False)

print(f"Dados de exemplo gravados em: {CAMINHO_SAIDA}")
print(f"  Aba 'Vendas'         : {len(df)} linhas (limpa com problemas injetados)")
print(f"  Aba 'Vendas_Bagunca' : {len(df_bagunca)} linhas (inclui coluna com tipo misto)")
