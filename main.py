import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#Configuração da página
st.set_page_config(
    page_title="DashBoards de Vendas",
    page_icon='https://i5.walmartimages.com/seo/MGK-Tickets-To-My-Downfall-Music-Performance-CD_a667eb89-32f9-4a2a-b564-cff86a18d774.c1d70ee33cdb30a4a0a4395db89c254d.jpeg?odnHeight=640&odnWidth=640&odnBg=FFFFFF',
    layout="wide"
)
def open(loja):
    df = pd.read_csv(loja)
    df = pd.DataFrame(df)
    return df


# Barra lateral
with st.sidebar:
    df = st.selectbox("Escolha a loja",options=['Loja 1','Loja 2','Loja 3','Loja 4'],index=0)
    if df == "Loja 2":
        df = open("loja_2.csv")

    elif df == "Loja 1":
        df = open("loja_1.csv")

    elif df == "Loja 3":
        df = open("loja_3.csv")

    elif df == "Loja 4":
        df = open("loja_4.csv")

    top_n = st.select_slider('Selecione o Top produtos',
                                 options=[5,10,20,30,"Todos"],
                                 )
    st.write(f"Exibindo o top {top_n} produtos mais vendidos")

vendas1 = df.groupby('Produto')['Preço'].count().reset_index(name="Quantidade")
vendas1 = vendas1.sort_values("Quantidade", ascending=False)
if top_n != "Todos":
    vendas1 = vendas1.head(top_n)

categorias1 = df.groupby("Categoria do Produto")['Produto'].count().reset_index(name="Quantidade Vendida")
categorias1 = categorias1.sort_values("Quantidade Vendida", ascending=True)

fig_vendas1 = px.bar(vendas1,
                    x='Produto',
                    y="Quantidade",
                    text="Quantidade",
                    orientation='v',
                    height=200,
                    color_discrete_sequence=['#111170'])

fig_vendas1.update_traces(
    showlegend= False,
)

fig_vendas1.update_layout(
    template="plotly_white",
    title = f"Top {top_n} produtos mais vendidos",
    font_size = 12,
    font_family = "Arial",
    showlegend = False,
    xaxis = dict(showticklabels=True),
    yaxis = dict(showticklabels=False)

)

fig_categorias1 = px.funnel(categorias1,
                            y = "Categoria do Produto",
                            x = "Quantidade Vendida",
                            color = "Categoria do Produto",
                            title="Categorias mais vendidas",
                            text = "Categoria do Produto",
                            orientation='h'
                            )

fig_categorias1.update_layout(
    template="plotly_white",
    showlegend = False,
    xaxis = dict(showticklabels=False),
    yaxis = dict(showticklabels=False),
    font_size = 18
)

fig_faturamento = go.Figure(go.Indicator(
    mode='number',
    value=df['Preço'].sum(),
    title={"text":"Faturamento Total",
            "font":{'size':16,'color':"white","family":"Arial Black"}},
    number={"font":{'size':50,"color":"#74ff73","family":"Arial"},
            'prefix':"R$"}
))

fig_faturamento.update_layout(
template="plotly_white",
height=110,
margin=dict(t=27.5, b=27.5, l=27.5, r=27.5),
paper_bgcolor="#111140",
plot_bgcolor="#111140"
)

ticket_medio = go.Figure(go.Indicator(
mode='number',
value=(df['Preço'].sum()) / df['Preço'].count(),
number={'prefix': "R$", "font": {'size': 50, "color": "red", "family":"Arial"}},
title={'text': 'Ticket Médio',
        'font':{'size':16,'color':"white", "family":"Arial Black"}}
))

ticket_medio.update_layout(
template="plotly_dark",
height=110,
margin=dict(t=27.5, b=27.5, l=27.5, r=27.5),
paper_bgcolor="#111140",  # cinza claro (fundo do "card")
plot_bgcolor="#111170"
)

notas_5 = df[df['Avaliação da compra']==5].shape[0]

fig_taxa_satisfação = go.Figure(go.Indicator(
    mode="number",
    value = float(notas_5 / df['Avaliação da compra'].count()),
    number={'valueformat': '.1%', 'font': {'size': 50,"family":"Arial",'color':'#FFD700'}},
    title={'text': "Taxa de Satisfação",
            'font':{"family":"Arial Black","color":"white",'size':16}}
))

fig_taxa_satisfação.update_layout(
    template='plotly_white',
    height=110,
    margin=dict(t=27.5,b=27.5,l=27.5,r=27.5),
    paper_bgcolor="#111140",
    plot_bgcolor='#111170'
)

media_notas = round(df.groupby('Vendedor')['Avaliação da compra'].mean().reset_index(name='Média de Avaliação'),2)
media_notas = media_notas.sort_values('Média de Avaliação',ascending=True)
fig_media = px.bar(media_notas,
                    y='Vendedor',
                    x="Média de Avaliação",
                    orientation='h',
                    text_auto=True,
                    color_discrete_sequence=['#111170'],
                    title="Média de avaliação por vendedor")

media_frete = round(df.groupby("Produto")['Frete'].mean(),2).reset_index(name="Média do Frete")
media_frete = media_frete.sort_values("Média do Frete",ascending=False)
# Filtro para selecionar a quantidade de produtos a serem exibidos
if top_n != "Todos":
    media_frete = media_frete.head(top_n)
fig_frete = px.bar(
    media_frete,
    x="Produto",
    y="Média do Frete",
    orientation="v",
    text="Média do Frete",
    title="Média de frete por produto"
)

fig_frete.update_layout(
    yaxis=dict(showticklabels=False)

)

fig_frete.update_traces(
    textposition = 'inside',
    texttemplate='R$%{text:.2f}',
    textfont = dict(size=18,family='Arial Black')

)

col1,col2,col3 = st.columns(3) # 2 primeiras colunas

col1.plotly_chart(fig_faturamento) # 1 cartão na primeira coluna

col2.plotly_chart(ticket_medio) # 1 cartão na segunda coluna

col3.plotly_chart(fig_taxa_satisfação) 

st.plotly_chart(fig_vendas1) # 1 grafico de ponta a ponta

col3,col4 = st.columns(2) # Renderizar mais colunas

col3.plotly_chart(fig_categorias1, use_container_width=True)

col4.plotly_chart(fig_media,use_container_width=True)

st.plotly_chart(fig_frete)

df[['Produto','Categoria do Produto','Preço','Data da Compra','Local da compra']]