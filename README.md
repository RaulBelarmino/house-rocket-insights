# House Rocket Insights
![HR](https://user-images.githubusercontent.com/75793555/124668465-484eb100-de87-11eb-9cb4-47c956668b80.png)

Este é um projeto fictício. A empresa, o contexto e as perguntas de negócios não são reais. Este portfólio está seguindo as recomendações do blog [Seja um Data Scientist](https://sejaumdatascientist.com/os-5-projetos-de-data-science-que-fara-o-recrutador-olhar-para-voce/).

*logo criada é fictícia.*

## 1.Descrição
A House Rocket é uma empresa do ramo imobiliário que trabalha com compra e venda de imóveis. Onde busca boas oportunidades de negócio, afim de obter lucro. Neste sentido, o Cientista de dados da empresa, tem como objetivo ajudar a House Rocket a encontrar os melhores negócios. 
Os atributos das casas, às tornam mais atrativas, ou seja, a estratégia é encontrar imóveis com bons atributos, com preço abaixo do valor de mercado e revendê-las com uma margem de lucro praticável. Questões para serem respondidas:

**1)**	Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?

**2)**	Uma vez a casa em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?

**Deploy do projeto na plataforma do Streamlit:**

[<img alt="Streamlit App" src="https://camo.githubusercontent.com/767be70c92254555bd347ab07908fec67854c2264b77702581bd230fd7eac54f/68747470733a2f2f7374617469632e73747265616d6c69742e696f2f6261646765732f73747265616d6c69745f62616467655f626c61636b5f77686974652e737667"/>](https://share.streamlit.io/raulbelarmino/house-rocket-insights/main/house-rocket-insights.py)

## 2. Atributos dos dados
Os dados para este projeto podem ser encontrados no [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction/discussion/207885) 

Abaixo segue a definição para cada um dos 21 atributos:

|    Atributos    |                         Significado                          |
| :-------------: | :----------------------------------------------------------: |
|       id        |       Numeração única de identificação de cada imóvel        |
|      date       |                    Data da venda da casa                     |
|      price      |    Preço que a casa está sendo vendida pelo proprietário     |
|    bedrooms     |                      Número de quartos                       |
|    bathrooms    | Número de banheiros (0.5 = banheiro em um quarto, mas sem chuveiro) |
|   sqft_living   | Medida (em pés quadrado) do espaço interior dos apartamentos |
|    sqft_lot     |     Medida (em pés quadrado) quadrada do espaço terrestre     |
|     floors      |                 Número de andares do imóvel                  |
|   waterfront    | Variável que indica a presença ou não de vista para água (0 = não e 1 = sim) |
|      view       | Um índice de 0 a 4 que indica a qualidade da vista da propriedade. Varia de 0 a 4, onde: 0 = baixa  4 = alta |
|    condition    | Um índice de 1 a 5 que indica a condição da casa. Varia de 1 a 5, onde: 1 = baixo \|-\| 5 = alta |
|      grade      | Um índice de 1 a 13 que indica a construção e o design do edifício. Onde: 1-3 = baixo, 7 = médio e 11-13 = alta |
|  sqft_basement  | A metragem quadrada do espaço habitacional interior acima do nível do solo |
|    yr_built     |               Ano de construção de cada imóvel               |
|  yr_renovated   |                Ano de reforma de cada imóvel                 |
|     zipcode     |                         CEP da casa                          |
|       lat       |                           Latitude                           |
|      long       |                          Longitude                           |
| sqft_livining15 | Medida (em pés quadrado) do espaço interno de habitação para os 15 vizinhos mais próximo |
|   sqft_lot15    | Medida (em pés quadrado) dos lotes de terra dos 15 vizinhos mais próximo |

## 3.	Premissas de Negócio

Após pesquisas sobre fatores que tornam o imóvel mais atrativo, algumas premissas foram consideras para este projeto:

**Atributos considerados para encontrar os melhores imóveis:**

•	Localização, metragem, número de comodos, idade e condições do imóvel, e vista.

**Em relação ao dataset:**

•	A coluna price significa o preço que a casa foi / será comprada pela empresa House Rocket;

•	Valores iguais a zero no atributo yr_renovated são de imóveis nunca reformados;

•	Os valores não inteiros dos atributos bathrooms e floors foram arredondados para simplificar o projeto;

•	O imóvel registrado com valor 33 no atributo bathrooms foi considerado um erro e foi descartado das análises;

•	Os valores duplicados em ID foram removidos, mantendo apenas o valor mais recente de cada duplicata;

•	A localidade e a condição dos imóveis, foram os atributos cruciais para seleção de imóveis para compra;

•	A estação do ano foi a característica decisiva para atribuir o melhor momento para realizar um bom negócio.

## 4. Estratégia para Solução

Etapas para entendimento e solução do problema de negócio:

1)	Coleta de dados via Kaggle

3)	Entendimento de negócio

4)	Tratamento de dados

      a.	Tranformação de variáveis

      b.	Limpeza

      c.	Entendimento dos dados processados

5)	Exploração de dados

      a. Aplicação de estatística descritiva

      b. Metricas de negócio

      c. Análise e entendimento dos dados

6)	Responder problemas do negócio

7)	Resultados para o negócio

8)	Conclusão

## 5. Insights mais relevantes para o projeto:

**H4:** A mediana de preço de imóveis com 2 andares ou mais, com vista para água é 20% mais alta, que imóveis com 1 andar e com vista para água

**Verdadeiro**, imóveis com 2 andares ou mais são em média 94% mais valorizados do que imóveis single-story(casa térrea), com vista para água.

**H6:** Imóveis em más condições são 30%, mais baratos que imóveis com boas condições;

**Falso**, há diferença é de aproximadamente 60% em média.

**H9:** Imóveis de 3 quartos e 2 banheiros devem ser 10% mais caros que imóveis de 3 quartos e 1 banheiro

**Falso**, os imóveis com 3 quartos e 2 banheiro são mais caros, porém aproximadamente 29%.

## 6. Tradução dos resultados para o Negócio

O que as análises das hipóteses dizem sobre o negócio:

| Hipótese                                                     | Resultado  | Tradução para negócio                                        |
| ------------------------------------------------------------ | ---------- | ------------------------------------------------------------ |
|H1: Imóveis que possuem vista para água deveriam ser mais caros na média.|	Verdadeiro|	Investir em imóveis com vista para água.|
|H2: Imóveis com vista para água deveriam ser 50% mais caros, na média, que imóveis próximos ao lago sem vista.|	Falso|	Investir em imóveis proximos ao lago, idenpendente da vista.|
|H3: Imóveis com data de construção menor que 1955 sem renovação deveriam ser mais baratos, na média.|	Verdadeiro|	Investir em imóveis sem reforma pode ser uma oportunidade para maior lucratividade.|
|H4: A mediana de preço de imóveis com 2 andares ou mais, com vista para água deveria ser mais alta, que imóveis com 1 andar e com vista para água.|	Verdadeiro|	Investir em imóveis com dois andares ou mais, caso tenha vista para água.|
|H5: Imóveis renovados são 20% mais caros.|	Falso|	Investir em imóveis reformados, caso a média de preço seja abaixo da mediana da região.|
|H6: Imóveis em más condições devem ser mais baratos que imóveis com boas condições.|	Verdadeiro|	Não investir em imóveis em más condições, caso a mediana de preço seja maior que a mediana da região.|
|H7: Há um aumento do preço em média de 10% a cada banheiro adicional.|	Falso|	Há uma valorização de imóveis, quanto mais banheiros, demonstrando-se um bom negócio.|
|H8: Quanto maior o atributo grade do imóvel, a média de preço deve ser maior.|	Verdadeiro|	Não investir em imóveis com grade baixo.|
|H9: Imóveis de 3 quartos e 2 banheiros devem ser 10% mais caros que imóveis de 3 quartos e 1 banheiro.| Falso|	Os imóveis com 3 quartos e 2 banheiro são mais caros, porém aproximadamente 29%.|
|H10: Imóveis com porão deveriam ser mais caros que imóveis sem porão.|	Verdadeiro|	Imóveis com porão são mais valorizados, oportunidade caso o valor seja menor que a mediana da região.|

Também foi realizado um filtro para sugerir a compra dos Top 20 imóveis, por lucratividade, por baixo investimento e um Bônus de imóveis para reforma com maior lucro.

| Filtro | Investimento  | Lucro | Margem |
| ------ | ------------- | ----- | ------ |
| 1- Lucratividade| $26.404.300| $7.921.290| 30%|
| 2- Baixo Investimento| $1.950.450| $585.135| 30%|
| 3- Imóveis para reforma| $9.997.450 + $851.406 | $2.147.829| 19%|

**O valor da reforma dos imóveis para reforma, foi calculado da seguinte forma:**

8% do valor da compra de imóveis em condição 2 e 10% para imóveis em condições 1.

### **Observações**

Referente ao **filtro 1**, onde o objetivo é a margem de lucro, a concentração dos imóveis ficou em apenas uma região, podendo ser um risco de diversificação de portifólio para empresa.

Já o **filtro 2**, a margem de lucro é igual ao filtro 1, de 30%, porém o montante para investimento é menor e a relação de risco de diversificação é menos presente.

O **filtro 3 - bônus**, a margem de lucro é de 19%, menor que os outros. Contudo, a reforma pode valorizar, tendo a possibilidade de acrescentar uma margem de lucro melhor, mas o tempo para venda, pode ser maior.

## 7. Considerações Finais
O objetivo foi alcançado, pois após a criação de features como a mediana do preço do imóvel por zipcode, e a mediana do preço da região + season, e filtrando os imóveis que estão em boas condições. Foram encontradas 5172 imóveis com potencial para venda.
Com os imóveis aptos para compra, e com as medianas de preço das estações do ano por região descobertas, foi calculado o valor de venda. Caso o preço do imóvel for menor que a mediana da season + região, acrescimo de 30% no valor da compra, caso contrário o acrescimo é de 10%.

Neste sentido, resultando em uma tabela com os melhores imóveis para compra e o melhor momento para venda.

## 8. Próximos passos
Realizar uma classificação dos imóveis por atributos como: zipcode, metragems, número de comodos, vista e proximidade de entreterimento, exemplo: lagos.
Por fim, realizar a previsão da valorização do imóvel, afim de reter a venda, até o imóvel estar mais valorizado no mercado.
