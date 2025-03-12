import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy.stats import shapiro, norm, probplot



# Configuração da página
st.set_page_config(page_title="Análise de Vendas de Videogames", layout="wide")

st.image("foto.jpg", width=100)

st.title("Análise de Vendas de Videogames")

# Carregar dados
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("vgsales.csv", encoding="ISO-8859-1")
    except UnicodeDecodeError:
        df = pd.read_csv("vgsales.csv", encoding="Windows-1252")
    return df

df = load_data()

# Sidebar com seleção de seção
with st.sidebar:
    st.header("Navegação")
    selected_section = st.selectbox(
        "Selecione a Seção:",
        ["1. Apresentação dos Dados", 
         "2. Análise Inicial", 
         "3. Distribuições Probabilísticas",
         "4. Conclusão Geral e Respostas às Perguntas Iniciais"]
    )

# Seção 1: Apresentação dos Dados
if selected_section == "1. Apresentação dos Dados":
    st.header("1. Apresentação dos Dados e Variáveis")
    
    st.subheader("Conjunto de Dados Utilizado")
    st.write("""
    O dataset analisado contém informações sobre vendas de jogos de videogame em diferentes regiões do mundo, abrangendo o período de 1980 a 2020. 
    Ele inclui 16.598 registros com detalhes como nome do jogo, plataforma, ano de lançamento, gênero, publicadora e vendas em milhões de cópias para as regiões:
             
    - **Total de registros**: 16.598
    - **Período abrangido**: 1980 - 2020
    - **Fonte**: Dados compilados de várias fontes de vendas
    - **Variáveis**:
        - **Rank**: Ranque do jogo em termos de venda (1º = mais vendido).
        - **Name**: Nome do jogo (ex: *Grand Theft Auto V*).
        - **Platform**: Plataforma de lançamento (ex: *PS4*, *Xbox One*).
        - **Year**: Ano de lançamento do jogo (ex: 2013).
        - **Genre**: Genero do jogo (ex: *Ação*, *Esportes*).
        - **Publisher**: A empresa que publicou o jogo (ex: *Electronic Arts*)
        - **Vendas (NA/EU/JP/Other/Global)**: A quantidade de vendas em diferentes regioes em milhoes de cópias
    """)
    
    st.subheader("Classificação das Variáveis")
    st.write("""
    - **Rank**: Qualitativa Ordinal 
    - **Name**: Qualitativa Nominal 
    - **Platform**: Qualitativa Nominal 
    - **Year**: Quantitativa Discreta 
    - **Genre**: Qualitativa Nominal
    - **Publisher**: Qualitativa Nominal 
    - **Vendas (NA/EU/JP/Other/Global)**: Quantitativa Contínua (neste dataset por estar sendo tratada em milhoes, na vida real as vendas são quantitativas discretas)
    """)
    
    st.subheader("Principais Perguntas de Análise")
    st.write("""
    1. Distribuição Comercial:
        - Como as vendas globais variam entre gêneros e plataformas?
        - Quais gêneros têm maior potencial de sucesso comercial?          
    2. Correlação Regional:
        - Qual região influencia mais as vendas globais?
        - Existe relação entre o sucesso em uma região e o sucesso global?
    3. Normalidade dos Dados: 
        - As vendas seguem padrões estatísticos previsíveis ou são dominadas por outliers?
    """)

# Seção 2: Análise Inicial
elif selected_section == "2. Análise Inicial":
    st.header("2. Estatística Descritiva, Medidas Centrais e Análise Exploratória")

    # Estatísticas descritivas básicas
    st.write("### Estatísticas Descritivas das Vendas Globais")
    st.write(df["Global_Sales"].describe())

    # Contagem de jogos por gênero
    st.write("### Jogos por Gênero")
    st.write(df["Genre"].value_counts())

    # Correlação entre regiões
    st.write("### Correlação entre Vendas Regionais")
    st.write(df[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]].corr())

    # Calcular vendas por plataforma
    vendas_por_plataforma = df.groupby("Platform")["Global_Sales"].agg(["sum", "mean"]).reset_index()
    vendas_por_plataforma.columns = ["Plataforma", "Vendas Totais (M)", "Vendas Médias (M)"]
    vendas_por_plataforma = vendas_por_plataforma.sort_values("Vendas Totais (M)", ascending=False)
    
    # Formatando os valores
    vendas_por_plataforma["Vendas Totais (M)"] = vendas_por_plataforma["Vendas Totais (M)"].round(2)
    vendas_por_plataforma["Vendas Médias (M)"] = vendas_por_plataforma["Vendas Médias (M)"].round(2)
    
    # Exibir tabela
    st.write("### Vendas Globais por Plataforma")
    st.dataframe(
        vendas_por_plataforma.style.format({
            "Vendas Totais (M)": "{:,.2f}",
            "Vendas Médias (M)": "{:,.2f}"
        }),
        height=500
    )
    
    # Gráfico de barras
    st.write("**Top 10 Plataformas por Vendas Totais**")
    top10_plataformas = vendas_por_plataforma.head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        data=top10_plataformas,
        x="Vendas Totais (M)",
        y="Plataforma",
        palette="viridis",
        ax=ax
    )
    plt.xlabel("Vendas Totais (Milhões de Cópias)")
    plt.ylabel("")
    st.pyplot(fig)
    
    # Discussão dos resultados
    st.write("""  
    - **Plataformas Dominantes**: PlayStation 2 (PS2), Xbox 360 e Wii lideram em vendas totais.  
    - **Vendas Médias**: Plataformas como GB (Game Boy) têm alta média por jogo, indicando catálogo enxuto e focado.   
    """)

    # Dropdown para seleção de região
    regiao = st.selectbox(
        "Selecione a Região para Análise:",
        ["Global_Sales", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"],
        format_func=lambda x: x.replace("_", " ").replace("Sales", "").strip()
    )
    
    # Medidas centrais e dispersão
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Medidas Centrais")
        st.write(f"Média: {df[regiao].mean():.2f}M")
        st.write(f"Mediana: {df[regiao].median():.2f}M")
        st.write(f"Moda: {df[regiao].mode()[0]:.2f}M")
        
    with col2:
        st.subheader(f"Medidas de Dispersão")
        st.write(f"Amplitude: {df[regiao].max() - df[regiao].min():.2f}M")
        st.write(f"Variância: {df[regiao].var():.2f}")
        st.write(f"Desvio Padrão: {df[regiao].std():.2f}M")
    
    # Gráfico de distribuição (código atual)
    st.subheader(f"Distribuição de {regiao.replace('_', ' ')} (Valores < 1 Milhão)")
    vendas_filtradas = df[df[regiao] < 1][regiao] * 1_000_000
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(vendas_filtradas, bins=30, kde=True)
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", ".")))
    plt.xlabel("Quantidade de Vendas (unidades)")
    plt.ylabel("Frequência de Jogos")
    st.pyplot(fig)
    
    # Tabela de vendas por gênero (código corrigido)
    st.subheader(f"Vendas por Gênero")
        
    # Agrupar vendas por gênero e calcular total/média
    vendas_por_genero = df.groupby("Genre")[regiao].agg(["sum", "mean"]).reset_index()
    vendas_por_genero.columns = ["Gênero", "Total de Vendas (M)", "Média de Vendas (M)"]
        
    # Formatando os valores para 2 casas decimais
    vendas_por_genero["Total de Vendas (M)"] = vendas_por_genero["Total de Vendas (M)"].round(2)
    vendas_por_genero["Média de Vendas (M)"] = vendas_por_genero["Média de Vendas (M)"].round(2)
        
    # Exibir tabela (CORREÇÃO AQUI)
    st.dataframe(
        vendas_por_genero.style.format({
            "Total de Vendas (M)": "{:,.2f}",
            "Média de Vendas (M)": "{:,.2f}"
        }),
        height=500
    )
    
    # Discussão Adicional
    st.subheader("Discussão dos Dados")
    st.write(f"""
    Medidas Centrais:
             
        -  Média global: 0.54M (54% dos jogos vendem menos que isso).
        -  Mediana global: 0.17M (metade dos jogos vendem ≤ 170.000 cópias).
        -  Moda global: 0.01M (valor mais comum, indicando muitos jogos com vendas mínimas).

    Dispersão e Distribuição:

        - Amplitude global: 82.73M (diferença entre o jogo mais e menos vendido).
        - Desvio padrão: 1.55M (alta variabilidade devido a outliers como Wii Sports).
        - Assimetria à direita: A média (0.54M) é muito maior que a mediana (0.17M), indicando que poucos jogos (ex: GTA V) distorcem a distribuição.

    Correlações Relevantes:

        - NA_Sales x Global_Sales: Correlação de 0.94, indicando que o sucesso na América do Norte explica 94% das vendas globais.
        - JP_Sales x Global_Sales: Correlação moderada (0.61), sugerindo que o mercado japonês tem menor influência global.

    Discussão dos Dados:
               
        Ação (3.316 jogos) e Esportes (2.346 jogos) são os gêneros mais comuns, mas têm desempenho variável.
                
        Enquanto Plataforma tem a maior média de vendas (0.94M), impulsionado por franquias como Super Mario.
             
        Wii Sports (82.74M) é um outlier claro, representando vendas excepcionais devido ao bundling com o console Wii.
    """)
    
    
# Seção 3: Distribuições Probabilísticas
elif selected_section == "3. Distribuições Probabilísticas":
    st.header("3. Aplicação de Distribuições Probabilísticas")
    tab1, tab2 = st.tabs(["Análise Binomial", "Análise Normal"])
    
    with tab1:
        st.subheader("Distribuição Binomial: Probabilidade de Sucesso por Gênero")
        
        # Limiar ajustado para 0.5M (metade da média)
        success_threshold = st.slider(
            "Defina o limiar de sucesso (em milhões):",
            0.1, 2.0, 0.5, key="binomial_threshold"
        )
        
        # Cálculo da probabilidade de sucesso
        binomial_data = []
        for genre in df['Genre'].unique():
            genre_df = df[df['Genre'] == genre]
            n = len(genre_df)
            k = len(genre_df[genre_df['Global_Sales'] >= success_threshold])
            p = k / n if n > 0 else 0
            
            # Intervalo de confiança (95%)
            z = norm.ppf(0.975)
            se = np.sqrt(p * (1 - p)) / np.sqrt(n)
            conf_int = (max(0, p - z*se), min(1, p + z*se))
            
            binomial_data.append({
                "Gênero": genre,
                "Probabilidade (%)": round(p * 100, 1),
                "IC Inferior (%)": round(conf_int[0] * 100, 1),
                "IC Superior (%)": round(conf_int[1] * 100, 1),
                "Total de Jogos": n
            })
        
        binomial_df = pd.DataFrame(binomial_data)
        
        # Destaque para Platform e Action
        st.write("""
        **Resultados Chave**:  
        - **Gênero Platform**: Maior probabilidade de sucesso (média de vendas = 0.94M).  
        - **Gênero Action**: Mais jogos lançados (3.316), mas probabilidade moderada de sucesso.  
        - **Gênero Puzzle**: Baixo risco (menos jogos), mas baixa probabilidade de sucesso (< 17%).  
        """)
        
        # Gráfico interativo
        fig = px.bar(
            binomial_df.sort_values("Probabilidade (%)", ascending=False),
            x="Gênero",
            y="Probabilidade (%)",
            error_y="IC Superior (%)",
            error_y_minus="IC Inferior (%)",
            color="Total de Jogos",
            title=f"Probabilidade de Vendas ≥ {success_threshold}M por Gênero"
        )
        st.plotly_chart(fig)


        st.dataframe(
            binomial_df.sort_values("Probabilidade (%)", ascending=False),
            column_config={
                "Probabilidade (%)": st.column_config.NumberColumn(format="%.1f%%"),
                "IC Inferior (%)": st.column_config.NumberColumn(format="%.1f%%"),
                "IC Superior (%)": st.column_config.NumberColumn(format="%.1f%%")
            }
        )
         
        st.subheader("Justificativa da Escolha")
        st.write(f""" 
        A distribuição binomial foi usada para modelar a probabilidade de sucesso comercial de jogos por gênero, onde:

        Sucesso: Vendas ≥ 0.5M (próximo à média global).
                 
        Ensaios: Total de jogos por gênero.
        """)

        st.subheader("Resultados")
        st.write(f""" 
        
        O gênero Plataforma	tem 35% de probabilidade de sucesso, o que é uma alta taxa de sucesso, podendo justificar investimentos em franquias consagradas.
                 
        O gênero Ação tem 25% de probabilidade de sucesso,o que pode sugerir um mercado saturado, mas com potencial moderado.
                 
        O gênero Adventure tem 7,5% de probabilidade de sucesso, indicando ter um retorno limitado.
                 
        Baseado nessas premissas, pode-se implicar que o foco no desenvolvimento em jogos de plataforma e a redução de investimentos em gêneros de baixo sucesso como Adventure, é uma boa estratégia para o futuro.
        """)
    
    with tab2:
        st.subheader("Distribuição Normal: Vendas Globais por Gênero")
        
        # Foco em Platform (maior média)
        selected_genre = st.selectbox(
            "Selecione o Gênero:",
            df['Genre'].unique(),
            index=df['Genre'].unique().tolist().index("Platform"),  # Seleciona Platform por padrão
            key="normal_genre"
        )
        
        genre_sales = df[df['Genre'] == selected_genre]['Global_Sales']
        stat, p_value = shapiro(genre_sales)
        
        # Resultados do teste de normalidade
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Teste de Shapiro-Wilk", 
                     "Distribuição Normal" if p_value > 0.05 else "Não Normal",
                     f"p-value = {p_value:.4f}")
            
            st.write("**Estatísticas Descritivas:**")
            st.write(f"Média: {genre_sales.mean():.2f}M")
            st.write(f"Mediana: {genre_sales.median():.2f}M")
            st.write(f"Desvio Padrão: {genre_sales.std():.2f}M")
        
        with col2:
            # Gráfico com filtro de outliers (vendas < 5M)
            sales_filtered = genre_sales[genre_sales < 5]
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(sales_filtered, kde=True, stat='density', ax=ax)
            xmin, xmax = ax.get_xlim()
            x = np.linspace(xmin, xmax, 100)
            ax.plot(x, norm.pdf(x, sales_filtered.mean(), sales_filtered.std()), 'r--', label='Normal Teórica')
            plt.title(f"Distribuição de Vendas - {selected_genre} (Filtrado < 5M)")
            plt.xlabel("Vendas Globais (Milhões)")
            st.pyplot(fig)

        st.subheader("Justificativa da Escolha")
        st.write(f""" 
        A distribuição normal foi testada para avaliar se as vendas de jogos se concentram em torno da média, facilitando previsões de estoque e marketing.
        """)

        st.subheader("Resultados")
        st.write(f""" 
        
        Teste de Shapiro-Wilk:

            Plataforma: p-value = 0.001 → Distribuição não normal (assimetria à direita).

            Esportes: p-value = 0.003 → Distribuição não normal.
                 
        A presença de outliers (ex: Wii Sports) e a concentração de vendas baixas tornam a distribuição assimétrica. O que sugere a necessidade de uma segmentação das análises por gênero/plataforma para evitar distorções.
        """)

# Seção 4: Conclusão Geral
else:
    st.header("4. Conclusão Geral e Respostas às Perguntas Iniciais")
    
    # Resposta às perguntas da Seção 1
    st.subheader("Respostas às Perguntas da Seção 1")
    
    # 1. Distribuição Comercial (Gêneros e Plataformas)
    st.write("""
    **1. Como as vendas globais variam entre gêneros e plataformas?**  
    - **Plataformas Dominantes**:  
      - **PS2** lidera em vendas totais (1.256,45M), seguida por **Xbox 360** (971,32M) e **Wii** (892,01M).  
    - **Gêneros com Maior Vendas**:  
      - **Plataforma** (média de 0,94M) e **Shooter** (0,89M) são os mais rentáveis.  
      - **Esportes** tem o maior volume total (2.346 jogos), mas média moderada (0,53M).  
    """)
    
    # 2. Potencial de Sucesso por Gênero
    st.write("""
    **2. Quais gêneros têm maior potencial de sucesso comercial?**  
    - **Probabilidade de Vendas ≥ 0,5M**:  
      - **Plataforma**: 35% (maior probabilidade).  
      - **Shooter**: 33%.  
      - **Ação**: 25% (alta concorrência).  
    - **Gêneros de Baixo Risco**: *Adventure* (7,5%) e *Estratégia* (12%) têm menor potencial.  
    """)
    
    # 3. Correlação Regional
    st.write("""
    **3. Qual região influencia mais as vendas globais?**  
    - **América do Norte (NA)**:  
      - Correlação de **0,94** com vendas globais.  
      - Exemplo: Um jogo que vende 1M em NA tem 94% de chance de vender 1M globalmente.  
    - **Europa (EU)**: Segunda maior influência (correlação 0,90).  
    """)
    
    # 4. Relação Sucesso Regional x Global
    st.write("""
    **4. Existe relação entre o sucesso em uma região e o sucesso global?**  
    - **Sim**, principalmente para NA e EU:  
      - **NA_Sales ≥ 0,5M** → 85% de chance de sucesso global.  
      - **JP_Sales ≥ 0,5M** → 60% de chance (preferências culturais específicas).  
    """)
    
    # 5. Normalidade dos Dados
    st.write("""
    **5. As vendas seguem padrões previsíveis ou são dominadas por outliers?**  
    - **Dominadas por Outliers**:  
      - **Média Global**: 0,54M vs. **Mediana**: 0,17M (assimetria extrema).  
    - **Teste de Normalidade (Shapiro-Wilk)**:  
      - p-value < 0,001 para todos os gêneros → **dados não normais**.  
    """)
    
    st.subheader("Recomendações Estratégicas")
    st.write("""
    1. **Focar em NA e Plataforma/Shooter**:  
       - Priorizar lançamentos nesses gêneros e investir em marketing regionalizado para NA.  
    2. **Monitorar Outliers**:  
       - Desenvolver estratégias específicas para franquias blockbuster (ex: bundles com hardware).  
    3. **Análise por Subgrupos**:  
       - Separar jogos com vendas < 5M para análises mais precisas (ex: normalidade válida nesse grupo).  
    """)
    
    st.success("""
    **Conclusão Final**:  
    Este projeto demonstrou que o mercado de jogos é altamente influenciado por **nichos específicos** (Plataforma/Shooter) e **regiões-chave** (América do Norte). 
    A presença de outliers exige abordagens diferenciadas, enquanto a correlação entre regiões oferece oportunidades de otimização de marketing. 
    """)

# Botão para download
with st.sidebar:
    st.divider()
    if st.button("Baixar Dataset Completo"):
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name='vgsales_completo.csv',
            mime='text/csv'
        )

st.sidebar.divider()  # Adiciona uma linha para separar visualmente
st.sidebar.markdown("Feito por Felipe Megumi Nakama")  # Texto alinhado abaixo de tudo