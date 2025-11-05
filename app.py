import streamlit as st
import pandas as pd
import io
from math import floor

# --------------------------
# 🔹 CONFIGURATION
# --------------------------
st.set_page_config(page_title="Investment Annuity Calculator", page_icon="💰", layout="centered")

# --- Force White Background and Black Text ---
st.markdown(
    """
    <style>
        body, .stApp {
            background-color: #ffffff;
            color: #000000;
        }

        /* Make all labels and titles black */
        label, .stMarkdown, .stTextInput label, .stNumberInput label, .stSelectbox label {
            color: #000000 !important;
        }

        /* Adjust headers and sidebar */
        h1, h2, h3, h4, h5, h6, p {
            color: #000000 !important;
        }
        [data-testid="stSidebar"] {
            background-color: #f8f9fa;
            color: #000000;
        }

        /* Style for Download Button (gray) */
        div.stDownloadButton > button {
            background-color: #808080 !important;  /* gray */
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 0.6em 1.2em !important;
            font-weight: 600 !important;
            transition: background-color 0.2s ease-in-out;
        }

        div.stDownloadButton > button:hover {
            background-color: #6c757d !important;  /* darker gray */
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------
# 🔹 Utility Functions
# --------------------------

# Format numbers in Indian comma style
def indian_format(num):
    x = int(round(num, 0))
    s = str(x)
    if len(s) <= 3:
        return s
    else:
        last3 = s[-3:]
        rest = s[:-3]
        rest = list(rest)
        rest.reverse()
        new = []
        for i, digit in enumerate(rest):
            if i % 2 == 0 and i != 0:
                new.append(',')
            new.append(digit)
        new.reverse()
        return ''.join(new) + ',' + last3

# Convert number to Indian rupees in words
def num_to_words(n):
    from num2words import num2words
    try:
        words = num2words(floor(n), lang='en_IN')
        return words.replace(',', '').capitalize() + " rupees"
    except:
        return "Value too large to convert"

# --------------------------
# 🔹 LOGO + TITLE
# --------------------------
st.image("logo.png", width=190)
st.title("💰 Investment Annuity Calculator")
st.caption("Estimate how much annuity you can receive based on your investment and return expectations.")

# --------------------------
# 🔹 USER INPUTS
# --------------------------
col1, col2 = st.columns(2)
with col1:
    current_year = st.number_input("Current Year", value=2025, step=1, format="%d")
    initial_investment = st.number_input("Initial Investment (₹)", value=10000000, step=100000, format="%d")
    yearly_payment = st.number_input("Yearly Payment (₹, use negative for outflow)", value=-500000, step=50000, format="%d")
    expected_return = st.number_input("Expected Return (%)", value=15, step=1, format="%d") / 100

with col2:
    payment_till = st.number_input("Payment Till Year", value=2040, step=1, format="%d")
    waiting_till = st.number_input("Waiting Till Year", value=2040, step=1, format="%d")
    want_money_till = st.number_input("Want Money Till Year", value=2060, step=1, format="%d")

# --------------------------
# 🔹 CALCULATIONS
# --------------------------
r = expected_return
n1 = payment_till - current_year
n2 = payment_till - current_year
n3 = waiting_till - payment_till
n4 = want_money_till - waiting_till

# Step 1: FV of initial investment
fv_initial = initial_investment * (1 + r) ** n1

# Step 2: FV of annuity payments
fv_annuity = yearly_payment * ((1 + r) ** n2 - 1) / r

# Step 3: Total FV
fv_total = fv_initial + fv_annuity

# Step 4: FV till waiting year
fv_waiting = fv_total * (1 + r) ** n3

# Step 5: Calculate annuity from waiting till to want money till
annuity = fv_waiting * r / (1 - (1 + r) ** -n4)

# --------------------------
# 🔹 BUILD GROWTH DATA FOR CHART
# --------------------------
years = list(range(current_year, want_money_till + 1))
values = []

balance = initial_investment
for year in years:
    if year <= payment_till:
        balance = (balance * (1 + r) + yearly_payment)
    elif year <= waiting_till:
        balance = balance * (1 + r)
    else:
        withdrawal = annuity
        balance = (balance * (1 + r) - withdrawal)
    values.append(balance)

df = pd.DataFrame({"Year": years, "Portfolio Value (₹)": values})

# --------------------------
# 🔹 DISPLAY RESULTS
# --------------------------
st.subheader("📊 Results Summary")
st.write(f"**Future Value at Waiting Year ({waiting_till})**: ₹{indian_format(fv_waiting)}")
st.write(f"**Annuity you can get till {want_money_till}**: ₹{indian_format(annuity)}")
st.write(f"**In words:** {num_to_words(annuity)}")

# --------------------------
# 🔹 FOOTER
# --------------------------
st.markdown("---")
st.markdown("🔸 *Developed by Finideas — Smart Investment Tools for Smarter Decisions.*")
