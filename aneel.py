

URL = "https://dadosabertos.aneel.gov.br/api/3/action/datastore_search_sql"
RESOURCEID = "b1bd71e7-d0ad-4214-9053-cbd58e9564a7"
STORE_DATA = "downloadedData"

import requests
import os
import csv
import json

def getAneelData(month: int, year: int):
        query = f"select count(\"DthAtualizaCadastralEmpreend\") as totalEmpreendimentos, \"DscClasseConsumo\", \"MdaPotenciaInstaladaKW\", \"SigUF\" "
        query += f"from \"{RESOURCEID}\" where \"AnmPeriodoReferencia\" = \'{month}/{year}\'"
        query += f" group by \"DscClasseConsumo\", \"MdaPotenciaInstaladaKW\", \"SigUF\" "
        
        # Contact API
        try:
            request = f"{URL}?sql={query}"
            response = requests.get(request)
            response.raise_for_status()
        except requests.RequestException:
            return None

        # Parse response
        try:
            quote = response.json()
            return quote["result"]["records"]
        
        except (KeyError, TypeError, ValueError):
            return None
        
def storeAneelData(month: int, year: int, data):
    
    csv_filename = f'{STORE_DATA}/{month}_{year}.csv'
    
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter=';')
        writer.writerow(data[0].keys())

        # Escreve os dados no CSV
        for item in data:
            writer.writerow(item.values())
        
    # Save data to JSON
    json_filename = f'{STORE_DATA}/{month}_{year}.json'
    with open(json_filename, 'w') as jsonfile:
        json.dump(data, jsonfile)
            
    return True

def readAneelStoredData(month: int, year: int):
    
    json_filename = f'{STORE_DATA}/{month}_{year}.json'
    
    if not (os.path.isfile(json_filename)):
        return None
    
    with open(json_filename, 'r') as jsonfile:
        return json.load(jsonfile)