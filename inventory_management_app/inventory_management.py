import csv
import os
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Inventory Management System", 
    page_icon="📦", 
    layout="wide"
)

# File Setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(SCRIPT_DIR, "inventory.csv")

def initialize_file():
    """Creates the inventory CSV file with headers if it doesn't exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ProductID", "ProductName", "Quantity", "Price"])

initialize_file()

# Session state initialization to track active menu option
if "menu_selection" not in st.session_state:
    st.session_state.menu_selection = "View Inventory"

# ================= SIDEBAR NAVIGATION =================
with st.sidebar:
    st.markdown("## 🗂️ Navigation Menu")
    st.markdown("---")
    
    if st.button("📋 View Inventory", use_container_width=True):
        st.session_state.menu_selection = "View Inventory"
    if st.button("➕ Add New Product", use_container_width=True):
        st.session_state.menu_selection = "Add Product"
    if st.button("🔄 Update Existing Product", use_container_width=True):
        st.session_state.menu_selection = "Update Product"
    if st.button("⚠️ Check Low-Stock Alerts", use_container_width=True):
        st.session_state.menu_selection = "Check Low-Stock Alerts"
        
    st.markdown("---")
    #st.markdown("### ℹ️ System Status")
    #st.info("System is running locally with persistent CSV storage.")

# ================= MAIN WINDOW CONTENT =================
selection = st.session_state.menu_selection

# -------------------------------------------------------------------------
# 1. VIEW INVENTORY
# -------------------------------------------------------------------------
if selection == "View Inventory":
    st.title("📋 Current Inventory List")
    st.markdown("Monitor real-time stock quantities and total asset valuation.")
    st.markdown("---")

    if not os.path.exists(FILE_NAME) or os.stat(FILE_NAME).st_size == 0:
        st.info("Inventory is currently empty. Use the sidebar menu to add products.")
    else:
        df = pd.read_csv(FILE_NAME)
        df["Quantity"] = df["Quantity"].astype(int)
        df["Price"] = df["Price"].astype(float)
        
        total_items = len(df)
        total_valuation = (df["Quantity"] * df["Price"]).sum()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"""
                <div style="background-color: rgba(128, 128, 128, 0.05); padding: 10px; border-radius: 10px; border: 1px solid rgba(128, 128, 128, 0.1);">
                    <p style="font-size: 20px;font-weight: bold; color: gray; margin-bottom: 2px;">📦 Total Unique Products</p>
                    <h2 style="font-size: 35px; margin-top: 0;">{total_items}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"""
                <div style="background-color: rgba(128, 128, 128, 0.05); padding: 10px; border-radius: 10px; border: 1px solid rgba(128, 128, 128, 0.1);">
                    <p style="font-size: 20px;font-weight: bold; color: gray; margin-bottom: 2px;">💰 Total Stock Valuation</p>
                    <h2 style="font-size: 35px; margin-top: 0;">₹{total_valuation:,.2f}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown("### Stock Details")
        st.dataframe(df, use_container_width=True)

# -------------------------------------------------------------------------
# 2. ADD PRODUCT
# -------------------------------------------------------------------------
elif selection == "Add Product":
    st.title("➕ Add New Product")
    st.markdown("Enter details for a brand new inventory item.")
    st.markdown("---")

    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            prod_id = st.text_input("Product ID (e.g., P101)").strip().upper()
        with col2:
            prod_name = st.text_input("Product Name").strip().title()
            
        col3, col4 = st.columns(2)
        with col3:
            quantity = st.number_input("Initial Quantity", min_value=0, step=1)
        with col4:
            price = st.number_input("Price per Unit (₹)", min_value=0.0, format="%.2f")
            
        submitted = st.form_submit_button("Save New Product", type="primary", use_container_width=True)
        
        if submitted:
            if not prod_id or not prod_name:
                st.warning("⚠️ Product ID and Product Name are required fields.")
            else:
                # Check if ID already exists
                exists = False
                if os.path.exists(FILE_NAME):
                    with open(FILE_NAME, mode="r") as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            if row["ProductID"] == prod_id:
                                exists = True
                                break
                
                if exists:
                    st.error(f"❌ Product ID '{prod_id}' already exists! Please use the 'Update Existing Product' menu.")
                else:
                    with open(FILE_NAME, mode="a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([prod_id, prod_name, quantity, price])
                    st.success(f"Success: Product '{prod_name}' added successfully!")

# -------------------------------------------------------------------------
# 3. UPDATE PRODUCT (SHOWS CURRENT DETAILS FIRST)
# -------------------------------------------------------------------------
elif selection == "Update Product":
    st.title("🔄 Update Existing Product")
    st.markdown("Search by Product ID to view current details and modify stock or pricing.")
    st.markdown("---")

    # Read data to find existing IDs
    if not os.path.exists(FILE_NAME) or os.stat(FILE_NAME).st_size == 0:
        st.info("Inventory is empty. No products available to update.")
    else:
        df = pd.read_csv(FILE_NAME)
        product_ids = df["ProductID"].tolist()
        
        selected_id = st.selectbox("Select or Search Product ID", options=[""] + product_ids)
        
        if selected_id:
            # Fetch current details for the selected ID
            current_row = df[df["ProductID"] == selected_id].iloc[0]
            curr_name = current_row["ProductName"]
            curr_qty = int(current_row["Quantity"])
            curr_price = float(current_row["Price"])
            
            st.info(f"📌 **Current Details Found** — Name: **{curr_name}** | Qty: **{curr_qty}** | Price: **₹{curr_price:.2f}**")
            
            with st.form("update_form"):
                new_name = st.text_input("Product Name", value=curr_name).strip().title()
                col1, col2 = st.columns(2)
                with col1:
                    new_qty = st.number_input("New Quantity", min_value=0, value=curr_qty, step=1)
                with col2:
                    new_price = st.number_input("New Price (₹)", min_value=0.0, value=curr_price, format="%.2f")
                    
                update_submitted = st.form_submit_button("Save Changes", type="primary", use_container_width=True)
                
                if update_submitted:
                    rows = []
                    with open(FILE_NAME, mode="r") as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            if row["ProductID"] == selected_id:
                                row["ProductName"] = new_name
                                row["Quantity"] = new_qty
                                row["Price"] = new_price
                            rows.append(row)
                            
                    with open(FILE_NAME, mode="w", newline="") as file:
                        writer = csv.DictWriter(file, fieldnames=["ProductID", "ProductName", "Quantity", "Price"])
                        writer.writeheader()
                        writer.writerows(rows)
                        
                    st.success(f"Success: Product ID '{selected_id}' has been updated successfully!")

# -------------------------------------------------------------------------
# 4. LOW STOCK ALERTS
# -------------------------------------------------------------------------
elif selection == "Check Low-Stock Alerts":
    st.title("⚠️ Low-Stock Warnings")
    st.markdown("Review items that have fewer than 5 units remaining in stock.")
    st.markdown("---")

    if not os.path.exists(FILE_NAME):
        st.info("No inventory data found.")
    else:
        df = pd.read_csv(FILE_NAME)
        df["Quantity"] = df["Quantity"].astype(int)
        low_stock_df = df[df["Quantity"] < 5]
        
        if low_stock_df.empty:
            st.success("🎉 All inventory items have healthy stock levels (>= 5 units)!")
        else:
            st.warning("⚠️ The following items require immediate restock:")
            st.dataframe(low_stock_df, use_container_width=True)