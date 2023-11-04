from pathlib import Path

import duckdb
from PIL import Image

import streamlit as st
import streamlit.components.v1 as components

db = "duck.db"
destination_table_name = "igem_parts_registry.parts"
filename = "data/processed/duck.db"


def load_file(
    db: str = "duck.db",
    duckdb_path: str = "data/processed/duck.db",
    table_name: str = "igem_parts_registry.parts",
):
    with duckdb.connect(db) as conn:
        conn.execute("""SELECT * FROM duck.parts;""")
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
    # load_file(db=db, duckdb_path=filename, table_name=destination_table_name)
    data = execute_query("select * from duck.parts", db=db, return_type="df")

    st.write("## Parts Table")
    st.dataframe(data.head(10), height=300)

    st.write("## Query network example")
    HtmlFile = open(
        "streamlit/figure/BBa_K3085004_subgraph.html", "r", encoding="utf-8"
    )
    source_code = HtmlFile.read()
    components.html(source_code, height=600)

    st.write("## Data Visualization example")

    image_dir = Path("streamlit/figure")
    selection = [
        "iGEM Teams Applicants Year by Year.png",
        "iGEM 2023 Track distribution.png",
        "iGEM 2023 Country distribution.png",
        "iGEM Kind Year by Year.png",
        "iGEM 2023 Kind distribution.png",
        "iGEM Regions Year by Year.png",
        "iGEM Tracks Year by Year.png",
        "wordcloud-manufacturing.png",
        "manufacturing Keywords.png",
        "diagnostics Keywords.png",
        "wordcloud-diagnostics.png",
        "wordcloud-asia.png",
        "asia Keywords.png",
        "wordcloud-community lab.png",
        "wordcloud-high school.png",
        "policy  practices Keywords.png",
        "wordcloud-general.png",
        "General Keywords.png",
        "wordcloud-software  ai.png",
    ]
    for s in selection:
        image_file = image_dir / s
        image = Image.open(image_file)
        st.image(image, caption=image_file.stem)
