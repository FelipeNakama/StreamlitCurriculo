import streamlit as st

st.set_page_config(page_title="Skills", layout="wide")
st.sidebar.markdown("Feito por Felipe Megumi Nakama")

# st.logo("")
st.image("foto.jpg", width=100)

st.title("Skills")

# Seção de Habilidades Técnicas
st.markdown("### Habilidades Técnicas")
st.write("""
Desenvolvi habilidades técnicas e conhecimentos em diversas áreas da Engenharia de Software, incluindo:
""")

st.markdown("#### Programação e Desenvolvimento")
st.write("""
- **Linguagens:** Python, Java, SQL
- **Frameworks e Ferramentas:** Streamlit, Plotnine, Cisco Packet Tracer
- **Metodologias:** Agile, Scrum
""")

st.markdown("#### Segurança e Redes")
st.write("""
- Configuração de redes e roteadores (OSPF)
- Conceitos básicos de segurança cibernética (*Cursando:* Cybersecurity)
""")

st.markdown("#### Banco de Dados e Análise de Dados")
st.write("""
- Modelagem de banco de dados (Oracle SQL Data Modeler)
- Análise estatística e visualização de dados com Python e Plotnine
""")

st.markdown("#### Outros Conhecimentos")
st.write("""
- Design Thinking para resolução de problemas
- Sustentabilidade e ESG no contexto empresarial
""")
