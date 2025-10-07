import pandas as pd
import streamlit as st
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(
    page_title="Dashboard de Veículos Usados",
    layout="wide"
)

df = pd.read_csv('vehicles_final.csv') 

st.title('Análise de Mercado de Veículos Usados')

# 5. Seção do Gráfico de Dispersão (Exemplo 1: Preço vs. Idade)
st.header("Relação entre Preço, Idade e Condição")

# Cria um controle de seleção para a Condição (checkbox)
condition_list = df['condition'].unique()
selected_conditions = st.multiselect(
    'Selecione as Condições:',
    options=condition_list,
    default=condition_list
)

# Filtra o DataFrame com base nas condições selecionadas
df_filtered = df[df['condition'].isin(selected_conditions)]

# Cria o gráfico de dispersão interativo com Plotly
fig_scatter = px.scatter(
    df_filtered,
    x="age",
    y="price",
    color="condition",
    hover_data=['model_year', 'odometer', 'manufacturer'],
    title="Preço do Veículo pela Idade (filtrado por Condição)"
)

# Exibe o gráfico no Streamlit
st.plotly_chart(fig_scatter, use_container_width=True)

st.header("Distribuição de Tipos de Veículo por Fabricante")

# Cria a Tabela Pivot de Contagem (igual à que você fez no EDA)
contagem_fabricante_tipo = df.pivot_table(
    index='manufacturer', 
    columns='type', 
    values='price', 
    aggfunc='count',
    fill_value=0
)

# Cria uma nova coluna para o eixo Y
contagem_fabricante_tipo['Total'] = contagem_fabricante_tipo.sum(axis=1)

# Filtra para mostrar apenas os 20 fabricantes com mais veículos (opcional, mas limpa o gráfico)
top_manufacturers = contagem_fabricante_tipo.sort_values('Total', ascending=False).head(20).index
df_top = df[df['manufacturer'].isin(top_manufacturers)]


# Cria o gráfico de barras empilhadas com Plotly Express
fig_bar = px.histogram(
    df_top,
    x='manufacturer',
    color='type',
    title='Contagem de Veículos por Fabricante (Top 20)',
    labels={'manufacturer': 'Fabricante', 'count': 'Contagem de Veículos'},
    height=500
)

# Ajusta o layout para evitar que o rótulo do fabricante se sobreponha
fig_bar.update_xaxes(categoryorder='total descending', tickangle=45) 
fig_bar.update_layout(bargap=0.1)

# Exibe o gráfico no Streamlit
st.plotly_chart(fig_bar, use_container_width=True)

# Ajusta o layout para evitar que o rótulo do fabricante se sobreponha
fig_bar.update_xaxes(categoryorder='total descending', tickangle=45) 
# MUDE ESTA LINHA:
fig_bar.update_layout(bargap=0.4)