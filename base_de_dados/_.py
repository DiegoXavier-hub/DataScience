import duckdb
from pathlib import Path

pasta_raiz = Path(".")

# encontra todos os .csv recursivamente (pasta + subpastas)
csvs = list(pasta_raiz.rglob("*.csv"))
print(f"Encontrados {len(csvs)} arquivos CSV")

con = duckdb.connect()

for csv_path in csvs:
    parquet_path = csv_path.with_suffix(".parquet")

    con.sql(f"""
        COPY (SELECT * FROM read_csv('{csv_path.as_posix()}', header=true))
        TO '{parquet_path.as_posix()}' (FORMAT PARQUET)
    """)

    print(f"✓ {csv_path.name} -> {parquet_path.name}")

con.close()
print("Concluído!")