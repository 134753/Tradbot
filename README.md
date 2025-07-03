# 💬 TadBot – Chatbot Financier en Streamlit

TadBot est une application web interactive développée avec [Streamlit](https://streamlit.io/) permettant d’analyser une entreprise cotée en bourse ou de comparer plusieurs entreprises en un clic.

Elle s'appuie sur les données de **Yahoo Finance** via les bibliothèques `yfinance` et `yahooquery`, et propose également une **fonction de prévision** du cours de l’action grâce à un modèle de **régression linéaire**.

---

## 🚀 Fonctionnalités

- 🔍 Détection intelligente du ticker à partir d’un nom de société ou de marque
- 📊 Analyse complète d’une entreprise : cours de l’action, dividende, PE Ratio, etc.
- 🔮 Prévision du cours sur 30 jours (modèle simple)
- 📋 Comparaison de plusieurs entreprises dans un tableau interactif
- 📈 Graphique de cours sur 6 mois
- 📥 Export des données comparées au format CSV
- 💼 Alias intégrés pour des marques populaires (ex: Instagram → Meta)

---

## 🧰 Technologies utilisées

- Python 3.10 ou 3.11 recommandé
- Streamlit
- yfinance
- yahooquery
- scikit-learn
- pandas, numpy

---

## ⚙️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-utilisateur/chatbot-financier.git
cd chatbot-financier

### 2. Créer un environnement virtuel (optionnel mais conseillé)

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate    

### 3. Installer les dépendances

pip install --upgrade pip
pip install -r requirements.txt

### ▶️ Lancer le projet

Pour démarrer le chatbot :

faire cette commande dans le Terminal : 

    streamlit run app.py 

Et une fois lancé, l’application sera accessible dans votre navigateur à l’adresse suivante :

👉 http://localhost:8501