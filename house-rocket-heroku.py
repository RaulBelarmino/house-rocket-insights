import pandas           as pd
import numpy            as np
import streamlit        as st
import plotly.express   as px
import folium
import base64

import xlsxwriter
from xlsxwriter         import Workbook
from io                 import BytesIO
from PIL                import Image
from streamlit_folium   import folium_static

(pd.set_option('display.float_format', lambda x: '%.3f' % x))
st.set_page_config(layout='wide')

image=Image.open(r'C:\Users\Raul Belarmino\DataScience\HR.png')
st.sidebar.image(image,use_column_width=True,caption='House Rocket Company')

menu = st.sidebar.radio('Selecione uma das opções de página do Projeto:',
                        ('Home','Estatística Descritiva','Hipóteses','Questões de Negócio e Soluções'))
st.sidebar.write('Para mais informações sobre o projeto, acesse: '"[GitHub](https://github.com/RaulBelarmino/house-rocket-insights/)")

@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)

    return data

@st.cache(allow_output_mutation=True)
def get_data_solution(path_1):
    data = pd.read_csv(path_1)

    return data

def transform_data(data):
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')
    data = data.drop_duplicates(subset=['id'], keep='last')
    data = data.drop(15870, axis=0)

    return data

def home(data):
    link = '[Seja um Data Scientist]' \
               '(https://sejaumdatascientist.com/os-5-projetos-de-data-science-que-fara-o-recrutador-olhar-para-voce/)'

    st.markdown(
        "<h1 style='text-align: center; color: #565656; background: #FADBD8'> House Rocket - Report Analisys </h1>",
        unsafe_allow_html=True)
    st.write('Este é um projeto fictício. A empresa, o contexto e as perguntas de negócios não são reais.'
             ' Este portfólio está seguindo as recomendações do blog Seja um Data Scientist ')
    st.markdown(link, unsafe_allow_html=True)
    st.write('A House Rocket é uma empresa do ramo imobiliário que trabalha com compra e venda de imóveis. '
             'Onde busca boas oportunidades de negócio, afim de obter maior lucro. Neste sentido, o Cientista de dados '
             'da empresa, tem como objetivo ajudar a House Rocket a encontrar os melhores negócios. Os atributos das casas, às tornam mais atrativas, ou seja, a estratégia é encontrar imóveis com bons atributos, com preço abaixo do valor de mercado e revendê-las com uma margem de lucro praticável. Demandas para entrega:')

    st.write('1) Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?')
    st.write(
        '2) Uma vez a casa em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?')

    st.write('Abaixo, uma amostra do dataset original, coletado do Kaggle:')
    st.write(data.head(50))

    st.header('Premissas do Negócio')
    st.write(
        'Após algumas pesquisas sobre fatores que tornam o imóvel mais atrativo e adequação aos atributos dos dados, algumas premissas foram consideras para este projeto:')
    st.write(
        '• Fatores externos que tornam o imóvel mais atrativo são as condições do imóvel, qualidade de acabamento, localização, segurança e metragem;')
    st.write(
        '• Características como vista, número de cômodos e banheiros, possibilidade de customização, necessidade de reforma, altura do imóvel.')
    st.write('Em relação ao dataset:')
    st.write('• A coluna price significa o preço que a casa foi / será comprada pela empresa House Rocket;')
    st.write('•	Valores iguais a zero no atributo yr_renovated são de imóveis nunca reformados;')
    st.write(
        '•	Os valores não inteiros dos atributos bathrooms e floors foram arredondados para simplificar o projeto;')
    st.write(
        '•	O imóvel registrado com valor 33 no atributo bathrooms foi considerado um erro e foi descartado das análises;')
    st.write('• Os valores duplicados em ID foram removidos, mantendo apenas o valor mais recente de cada duplicata;')
    st.write(
        '• A localidade e a condição dos imóveis, foram os atributos cruciais para seleção de imóveis para compra;')
    st.write(
        '• A estação do ano foi a característica decisiva para atribuir o melhor momento para realizar um bom negócio.')

    return None

def descriptive_metrics(data):
    st.markdown(
        "<h1 style='text-align: center; color: #565656; background: #F5B7B1'> Estatística descritiva e distribuição dados </h1>",
        unsafe_allow_html=True)

    st.write('Algumas estatísticas e métricas, para melhor entendimento de negócio:')
    df = data.copy()
    df['id'] = df.astype(str)

    c1, c2 = st.beta_columns((1, 1))

    # central tendency metrics
    attributes_num = df.select_dtypes(include=['int64', 'float64'])
    df_mean = pd.DataFrame(attributes_num.apply(np.mean))
    df_median = pd.DataFrame(attributes_num.apply(np.median))

    # measures of dispersion
    df_min = pd.DataFrame(attributes_num.apply(np.min))
    df_max = pd.DataFrame(attributes_num.apply(np.max))
    df_std = pd.DataFrame(attributes_num.apply(np.std))

    statics = pd.concat([df_mean, df_median, df_min, df_max, df_std], axis=1).reset_index()
    statics.columns = ['attributes', 'mean', 'median', 'min', 'max', 'std']
    statics = statics.iloc[
              [True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False,
               True, True], :]
    c1.header('Statistcs Descriptive')
    c1.dataframe(statics, height=1000)

    # Average Metrics
    df['sqm_living'] = df['sqft_living'] / 10.764
    df['sqm_lot'] = df['sqft_lot'] / 10.764
    df['price_sqm'] = df['price'] / df['sqm_living']
    df1 = df[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    df2 = df[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df3 = df[['sqm_living', 'zipcode']].groupby('zipcode').mean().reset_index()
    df4 = df[['price_sqm', 'zipcode']].groupby('zipcode').mean().reset_index()

    # Merge
    m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    m3 = pd.merge(m2, df4, on='zipcode', how='inner')
    m3.columns = ['Zipcode', 'Total Houses', 'Price', 'M² Living', 'Price m²']

    c2.header('Average Metrics')
    c2.dataframe(m3, height=430)

    # Plots
    c1, c2 = st.beta_columns(2)
    c3, c4 = st.beta_columns(2)
    c5, c6 = st.beta_columns(2)

    fig = px.histogram(df, x='price', nbins=19)
    fig.update_layout(height=300, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c1.header('Price Distribution')
    c1.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(df, x='sqm_living', nbins=50)
    fig.update_layout(height=300, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c2.header('SQM Living Distribution')
    c2.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(df, x='condition')
    fig.update_layout(height=300, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c3.header('Condition Houses Distribution')
    c3.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(df, x='grade')
    fig.update_layout(height=300, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c4.header('Grade Design Distribution')
    c4.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(df, x='yr_built', nbins=20)
    fig.update_layout(height=300, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c5.header('Year Built Distribution')
    c5.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(df, x='bathrooms', nbins=10)
    fig.update_layout(height=300, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c6.header('Bathrooms Distribution')
    c6.plotly_chart(fig, use_container_width=True)

    return statics

def hypotheses(data):
    st.markdown(
        "<h1 style='text-align: center; color: #565656; background: #F1948A'> Hipóteses de Negócio </h1>",
        unsafe_allow_html=True)
    st.write('Apresentação das hipóteses de negócio')

    if st.checkbox('Top Insights'):
        st.markdown('**Insights mais relevantes para o projeto:**')

        st.markdown(
            '**H4:** A mediana de preço de imóveis com 2 andares ou mais, com vista para água é 20% mais alta, que imóveis com 1 andar e com vista para água')
        st.markdown(
            '**Verdadeiro**, imóveis com 2 andares ou mais são em média 94% mais valorizados do que imóveis single-story(casa térrea), com vista para água.')

        st.markdown('**H6:** Imóveis em más condições são 30%, mais baratos que imóveis com boas condições;')
        st.markdown('**Falso**, há diferença é de aproximadamente 60% em média.')

        st.markdown('**H10:** Quanto maior o atributo grade do imóvel, a média de preço cresce 20%;')
        st.markdown('**Verdadeiro**, há média de chega a 35%, quanto maior o grade (design) do imóvel.')

    df = data.copy()

    c1, c2 = st.beta_columns(2)
    c3, c4 = st.beta_columns(2)
    c5, c6 = st.beta_columns(2)
    c7, c8 = st.beta_columns(2)

    # H1
    c1.subheader('H1: Imóveis que possuem vista para água, são 30% mais caros, na média.')
    h1 = df[['waterfront', 'price']].groupby('waterfront').mean().reset_index()
    h1['waterfront'] = h1['waterfront'].apply(lambda x: 'yes' if x == 1 else 'no')

    fig = px.bar(h1, x='waterfront', y='price', color='waterfront')
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c1.plotly_chart(fig, use_container_width=True)

    # H2
    c2.subheader('H2: Imóveis com data de construção menor que 1955 são 50% mais baratos, na média.')
    h2 = df.copy()
    h2['built'] = h2['yr_built'].apply(lambda x: '<1955' if x <= 1955 else '>1955')
    h2 = h2[['built', 'price']].groupby('built').mean().reset_index()

    fig = px.bar(h2, x='built', y='price', color='built')
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c2.plotly_chart(fig, use_container_width=True)

    # H3
    c3.subheader('H3: Imóveis sem porão (sqft_lot), são 40% maiores que os imóveis com porão')
    h3 = df.copy()
    h3['basement'] = h3['sqft_basement'].apply(lambda x: True if x > 0 else False)
    h3 = h3[['basement', 'sqft_lot', 'price']].groupby('basement').median().reset_index()

    fig = px.bar(h3, x='basement', y='sqft_lot', color='basement')
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c3.plotly_chart(fig, use_container_width=True)

    # H4
    c4.subheader(
        'H4: A mediana de preço de imóveis com 2 andares ou mais, com vista para água é 20% mais alta, que imóveis com 1 andar e com vista para água')
    h4 = df.copy()
    h4['floors_type'] = h4['floors'].apply(lambda x: 'single-story' if x == 1 else 'two-story-or-more')
    h4 = h4[['floors_type', 'waterfront', 'price']].groupby(['floors_type', 'waterfront']).median().reset_index()
    h4 = h4[h4['waterfront'] == 1]

    fig = px.bar(h4, x='floors_type', y='price', color='floors_type')
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c4.plotly_chart(fig, use_container_width=True)

    # H5
    c5.subheader('H5: Imóveis renovados são 20% mais caros')
    h5 = df.copy()
    h5['renovated'] = h5['yr_renovated'].apply(lambda x: 'yes' if x > 0 else 'no')
    h5 = h5[['renovated', 'price']].groupby('renovated').mean().reset_index()

    fig = px.bar(h5, x='renovated', y='price', color='renovated')
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c5.plotly_chart(fig, use_container_width=True)

    # H6
    c6.subheader('H6: Imóveis em más condições são 30%, mais baratos que imóveis com boas condições')
    h6 = df.copy()
    h6['condition_type'] = h6['condition'].apply(lambda x: 'bad' if x <= 2 else 'good')
    h6 = h6[['condition_type', 'price']].groupby('condition_type').median().reset_index()

    fig = px.bar(h6, x='condition_type', y='price', color='condition_type')
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c6.plotly_chart(fig, use_container_width=True)

    # H7
    c7.subheader(
        'H7: Imóveis com más condições e grade baixo são 50% mais baratos que imóveis com boas condições e grade alto.')
    h7 = df.copy()
    h7['condition_type'] = h7['condition'].apply(lambda x: 'bad' if x <= 2 else 'good')
    h7['grade_design'] = h7['grade'].apply(lambda x: 'bad' if x < 6 else 'good')
    h7['renovated'] = h7['yr_renovated'].apply(lambda x: 'yes' if x > 0 else 'no')
    h7 = h7[['grade_design', 'condition_type', 'price']].groupby(
        ['condition_type', 'grade_design']).mean().reset_index()
    h7 = h7[(h7['condition_type'] == 'bad') & (h7['grade_design'] == 'bad') | (h7['condition_type'] == 'good') & (
                h7['grade_design'] == 'good')]
    h7.columns = ['condition_type', 'grade_and_condition', 'price']

    fig = px.bar(h7, x='grade_and_condition', y='price', color='grade_and_condition')
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c7.plotly_chart(fig, use_container_width=True)

    # H8
    c8.subheader('H8: Há um aumento do preço em 10% a cada banheiro adicional')
    h8 = df.copy()
    h8['bathrooms'] = h8['bathrooms'].astype('int64')
    h8 = h8[['bathrooms', 'price']].groupby('bathrooms').median().reset_index()
    p = h8[['price']].pct_change()
    p = p.fillna(0)
    p = p.reset_index()
    p.columns = ['bathrooms', 'price']

    fig = px.bar(h8, x='bathrooms', y='price', color='bathrooms')
    fig.update_layout(showlegend=False)
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c8.plotly_chart(fig, use_container_width=True)

    # H9
    st.subheader('H9: Imóveis com 3 banheiros tem um crescimento Mounth over Mounth de 15%')
    h9 = df.copy()
    h9['year_mounth'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
    h9 = h9[h9['bathrooms'] == 3][['price', 'year_mounth']]
    h9 = h9[['price', 'year_mounth']]
    h9 = h9.groupby('year_mounth').sum()
    h9 = h9.pct_change(periods=1)
    h9 = h9.fillna(0)
    h9 = h9.reset_index()
    h9['price'] = round(h9['price'], 2) * 100
    h9.columns = ['mounth', 'pct']

    fig = px.line(h9, x='mounth', y='pct')
    fig.update_layout(height=350, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    st.plotly_chart(fig, use_container_width=True)

    # H10
    st.subheader('H10: Quanto maior o atributo grade do imóvel, a média de preço cresce 20%')
    h10 = df.copy()
    h10 = h10[['grade', 'price']].groupby('grade').mean().reset_index()
    h11 = h10.copy()
    h11['grade'] = h11['grade'].astype(str)
    h10['price'] = h10['price'].pct_change()
    h10['grade'] = h10['grade'].astype(str)
    h10['price'] = round(h10['price'], 2) * 100
    h10.columns = ['grade', 'pct']

    fig = px.line(h10, x='grade', y='pct')
    fig.update_layout(height=200, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(h11, x='grade', y='price', color='grade')
    fig.update_layout(height=200, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    st.plotly_chart(fig, use_container_width=True)

    return None

def solution(data):
    st.markdown(
        "<h1 style='text-align: center; color: #FFFFFF; background: #FB6A6A'> Questões de Negócio e Soluções </h1>",
        unsafe_allow_html=True)

    st.write('O objetivo final desse projeto era responder a duas questões principais:')
    st.write('1. Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?')
    st.write('Após a criação de novas features que são reponsáveis por apresentar os melhores imóveis '
             'para revenda. Features como a mediana do preço do imóvel por zipcode, a mediana do preço'
             'da região + season, e filtrando os imóveis que estão em boas condições. Foram encontradas 5222 '
             'imóveis com potencial para venda')

    data['marker_color'] = ''
    for i, row in data.iterrows():
        if (row['status'] == 'buy'):
            data.loc[i, 'marker_color'] = 'green'
        else:
            data.loc[i, 'marker_color'] = 'red'

    if st.checkbox('Mostrar mapa dos imóveis para compra'):
        mapa = folium.Map(width=600, height=350,
                          location=[data['lat'].mean(),data[ 'long'].mean()],
                          default_zoom_start=30)

        features = {}

        for row in pd.unique(data['marker_color']):
            features[row] = folium.FeatureGroup(name=row)

        for index, row in data.iterrows():
            circ = folium.Circle([row['lat'], row['long']],
                                 radius=150, color=row['marker_color'], fill_color=row['marker_color'],
                                 fill_opacity=1, popup='Compra: {0}, Preço: {1}'.format(row['status'],
                                                                                        row['price']))
            circ.add_to(features[row['marker_color']])

        for row in pd.unique(data["marker_color"]):
            features[row].add_to(mapa)

        folium.LayerControl().add_to(mapa)
        folium_static(mapa)


    st.write('2. Uma vez a casa em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?')
    st.write('Com os imóveis aptos para compra selecionados, e com as medianas de preço das estações do ano por região '
             'descobertas, foi calculado o valor de venda. Caso o preço do imóvel for menor que a mediana da season'
             ' + região, acrescimo de 30% no valor da compra, caso contrário o acrescimo é de 10%.')


    st.header('Tabela com os melhores imóveis para negócio')
    df = data[['id', 'zipcode', 'season', 'price', 'price_median', 'status', 'sell_price', 'profit', 'best_season']]
    report = df[(df['best_season'] != 'no_season') & (df['status'] == 'buy')].sort_values('id', ascending=True).reset_index()
    report = report.drop('index', axis=1)
    st.write(report)
    get_df = report.copy()
    st.markdown(get_table_download_link(get_df), unsafe_allow_html=True)

    st.write('Também foi realizado um filtro para sugerir a compra dos Top 20 imóveis, por lucratividade, '
             'por baixo investimento e um Bônus de imóveis para reforma com maior ganho.')

    filter = st.radio('Selecione o filtro para sugestão:', ('Filtro 1: Lucratividade','Filtro 2: Baixo investimento','Bônus: Imóveis para Reforma com maior ganho'))

    if filter == 'Filtro 1: Lucratividade':
        report = report[(report['best_season'] != 'no_season') & (report['status'] == 'buy')].sort_values('profit', ascending=False)
        sample = report.iloc[0:21,:].copy()

        dic = {"Investimento Inicial": sample['price'].sum(), 'Lucro Esperado': sample['profit'].sum()}
        capital = pd.Series(dic).to_frame('Valor USD')
        st.table(capital)
        st.header('Tabela com Top 20 por Lucratividade')
        st.write(sample)

    if filter == 'Filtro 2: Baixo investimento':
        report = report[(report['best_season'] != 'no_season') & (report['status'] == 'buy')].sort_values('price', ascending=True)
        sample2 = report.iloc[0:21,:].copy()

        dic2 = {"Investimento Inicial": sample2['price'].sum(), 'Lucro Esperado': sample2['profit'].sum()}
        capital2 = pd.Series(dic2).to_frame('Valor USD')
        st.table(capital2)
        st.header('Baixo investimento')
        st.write(sample2)

    if filter == 'Bônus: Imóveis para Reforma com maior ganho':
        report3 = data[(data['best_season'] != 'no_season') & (data['status'] == 'dont buy')]
        report3 = report3[report3['condition'] < 3].sort_values('profit',ascending=False)
        report3 = report3[['id', 'zipcode', 'season', 'price', 'price_median', 'condition', 'sell_price', 'profit', 'best_season']]
        sample3 = report3.iloc[0:21,:].copy().reset_index()
        sample3 = sample3.drop('index', axis=1)

        for i in range(len(sample3)):
            if sample3.loc[i, 'condition'] == 2:
                sample3.loc[i, 'renovate_cost'] = sample3.loc[i, 'price'] * 0.08
            else:
                sample3.loc[i, 'renovate_cost'] = sample3.loc[i, 'price'] * 0.10

        for i in range(len(sample3)):
            sample3.loc[i, 'profit_adjusted'] = sample3.loc[i, 'profit'] - sample3.loc[i, 'renovate_cost']

        sample3 = sample3[['id', 'zipcode', 'season', 'price', 'price_median', 'condition','renovate_cost','sell_price', 'profit_adjusted', 'best_season']]

        dic3 = {"Investimento Inicial": sample3['price'].sum(),
                "Investimento em reforma": sample3['renovate_cost'].sum(), 'Lucro Esperado': sample3['profit_adjusted'].sum()}
        capital3 = pd.Series(dic3).to_frame('Valor USD')
        st.table(capital3)
        st.markdown('**O valor da reforma foi calculado da seguinte forma: **')
        st.write('8% do valor da compra de imóveis em condição 2 e 10% para imóveis em condições 1')
        st.header('Bônus: Imóveis para Reforma com maior ganho')
        st.write(sample3)

    transform_profit(data, report)

    return None

def transform_profit(data, report):
    report1 = report[(report['best_season'] != 'no_season') & (report['status'] == 'buy')].sort_values('profit',
                                                                                                      ascending=False)
    sample = report1.iloc[0:21, :].copy()

    report2 = report[(report['best_season'] != 'no_season') & (report['status'] == 'buy')].sort_values('price',
                                                                                                      ascending=True)
    sample2 = report2.iloc[0:21, :].copy()

    report3 = data[(data['best_season'] != 'no_season') & (data['status'] == 'dont buy')]
    report3 = report3[report3['condition'] < 3].sort_values('profit', ascending=False)
    report3 = report3[
        ['id', 'zipcode', 'season', 'price', 'price_median', 'condition', 'sell_price', 'profit', 'best_season']]
    sample3 = report3.iloc[0:21, :].copy().reset_index()
    sample3 = sample3.drop('index', axis=1)

    for i in range(len(sample3)):
        if sample3.loc[i, 'condition'] == 2:
            sample3.loc[i, 'renovate_cost'] = sample3.loc[i, 'price'] * 0.08
        else:
            sample3.loc[i, 'renovate_cost'] = sample3.loc[i, 'price'] * 0.10

    for i in range(len(sample3)):
        sample3.loc[i, 'profit_adjusted'] = sample3.loc[i, 'profit'] - sample3.loc[i, 'renovate_cost']

    sample3 = sample3[['id', 'zipcode', 'season', 'price', 'price_median', 'condition', 'renovate_cost', 'sell_price',
                       'profit_adjusted', 'best_season']]

    sample.reset_index(drop=True, inplace=True)
    sample2.reset_index(drop=True, inplace=True)
    sample3.reset_index(drop=True, inplace=True)

    if st.checkbox('Mostrar comparativo e observações'):
        st.subheader('Tabela comparativa')
        profits = pd.concat([sample['profit'], sample2['profit'], sample3['profit_adjusted']], axis=1)
        profits.columns = ['Filtro-1', 'Filtro-2', 'Filtro-Bônus']
        profits = pd.DataFrame(profits.sum())
        profits.columns = ['Lucro']
        st.write(profits)

        st.subheader('Observações')
        st.write('Referente ao filtro 1, onde foi dada a importância para margem de lucro, a concentração '
                 'dos imóveis ficou em apenas uma região, podendo ser um risco de diversificação de portifólio para empresa.')
        st.write('Já o filtro 2, a margem de lucro é igual ao filtro 1, porém o montante é menor, porém a '
                 'relação de risco de diversificação é menos presente, e o investimento é baixo')
        st.write('O filtro bônus, a margem de lucro é de 19%, menor que os outros que a margem é 30%. '
                 'Porém, dependendo do tipo de reforma, o imóvel pode valorizar, tendo a possibilidade de '
                 'acrescentar uma margem de lucro melhor, mas o tempo para venda, '
                 'pode ser maior, devido ao periodo de reforma.')

    return None

def to_excel(get_df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    get_df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(get_df):
    val = to_excel(get_df)
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="best-houses.xlsx">Download do arquivo em excel</a>'

if __name__ == '__main__':
    path = r'C:\Users\Raul Belarmino\DataScience\Datasets\kc_house_data.csv'
    path_1 = r'C:\Users\Raul Belarmino\DataScience\Datasets\kc_houses_solution.csv'
    data = get_data(path)
    data = transform_data(data)

    if menu == 'Home':
        home(data)

    if menu == 'Estatística Descritiva':
        descriptive_metrics(data)

    if menu == 'Hipóteses':
        hypotheses(data)

    if menu == 'Questões de Negócio e Soluções':
        data = get_data_solution(path_1)
        solution(data)


