"""
Sistema Integrado de Brix Médio e Índice de Maturação (IM)
Versão final consolidada:
- Menu interativo
- Memória temporária (lista)
- Carregamento do JSON para memória
- Exibição com contagens (Memória / JSON / Oracle)
- Remover por local (Memória / JSON / Oracle)
- Salvar seletivo (JSON / TXT / Oracle / Tudo)
- Conexão Oracle via oracledb
"""

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import json
import os
import oracledb

# ===========================
# CONFIGURAÇÃO ORACLE
# ===========================
ORACLE_USER = "seu_usuario"
ORACLE_PASSWORD = "sua_senha"
ORACLE_DSN = "oracle.fiap.com.br:1521/ORCL"

def conectar_oracle():
    try:
        conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN)
        return conn
    except oracledb.Error as e:
        print(f"[Oracle] Erro ao conectar: {e}")
        return None

def criar_tabela_oracle():
    conn = conectar_oracle()
    if not conn:
        return
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("""
        BEGIN
            EXECUTE IMMEDIATE '
                CREATE TABLE resultados_colheita (
                    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    brix_base NUMBER(7,2),
                    brix_meio NUMBER(7,2),
                    brix_ponta NUMBER(7,2),
                    brix_medio NUMBER(7,2),
                    indice_maturacao NUMBER(7,2)
                )';
        EXCEPTION
            WHEN OTHERS THEN
                IF SQLCODE != -955 THEN RAISE; END IF;
        END;
        """)
        conn.commit()
    except oracledb.Error as e:
        print(f"[Oracle] Erro ao criar tabela: {e}")
    finally:
        if cur:
            cur.close()
        conn.close()

def inserir_resultados_oracle(lista_resultados):
    """Insere uma lista de dicionários no Oracle."""
    conn = conectar_oracle()
    if not conn:
        print("[Oracle] Conexão falhou. Não foi possível salvar no Oracle.")
        return
    cur = None
    try:
        cur = conn.cursor()
        for r in lista_resultados:
            cur.execute("""
                INSERT INTO resultados_colheita
                (brix_base, brix_meio, brix_ponta, brix_medio, indice_maturacao)
                VALUES (:1,:2,:3,:4,:5)
            """, (r["Brix Base"], r["Brix Meio"], r["Brix Ponta"], r["Brix Médio"], r["Índice de Maturação"]))
        conn.commit()
        print(f"[Oracle] {len(lista_resultados)} resultado(s) inserido(s) com sucesso.")
    except oracledb.Error as e:
        print(f"[Oracle] Erro ao inserir: {e}")
    finally:
        if cur:
            cur.close()
        conn.close()

def obter_resultados_oracle():
    """Retorna lista de tuplas com rows (id, brix_base, ...). Não imprime."""
    conn = conectar_oracle()
    if not conn:
        return []
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, brix_base, brix_meio, brix_ponta, brix_medio, indice_maturacao FROM resultados_colheita ORDER BY id")
        rows = cur.fetchall()
        return rows
    except oracledb.Error as e:
        print(f"[Oracle] Erro ao consultar: {e}")
        return []
    finally:
        if cur:
            cur.close()
        conn.close()

def listar_resultados_oracle():
    rows = obter_resultados_oracle()
    if not rows:
        print("Nenhum resultado no Oracle.")
        return rows
    print("\n=== Resultados no Oracle ===")
    for row in rows:
        print(f"ID {int(row[0])}: Base={row[1]}, Meio={row[2]}, Ponta={row[3]}, Médio={row[4]}, IM={row[5]}")
    return rows

# ===========================
# CÁLCULO Brix e IM
# ===========================
def calcular_brix_medio(leituras):
    return sum(leituras) / len(leituras)

def calcular_indice_maturacao(brix_base, brix_ponta):
    if brix_base == 0:
        return 0.0
    return (brix_ponta / brix_base) * 100.0

def procedimento_calculo():
    try:
        brix_base = float(input("Brix Base: "))
        brix_meio = float(input("Brix Meio: "))
        brix_ponta = float(input("Brix Ponta: "))
    except ValueError:
        print("Entrada inválida. Use números (ex: 12.5).")
        return None

    leituras = (brix_base, brix_meio, brix_ponta)
    brix_medio = calcular_brix_medio(leituras)
    indice = calcular_indice_maturacao(brix_base, brix_ponta)

    resultado = {
        "Brix Base": round(brix_base, 2),
        "Brix Meio": round(brix_meio, 2),
        "Brix Ponta": round(brix_ponta, 2),
        "Brix Médio": round(brix_medio, 2),
        "Índice de Maturação": round(indice, 2)
    }
    return resultado

# ===========================
# MANIPULAÇÃO ARQUIVOS
# ===========================
JSON_FILE = "resultados_colheita.json"
TXT_FILE = "resultados_colheita.txt"

def carregar_json(arquivo=JSON_FILE):
    if not os.path.exists(arquivo):
        return []
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            data = json.load(f)
        # garante dicionários
        clean = []
        for item in data:
            if isinstance(item, dict):
                clean.append(item)
            else:
                try:
                    # tenta desserializar string-JSON caso exista
                    parsed = json.loads(item)
                    if isinstance(parsed, dict):
                        clean.append(parsed)
                except Exception:
                    pass
        return clean
    except Exception as e:
        print(f"Erro ao carregar JSON: {e}")
        return []

def salvar_json(lista_resultados, arquivo=JSON_FILE):
    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(lista_resultados, f, ensure_ascii=False, indent=4)
        print(f"[Arquivo] {len(lista_resultados)} resultado(s) salvo(s) em '{arquivo}'.")
    except Exception as e:
        print(f"Erro ao salvar JSON: {e}")

def salvar_txt(lista_resultados, arquivo=TXT_FILE):
    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            for r in lista_resultados:
                for k, v in r.items():
                    f.write(f"{k}: {v}\n")
                f.write("\n")
        print(f"[Arquivo] {len(lista_resultados)} resultado(s) salvo(s) em '{arquivo}'.")
    except Exception as e:
        print(f"Erro ao salvar TXT: {e}")

def carregar_json_na_memoria(memoria):
    lista = carregar_json()
    if not lista:
        print("Nenhum resultado no JSON para carregar.")
        return
    memoria.extend(lista)
    print(f"{len(lista)} resultado(s) carregado(s) do JSON para a memória.")

# ===========================
# UTILITÁRIOS / RESUMO
# ===========================
def contar_resultados(memoria):
    memoria_count = len(memoria)
    json_count = len(carregar_json())
    oracle_rows = obter_resultados_oracle()
    oracle_count = len(oracle_rows)
    print("\n--- Resumo de Resultados ---")
    print(f"Memória: {memoria_count}")
    print(f"JSON  : {json_count}")
    print(f"Oracle: {oracle_count}")
    print("----------------------------\n")



def prever_momento_colheita(memoria):
    print("\n--- PREVISÃO DE MOMENTO IDEAL DE COLHEITA ---")

    if not memoria:
        print("Nenhum dado disponível para previsão.")
        return

    # Simulando que cada entrada na memória representa uma coleta diária
    dias = np.arange(len(memoria))
    brix_values = [r.get("brix", 0) for r in memoria]
    im_values = [r.get("IM", 0) for r in memoria]

    # Ajuste de regressão polinomial de grau 2 (curva suave)
    coef_brix = np.polyfit(dias, brix_values, 2)
    coef_im = np.polyfit(dias, im_values, 2)

    poly_brix = np.poly1d(coef_brix)
    poly_im = np.poly1d(coef_im)

    # Previsão futura
    dias_futuros = np.linspace(0, len(memoria) + 10, 100)
    previsao_brix = poly_brix(dias_futuros)
    previsao_im = poly_im(dias_futuros)

    # Determinar o ponto mais próximo da maturação ideal
    for i, (b, im) in enumerate(zip(previsao_brix, previsao_im)):
        if b >= 18 and 0.95 <= im <= 1.05:
            dias_para_colheita = i - len(memoria)
            data_prevista = datetime.now() + timedelta(days=dias_para_colheita)
            print(f"\n📅 Previsão: A cana deve atingir o ponto ideal em aproximadamente {dias_para_colheita} dias.")
            print(f"Data estimada da colheita: {data_prevista.strftime('%d/%m/%Y')}")
            break
    else:
        print("\n⚠️ Nenhum ponto ideal previsto nos próximos 10 dias.")

def gerar_grafico(memoria):
    print("\n--- GRÁFICO DE EVOLUÇÃO DO BRIX E IM ---")

    if not memoria:
        print("Nenhum dado disponível para gerar gráfico.")
        return

    dias = np.arange(1, len(memoria) + 1)
    brix_values = [r.get("brix", 0) for r in memoria]
    im_values = [r.get("IM", 0) for r in memoria]

    plt.figure(figsize=(10, 6))
    plt.plot(dias, brix_values, marker='o', label="Brix (°)")
    plt.plot(dias, im_values, marker='x', label="Índice de Maturação (IM)")

    plt.axhline(18, color='green', linestyle='--', label="Brix ideal (18°)")
    plt.axhline(1.0, color='orange', linestyle='--', label="IM ideal (1.0)")

    plt.title("Evolução do Brix e Índice de Maturação da Cana-de-Açúcar")
    plt.xlabel("Dias de amostragem")
    plt.ylabel("Valor medido")
    plt.legend()
    plt.grid(True)
    plt.show()

def momento_ideal_colheita(memoria):
    print("\n--- ANÁLISE DE MOMENTO IDEAL DE COLHEITA ---")
    if not memoria:
        print("Nenhum dado disponível na memória.")
        return

    colheitas_ideais = []
    verdes = []
    supermaturas = []

    for r in memoria:
        brix = r.get("brix", 0)
        im = r.get("IM", 0)

        if brix >= 18 and 0.95 <= im <= 1.05:
            colheitas_ideais.append(r)
        elif im < 0.95:
            verdes.append(r)
        elif im > 1.05:
            supermaturas.append(r)

    print("\nResultados classificados:")
    print("-" * 40)

    if colheitas_ideais:
        print("\n✅ Cana pronta para colheita:")
        for r in colheitas_ideais:
            print(f"  Brix: {r['brix']} | IM: {r['IM']}")
    else:
        print("\n⚠️ Nenhum lote ideal para colheita no momento.")

    if verdes:
        print("\n🌱 Cana ainda verde:")
        for r in verdes:
            print(f"  Brix: {r['brix']} | IM: {r['IM']}")

    if supermaturas:
        print("\n🥀 Cana supermatura (risco de degradação):")
        for r in supermaturas:
            print(f"  Brix: {r['brix']} | IM: {r['IM']}")

    print("-" * 40)

# ===========================
# SUBMENUS DE EXIBIÇÃO & AÇÕES
# ===========================
def exibir_resultados_submenu(memoria):
    while True:
        contar_resultados(memoria)
        print("""--- EXIBIR RESULTADOS ---
1. Memória
2. JSON
3. Oracle
4. Voltar""")
        opc = input("Escolha: ").strip()
        if opc == "1":
            if not memoria:
                print("Memória vazia.")
            else:
                print("\n=== Resultados em Memória ===")
                for i, r in enumerate(memoria, start=1):
                    print(f"ID {i}: Base={r['Brix Base']}, Meio={r['Brix Meio']}, Ponta={r['Brix Ponta']}, Médio={r['Brix Médio']}, IM={r['Índice de Maturação']}")
        elif opc == "2":
            lista = carregar_json()
            if not lista:
                print("JSON vazio.")
            else:
                print("\n=== Resultados no JSON ===")
                for i, r in enumerate(lista, start=1):
                    print(f"ID {i}: Base={r['Brix Base']}, Meio={r['Brix Meio']}, Ponta={r['Brix Ponta']}, Médio={r['Brix Médio']}, IM={r['Índice de Maturação']}")
        elif opc == "3":
            listar_resultados_oracle()
        elif opc == "4":
            break
        else:
            print("Opção inválida.")

def remover_resultado(memoria):
    contar_resultados(memoria)
    print("""De onde deseja remover?
1. Memória
2. JSON
3. Oracle
4. Cancelar""")
    opc = input("Escolha: ").strip()
    if opc == "1":
        if not memoria:
            print("Memória vazia.")
            return
        for i, r in enumerate(memoria, start=1):
            print(f"ID {i}: Base={r['Brix Base']}, Meio={r['Brix Meio']}, Ponta={r['Brix Ponta']}, IM={r['Índice de Maturação']}")
        try:
            idx = int(input("Digite o ID para remover: "))
            if 1 <= idx <= len(memoria):
                memoria.pop(idx-1)
                print("Removido da memória.")
            else:
                print("ID inválido.")
        except ValueError:
            print("Digite um número válido.")
    elif opc == "2":
        lista = carregar_json()
        if not lista:
            print("JSON vazio.")
            return
        for i, r in enumerate(lista, start=1):
            print(f"ID {i}: Base={r['Brix Base']}, Meio={r['Brix Meio']}, Ponta={r['Brix Ponta']}, IM={r['Índice de Maturação']}")
        try:
            idx = int(input("Digite o ID para remover do JSON: "))
            if 1 <= idx <= len(lista):
                lista.pop(idx-1)
                salvar_json(lista)
                print("Removido do JSON.")
            else:
                print("ID inválido.")
        except ValueError:
            print("Digite um número válido.")
    elif opc == "3":
        rows = listar_resultados_oracle()
        if not rows:
            return
        try:
            id_to_remove = int(input("Digite o ID (campo 'id') do Oracle para remover: "))
            conn = conectar_oracle()
            if not conn:
                return
            cur = conn.cursor()
            cur.execute("DELETE FROM resultados_colheita WHERE id = :id", {"id": id_to_remove})
            conn.commit()
            print("Comando enviado: remoção do Oracle (se existia).")
        except ValueError:
            print("Digite um número válido.")
        except oracledb.Error as e:
            print(f"[Oracle] Erro ao remover: {e}")
        finally:
            try:
                if cur: cur.close()
                if conn: conn.close()
            except Exception:
                pass
    elif opc == "4":
        print("Cancelado.")
    else:
        print("Opção inválida.")

def salvar_resultados(memoria):
    contar_resultados(memoria)
    if not memoria:
        print("Memória vazia. Nada a salvar.")
        return
    print("""Onde deseja salvar?
1. JSON
2. TXT
3. Oracle
4. Tudo (JSON + TXT + Oracle)
5. Cancelar""")
    opc = input("Escolha: ").strip()
    if opc == "1":
        salvar_json(memoria)
    elif opc == "2":
        salvar_txt(memoria)
    elif opc == "3":
        inserir_resultados_oracle(memoria)
    elif opc == "4":
        salvar_json(memoria)
        salvar_txt(memoria)
        inserir_resultados_oracle(memoria)
    elif opc == "5":
        print("Operação cancelada.")
    else:
        print("Opção inválida.")

# ===========================
# MENU PRINCIPAL
# ===========================
def menu():
    criar_tabela_oracle()
    memoria = []
    while True:
        contar_resultados(memoria)
        print("""
        ==============================
        SISTEMA AGRÍCOLA INTEGRADO
        ==============================
        1. Adicionar Novo Resultado (Brix e IM)
        2. Exibir Resultados
        3. Remover Resultado
        4. Carregar resultados do JSON para Memória
        5. Salvar Resultados
        6. Analisar Momento Ideal de Colheita
        7. Prever Data Ideal de Colheita
        8. Gerar Gráfico de Evolução
        9. Sair
        ==============================
        """)

        opc = input("Escolha: ").strip()
        if opc == "1":
            r = procedimento_calculo()
            if r:
                memoria.append(r)
                print("Resultado adicionado à memória.")
        elif opc == "2":
            exibir_resultados_submenu(memoria)
        elif opc == "3":
            remover_resultado(memoria)
        elif opc == "4":
            carregar_json_na_memoria(memoria)
        elif opc == "5":
            salvar_resultados(memoria)
        elif opc == "6":
            momento_ideal_colheita(memoria)
        elif opc == "7":
            prever_momento_colheita(memoria)
        elif opc == "8":
            gerar_grafico(memoria)
        elif opc == "9":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
