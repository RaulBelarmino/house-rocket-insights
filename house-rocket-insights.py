import pandas           as pd
import numpy            as np
import streamlit        as st
import plotly.express   as px
import folium
import base64

import xlsxwriter
from xlsxwriter         import Workbook
from geopy.distance     import great_circle
from io                 import BytesIO
from collections        import Counter
from PIL                import Image
from streamlit_folium   import folium_static
from folium.plugins     import MarkerCluster

(pd.set_option('display.float_format', lambda x: '%.3f' % x))
st.set_page_config(layout='wide')

image=Image.open('images/HR.png')
st.sidebar.image(image,use_column_width=True,caption='House Rocket Company')

menu = st.sidebar.radio('Selecione uma das opções de página do Projeto:',
                        ('Data Overview','Insights','Business Solution'))
st.sidebar.write('Para mais informações sobre o projeto, acesse: '"[GitHub](https://github.com/RaulBelarmino/house-rocket-insights/)")

def get_data(path):
    data = pd.read_csv(path)

    return data

def get_data_clean():
    data = pd.read_csv('data_clean.csv')

    return data

def get_data_solution():
    data = pd.read_csv('kc_houses_solution.csv')

    return data

def data_overview(data):
    st.markdown(
        "<h1 style='text-align: center; color: #565656; background: #FADBD8'> Data Overview </h1>",
        unsafe_allow_html=True)

    st.write(data.head(100))

    # Overview map

    df1 = data.copy()

    # Base map
    density_map = folium.Map(location=[df1['lat'].mean(), df1['long'].mean()],
                             default_zoom_start=15)

    make_cluster = MarkerCluster().add_to(density_map)
    for name, row in df1.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Price R${0} on: {1}. Sqft: {2} \n\nId: {3} '
                            'Bedrooms: {4} Bathrooms: {5} '
                            'Year Built: {6}'.format(row['price'],
                                                     row['date'],
                                                     row['sqft_lot'],
                                                     row['id'],
                                                     row['bedrooms'],
                                                     row['bathrooms'],
                                                     row['yr_built'])).add_to(make_cluster)

    folium_static(density_map, width=865, height=400)

    # descriptive statistics
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

    return None

def hypotheses(df_clean):
    st.markdown(
        "<h1 style='text-align: center; color: #565656; background: #F1948A'> Hipóteses de Negócio </h1>",
        unsafe_allow_html=True)

    df2 = df_clean.copy()

    st.write('Apresentação das hipóteses de negócio')

    if st.checkbox('Top Insights'):
        st.markdown('**Insights mais relevantes para o projeto:**')

        st.markdown(
            '**H4:** A mediana de preço de imóveis com 2 andares ou mais, com vista para água é 20% mais alta, que imóveis com 1 andar e com vista para água')
        st.markdown(
            '**Verdadeiro**, imóveis com 2 andares ou mais são em média 94% mais valorizados do que imóveis single-story(casa térrea), com vista para água.')

        st.markdown('**H6:** Imóveis em más condições são 30%, mais baratos que imóveis com boas condições')
        st.markdown('**Falso**, há diferença é de aproximadamente 60% em média.')

        st.markdown('**H10:** Imóveis de 3 quartos e 2 banheiros devem ser 10% mais caros que imóveis de 3 quartos e 1 banheiro.')
        st.markdown('**Falso**, os imóveis com 3 quartos e 2 banheiro são mais caros, porém aproximadamente 29%.')


    c1, c2 = st.beta_columns(2)
    c3, c4 = st.beta_columns(2)
    c5, c6 = st.beta_columns(2)
    c7, c8 = st.beta_columns(2)
    c9, c10 = st.beta_columns(2)

    # H1
    c1.subheader('H1: Imóveis que possuem vista para água deveriam ser mais caros na média.')
    h1 = df2[['waterfront','price']].groupby('waterfront').median().reset_index()
    h1['waterfront'] = h1['waterfront'].apply(lambda x: 'yes' if x == 1 else 'no')

    fig = px.bar(h1, x='waterfront', y='price', color='waterfront')
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c1.plotly_chart(fig, use_container_width=True)

    # H2
    c2.subheader('H2: Imóveis com vista para água deveriam ser 50% mais caros, na média, que imóveis próximos ao lago sem vista.')
    h2 = df2.copy()
    h2['lat_long'] = h2[['lat', 'long']].apply(lambda x: str(x['lat']) + ',' + str(x['long']), axis=1)

    # lat and long of 4 spots of lake washington
    lake_tuple1 = 47.508853, -122.219156
    lake_tuple2 = 47.593199, -122.228501
    lake_tuple3 = 47.667237, -122.232624
    lake_tuple4 = 47.744864, -122.269727

    # distance from Lake in km
    h2['dist_fromlake1'] = h2['lat_long'].apply(lambda x: great_circle(lake_tuple1, x).km)
    h2['dist_fromlake2'] = h2['lat_long'].apply(lambda x: great_circle(lake_tuple2, x).km)
    h2['dist_fromlake3'] = h2['lat_long'].apply(lambda x: great_circle(lake_tuple3, x).km)
    h2['dist_fromlake4'] = h2['lat_long'].apply(lambda x: great_circle(lake_tuple4, x).km)

    h2 = h2[(h2['dist_fromlake1'] < 5) | (h2['dist_fromlake2'] < 5) | (h2['dist_fromlake3'] < 5) | (h2['dist_fromlake4'] < 5)]
    
    h2['built'] = h2['yr_built'].apply(lambda x: '<1955' if x <= 1955 else '>1955')
    h2 = h2[['waterfront','price']].groupby('waterfront').mean().reset_index()
    h2['waterfront'] = h2['waterfront'].apply(lambda x: 'yes' if x == 1 else 'no')

    fig = px.bar(h2, x='waterfront', y='price', color='waterfront')
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c2.plotly_chart(fig, use_container_width=True)

    # H3
    c3.subheader('H3: Imóveis com data de construção menor que 1955 sem renovação deveriam ser mais baratos, na média.')
    h3 = df2.copy()
    h3 = h3[['built','renovated','price']].groupby(['built','renovated']).mean().reset_index()

    fig = px.bar(h3, x='built', y='price', color='renovated', barmode='group')
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c3.plotly_chart(fig, use_container_width=True)

    # H4
    c4.subheader('H4. A mediana de preço de imóveis com 2 andares ou mais, com vista para água deveria ser mais alta, que imóveis com 1 andar e com vista para água.')
    h4 = df2.copy()
    h4 = h4[h4['waterfront'] == 1]
    h4 = h4[['floors_type','waterfront','price']].groupby(['floors_type','waterfront']).median().reset_index()

    fig = px.bar(h4, x='floors_type', y='price', color='floors_type')
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c4.plotly_chart(fig, use_container_width=True)

    # H5
    c5.subheader('H5. Imóveis renovados são 20% mais caros.')
    h5 = df2.copy()
    h5 = h5[['renovated','price']].groupby('renovated').median().reset_index()

    fig = px.bar(h5, x='renovated', y='price', color='renovated')
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c5.plotly_chart(fig, use_container_width=True)

    # H6
    c6.subheader('H6. Imóveis em más condições devem ser mais baratos que imóveis com boas condições.')
    h6 = df2.copy()
    h6 = h6[['condition_type','price']].groupby('condition_type').median().reset_index()

    fig = px.bar(h6, x='condition_type', y='price', color='condition_type')
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c6.plotly_chart(fig, use_container_width=True)

    # H7
    c7.subheader('H7. Imóveis em más condições devem ser mais baratos que imóveis com boas condições.')
    h7 = df2.copy()

    h7 = h7[['bathrooms', 'price']].groupby('bathrooms').mean().reset_index()
    pct = h7[['price']].pct_change().fillna(0).reset_index()
    pct.columns = ['bathrooms', 'price']
    p = round(pct['price'], 2)

    fig = px.bar(h7, x='bathrooms', y='price', text=p, color_discrete_sequence=px.colors.qualitative.Plotly)
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c7.plotly_chart(fig, use_container_width=True)

    # H8
    c8.subheader('H8. Quanto maior o atributo grade do imóvel, a média de preço deve ser maior.')
    h8 = df2.copy()
    h8 = h8[['grade', 'price']].groupby('grade').mean().reset_index()

    fig = px.bar(h8, x='grade', y='price', color='grade')
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c8.plotly_chart(fig, use_container_width=True)

    # H9
    c9.subheader('H9. Imóveis de 3 quartos e 2 banheiros devem ser 10% mais caros que imóveis de 3 quartos e 1 banheiro.')
    h9 = df2.copy()
    h9 = h9[(h9['bedrooms'] == 3) & (h9['bathrooms'] <= 2) ]
    h9 = h9[h9['bathrooms'] != 0]
    h9 = h9[['bathrooms', 'price']].groupby('bathrooms').mean().reset_index()

    fig = px.bar(h9, x='bathrooms', y='price', color='bathrooms')
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c9.plotly_chart(fig, use_container_width=True)

    # H10
    c10.subheader('H10. Imóveis com porão deveriam ser mais caros que imóveis sem porão.')
    h10 = df2.copy()
    h10 = h10[['basement','price']].groupby('basement').mean().reset_index()

    fig = px.bar(h10, x='basement', y='price', color='basement')
    fig.update_layout(height=430, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    c10.plotly_chart(fig, use_container_width=True)

    return None

def solution(data_solution):
    st.markdown(
        "<h1 style='text-align: center; color: #FFFFFF; background: #FB6A6A'> Business Solution </h1>",
        unsafe_allow_html=True)
    data = data_solution.copy()

    st.write('O objetivo final desse projeto era responder a duas questões principais:')
    st.write('1. Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?')
    st.write('Após a criação de novas features que são reponsáveis por apresentar os melhores imóveis '
             'para revenda. Features como a mediana do preço do imóvel por zipcode, a mediana do preço '
             ' da região + season, e filtrando os imóveis que estão em boas condições. Foram encontradas 5172 '
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

    season = data[(data['best_season'] != 'no_season') & (data['status'] == 'buy')].copy()
    season = season['best_season'].tolist()
    season = ','.join(season)
    season = season.split(',')
    season_count = Counter(season)
    season_count = pd.DataFrame(([season_count]))
    season_count = season_count.melt().sort_values('value', ascending=False)
    st.header('Qual o melhor momento para venda?')
    st.write('Referente a tabela anterior, o gráfico representa recorrência das estações como melhor período para venda.')

    fig = px.bar(season_count, x='variable', y='value', color='variable')
    fig.update_layout(height=200, margin={'l': 0, 'b': 0, 'r': 0, 't': 0})
    st.plotly_chart(fig, use_container_width=True)

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

    transform_profit(data_solution, report)

    return None

def transform_profit(data_solution, report):
    report1 = report[(report['best_season'] != 'no_season') & (report['status'] == 'buy')].sort_values('profit',
                                                                                                      ascending=False)
    sample = report1.iloc[0:21, :].copy()

    report2 = report[(report['best_season'] != 'no_season') & (report['status'] == 'buy')].sort_values('price',
                                                                                                      ascending=True)
    sample2 = report2.iloc[0:21, :].copy()

    report3 = data_solution[(data_solution['best_season'] != 'no_season') & (data_solution['status'] == 'dont buy')]
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
    path = 'kc_house_data.csv'
    data = get_data(path)

    if menu == 'Data Overview':
        data_overview(data)

    if menu == 'Insights':
        df_clean = get_data_clean()
        hypotheses(df_clean)

    if menu == 'Business Solution':
        data_solution = get_data_solution()
        solution(data_solution)


