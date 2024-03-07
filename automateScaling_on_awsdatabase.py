import boto3

def get_cpu_utilization(instance_id):
    cloudwatch_client = boto3.client('cloudwatch')
    response = cloudwatch_client.get_metric_statistics(
        Namespace='AWS/RDS',
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'DBInstanceIdentifier',
                'Value': instance_id
            },
        ],
        StartTime=...,  # Specify the start time for the metric data
        EndTime=...,    # Specify the end time for the metric data
        Period=300,     # Use a period of 5 minutes for monitoring
        Statistics=['Average']
    )

    datapoints = response['Datapoints']
    if datapoints:
        return datapoints[-1]['Average']  # Return the latest CPU utilization value
    else:
        return None

def modify_instance(instance_id, instance_class):
    rds_client = boto3.client('rds')
    response = rds_client.modify_db_instance(
        DBInstanceIdentifier=instance_id,
        DBInstanceClass=instance_class,
        ApplyImmediately=True
    )

    return response

def scale_database(instance_id, target_cpu_utilization):
    current_cpu_utilization = get_cpu_utilization(instance_id)
    if current_cpu_utilization is not None:
        if current_cpu_utilization > target_cpu_utilization:
            print(f"CPU utilization ({current_cpu_utilization}%) is above the target threshold.")
            # Increase instance class to handle increased workload
            # Example: For AWS RDS, modify the instance class to a higher tier
            new_instance_class = 'db.t3.large'  # Change this to the desired instance class
            response = modify_instance(instance_id, new_instance_class)
            print("Database instance scaled up to handle increased workload.")
        else:
            print(f"CPU utilization ({current_cpu_utilization}%) is within the target threshold.")
    else:
        print("Failed to retrieve CPU utilization data.")

if __name__ == "__main__":
    # AWS credentials and region
    aws_access_key_id = 'YOUR_AWS_ACCESS_KEY_ID'
    aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY'
    aws_region = 'YOUR_AWS_REGION'

    # Database instance details
    rds_instance_id = 'YOUR_RDS_INSTANCE_ID'

    # Target CPU utilization threshold (percentage)
    target_cpu_utilization = 70  # Adjust this threshold based on workload demand

    # Set up AWS credentials and region
    boto3.setup_default_session(region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Scale the database instance based on CPU utilization
    scale_database(rds_instance_id, target_cpu_utilization)
