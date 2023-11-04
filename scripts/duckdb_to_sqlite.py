from pathlib import Path

import duckdb


def convert_sqlite_to_duckdb(sqlite_path: str, duckdb_path: str):
    """
    Converts an SQLite database to a DuckDB database.

    Parameters:
    sqlite_path (str): The file path to the source SQLite database.
    duckdb_path (str): The file path for the output DuckDB database.
    """
    # Ensure the output directory exists
    outfile = Path(duckdb_path)
    outfile.parent.mkdir(parents=True, exist_ok=True)

    # Connect to the DuckDB database
    with duckdb.connect(str(outfile)) as conn:
        try:
            # Attach the SQLite database and copy its contents to a new DuckDB table
            conn.execute(
                f"ATTACH '{sqlite_path}' AS sqlite_db; CREATE OR REPLACE TABLE parts AS SELECT * FROM sqlite_db.parts"
            )
        except duckdb.duckdb.BinderException as e:
            # Handle the exception if the table does not exist in the SQLite database
            print(f"An error occurred: {e}")
        finally:
            # Commit the transaction and close the connection
            conn.commit()


# Example usage:
# sqlite_path = "../data/raw/igem_parts_registry.sqlite"
# duckdb_path = "../data/processed/duck.db"
# convert_sqlite_to_duckdb(sqlite_path, duckdb_path)
