import streamlit as st

st.set_page_config(page_title="Formação Profissional/Experiências", layout="wide")
st.sidebar.markdown("Feito por Felipe Megumi Nakama")

# st.logo("")
st.image("foto.jpg", width=100)

st.title("Formação Profissional e Experiências")

# Seção de Formação Acadêmica
st.markdown("### Formação Acadêmica")
st.write("""
Atualmente, estou cursando **Engenharia de Software na FIAP**, onde desenvolvo habilidades em metodologias ágeis, ciência de dados, segurança cibernética, redes e desenvolvimento de software.

Durante minha trajetória acadêmica, participei de diversos projetos práticos, incluindo:
- **VisionCar+** – Aplicativo para otimização e gestão de veículos.
- **Sistema de monitoramento energético** – Projeto voltado para energias renováveis e consumo inteligente.
- **Configuração de redes** – Implementação de roteamento OSPF no Cisco Packet Tracer.
- **Análise de dados** – Utilização do Python e Plotnine para estatísticas e visualização de dados.
- **Gerenciamento de bibliotecas** – Desenvolvimento de um sistema com modelagem de banco de dados e backlog de produto.

Embora ainda não tenha experiência profissional, estou constantemente aprimorando minhas habilidades e buscando oportunidades na área de cybersecurity.
""")

# Seção de Cursos e Certificações
st.markdown("### Cursos e Certificações")
st.write("""
Além da minha formação acadêmica, concluí cursos complementares para aprofundar meu conhecimento:

- **Algoritmos: Aprenda a Programar** (80h) – Introdução à lógica de programação e construção de algoritmos.
- **Design Thinking: Process** (40h) – Metodologia para resolução de problemas criativos.
- **Formação Social e Sustentabilidade** (80h) – ESG e impactos sociais, ambientais e econômicos.

Atualmente, estou cursando:
- **Cybersecurity** (120h) – Proteção de sistemas contra vulnerabilidades e ataques cibernéticos.
- **Linux Fundamentos** (40h) – Comandos e recursos avançados do sistema operacional Linux.
""")
