import streamlit as st
import yfinance as yf
from yahooquery import search
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# === CONFIG APP ===
st.set_page_config(
    page_title="Chatbot Financier",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.title("💬 Chatbot Financier")

# 🔁 Base manuelle des marques/filiales → maison mère
manual_aliases = {
    "rockstar": "Take-Two",
    "instagram": "Meta",
    "whatsapp": "Meta",
    "oculus": "Meta",
    "youtube": "Alphabet",
    "gmail": "Alphabet",
    "google": "Alphabet",
    "android": "Alphabet",
    "linkedin": "Microsoft",
    "bing": "Microsoft",
    "blizzard": "Activision Blizzard",
    "call of duty": "Activision Blizzard",
    "riot games": "Tencent",
    "tesla energy": "Tesla",
}

def get_ticker_from_name(company_name):
    name = company_name.lower().strip()
    alias_used = None

    if name in manual_aliases:
        alias_used = name
        name = manual_aliases[name]

    results = search(name)
    for item in results.get("quotes", []):
        if item.get("quoteType") == "EQUITY":
            return item.get("symbol"), manual_aliases.get(alias_used, None)
    return None, None

def forecast_stock_price(hist_df, days_ahead=30):
    df = hist_df.reset_index()
    df["Date"] = df["Date"].map(pd.Timestamp.toordinal)

    X = np.array(df["Date"]).reshape(-1, 1)
    y = df["Close"].values

    model = LinearRegression()
    model.fit(X, y)

    future_dates = [df["Date"].max() + i for i in range(1, days_ahead + 1)]
    future_X = np.array(future_dates).reshape(-1, 1)
    forecast = model.predict(future_X)

    future_df = pd.DataFrame({
        "Date": pd.to_datetime([pd.Timestamp.fromordinal(int(d)) for d in future_dates]),
        "Forecast": forecast
    })

    return future_df

# 🧭 Choix du mode
mode = st.selectbox("📌 Que souhaitez-vous faire ?", ["Analyser une entreprise", "Comparer plusieurs entreprises"])

# =============================
# 🔹 MODE 1 : Analyse unique
# =============================
if mode == "Analyser une entreprise":
    company_name = st.text_input("🔎 Entrez le nom de l’entreprise (ex: Microsoft, LVMH)")

    if st.button("📈 Analyser"):
        with st.spinner("🔄 Chargement des données..."):
            ticker, parent = get_ticker_from_name(company_name)

            if not ticker:
                st.error("❌ Impossible de trouver le ticker.")
            else:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    hist = stock.history(period="1y")

                    st.success(f"✅ Ticker détecté : {ticker}")
                    if parent:
                        st.info(f"ℹ️ **{company_name}** est une marque de **{parent}**")

                    st.subheader(f"📊 Rendements – {info.get('shortName', company_name)}")

                    # Affichage des indicateurs
                    st.write(f"• **Rendement du dividende** : {info.get('dividendYield') * 100:.2f} %" if info.get("dividendYield") else "• Rendement du dividende : Non disponible")
                    st.write(f"• **PE Ratio** : {info.get('trailingPE'):.2f}" if info.get("trailingPE") else "• PE Ratio : Non disponible")
                    st.write(f"• **Performance 52 semaines** : {info.get('52WeekChange') * 100:.2f} %" if info.get("52WeekChange") else "• Performance 52 semaines : Non disponible")
                    st.write(f"• **YTD** : {info.get('ytdReturn') * 100:.2f} %" if info.get("ytdReturn") else "• YTD : Non disponible")

                    st.subheader("📉 Évolution du cours (1 an)")
                    st.line_chart(hist["Close"])

                    st.subheader("🔮 Prévision du cours (30 jours)")
                    forecast_df = forecast_stock_price(hist)
                    full_df = pd.concat([hist["Close"].reset_index(), forecast_df.rename(columns={"Forecast": "Close"})])
                    full_df = full_df.set_index("Date")
                    st.line_chart(full_df["Close"])

                except Exception as e:
                    st.error(f"Erreur lors de la récupération des données : {e}")

# =============================
# 🔸 MODE 2 : Comparaison
# =============================
elif mode == "Comparer plusieurs entreprises":
    company_input = st.text_input("Entrez les noms des entreprises séparés par des virgules (ex: Microsoft, Apple, Tesla)", value="Microsoft, Apple, Tesla")

    if st.button("📊 Comparer"):
        with st.spinner("🔄 Chargement des données..."):
            companies = [name.strip() for name in company_input.split(",")]
            data = []
            hist_data = {}

            for name in companies:
                ticker, parent = get_ticker_from_name(name)
                if ticker:
                    try:
                        stock = yf.Ticker(ticker)
                        info = stock.info
                        hist = stock.history(period="6mo")
                        hist_data[name] = hist["Close"]

                        data.append({
                            "Nom Entré": name,
                            "Entreprise": info.get("shortName", name),
                            "Maison Mère": parent if parent else "",
                            "Ticker": ticker,
                            "Dividende (%)": round(info.get("dividendYield", 0) * 100, 2) if info.get("dividendYield") else None,
                            "PE Ratio": round(info.get("trailingPE", 0), 2) if info.get("trailingPE") else None,
                            "52w Perf. (%)": round(info.get("52WeekChange", 0) * 100, 2) if info.get("52WeekChange") else None,
                            "YTD (%)": round(info.get("ytdReturn", 0) * 100, 2) if info.get("ytdReturn") else None
                        })
                    except Exception as e:
                        st.warning(f"Erreur pour {name} ({ticker}) : {e}")
                else:
                    st.warning(f"❌ Ticker introuvable pour : {name}")

            if data:
                df = pd.DataFrame(data)
                st.subheader("📋 Tableau comparatif")
                st.dataframe(df.set_index("Entreprise"), use_container_width=True)

                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Télécharger en CSV", data=csv, file_name="comparaison_entreprises.csv", mime="text/csv")

                st.subheader("📉 Cours des actions (6 derniers mois)")
                price_df = pd.DataFrame(hist_data)
                st.line_chart(price_df)
            else:
                st.error("Aucune donnée disponible.")
