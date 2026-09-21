# Contribuindo com o Excel Data Analyst AI

Obrigado pelo interesse em contribuir! Este guia explica como participar do projeto.

---

## 📋 Pré-requisitos

- Python 3.10+
- Git

---

## 🛠️ Configuração do ambiente

```bash
# 1. Faça um fork do repositório e clone localmente
git clone https://github.com/SEU_USUARIO/Projeto-Excel-Data-Analyst-AI.git
cd Projeto-Excel-Data-Analyst-AI

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Gere a base de dados de exemplo
python gerar_dados_exemplo.py

# 4. Confirme que todos os testes passam
pytest tests/ -v
```

---

## 🔄 Fluxo de contribuição

1. Crie uma branch para sua feature ou correção:
   ```bash
   git checkout -b feat/nome-da-feature
   # ou
   git checkout -b fix/descricao-do-bug
   ```

2. Faça suas alterações seguindo as convenções do projeto

3. **Rode os testes antes de commitar** — não envie PRs com testes quebrando:
   ```bash
   pytest tests/ -v
   ```

4. Commit com mensagem descritiva:
   ```bash
   git commit -m "feat: adiciona suporte a arquivos .csv"
   ```

5. Abra um Pull Request descrevendo o que foi feito e por quê

---

## 🧪 Adicionando testes

Ao implementar algo novo, adicione testes correspondentes em `tests/`. O projeto usa `pytest` — siga o padrão dos arquivos existentes como referência.

---

## 💡 Ideias de contribuição

- Suporte a arquivos `.csv`
- Interface web simples com Streamlit
- Integração com LangChain como Tool
- Exportação de relatório em formato `.pdf`
- Suporte a múltiplas abas ao mesmo tempo

---

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a [MIT License](LICENSE).
