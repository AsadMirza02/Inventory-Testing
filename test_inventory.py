import pytest
import mysql.connector

# Fixture to connect to the MySQL database
@pytest.fixture
def db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="Bingochingo11!",  # Replace with your MySQL password
        database="inventory_system"
    )
    yield conn
    conn.close()

# Test Case 1: Insert a new product
def test_insert_product(db_connection):
    cursor = db_connection.cursor()

    # Insert a new product
    cursor.execute("INSERT INTO Products (name, stock) VALUES ('Headphones', 15)")
    db_connection.commit()

    # Validate the insertion
    cursor.execute("SELECT * FROM Products WHERE name = 'Headphones'")
    result = cursor.fetchone()

    assert result[1] == 'Headphones'
    assert result[2] == 15

# Test Case 2: Update stock for a product
def test_update_stock(db_connection):
    cursor = db_connection.cursor()

    # Update stock
    cursor.execute("UPDATE Products SET stock = stock + 10 WHERE name = 'Laptop'")
    db_connection.commit()

    # Validate the update
    cursor.execute("SELECT stock FROM Products WHERE name = 'Laptop'")
    result = cursor.fetchone()

    assert result[0] == 60

# Test Case 3: Prevent negative stock
def test_prevent_negative_stock(db_connection):
    cursor = db_connection.cursor()

    # Try to set stock to a negative value
    try:
        cursor.execute("UPDATE Products SET stock = -10 WHERE name = 'Phone'")
        db_connection.commit()
    except mysql.connector.Error as e:
        db_connection.rollback()

    # Validate that stock didn't change
    cursor.execute("SELECT stock FROM Products WHERE name = 'Phone'")
    result = cursor.fetchone()

    assert result[0] == 30

# Test Case 4: Place an order
def test_place_order(db_connection):
    cursor = db_connection.cursor()

    # Place an order
    cursor.execute("INSERT INTO Orders (product_id, quantity) VALUES (1, 5)")
    db_connection.commit()

    # Validate the order
    cursor.execute("SELECT * FROM Orders WHERE product_id = 1")
    result = cursor.fetchone()

    assert result[1] == 1
    assert result[2] == 5

# Test Case 5: Check stock after order
def test_stock_after_order(db_connection):
    cursor = db_connection.cursor()

    # Check stock after placing an order
    cursor.execute("SELECT stock FROM Products WHERE id = 1")
    result = cursor.fetchone()

    assert result[0] == 45  # Assuming initial stock was 50 and 5 were ordered
