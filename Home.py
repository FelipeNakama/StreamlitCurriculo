import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.app_logo import add_logo

# Configuração da página
st.set_page_config(page_title="Currículo", layout="wide")
st.sidebar.markdown("Feito por Felipe Megumi Nakama")

# Adicionando o logo
# st.logo("")

# Adicionando a foto
st.image("foto.jpg", width=100)

st.title("Felipe Megumi Nakama")

# Seção "Quem sou Eu"
st.markdown("### Quem sou")
st.write("""
Olá! 
         
Eu sou um estudante de Engenharia de Software na FIAP, atualmente no segundo ano, com interesse em desenvolvimento de software, desenvolvimento de jogos e cybersecurity 

Minha formação inclui metodologias ágeis, ciência de dados, design de banco de dados e programação em diversas linguagens, como Python e Java. 

Além disso, já desenvolvi projetos envolvendo redes e segurança, como a configuração de roteadores com OSPF no Cisco Packet Tracer. 

Busco oportunidades para aplicar e expandir meus conhecimentos em segurança cibernética, contribuindo para a proteção e otimização de sistemas.

Para mais detalhes sobre minha trajetória acadêmica e profissional, confira a seção "Formação". 
Minhas habilidades técnicas e conhecimentos podem ser encontrados na aba "Skills".

""")

# Socials
st.markdown("### Contato")
st.markdown("""
- **LinkedIn:** [Meu Perfil no LinkedIn](https://www.linkedin.com/in/seu-linkedin/)
- **GitHub:** [Meu Repositório no GitHub](https://github.com/seu-github)
- **Email:** [meu.email@example.com](mailto:meu.email@example.com)
""")