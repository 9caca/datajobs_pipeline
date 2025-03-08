import streamlit as st
import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Set the dashboard width to full screen width
st.set_page_config(layout="wide")

load_dotenv()

# Conecte-se ao banco de dados
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

# Crie o dashboard
st.title("Dashboard de Vagas de Emprego")

# Seção de Requirements
st.header("Requirements mais solicitados")

# Consulta para obter os requirements mais frequentes
requirements_query = """
SELECT r.name, r.category, COUNT(jr.job_id) as job_count
FROM requirements r
JOIN job_requirements jr ON r.id = jr.requirement_id
GROUP BY r.name, r.category
ORDER BY job_count DESC
LIMIT 20;
"""
requirements_df = pd.read_sql(requirements_query, conn)

if not requirements_df.empty:
    # Criar duas colunas para exibir gráfico e tabela
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras para os requirements mais frequentes
        st.subheader("Top Requirements")
        st.bar_chart(requirements_df.set_index('name')['job_count'])
    
    with col2:
        # Tabela com detalhes
        st.subheader("Detalhes dos Requirements")
        st.dataframe(requirements_df)
else:
    st.info("Não há requirements cadastrados ainda.")

# Seção de Tasks
st.header("Tasks mais comuns")

# Consulta para obter as tasks mais comuns
tasks_query = """
SELECT task, COUNT(job_id) as job_count
FROM job_tasks
GROUP BY task
ORDER BY job_count DESC
LIMIT 20;
"""
tasks_df = pd.read_sql(tasks_query, conn)

if not tasks_df.empty:
    # Criar duas colunas para exibir gráfico e tabela
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras para as tasks mais comuns
        st.subheader("Top Tasks")
        st.bar_chart(tasks_df.set_index('task')['job_count'])
    
    with col2:
        # Tabela com detalhes
        st.subheader("Detalhes das Tasks")
        st.dataframe(tasks_df)
else:
    st.info("Não há tasks cadastradas ainda.")

# Adicionar um separador
st.markdown("---")

# Seção de Jobs (original)
st.header("Lista de Vagas")

# Consulta melhorada para mostrar mais informações
jobs_query = """
SELECT j.id, j.title, c.name as company, j.location, j.salary_range, 
       j.date_posted, j.experience_required, j.work_setting
FROM jobs j
JOIN companies c ON j.company_id = c.id
ORDER BY j.date_posted DESC;
"""
jobs_df = pd.read_sql(jobs_query, conn)

# Adicionar filtros
col1, col2, col3 = st.columns(3)
with col1:
    if 'location' in jobs_df.columns:
        unique_locations = ['Todos'] + list(jobs_df['location'].dropna().unique())
        location_filter = st.selectbox("Filtrar por localização", unique_locations)
with col2:
    if 'work_setting' in jobs_df.columns:
        unique_settings = ['Todos'] + list(jobs_df['work_setting'].dropna().unique())
        setting_filter = st.selectbox("Filtrar por modalidade", unique_settings)
with col3:
    if 'experience_required' in jobs_df.columns:
        unique_exp = ['Todos'] + list(jobs_df['experience_required'].dropna().unique())
        exp_filter = st.selectbox("Filtrar por experiência", unique_exp)

# Aplicar filtros
filtered_df = jobs_df.copy()
if 'location' in jobs_df.columns and location_filter != 'Todos':
    filtered_df = filtered_df[filtered_df['location'] == location_filter]
if 'work_setting' in jobs_df.columns and setting_filter != 'Todos':
    filtered_df = filtered_df[filtered_df['work_setting'] == setting_filter]
if 'experience_required' in jobs_df.columns and exp_filter != 'Todos':
    filtered_df = filtered_df[filtered_df['experience_required'] == exp_filter]

# Mostrar dados
st.dataframe(filtered_df)

# Estatísticas rápidas
st.subheader("Estatísticas Rápidas")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Vagas", len(jobs_df))
col2.metric("Empresas Únicas", jobs_df['company'].nunique())
if 'location' in jobs_df.columns:
    col3.metric("Localizações", jobs_df['location'].nunique())
if 'work_setting' in jobs_df.columns:
    col4.metric("Vagas Remotas", len(jobs_df[jobs_df['work_setting'] == 'Remote']))

# Fechar a conexão
conn.close()