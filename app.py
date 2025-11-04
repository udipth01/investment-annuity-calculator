import streamlit as st
import pandas as pd
import io

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

        /* Hover effect for button */
        div.stDownloadButton > button:hover {
            background-color: #6c757d !important;  /* darker gray */
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------
# 🔹 LOGO + TITLE
# --------------------------
# Replace 'logo.png' with your logo filename (ensure it's in the same folder as app.py)
st.image("logo.png", width=190)
st.title("💰 Investment Annuity Calculator")
st.caption("Estimate how much annuity you can receive based on your investment and return expectations.")

# --------------------------
# 🔹 USER INPUTS
# --------------------------
col1, col2 = st.columns(2)
with col1:
    current_year = st.number_input("Current Year", value=2025)
    initial_investment = st.number_input("Initial Investment (₹)", value=10000000.0, step=100000.0)
    yearly_payment = st.number_input("Yearly Payment (₹, use negative for outflow)", value=-500000.0, step=50000.0)
    expected_return = st.number_input("Expected Return (%)", value=15.0, step=0.1) / 100

with col2:
    payment_till = st.number_input("Payment Till Year", value=2040)
    waiting_till = st.number_input("Waiting Till Year", value=2040)
    want_money_till = st.number_input("Want Money Till Year", value=2060)

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
annuity = fv_waiting * r / (1-(1 + r) ** -n4 )

# --------------------------
# 🔹 BUILD GROWTH DATA FOR CHART
# --------------------------
years = list(range(current_year, want_money_till + 1))
values = []

balance = initial_investment
for year in years:
    if year <= payment_till:
        balance = (balance  * (1 + r) + yearly_payment)
    elif year <= waiting_till:
        balance = balance * (1 + r)
    else:
        # during annuity withdrawal
        withdrawal = annuity
        balance = (balance * (1 + r) - withdrawal) 
    values.append(balance)

df = pd.DataFrame({"Year": years, "Portfolio Value (₹)": values})

# --------------------------
# 🔹 DISPLAY RESULTS
# --------------------------
st.subheader("📊 Results Summary")
st.write(f"**Future Value at Waiting Year ({waiting_till})**: ₹{fv_waiting:,.2f}")
st.write(f"**Annuity you can get till {want_money_till}**: ₹{annuity:,.0f}")

# # --------------------------
# # 🔹 LINE CHART
# # --------------------------
# st.subheader("📈 Portfolio Growth Over Time")
# st.line_chart(df.set_index("Year"))

# # --------------------------
# # 🔹 CSV DOWNLOAD
# # --------------------------
# csv_buffer = io.StringIO()
# df.to_csv(csv_buffer, index=False)
# st.download_button(
#     label="💾 Download Portfolio Data as CSV",
#     data=csv_buffer.getvalue(),
#     file_name="investment_annuity_projection.csv",
#     mime="text/csv"
# )

# --------------------------
# 🔹 FOOTER
# --------------------------
st.markdown("---")
st.markdown("🔸 *Developed by Finideas — Smart Investment Tools for Smarter Decisions.*")
