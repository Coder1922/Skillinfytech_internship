import csv
import os
from datetime import datetime
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Expense Tracker Hub", page_icon="💰", layout="centered"
)

# Custom CSS to reduce whitespace and style metrics
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        div.stMetric {
            background-color: rgba(128, 128, 128, 0.05);
            padding: 12px;
            border-radius: 10px;
            border: 1px solid rgba(128, 128, 128, 0.1);
        }
    </style>
""",
    unsafe_allow_html=True,
)

# File Setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(SCRIPT_DIR, "expenses.csv")


def initialize_file():
  """Creates the CSV file with headers if it does not already exist."""
  if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, mode="w", newline="") as file:
      writer = csv.writer(file)
      writer.writerow(["Date", "Category", "Amount", "Description"])


initialize_file()

# App Header
st.title("💰 Personal Expense Tracker")
st.markdown("Manage, track, and visualize your daily spending effortlessly.")
st.markdown("---")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(
    ["➕ Add Expense", "👁️ View & Filter", "📊 Reports & Charts"]
)

# ================= TAB 1: ADD EXPENSE =================
with tab1:
  st.subheader("Record a New Expense")

  with st.form("expense_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
      expense_date = st.date_input("Date", value=datetime.now())
    with col2:
      category = st.selectbox(
          "Category",
          ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Pets", "Other"],
      )

    amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
    description = st.text_input(
        "Description", placeholder="e.g., Grocery shopping, Uber ride"
    )

    submitted = st.form_submit_button(
        "Save Expense", type="primary", width="stretch"
    )

    if submitted:
      if amount <= 0:
        st.warning("⚠️ Please enter an amount greater than zero.")
      else:
        date_str = expense_date.strftime("%Y-%m-%d")
        formatted_category = category.strip().title()
        clean_desc = description.strip()

        with open(FILE_NAME, mode="a", newline="") as file:
          writer = csv.writer(file)
          writer.writerow([date_str, formatted_category, amount, clean_desc])

        st.success(
            f"Successfully added ₹{amount:.2f} under **{formatted_category}**!"
        )

# ================= TAB 2: VIEW & FILTER =================
with tab2:
  st.subheader("All Recorded Expenses")

  if not os.path.exists(FILE_NAME) or os.stat(FILE_NAME).st_size == 0:
    st.info("No expenses recorded yet. Switch to the 'Add Expense' tab to start.")
  else:
    df = pd.read_csv(FILE_NAME)

    if df.empty:
      st.info("Your expense log is currently empty.")
    else:
      filter_type = st.radio(
          "Filter by:", ["All", "Category", "Date"], horizontal=True
      )

      filtered_df = df.copy()
      if filter_type == "Category":
        selected_cat = st.selectbox(
            "Select Category", df["Category"].unique()
        )
        filtered_df = df[df["Category"] == selected_cat]
      elif filter_type == "Date":
        selected_date = st.date_input("Select Date", value=datetime.now())
        filtered_df = df[df["Date"] == selected_date.strftime("%Y-%m-%d")]

      total_filtered = filtered_df["Amount"].astype(float).sum()
      st.metric(
          label="Total Amount for Selection", value=f"₹{total_filtered:.2f}"
      )

      st.dataframe(filtered_df, width="stretch")

# ================= TAB 3: REPORTS & CHARTS =================
with tab3:
  st.subheader("Spending Breakdown & Analytics")

  if not os.path.exists(FILE_NAME) or os.stat(FILE_NAME).st_size == 0:
    st.info("No data available to generate reports.")
  else:
    df = pd.read_csv(FILE_NAME)

    if df.empty:
      st.info("Not enough data for reports yet.")
    else:
      df["Amount"] = df["Amount"].astype(float)
      total_spent = df["Amount"].sum()

      category_summary = (
          df.groupby("Category")["Amount"].sum().reset_index()
      )

      st.metric(label="Total Lifetime Spending", value=f"₹{total_spent:.2f}")
      st.markdown("---")

      st.markdown("### Spending by Category")
      if not category_summary.empty:
        st.bar_chart(
            category_summary.set_index("Category")["Amount"], color="#4CAF50"
        )

      st.markdown("### Category Totals Table")
      st.dataframe(category_summary, width="stretch")