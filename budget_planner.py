import streamlit as st
import pandas as pd
import plotly.express as px

# Set title
st.title("Personal Budget Planner")

# Create a dataframe to store the user's budget info
data = pd.DataFrame(columns=["Category", "Budgeted", "Spent"])

# Sidebar Inputs
st.sidebar.header("Add New Expense")

category = st.sidebar.text_input("Category (e.g., Food, Rent, Entertainment)")
budgeted = st.sidebar.number_input("Budgeted Amount", min_value=0.0, step=0.1)
spent = st.sidebar.number_input("Spent Amount", min_value=0.0, step=0.1)

# Add button to save data
if st.sidebar.button("Add Expense"):
    if category and budgeted > 0 and spent >= 0:
        new_row = pd.DataFrame({"Category": [category], "Budgeted": [budgeted], "Spent": [spent]})
        data = pd.concat([data, new_row], ignore_index=True)
        st.success(f"Added {category} with Budgeted: ${budgeted} and Spent: ${spent}")
    else:
        st.warning("Please fill all fields with valid data.")

# Display the data
st.write("### Budget Overview")
st.dataframe(data)

# Calculate the remaining balance
data["Remaining"] = data["Budgeted"] - data["Spent"]
total_budget = data["Budgeted"].sum()
total_spent = data["Spent"].sum()
total_remaining = data["Remaining"].sum()

st.write(f"### Total Budget: ${total_budget}")
st.write(f"### Total Spent: ${total_spent}")
st.write(f"### Remaining Balance: ${total_remaining}")

# Plot a pie chart of expenses vs. remaining budget
fig = px.pie(data, names="Category", values="Remaining", title="Remaining Budget by Category")
st.plotly_chart(fig)

# Deploy to Streamlit
# You can run this using: streamlit run <script_name.py>
