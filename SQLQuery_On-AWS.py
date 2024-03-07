import psycopg2 #PostgreSQL adapter for Python
from psycopg2 import Error #andle exceptions in db operations

def execute_sql_query():
    # Database connection parameters
    db_host = 'your_database_host'
    db_port = 'your_database_port'
    db_name = 'your_database_name'
    db_user = 'your_database_username'
    db_password = 'your_database_password'

    try:
        # Establish database connection
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # SQL query to retrieve the total number of orders placed by each customer
        sql_query = """
            SELECT customer_id, COUNT(*) AS total_orders
            FROM orders
            GROUP BY customer_id
            ORDER BY total_orders DESC
        """

        # Execute the SQL query
        cursor.execute(sql_query)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Print the results by iterating fetched rows
        for row in rows:
            customer_id, total_orders = row
            print(f"Customer ID: {customer_id}, Total Orders: {total_orders}")

    except Error as e:
        print("Error connecting to the database:", e)

    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    execute_sql_query()
