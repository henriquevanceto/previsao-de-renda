import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

sns.set(context='talk', style='ticks')

renda = pd.read_csv(r"C:\Users\henri\OneDrive\Documentos\EBAC\Previsão de Renda\Input\previsao_de_renda.csv")

st.set_page_config(
     page_title="Previsão de Renda",
     page_icon="https://cdn-icons-png.flaticon.com/512/3444/3444339.png",
     layout="wide",
)

st.write('# Análise exploratória da previsão de renda')

renda['data_ref'] = pd.to_datetime(renda['data_ref'], format='%Y-%m-%d')

min_data = renda.data_ref.min()
max_data = renda.data_ref.max()

data_inicial = st.sidebar.date_input('Data inicial', 
               value=min_data, 
               min_value=min_data,
               max_value=max_data
)

data_final = st.sidebar.date_input('Data Final', 
               value=max_data, 
               min_value=min_data,
               max_value=max_data
)

st.write('Data inicial ', data_inicial)
st.write('Data final ', data_final)

renda = renda[(renda['data_ref'] >= pd.to_datetime(data_inicial)) & (renda['data_ref'] <= pd.to_datetime(data_final))]

with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader('Quantidade de pessoas por sexo')
        fig = px.histogram(renda, x='sexo')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader('Distribuição de pessoas por tipo de renda')
        fig = px.histogram(renda, x='tipo_renda')
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.subheader('Quantidade de pessoas que vivem em uma mesma residência')
        fig = px.histogram(renda, x='qt_pessoas_residencia')
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Média de Renda por Idade')
        
        media_renda_por_idade = renda.groupby('idade')['renda'].mean().reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=media_renda_por_idade['idade'],
            y=media_renda_por_idade['renda'],
            marker_color='#87CEEB'
        ))

        fig.update_layout(
            xaxis_title='Idade',
            yaxis_title='Média de Renda',
            template='plotly_white'
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader('Escolaridade')
        
        fig = px.pie(
            renda,
            names='educacao',
            title='Distribuição por Escolaridade',
            hole=0.3
        )

        fig.update_traces(textinfo='percent+label')

        st.plotly_chart(fig, use_container_width=True)
