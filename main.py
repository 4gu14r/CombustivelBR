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
        print(f"[INFO] Iniciando scraping de {url}")
        
        # 1. Scrape latest Excel link from ANP
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        target_link = next((a['href'] for a in soup.find_all('a', href=True) if 'resumo_semanal' in a['href']), None)

        if not target_link:
            error_msg = "Excel link not found on ANP page."
            print(f"[ERROR] {error_msg}")
            return None, error_msg

        print(f"[INFO] Link encontrado: {target_link}")
        
        # Logic to avoid re-downloading the same data
        file_id = target_link.split('/')[-1].replace('.xlsx', '')
        
        # 2. Download and process Excel content
        print(f"[INFO] Baixando arquivo Excel...")
        excel_content = requests.get(target_link, timeout=20).content
        df_raw = pd.read_excel(io.BytesIO(excel_content), sheet_name='BRASIL')

        # Find the row where the data table actually starts
        header_row_idx = next((i for i, row in df_raw.iterrows() if 'PRODUTO' in row.values), None)
        if header_row_idx is None:
            error_msg = "Header 'PRODUTO' not found in Excel."
            print(f"[ERROR] {error_msg}")
            return None, error_msg

        print(f"[INFO] Header encontrado no índice: {header_row_idx}")
        
        # Clean and format the dataframe
        df = pd.read_excel(io.BytesIO(excel_content), sheet_name='BRASIL', skiprows=header_row_idx + 1)
        df.columns = [str(col).strip() for col in df.columns]
        df = df.dropna(subset=['PRODUTO'])
        data_list = df.to_dict(orient='records')

        print(f"[INFO] {len(data_list)} registros processados")
        
        # 3. Save as a single JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=4, default=str)

        success_msg = f"File updated: {output_file} ({file_id})"
        print(f"[SUCCESS] {success_msg}")
        return data_list, success_msg

    except requests.exceptions.RequestException as e:
        error_msg = f"Erro na requisição HTTP: {str(e)}"
        print(f"[ERROR] {error_msg}")
        return None, error_msg
    except Exception as e:
        error_msg = f"Erro inesperado: {str(e)}"
        print(f"[ERROR] {error_msg}")
        import traceback
        traceback.print_exc()
        return None, error_msg

if __name__ == "__main__":
    print("[START] Iniciando script de sincronização de combustíveis")
    extracted_data, result_msg = run_combustivel_br()
    print(f"[RESULTADO] {result_msg}")
    print("[END] Script finalizado")