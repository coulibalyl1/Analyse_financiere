import streamlit as st
import yfinance as yf
import pandas as pd

# 🔹 Classe
class FinancialRatios:
    def __init__(self, ticker):
        self.company = yf.Ticker(ticker)
        self.balance_sheet = self.company.balance_sheet

    def get_value(self, item, years):
        try:
            return self.balance_sheet.loc[item, years]
        except KeyError:
            return pd.Series([None]*len(years), index=years)

    def current_ratio(self, years):
        current_assets = self.get_value('Current Assets', years)
        current_liabilities = self.get_value('Current Liabilities', years)
        return current_assets / current_liabilities


# 🔹 Interface Streamlit

st.title("📊 Analyse Financière")

# input utilisateur
ticker = st.text_input("Entrez le ticker (ex: AMZN, AAPL, TSLA)", "AMZN")

if ticker:
    try:
        ratios = FinancialRatios(ticker)

        # récupérer les dates disponibles
        available_years = list(ratios.balance_sheet.columns.astype(str))

        # sélection utilisateur
        selected_years = st.multiselect(
            "Choisissez les années",
            available_years,
            default=available_years[:2]
        )

        if selected_years:
            result = ratios.current_ratio(selected_years)

            st.subheader("Current Ratio")
            st.write(result)
            st.line_chart(result)

    except Exception as e:
        st.error(f"Erreur : {e}")
