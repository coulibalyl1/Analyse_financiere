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

import streamlit as st
import pandas as pd

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

            # convertir en DataFrame si nécessaire
            if isinstance(result, dict):
                df_result = pd.DataFrame({
                    "selected_years": list(result.keys()),
                    "current_ratio": list(result.values())
                })
            else:
                df_result = pd.DataFrame(result)

            # s'assurer que les colonnes existent
            if "selected_years" not in df_result.columns:
                df_result["selected_years"] = selected_years

            if "current_ratio" not in df_result.columns:
                possible_col = df_result.columns[0]
                df_result = df_result.rename(columns={possible_col: "current_ratio"})

            st.line_chart(
                df_result.set_index("selected_years")["current_ratio"]
            )

    except Exception as e:
        st.error(f"Erreur : {e}")
