import duckdb
import streamlit as st
import streamlit.components.v1 as components

db = "duck.db"
destination_table_name = "igem_parts_registry.parts"
filename = "data/processed/duck.db"

def load_file(db: str = "duck.db", duckdb_path: str = "data/processed/duck.db", table_name: str = "igem_parts_registry.parts"):
    with duckdb.connect(db) as conn:
        conn.execute(f"""SELECT * FROM duck.parts;""")
    return True

def execute_query(query: str, db: str, return_type: str = "df"):
    with duckdb.connect(db, read_only=True) as con:
        if return_type == "df":
            return con.execute(query).df()
        elif return_type == "arrow":
            return con.execute(query).arrow()
        elif return_type == "list":
            return con.execute(query).fetchall()

if __name__ == "__main__":
    st.title("iGEM Project and Parts Discovery")
    #load_file(db=db, duckdb_path=filename, table_name=destination_table_name)
    data = execute_query(f"select * from duck.parts", db=db, return_type="df")

    st.write("## Parts Table")
    st.dataframe(data.head(10), height=300)



    st.write("## Query network example")
    HtmlFile = open("figures/BBa_K3085004_subgraph.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600)
