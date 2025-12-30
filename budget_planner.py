import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load the data (initializes an empty dataframe)
def load_data():
    return pd.DataFrame(columns=["Category", "Budgeted", "Spent"])

# Function to add an expense to the dataframe
def add_expense(data, category, budgeted, spent):
    new_row = pd.DataFrame({"Category": [category], "Budgeted": [budgeted], "Spent": [spent]})
    data = pd.concat([data, new_row], ignore_index=True)
    return data

# Function to display the total budget overview
def display_total(data):
    data["Remaining"] = data["Budgeted"] - data["Spent"]
    total_budget = data["Budgeted"].sum()
    total_spent = data["Spent"].sum()
    total_remaining = data["Remaining"].sum()

    # Display total budget, spent, and remaining balance
    st.write(f"### Total Budget: ${total_budget:.2f}")
    st.write(f"### Total Spent: ${total_spent:.2f}")
    st.write(f"### Remaining Balance: ${total_remaining:.2f}")

# Function to create and display a pie chart
def display_pie_chart(data):
    fig = px.pie(data, names="Category", values="Remaining", title="Remaining Budget by Category")
    st.plotly_chart(fig)

# Main function to run the Streamlit app
def main():
    # Streamlit page configuration
    st.set_page_config(page_title="Budget Planner", page_icon="💸", layout="wide")

    # App Title
    st.title("💸 Personal Budget Planner")
    st.markdown(
        """
        Welcome to the **Budget Planner**! This app helps you track your budget and expenses, visualize 
        your spending, and ensure you're staying on track financially.
        """
    )

    # Sidebar Inputs
    st.sidebar.header("Add New Expense")
    
    # Input fields
    category = st.sidebar.text_input("Category (e.g., Food, Rent, Entertainment)", "")
    budgeted = st.sidebar.number_input("Budgeted Amount", min_value=0.0, step=0.1, format="%.2f")
    spent = st.sidebar.number_input("Spent Amount", min_value=0.0, step=0.1, format="%.2f")

    # Feedback on invalid data (if spent exceeds budgeted)
    if budgeted < spent:
        st.sidebar.warning("⚠️ Spent amount can't exceed budgeted amount!")

    # Load or initialize data in session state (so data persists across reruns)
    if 'data' not in st.session_state:
        st.session_state['data'] = load_data()
    
    data = st.session_state['data']

    # Add Expense Button
    if st.sidebar.button("Add Expense"):
        # Check if inputs are valid before adding
        if category and budgeted > 0 and spent >= 0:
            data = add_expense(data, category, budgeted, spent)
            st.session_state['data'] = data
            st.success(f"✅ Added {category} with Budgeted: ${budgeted:.2f} and Spent: ${spent:.2f}")
        else:
            st.sidebar.warning("⚠️ Please fill all fields with valid data.")
    
    # Layout for the main content using columns
    col1, col2 = st.columns([3, 1])

    with col1:
        # Display data table with a neat style
        st.write("### Budget Overview")
        st.dataframe(data, use_container_width=True)

    with col2:
        # Display total budget, pie chart, and any other useful info
        display_total(data)
        display_pie_chart(data)

# Run the app
if __name__ == "__main__":
    main()
