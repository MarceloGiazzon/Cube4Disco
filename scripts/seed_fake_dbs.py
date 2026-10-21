#!/usr/bin/env python3
"""
Gera bancos de dados SQLite simulados para testes do Cube4Disco:
1. data/mock/erp_agro_legado.db (Vendas e produtos com schema estilo Protheus)
2. data/mock/balanca_romaneio.db (Recepção física e pesagem de grãos)
"""

import os
import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path("/home/marcelo/repos/Cube4Disco/data/mock")
BASE_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------
# 1. Banco ERP Legado (Faturamento de Insumos e Venda de Grãos)
# ----------------------------------------------------------------------
def seed_erp_legado():
    db_path = BASE_DIR / "erp_agro_legado.db"
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # DDL
    cur.execute("""
    CREATE TABLE SB1010 (
        B1_COD TEXT PRIMARY KEY,
        B1_DESC TEXT,
        B1_TIPO TEXT,
        B1_UM TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE SA1010 (
        A1_COD TEXT PRIMARY KEY,
        A1_NOME TEXT,
        A1_MUN TEXT,
        A1_IBGE TEXT,
        A1_EST TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE SD2010 (
        D2_DOC TEXT,
        D2_SERIE TEXT,
        D2_EMISSAO TEXT,
        D2_CLIENTE TEXT,
        D2_COD TEXT,
        D2_QUANT REAL,
        D2_TOTAL REAL,
        FOREIGN KEY(D2_COD) REFERENCES SB1010(B1_COD),
        FOREIGN KEY(D2_CLIENTE) REFERENCES SA1010(A1_COD)
    );
    """)

    # Produtos: Fertilizantes, Sementes e Grãos
    produtos = [
        ("FERT01", "ADUBO NPK 04-14-08", "INSUMO", "TON"),
        ("FERT02", "UREIA AGRICOLA 46%", "INSUMO", "TON"),
        ("DEF01", "HERBICIDA GLIFOSATO", "INSUMO", "L"),
        ("SEM01", "SEMENTE SOJA INTACTA", "INSUMO", "SAC"),
        ("GRAO01", "SOJA EM GRAO PADRAO", "COMMODITY", "SAC"),
        ("GRAO02", "MILHO EM GRAO SAFRINHA", "COMMODITY", "SAC"),
    ]
    cur.executemany("INSERT INTO SB1010 VALUES (?, ?, ?, ?);", produtos)

    # Clientes (Municípios do Agro de MT/GO/PR)
    clientes = [
        ("CLI001", "FAZENDA BOA ESPERANCA", "SORRISO", "5107925", "MT"),
        ("CLI002", "AGROPECUARIA RIO VERDE", "RIO VERDE", "5218805", "GO"),
        ("CLI003", "COOPERATIVA CASCAVEL", "CASCAVEL", "4104808", "PR"),
        ("CLI004", "FAZENDA SAO MIGUEL", "NOVA MUTUM", "5106224", "MT"),
    ]
    cur.executemany("INSERT INTO SA1010 VALUES (?, ?, ?, ?, ?);", clientes)

    # Gerar transações diárias (2023 a 2024)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    curr_date = start_date

    doc_counter = 1000
    vendas = []

    while curr_date <= end_date:
        mes = curr_date.month
        # Simula sazonalidade: adubos e sementes em Set/Out/Nov; grãos em Fev/Mar/Jun
        if mes in [8, 9, 10, 11]:  # Plantio
            prod = random.choice(["FERT01", "FERT02", "DEF01", "SEM01"])
            qtd = random.uniform(5, 50)
            valor = qtd * (3200 if "FERT" in prod else 450)
        elif mes in [2, 3, 6, 7]:   # Colheita
            prod = random.choice(["GRAO01", "GRAO02"])
            qtd = random.uniform(100, 1500)
            valor = qtd * (135 if prod == "GRAO01" else 55)
        else:
            prod = random.choice(["DEF01", "FERT02"])
            qtd = random.uniform(1, 10)
            valor = qtd * 500

        cli = random.choice(clientes)[0]
        data_str = curr_date.strftime("%Y%m%d")

        vendas.append((f"{doc_counter}", "1", data_str, cli, prod, round(qtd, 2), round(valor, 2)))
        doc_counter += 1
        curr_date += timedelta(days=random.choice([1, 2]))

    cur.executemany("INSERT INTO SD2010 VALUES (?, ?, ?, ?, ?, ?, ?);", vendas)
    conn.commit()
    conn.close()
    print(f"[OK] Banco gerado: {db_path} ({len(vendas)} registros em SD2010)")


# ----------------------------------------------------------------------
# 2. Banco Balança / Recebimento de Armazém
# ----------------------------------------------------------------------
def seed_balanca_romaneio():
    db_path = BASE_DIR / "balanca_romaneio.db"
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE tb_romaneio (
        id_romaneio INTEGER PRIMARY KEY AUTOINCREMENT,
        data_hora_entrada TEXT,
        codigo_ibge_origem TEXT,
        tipo_grao TEXT,
        peso_bruto_kg REAL,
        tara_caminhao_kg REAL,
        peso_liquido_kg REAL,
        percentual_umidade REAL,
        percentual_impureza REAL
    );
    """)

    romaneios = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    curr_date = start_date

    while curr_date <= end_date:
        # Picos de safra no recebimento
        if curr_date.month in [2, 3, 4, 6, 7]:
            cargas_dia = random.randint(3, 8)
        else:
            cargas_dia = random.randint(0, 2)

        for _ in range(cargas_dia):
            ibge = random.choice(["5107925", "5218805", "4104808", "5106224"])
            grao = "SOJA" if curr_date.month in [2, 3, 4] else "MILHO"
            peso_bruto = random.uniform(38000, 52000)
            tara = random.uniform(14000, 16000)
            liquido = peso_bruto - tara
            umidade = random.uniform(11.5, 17.0)
            impureza = random.uniform(0.8, 3.0)

            dt_full = curr_date.strftime("%Y-%m-%d %H:%M:%S")
            romaneios.append((
                dt_full, ibge, grao,
                round(peso_bruto, 1), round(tara, 1), round(liquido, 1),
                round(umidade, 2), round(impureza, 2)
            ))

        curr_date += timedelta(days=1)

    cur.executemany("""
    INSERT INTO tb_romaneio (
        data_hora_entrada, codigo_ibge_origem, tipo_grao,
        peso_bruto_kg, tara_caminhao_kg, peso_liquido_kg,
        percentual_umidade, percentual_impureza
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, romaneios)

    conn.commit()
    conn.close()
    print(f"[OK] Banco gerado: {db_path} ({len(romaneios)} registros em tb_romaneio)")


if __name__ == "__main__":
    seed_erp_legado()
    seed_balanca_romaneio()
