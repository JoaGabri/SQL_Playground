import streamlit as st
import pandas as pd
import sqlite3
import base64

conn = sqlite3.connect('data/world.sqlite')
c = conn.cursor()

def sql_executer(raw_code):
    c.execute(raw_code)
    data = c.fetchall()
    return data

@st.cache_data
def get_img_as_base64(file):
    with open(file, "r") as f:
        data = f.read()  # Corrigir para f.read()
        return base64.b64encode(data.encode()).decode()

img = get_img_as_base64("Component.svg")

def main():
    ## style.css method
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    bg_img = f"""
        <style>
        .css-1wrcr25 {{
            background-image: url("data:image/svg+xml;base64,{img}");

        }}
        </style>
    """
    st.markdown(bg_img, unsafe_allow_html=True)

    ##app
    st.title("SQLite Playground")
    
    menu = ["home", "about"]
    choice = st.sidebar.selectbox("menu", menu)
    
    if choice == "home":

        col1, col2 = st.columns(2)
        with col1:
            with st.form(key='query_form'):
                raw_code = st.text_area("SQL Code")
                submit_code = st.form_submit_button("Execute")

                # Table
            with col2:
                if submit_code:
                    
                    query_results = sql_executer(raw_code)
                    # Transformar a lista de resultados em um DataFrame com colunas nomeadas
                    query_df = pd.DataFrame(query_results, columns=[desc[0] for desc in c.description])
                    st.dataframe(query_df)

    else:
        st.subheader("about")
        st.write("This is a tiny project made with Streamlit and Python, creating a SQL PLAYGROUND.")
        st.write("There are three tables with a lot of information about the world. The names of the tables are:")
        st.write("- city")
        st.write("- country")
        st.write("- countrylanguage")
        st.write("Try using 'SELECT * FROM City' to see the table.")
        st.write("Made by Joa Gabri ;)")
    
if __name__ == '__main__':
    main()
