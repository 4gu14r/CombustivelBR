import os
import io
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

def run_combustivel_br():
    """
    Scrapes ANP fuel prices and exports a single JSON file to the /export folder.
    """
    url = "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/levantamento-de-precos-de-combustiveis-ultimas-semanas-pesquisadas"
    export_dir = "export"
    output_file = os.path.join(export_dir, "combustivel_br.json")
    
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    try:
        # 1. Scrape latest Excel link from ANP
        response = requests.get(url, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        target_link = next((a['href'] for a in soup.find_all('a', href=True) if 'resumo_semanal' in a['href']), None)

        if not target_link:
            return None, "Excel link not found on ANP page."

        # Logic to avoid re-downloading the same data
        # We store the source URL in a temporary check or just compare filenames
        file_id = target_link.split('/')[-1].replace('.xlsx', '')
        
        # 2. Download and process Excel content
        excel_content = requests.get(target_link).content
        df_raw = pd.read_excel(io.BytesIO(excel_content), sheet_name='BRASIL')

        # Find the row where the data table actually starts
        header_row_idx = next((i for i, row in df_raw.iterrows() if 'PRODUTO' in row.values), None)
        if header_row_idx is None:
            return None, "Header 'PRODUTO' not found in Excel."

        # Clean and format the dataframe
        df = pd.read_excel(io.BytesIO(excel_content), sheet_name='BRASIL', skiprows=header_row_idx + 1)
        df.columns = [str(col).strip() for col in df.columns]
        df = df.dropna(subset=['PRODUTO'])
        data_list = df.to_dict(orient='records')

        # 3. Save as a single JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=4, default=str)

        return data_list, f"File updated: {output_file} ({file_id})"

    except Exception as e:
        return None, f"Error: {str(e)}"

if __name__ == "__main__":
    extracted_data, result_msg = run_combustivel_br()