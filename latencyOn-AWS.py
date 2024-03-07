import boto3
import time
import random

# Function to provision a cloud-based database instance
def provision_database_instance(instance_id, db_instance_class, db_engine, db_username, db_password):
    rds_client = boto3.client('rds')
    response = rds_client.create_db_instance(
        DBInstanceIdentifier=instance_id,
        DBInstanceClass=db_instance_class,
        Engine=db_engine,
        MasterUsername=db_username,
        MasterUserPassword=db_password,
        AllocatedStorage=20,  # Adjust storage size as needed
        MultiAZ=False,        # Disable Multi-AZ for simplicity
        PubliclyAccessible=True,  # Make the database accessible over the internet
        Tags=[
            {
                'Key': 'Name',
                'Value': 'SampleDatabase'
            },
        ]
    )
    return response

# Function to initialize the database with sample data
def initialize_database(instance_endpoint, db_username, db_password):
    # Connect to the database using appropriate client library
    # For example, using psycopg2 for PostgreSQL
    # Replace the following code with database-specific initialization
    import psycopg2

    try:
        conn = psycopg2.connect(
            host=instance_endpoint,
            database='sample_db',  # Replace 'sample_db' with actual database name
            user=db_username,
            password=db_password
        )
        cursor = conn.cursor()

        # Execute SQL statements to create tables and insert sample data
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(255));")
        cursor.execute("INSERT INTO users (name) VALUES ('User1'), ('User2'), ('User3');")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized with sample data.")
    except Exception as e:
        print("Error initializing database:", e)

# Function to run performance tests and measure query latency
def run_performance_tests(instance_endpoint, db_username, db_password):
    # Connect to the database and execute sample queries
    # For example, using psycopg2 for PostgreSQL
    # Replace the following code with database-specific performance tests
    import psycopg2

    try:
        conn = psycopg2.connect(
            host=instance_endpoint,
            database='sample_db',  # Replace 'sample_db' with actual database name
            user=db_username,
            password=db_password
        )
        cursor = conn.cursor()

        # Run a series of sample queries and measure query latency
        query_latency = []
        for _ in range(10):  # Run 10 sample queries
            start_time = time.time()
            cursor.execute("SELECT * FROM users ORDER BY id;")
            query_latency.append(time.time() - start_time)
        
        avg_latency = sum(query_latency) / len(query_latency)
        print(f"Average query latency: {avg_latency:.3f} seconds")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error running performance tests:", e)

# Main function
def main():
    # AWS credentials and region
    aws_access_key_id = 'YOUR_AWS_ACCESS_KEY_ID'
    aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY'
    aws_region = 'YOUR_AWS_REGION'

    # Database instance details
    instance_id = 'sample-db-instance'
    db_instance_class = 'db.t2.micro'
    db_engine = 'postgres'  # PostgreSQL database engine
    db_username = 'admin'
    db_password = 'password'

    # Set up AWS credentials and region
    boto3.setup_default_session(region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Provision the database instance
    provision_response = provision_database_instance(instance_id, db_instance_class, db_engine, db_username, db_password)
    if provision_response.get('DBInstance'):
        instance_endpoint = provision_response['DBInstance']['Endpoint']['Address']
        print("Database instance provisioned successfully. Endpoint:", instance_endpoint)

        # Initialize the database with sample data
        initialize_database(instance_endpoint, db_username, db_password)

        # Run performance tests and measure query latency
        run_performance_tests(instance_endpoint, db_username, db_password)
    else:
        print("Failed to provision database instance.")

if __name__ == "__main__":
    main()
