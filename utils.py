from database_oracle import obter_resultados_oracle
from file_manager import carregar_json

def contar_resultados(memoria):
    memoria_count = len(memoria)
    json_count = len(carregar_json())
    oracle_count = len(obter_resultados_oracle())
    print(f"\n--- Resultados ---\nMemória: {memoria_count}\nJSON: {json_count}\nOracle: {oracle_count}\n")
