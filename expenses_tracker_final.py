import streamlit as st # for an interactive ui dashboard
import pandas as pd # Importing the pandas library for data manipulation and analysis
import plotly.express as px #for visualization
from db_utils import run_query  # Import function from the db_utils file which runs the sql queries by connecting to expenses db
from proj_info import show_project_info  # Import  function to display projectinfo when project info radio button is chosen


# mainpage title
st.title("💰 Expense Tracker Dashboard")
st.write("Analyze your spending habits with SQL-powered insights!")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["🖼️ Expense Tracker Dashboard","📌 Project Info", "🔍 SQL Queries", "📊 Data Visualization", "👩‍💻 Creator Info"])

if page == "🖼️ Expense Tracker Dashboard":
    st.image("expimage.png", use_column_width=True)
    
# -------------------------------- PAGE 1: Project Introduction --------------------------------
    
elif page == "📌 Project Info":
    show_project_info()
     
# -------------------------------- PAGE 2: SQL Queries --------------------------------    
elif page == "🔍 SQL Queries":
    st.subheader("🔍 SQL Query Execution")

    query_options = {
        "🔍Total Amount Spent per Category": "SELECT Category, SUM(Amount_Paid) AS Total_Spent FROM expenses GROUP BY Category",
        "🔍Total Amount Spent per Payment Mode": "SELECT Payment_Mode, SUM(Amount_Paid) AS Total_Spent FROM expenses GROUP BY Payment_Mode",
        "🔍Total Cashback Received": "SELECT SUM(Cashback) AS Total_Cashback FROM expenses",
        "🔍Top 5 most expensive categories": 
        "SELECT category, SUM(amount_paid) AS total_spent FROM expenses GROUP BY category ORDER BY total_spent DESC LIMIT 5;",
        "🔍Amount spent on transportation by payment mode": 
        "SELECT payment_mode, SUM(amount_paid) AS total_spent FROM expenses WHERE category = 'Transport' GROUP BY payment_mode ORDER BY total_spent DESC;",
        "🔍Transactions that resulted in cashback": 
        "SELECT * FROM expenses WHERE cashback > 0 ORDER BY cashback DESC;",
        "🔍Total spending in each month": 
        #"SELECT MONTHNAME(date) AS MONTHNAME, SUM(amount_paid) AS total_spent FROM expenses GROUP BY MONTHNAME ORDER BY MONTHNAME;"
        """SELECT MONTHNAME(date) AS month_name, SUM(amount_paid) AS total_spent FROM expenses GROUP BY month_name 
            ORDER BY FIELD(month_name, 'January', 'February', 'March', 'April', 'May', 'June', 
                                    'July', 'August', 'September', 'October', 'November', 'December');""",
        "🔍Highest spending month for Travel & Entertainment": 
        """(SELECT MONTHNAME(date) AS month, 'Travel' AS category, SUM(amount_paid) AS total_spent
            FROM expenses WHERE category = 'Travel' GROUP BY month ORDER BY total_spent DESC LIMIT 1)
        UNION
        (SELECT MONTHNAME(date) AS month, 'Entertainment' AS category, SUM(amount_paid) AS total_spent
            FROM expenses WHERE category = 'Entertainment' GROUP BY month ORDER BY total_spent DESC LIMIT 1);""",
        "🔍Recurring Expenses by Month": """
        SELECT MONTHNAME(date) AS month, category, COUNT(*) AS occurrences, SUM(amount_paid) AS total_amount
        FROM expenses
        GROUP BY month, category
        HAVING occurrences > 1
        ORDER BY FIELD(month, 'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December');
        """,
        "🔍Cashback/Rewards Earned Per Month": """
            SELECT MONTHNAME(date) AS month, SUM(cashback) AS total_cashback
            FROM expenses
            GROUP BY month
            ORDER BY FIELD(month, 'January', 'February', 'March', 'April', 'May', 'June', 
            'July', 'August', 'September', 'October', 'November', 'December');
        """,
        "🔍Spending Trends Over Time": """
        SELECT DATE_FORMAT(date, '%Y-%m') AS date, SUM(amount_paid) AS total_spent
        FROM expenses
        GROUP BY date
        ORDER BY date;
        """,
        "🔍Travel Cost Breakdown":"""SELECT description, AVG(amount_paid) AS avg_cost 
        FROM expenses WHERE category = 'Travel' GROUP BY description ORDER BY avg_cost DESC;""",
        "🔍Grocery Spending Patterns":"""SELECT DAYNAME(date) AS day_of_week, SUM(amount_paid) AS total_spent_on_groceries 
        FROM expenses WHERE category = 'Food'AND description = 'Bought groceries'  
        GROUP BY day_of_week 
        ORDER BY FIELD(day_of_week, 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday');""",
        "🔍High and Low Priority Categories": """
        SELECT category, SUM(amount_paid) AS total_spent,
        CASE 
            WHEN SUM(amount_paid) > (SELECT AVG(amount_paid) FROM expenses) THEN 'High'
            ELSE 'Low'
        END AS priority_level
        FROM expenses
        GROUP BY category
        ORDER BY total_spent DESC;
    """,
     "🔍Category Contribution to Total Spending": """
        SELECT category, 
               SUM(amount_paid) AS total_spent,
               ROUND((SUM(amount_paid) / (SELECT SUM(amount_paid) FROM expenses)) * 100, 2) AS percentage_of_total
        FROM expenses
        GROUP BY category
        ORDER BY total_spent DESC;
    """,
        "💾Top 5 Highest Spending Days":"""SELECT DAYNAME(date) AS Day_Of_Week, SUM(Amount_Paid) AS Total_Spent
            FROM expenses GROUP BY Day_Of_Week ORDER BY Total_Spent DESC LIMIT 5;""",
            
        "💾Highest Transaction in Each Category":"""SELECT Category, MAX(Amount_Paid) AS Highest_Transaction
            FROM expenses GROUP BY Category ORDER BY Category;""",
            
        "💾Average Spending by Payment Mode":"""SELECT Payment_Mode, ROUND(AVG(Amount_Paid), 2) AS Avg_Amount
                FROM expenses GROUP BY Payment_Mode ORDER BY Avg_Amount DESC;""",
                
        "💾Total amount spent on healthcare in each month":"""SELECT MONTHNAME(date) AS Month, SUM(Amount_Paid) AS Total_Spent
                        FROM expenses WHERE Category = 'Healthcare'GROUP BY MONTH(date), Month
                        ORDER BY FIELD(Month, 'January', 'February', 'March', 'April', 'May', 'June', 
                            'July', 'August', 'September', 'October', 'November', 'December');""",
                            
        "💾Monthly shopping trend":"""SELECT MONTHNAME(date) AS Month, 
                      SUM(Amount_Paid) AS Total_Spent FROM expenses
               WHERE Category = 'Shopping' GROUP BY MONTH(date), Month
               ORDER BY FIELD(Month, 'January', 'February', 'March', 'April', 'May', 'June', 
                                    'July', 'August', 'September', 'October', 'November', 'December');"""
    
    }

    selected_query = st.selectbox("Select a Query", list(query_options.keys()))

    # Run the query automatically when selection changes
    if selected_query:
        df = run_query(query_options[selected_query])
        st.dataframe(df)  # Display the DataFrame


# -------------------------------- PAGE 3: Expenses Data Visualization --------------------------------
elif page == "📊 Data Visualization":
    st.subheader("📊 Data Visualization")

    visualization_options = {
        "📈 Monthly Expense Trend": "SELECT MONTH(Date) AS Month, SUM(Amount_Paid) AS Total_Spent FROM expenses GROUP BY Month ORDER BY Month;",
        
        "📊 Spending Distribution by Category": "SELECT Category, SUM(Amount_Paid) AS Total_Spent FROM expenses GROUP BY Category ORDER BY Total_Spent DESC;",
       
        "🔢Frequency of Transactions per Category":"SELECT Category FROM expenses;",
        
        "💸 Total Cashback for Each Category": """SELECT category, SUM(cashback) AS total_cashback FROM expenses WHERE cashback > 0 
                                             GROUP BY category ORDER BY total_cashback DESC;""",
        
        "📡 Analyze Spending Patterns (Weekdays/Weekends)": """SELECT DAYNAME(date) AS day_of_week, SUM(amount_paid) AS total_spent FROM expenses
            GROUP BY day_of_week ORDER BY FIELD(day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');""",
    
        "💳 Total Amount Spent per Payment Mode":"SELECT Payment_Mode, SUM(Amount_Paid) AS Total_Spent FROM expenses  GROUP BY Payment_Mode;",

        "💰 Cashback/Rewards Earned Per Month":"""SELECT MONTH(date) AS month_number, MONTHNAME(date) AS month, SUM(cashback) AS total_cashback FROM expenses
                                                 GROUP BY month_number, month ORDER BY month_number;""",
        "🏥 Healthcare Spending Per Month": """SELECT MONTHNAME(date) AS Month, SUM(Amount_Paid) AS Total_Spent FROM expenses
               WHERE Category = 'Healthcare' GROUP BY MONTH(date), Month
               ORDER BY FIELD(Month, 'January', 'February', 'March', 'April', 'May', 'June', 
                                    'July', 'August', 'September', 'October', 'November', 'December');"""
    
    }

    selected_viz = st.selectbox("Select a Visualization", list(visualization_options.keys()))

    if selected_viz:
        query = visualization_options[selected_viz]
        df = run_query(query)

        if not df.empty:
            if selected_viz == "📈 Monthly Expense Trend":
                fig = px.line(df, x="Month", y="Total_Spent", markers=True, title=selected_viz)
                
            elif selected_viz == "📊 Spending Distribution by Category":
               # fig = px.pie(df, names="Category", values="Total_Spent", title=selected_viz)
                 fig = px.bar(df, x="Total_Spent", y="Category", title=selected_viz, 
               labels={"Total_Spent": "Total Amount Spent", "Category": "Expense Category"},
               orientation="h",  # Horizontal bar chart
               color="Total_Spent",  # Color based on spending
               color_continuous_scale="Blues")  # Blue gradient for better readability
                 
            elif selected_viz =="🔢Frequency of Transactions per Category":
                fig = px.histogram(df, x="Category", title="Transaction Frequency by Category",labels={"Category": "Expense Category"},color_discrete_sequence=["green"])
            
            elif selected_viz == "💰Category that spent the most in each month":
               # Plot the bar chart
                fig = px.bar(df, x="month_number", y="total_spent", color="category",
                    title="📊 Highest Spending Category Per Month",
                    labels={"month_number": "Month", "total_spent": "Total Spent", "category": "Category"},
                    text_auto=True)
                fig.update_xaxes(type="category")  # ✅ Ensures months are treated as categories (not continuous numbers)
                    
            elif selected_viz == "💳 Payment Mode Usage Over Time":
                fig = px.bar(df, x="Month", y="Total_Spent", color="Payment_Mode", barmode="stack", title=selected_viz)
            
            elif selected_viz == "💸 Total Cashback for Each Category":
                fig = px.bar(df, 
                     x="category", 
                     y="total_cashback", 
                     title="💸 Total Cashback for Each Category",
                     labels={"category": "Expense Category", "total_cashback": "Total Cashback"},
                     color="total_cashback",  # Coloring based on total cashback
                     color_continuous_scale="Viridis",  # Choosing a color scale for better visualization
                     text_auto=True)  # Adding text labels on bars

            elif selected_viz == "📡 Analyze Spending Patterns (Weekdays/Weekends)":
                df["day_of_week"] = pd.Categorical(df["day_of_week"], 
                                                categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], 
                                                ordered=True)

                # Ensure total_spent is numeric
                df["total_spent"] = pd.to_numeric(df["total_spent"], errors="coerce").fillna(0)

                # Categorize as Weekday or Weekend
                df["day_type"] = df["day_of_week"].apply(lambda x: "Weekend" if x in ["Saturday", "Sunday"] else "Weekday")

                # Create a grouped bar chart
                fig = px.bar(df, x="day_of_week", y="total_spent", color="day_type", 
                            title="Spending Patterns: Weekdays vs. Weekends",
                            labels={"total_spent": "Total Amount Spent", "day_of_week": "Day of the Week"},
                            barmode="group",
                            color_discrete_map={"Weekday": "blue", "Weekend": "red"})  # Custom colors
                
            elif selected_viz == "💳 Total Amount Spent per Payment Mode":
                fig = px.pie(df, names="Payment_Mode", values="Total_Spent", title="💳 Total Amount Spent per Payment Mode",hole=0.4,  # Creates a donut chart effect
                     color_discrete_sequence=px.colors.qualitative.Set2)  # Custom color theme
                
            elif selected_viz == "💰 Cashback/Rewards Earned Per Month":
                # Convert month names to categorical for correct ordering
                month_order = ["January", "February", "March", "April", "May", "June", 
                            "July", "August", "September", "October", "November", "December"]
                
                df["month"] = pd.Categorical(df["month"], categories=month_order, ordered=True)
                df = df.sort_values("month")

                # Create a bar chart for cashback earned per month
                fig = px.bar(df, x="month", y="total_cashback", title="💰 Cashback/Rewards Earned Per Month", 
                            labels={"month": "Month", "total_cashback": "Total Cashback Earned"},
                            text_auto=True, color="total_cashback", color_continuous_scale="Blues")
            
            elif selected_viz == "🏥 Healthcare Spending Per Month":
                # Ensure months are categorical for correct ordering
                month_order = ["January", "February", "March", "April", "May", "June", 
                            "July", "August", "September", "October", "November", "December"]
                
                df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)
                df = df.sort_values("Month")

                # Create a bar chart
                fig = px.bar(df, x="Month", y="Total_Spent", 
                            title="🏥 Healthcare Spending Per Month", labels={"Month": "Month", "Total_Spent": "Total Amount Spent"},
                            text_auto=True,  color="Total_Spent",  color_continuous_scale="Blues")
    
    
            st.plotly_chart(fig)
        else:
            st.warning("No data available for this visualization.")
            
# -------------------------------- PAGE 4: Creator Info --------------------------------

elif page == "👩‍💻 Creator Info":
    st.subheader("👩‍💻 Creator Information")
    st.write("Developed by Priya.")
    st.write("Built using Python, MySQL, and Streamlit.")         