import oracledb

ORACLE_USER = "rm566848"
ORACLE_PASSWORD = "270506"
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
    cur = conn.cursor()
    try:
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
        cur.close()
        conn.close()


def inserir_resultados_oracle(lista_resultados):
    conn = conectar_oracle()
    if not conn:
        print("[Oracle] Conexão falhou.")
        return
    cur = conn.cursor()
    try:
        for r in lista_resultados:
            cur.execute("""
                INSERT INTO resultados_colheita
                (brix_base, brix_meio, brix_ponta, brix_medio, indice_maturacao)
                VALUES (:1,:2,:3,:4,:5)
            """, (r["Brix Base"], r["Brix Meio"], r["Brix Ponta"], r["Brix Médio"], r["Índice de Maturação"]))
        conn.commit()
        print(f"[Oracle] {len(lista_resultados)} resultado(s) inserido(s).")
    except oracledb.Error as e:
        print(f"[Oracle] Erro ao inserir: {e}")
    finally:
        cur.close()
        conn.close()


def obter_resultados_oracle():
    conn = conectar_oracle()
    if not conn:
        return []
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, brix_base, brix_meio, brix_ponta, brix_medio, indice_maturacao FROM resultados_colheita ORDER BY id")
        return cur.fetchall()
    except oracledb.Error as e:
        print(f"[Oracle] Erro ao consultar: {e}")
        return []
    finally:
        cur.close()
        conn.close()


def remover_resultado_oracle(id_to_remove):
    conn = conectar_oracle()
    if not conn:
        return
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM resultados_colheita WHERE id = :id", {"id": id_to_remove})
        conn.commit()
        print(f"[Oracle] ID {id_to_remove} removido (se existia).")
    except oracledb.Error as e:
        print(f"[Oracle] Erro ao remover: {e}")
    finally:
        cur.close()
        conn.close()
