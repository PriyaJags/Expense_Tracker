import random
import calendar
import datetime
import pandas as pd
from faker import Faker
from db_utils import get_db_connection

# Expense categories & descriptions
categories = ["Food", "Transport", "Bills", "Entertainment", "Shopping", "Healthcare", "Travel", "Subscriptions"]
payment_modes = ["Cash", "Credit Card", "Debit Card", "UPI", "Net Banking"]

# Description lists (customized for categories)
descriptions = {
    "Food": ["Lunch at McDonald's", "Dinner at Italian Restaurant", "Bought groceries"],
    "Transport": ["Uber Ride", "Metro Ticket", "fuel"],
    "Bills": ["Electricity bill", "Water bill", "House maintenance"],
    "Entertainment": ["Movie ticket", "Concert pass", "Amusement park entry"],
    "Shopping": ["Bought new shoes", "Electronics purchase","clothing","beauty products","branded bag"],
    "Healthcare": ["Doctor's consultation", "Pharmacy purchase", "Dental checkup"],
    "Travel": ["Flight ticket booking", "Hotel stay", "Train ticket purchase"],
    "Subscriptions": ["Netflix Subscription", "Spotify Premium", "Amazon Prime"]
}

# Generate random expenses
def generate_expenses(num_records_per_month):
    data = []
    fake = Faker()
    
    for month in range(1, 13):  # January to December
        last_day = calendar.monthrange(2024, month)[1]  # Last day of month
        
        for _ in range(num_records_per_month):
            category = random.choice(categories)
            description = random.choice(descriptions[category])
            random_date = fake.date_between(datetime.date(2024, month, 1), datetime.date(2024, month, last_day))
            
            expense = {
                "date": random_date,
                "category": category,
                "payment_mode": random.choice(payment_modes),
                "description": description,
                "amount_paid": round(random.uniform(500, 10000), 2),
                "cashback": round(random.uniform(0, 20), 2) if random.random() < 0.1 else 0
            }
            data.append(expense)
    
    return pd.DataFrame(data)

# Insert data into MySQL database
def insert_expenses_into_db(df):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE,
        category VARCHAR(50),
        payment_mode VARCHAR(50),
        description VARCHAR(255),
        amount_paid DECIMAL(10,2),
        cashback DECIMAL(10,2)
    );
    """
    cursor.execute(create_table_query)
    
    insert_query = """
    INSERT INTO expenses (date, category, payment_mode, description, amount_paid, cashback) 
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    records = list(df.itertuples(index=False, name=None))
    cursor.executemany(insert_query, records)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Data inserted successfully!")

# Run this only when executing this script directly
if __name__ == "__main__":
    num_recs=100
    df = generate_expenses(num_recs)  # Generate 12 records per month
    insert_expenses_into_db(df)