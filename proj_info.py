import streamlit as st

def show_project_info():
    st.subheader("📌 Project Information")
    st.write("""
    ##### **Overview**  
    This **Expense Tracker Dashboard** helps you analyze your spending habits using **SQL and Streamlit**.  
    It provides **insights into expenses**, identifies **cashback opportunities**, and visualizes spending patterns with interactive charts.
    """)

    st.write("""
    ##### **Features**  
    ✅ **Track Total Spending**: View expenses across different categories.  
    ✅ **Cashback Insights**: Identify transactions that earned cashback.  
    ✅ **Monthly Trends**: See how your expenses change over time.  
    ✅ **Payment Mode Analysis**: Understand which payment methods you use the most.  
    ✅ **Category Breakdown**: Find out which expense category consumes the highest budget.  
    ✅ **Data Visualization**: Interactive charts powered by **Plotly**.
    """)

    st.write("""
    ##### **Technology Stack**  
    🔹 **Python** (for data processing)  
    🔹 **Streamlit** (for dashboard UI)  
    🔹 **MySQL** (for database management)  
    🔹 **Plotly** (for data visualization)
    """)

    st.write("""
    ##### **How It Works**  
    1️⃣ **Data Collection**: Expenses are stored in a MySQL database.  
    2️⃣ **Query Execution**: SQL queries fetch insights from the database.  
    3️⃣ **Visualization**: Data is presented in interactive charts for easy analysis.  
    4️⃣ **Synthetic Data Generation**: The Faker library creates realistic expense data for testing.  
""")

    # Display the image
    #st.image("images/expense_tracking.png", caption="Expense Tracking Concept", use_column_width=True)