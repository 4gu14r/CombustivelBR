# ⛽ CombustivelBR - API de Preços Semanais

![Data Sync Status](https://github.com/4gu14r/CombustivelBR/actions/workflows/file.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

O **CombustivelBR** é uma automação inteligente (ETL) que extrai, processa e disponibiliza os dados oficiais do Levantamento de Preços de Combustíveis (LPC) da **Agência Nacional do Petróleo, Gás Natural e Biocombustíveis (ANP)**.

Diferente de consultas manuais, este projeto transforma planilhas complexas em um **endpoint JSON estático**, pronto para ser consumido por aplicativos, dashboards ou outros sistemas de backend.

---

## 🚀 Como funciona o Pipeline (Data Sync)

O projeto utiliza **GitHub Actions** para garantir que os dados estejam sempre atualizados sem intervenção humana.

1.  **Trigger:** Todo sábado às 06:00 (BRT), o workflow `data sync` é iniciado.
2.  **Extraction:** O script `main.py` acessa o portal da ANP e localiza dinamicamente o link do arquivo Excel mais recente.
3.  **Transformation:** O motor **Pandas** processa a aba "BRASIL", remove ruídos de cabeçalho e limpa os dados.
4.  **Loading:** O resultado é persistido na pasta `/export` como um arquivo JSON estruturado.

---

## 📦 Consumindo a API (Endpoint Raw)

Você pode consumir os dados mais recentes diretamente através da URL Raw do GitHub. Este link é permanente e atualizado semanalmente.

**URL do Endpoint:**
`https://raw.githubusercontent.com/4gu14r/CombustivelBR/main/export/combustivel_br.json`

### Exemplo de Resposta JSON:
```json
[
    {
        "DATA INICIAL": "2026-03-15 00:00:00",
        "PRODUTO": "GASOLINA COMUM",
        "UNIDADE DE MEDIDA": "R$/l",
        "PREÇO MÉDIO REVENDA": 6.65,
        "PREÇO MÍNIMO REVENDA": 5.49,
        "PREÇO MÁXIMO REVENDA": 9.39
    }
]
```

## 🛠️ Tecnologias Utilizadas

- Python 3.10+: Linguagem base.
- Pandas & Openpyxl: Processamento de grandes volumes de dados em Excel.
- BeautifulSoup4: Web Scraping para localização de arquivos dinâmicos.
- GitHub Actions: Automação e agendamento (Cron jobs).

## 🛠️ Instalação Local (Desenvolvimento)
Caso queira rodar o extrator em sua máquina:

1. Clone o repositório:
```Bash
git clone [https://github.com/4gu14r/CombustivelBR.git](https://github.com/4gu14r/CombustivelBR.git)
```

2. Instale as dependências:
```Bash
pip install -r requirements.txt
```

3. Execute o script principal:
```Bash
python main.py
```

Os dados serão gerados na pasta `export/`.

## ⚖️ Licença e Fonte dos Dados
- **Fonte:** Agência Nacional do Petróleo, Gás Natural e Biocombustíveis (ANP).
- **Licença:** Este projeto está sob a licença MIT. Os dados extraídos são de domínio público.
---
**Disclaimer:** Este projeto não possui vínculo oficial com a ANP. É uma ferramenta de automação para facilitar o acesso a dados públicos.
