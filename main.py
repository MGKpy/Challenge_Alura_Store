import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide')

loja1 = pd.read_csv('loja_1.csv')
loja2 = pd.read_csv('loja_2.csv')
loja3 = pd.read_csv('loja_3.csv')
loja4 = pd.read_csv('loja_4.csv')

loja1 = pd.DataFrame(loja1)
loja2 = pd.DataFrame(loja2)
loja3 = pd.DataFrame(loja3)
loja4 = pd.DataFrame(loja4)

produtos_mais_vendidos = loja1.groupby('Produto')['Preço'].count().sort_values(ascending=False).reset_index()
produtos_mais_vendidos_fig = px.histogram(
    produtos_mais_vendidos,
    x='Preço',
    y='Produto',
    color='Produto',
    text_auto=True,
)

produtos_mais_vendidos_fig.update_traces(
    textfont_size=24,
    textangle=0,
    textposition='inside',
    cliponaxis=False,
)

produtos_mais_vendidos_fig.update_layout(showlegend=False)

col1,col2 = st.columns(2)

col1.plotly_chart(produtos_mais_vendidos_fig,use_container_width=True)