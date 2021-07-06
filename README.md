# House Rocket Insights
![HR](https://user-images.githubusercontent.com/75793555/124668465-484eb100-de87-11eb-9cb4-47c956668b80.png)

Este é um projeto fictício. A empresa, o contexto e as perguntas de negócios não são reais. Este portfólio está seguindo as recomendações do blog [Seja um Data Scientist](https://sejaumdatascientist.com/os-5-projetos-de-data-science-que-fara-o-recrutador-olhar-para-voce/).

*logo criada é fictícia.*

## 1.Descrição
A House Rocket é uma empresa do ramo imobiliário que trabalha com compra e venda de imóveis. Onde busca boas oportunidades de negócio, afim de obter lucro. Neste sentido, o Cientista de dados da empresa, tem como objetivo ajudar a House Rocket a encontrar os melhores negócios. 
Os atributos das casas, às tornam mais atrativas, ou seja, a estratégia é encontrar imóveis com bons atributos, com preço abaixo do valor de mercado e revendê-las com uma margem de lucro praticável. Questões para serem respondidas:

**1)**	Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?

**2)**	Uma vez a casa em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?

**Deploy do projeto na plataforma Heroku:**

[<img alt="Heroku" src="https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white"/>](https://house-rocket-rbelarmino.herokuapp.com)

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

Após algumas pesquisas sobre fatores que tornam o imóvel mais atrativo e adequação aos atributos dos dados, algumas premissas foram consideras para este projeto:

•	Fatores externos que tornam o imóvel mais atrativo são as condições do imóvel, qualidade de acabamento, localização, segurança e metragem;

•	Características como vista, número de cômodos e banheiros, possibilidade de customização, necessidade de reforma, altura do imóvel.


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

**H10:** Quanto maior o atributo grade do imóvel, a média de preço cresce 20%;

**Verdadeiro**, há média de chega a 35%, quanto maior o grade (design) do imóvel.

## 6. Tradução dos resultados para o Negócio

O que as análises das hipóteses dizem sobre o negócio:

| Hipótese                                                     | Resultado  | Tradução para negócio                                        |
| ------------------------------------------------------------ | ---------- | ------------------------------------------------------------ |
|H1: Imóveis que possuem vista para água, são 30% mais caros, na média.|	Verdadeiro|	Investir em imóveis com vista para água.|
|H2: Imóveis com data de construção menor que 1955 são 50% mais baratos, na média.|	Falsa|	Investir em imóveis independente da data de construção.|
|H3: Imóveis sem porão (sqft_lot), são 40% maiores que os imóveis com porão.|	Falsa|	Investir em imóveis independente da existência ou não de porão.|
|H4: A mediana de preço de imóveis com 2 andares ou mais, com vista para água é 20% mais alta, que imóveis com 1 andar e com vista para água.|	Verdadeiro|	Investir em imóveis com dois andares ou mais, caso tenha vista para água.|
H5: Imóveis renovados são 20% mais caros.|	Verdadeira|	Investir em imóveis reformados.|
|H6: Imóveis em más condições são 30% mais baratos que imóveis com boas condições.|	Verdadeira|	Não investir em imóveis em más condições.|
|H7: Imóveis com más condições e grade baixo são 50% mais baratos que imóveis com boas condições e grade alto.|	Verdadeira|	Investir em imóveis com boas condições e grade alto.|
|H8: Há um aumento do preço em 10% a cada banheiro adicional.|	Verdadeira|	Há uma valorização de imóveis, quanto mais banheiros, demonstrando-se um bom negócio.|
|H9: Imóveis com 3 banheiros tem um crescimento de MoM (Mounth over Mounth) de 15%.| Falsa|	Investir em meses onde o preço do imóvel é menor.|
|H10: Quanto maior o atributo grade do imóvel, a média de preço cresce 20%.|	Verdadeira|	Investir em imóveis com grade alto.|

Também foi realizado um filtro para sugerir a compra dos Top 20 imóveis, por lucratividade, por baixo investimento e um Bônus de imóveis para reforma com maior lucro.

| Filtro | Investimento  | Lucro | Margem |
| ------ | ------------- | ----- | ------ |
| Lucratividade| $26.254.300| $7.876.290| 30%|
| Baixo Investimento| $1.882.950| $564.885| 30%|
| Imóveis para reforma| $9.895.400 + $850.301 | $2.118.319| 19%|

**O valor da reforma dos imóveis para reforma, foi calculado da seguinte forma:**

8% do valor da compra de imóveis em condição 2 e 10% para imóveis em condições 1.

### **Observações**

Referente ao **filtro 1**, onde foi dada a importância para margem de lucro, a concentração dos imóveis ficou em apenas uma região, podendo ser um risco de diversificação de portifólio para empresa.

Já o **filtro 2**, a margem de lucro é igual ao filtro 1, porém o montante é menor, porém a relação de risco de diversificação é menos presente, e o investimento é baixo

O **filtro bônus**, a margem de lucro é de 19%, menor que os outros que a margem é 30%. Porém, dependendo do tipo de reforma, o imóvel pode valorizar, tendo a possibilidade de acrescentar uma margem de lucro melhor, mas o tempo para vend, pode ser maior, devido ao periodo de reforma.

## 7. Considerações Finais
O objetivo foi alcançado, pois após a criação features que são reponsáveis por apresentar os melhores imóveis para revenda. Features como a mediana do preço do imóvel por zipcode, e a mediana do preço da região + season, e filtrando os imóveis que estão em boas condições. Foram encontradas 5222 imóveis com potencial para venda.
Com os imóveis aptos para compra selecionados, e com as medianas de preço das estações do ano por região descobertas, foi calculado o valor de venda. Caso o preço do imóvel for menor que a mediana da season + região, acrescimo de 30% no valor da compra, caso contrário o acrescimo é de 10%.

Neste sentido, resultando em uma tabela com os melhores imóveis para compra e o melhor momento para venda.

## 8. Próximos passos
Realizar uma coleta de dados mais robusta, para obter dados como o bairro de cara imóvel e realizar o agrupamento por bairro de descobrir o valor mediano da localidade, para realizar a filtragem dos melhores imóveis pelo preço mediano do bairro. Por fim, realizar a previsão da valorização do imóvel, afim de reter a venda, até o imóvel estar mais valorizado no mercado.
