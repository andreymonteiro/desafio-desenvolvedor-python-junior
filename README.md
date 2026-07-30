# Dependency Inspector

Script que lê as dependências de um projeto Python (requirements.txt ou pyproject.toml),
busca informações de cada pacote no PyPI e no Snyk, e gera um relatório em Excel.

## Como rodar

```bash
python -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate
pip install -r requirements.txt

python main.py exemplo/requirements.txt --saida relatorio.xlsx
```

Também funciona com `pyproject.toml`:

```bash
python main.py pyproject.toml --saida relatorio.xlsx
```

## O que o relatório mostra

- Nome e versão do pacote
- Licença e data da última publicação (via API do PyPI)
- Score de segurança e quantidade de vulnerabilidades (via Snyk)
- Linhas com score abaixo de 65 ficam destacadas em vermelho

## Observações

- O Selenium precisa do Chrome instalado. A partir da versão 4.6 ele baixa o
  chromedriver sozinho, não precisa configurar nada extra.
- Os logs de cada execução ficam salvos em `logs/`.
- Se algum pacote não for encontrado no PyPI ou no Snyk, o script continua e
  preenche os campos como N/A em vez de quebrar.
