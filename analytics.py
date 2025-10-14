import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def calcular_brix_medio(leituras):
    return sum(leituras) / len(leituras)


def calcular_indice_maturacao(brix_base, brix_ponta):
    return 0.0 if brix_base == 0 else (brix_ponta / brix_base) * 100.0


def prever_momento_colheita(memoria):
    if not memoria:
        print("Sem dados para previsão.")
        return

    dias = np.arange(len(memoria))
    brix_values = [r["Brix Médio"] for r in memoria]
    im_values = [r["Índice de Maturação"] for r in memoria]

    coef_brix = np.polyfit(dias, brix_values, 2)
    coef_im = np.polyfit(dias, im_values, 2)

    poly_brix = np.poly1d(coef_brix)
    poly_im = np.poly1d(coef_im)

    dias_futuros = np.linspace(0, len(memoria) + 10, 100)
    previsao_brix = poly_brix(dias_futuros)
    previsao_im = poly_im(dias_futuros)

    for i, (b, im) in enumerate(zip(previsao_brix, previsao_im)):
        if b >= 18 and 0.95 <= im <= 1.05:
            dias_para_colheita = i - len(memoria)
            data_prevista = datetime.now() + timedelta(days=dias_para_colheita)
            print(f"A cana deve atingir o ponto ideal em {dias_para_colheita} dias ({data_prevista:%d/%m/%Y}).")
            break
    else:
        print("Nenhum ponto ideal previsto nos próximos 10 dias.")


def gerar_grafico(memoria):
    if not memoria:
        print("Sem dados para gráfico.")
        return

    dias = np.arange(1, len(memoria) + 1)
    brix_values = [r["Brix Médio"] for r in memoria]
    im_values = [r["Índice de Maturação"] for r in memoria]

    plt.plot(dias, brix_values, marker='o', label="Brix (°)")
    plt.plot(dias, im_values, marker='x', label="IM")

    plt.axhline(18, color='green', linestyle='--', label="Brix ideal (18°)")
    plt.axhline(1.0, color='orange', linestyle='--', label="IM ideal (1.0)")

    plt.title("Evolução do Brix e IM")
    plt.xlabel("Dias")
    plt.ylabel("Valor")
    plt.legend()
    plt.grid(True)
    plt.show()
