from database_oracle import criar_tabela_oracle, inserir_resultados_oracle, remover_resultado_oracle, obter_resultados_oracle
from file_manager import carregar_json, salvar_json, salvar_txt
from analytics import calcular_brix_medio, calcular_indice_maturacao, prever_momento_colheita, gerar_grafico
from utils import contar_resultados


def procedimento_calculo():
    try:
        brix_base = float(input("Brix Base: "))
        brix_meio = float(input("Brix Meio: "))
        brix_ponta = float(input("Brix Ponta: "))
    except ValueError:
        print("Entrada inválida.")
        return None

    brix_medio = calcular_brix_medio((brix_base, brix_meio, brix_ponta))
    im = calcular_indice_maturacao(brix_base, brix_ponta)

    return {
        "Brix Base": round(brix_base, 2),
        "Brix Meio": round(brix_meio, 2),
        "Brix Ponta": round(brix_ponta, 2),
        "Brix Médio": round(brix_medio, 2),
        "Índice de Maturação": round(im, 2)
    }


def menu():
    criar_tabela_oracle()
    memoria = []
    while True:
        contar_resultados(memoria)
        print("""
1. Adicionar Resultado
2. Exibir Resultados
3. Remover Resultado
4. Salvar Resultados
5. Prever Momento da Colheita
6. Gerar Gráfico
7. Sair
""")
        opc = input("Escolha: ").strip()
        if opc == "1":
            r = procedimento_calculo()
            if r:
                memoria.append(r)
        elif opc == "4":
            salvar_json(memoria)
            salvar_txt(memoria)
            inserir_resultados_oracle(memoria)
        elif opc == "5":
            prever_momento_colheita(memoria)
        elif opc == "6":
            gerar_grafico(memoria)
        elif opc == "7":
            break
        else:
            print("Opção inválida.")
