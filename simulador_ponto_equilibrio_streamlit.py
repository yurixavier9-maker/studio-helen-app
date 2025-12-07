import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulador do Ponto de Equilíbrio", layout="centered")

st.title("📊 Simulador de Ponto de Equilíbrio")
st.write("Insira os dados abaixo para calcular o ponto de equilíbrio e simular cenários.")

# --- Inputs ---
preco_venda = st.number_input("Preço de Venda Unitário (R$)", min_value=0.0, value=100.0)
custo_variavel = st.number_input("Custo Variável Unitário (R$)", min_value=0.0, value=40.0)
custos_fixos = st.number_input("Custos Fixos Totais (R$)", min_value=0.0, value=10000.0)

st.divider()
submitted = st.button("Calcular Ponto de Equilíbrio")

if submitted:
    mc_unit = preco_venda - custo_variavel

    if mc_unit <= 0:
        st.error("Margem de contribuição negativa! Ajuste os valores.")
    else:
        pe_qtd = custos_fixos / mc_unit
        pe_valor = pe_qtd * preco_venda

        st.subheader("📌 Resultado do Ponto de Equilíbrio")
        st.metric("Ponto de Equilíbrio (Unidades)", f"{pe_qtd:.2f}")
        st.metric("Ponto de Equilíbrio (R$)", f"{pe_valor:,.2f}")

        st.divider()
        st.subheader("📈 Simulação de Cenários - Variação do Preço de Venda")

        pct_changes = range(-20, 25, 5)
        dados = []

        for pct in pct_changes:
            pv = preco_venda * (1 + pct / 100)
            mc_u = pv - custo_variavel
            if mc_u <= 0:
                pe_q = float('inf')
                pe_v = float('inf')
            else:
                pe_q = custos_fixos / mc_u
                pe_v = pe_q * pv
            dados.append([pct, pv, mc_u, pe_q, pe_v])

        df = pd.DataFrame(dados, columns=[
            "% Var Preço", "Preço Venda", "MC Unitária", "PE Unidades", "PE (R$)"
        ])

        st.dataframe(df, use_container_width=True)