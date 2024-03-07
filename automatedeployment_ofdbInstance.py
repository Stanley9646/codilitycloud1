import boto3

def create_database_instance(instance_id, db_instance_class, db_engine, db_username, db_password):
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

        # Execute SQL statements to create tables based on predefined schema
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("Database initialized with tables based on predefined schema.")
    except Exception as e:
        print("Error initializing database:", e)
    finally:
        cursor.close()
        conn.close()

def configure_security(instance_id, security_group_id):
    rds_client = boto3.client('rds')
    response = rds_client.modify_db_instance(
        DBInstanceIdentifier=instance_id,
        VpcSecurityGroupIds=[
            security_group_id
        ],
        ApplyImmediately=True
    )
    return response

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

    # Security group details
    security_group_id = 'sg-1234567890'  # Replace with actual security group ID

    # Set up AWS credentials and region
    boto3.setup_default_session(region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Provision the database instance
    provision_response = create_database_instance(instance_id, db_instance_class, db_engine, db_username, db_password)
    if provision_response.get('DBInstance'):
        instance_endpoint = provision_response['DBInstance']['Endpoint']['Address']
        print("Database instance provisioned successfully. Endpoint:", instance_endpoint)

        # Initialize the database with predefined schema
        initialize_database(instance_endpoint, db_username, db_password)

        # Configure security settings
        configure_security(instance_id, security_group_id)
        print("Security settings configured.")
    else:
        print("Failed to provision database instance.")

if __name__ == "__main__":
    main()
