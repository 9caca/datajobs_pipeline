import streamlit as st
import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Conecte-se ao banco de dados
conn = psycopg2.connect(
    host= "localhost",
    port="5432",
    database= os.getenv("POSTGRES_DB"),
    user= os.getenv("POSTGRES_USER"),
    password= os.getenv("POSTGRES_PASSWORD")
)

# Consulte as vagas
query = "SELECT * FROM jobs;"
df = pd.read_sql(query, conn)

# Crie o dashboard
st.title("Dashboard de Vagas de Emprego")
st.write("Aqui estão as vagas coletadas:")
st.dataframe(df)