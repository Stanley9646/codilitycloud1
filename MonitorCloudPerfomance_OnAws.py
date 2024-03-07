import boto3
from datetime import datetime, timedelta

# Function to retrieve CloudWatch metrics for a specific RDS instance
def get_rds_metrics(instance_id, metric_name, period, threshold):
    cloudwatch_client = boto3.client('cloudwatch')

    # Calculate the start and end time for the metric data
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=period)

    # Retrieve metric data from CloudWatch
    response = cloudwatch_client.get_metric_statistics(
        Namespace='AWS/RDS',
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': 'DBInstanceIdentifier',
                'Value': instance_id
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=60,  # Use a period of 60 seconds for more granular data
        Statistics=['Average']
    )

    # Extract the data points from the response
    datapoints = response['Datapoints']

    # Check if any data point exceeds the threshold
    for datapoint in datapoints:
        average_value = datapoint['Average']
        if average_value > threshold:
            print(f"Alert: {metric_name} for instance {instance_id} exceeded threshold ({threshold}): {average_value}")

# Main function
def main():
    # AWS credentials and region
    aws_access_key_id = 'YOUR_AWS_ACCESS_KEY_ID'
    aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY'
    aws_region = 'YOUR_AWS_REGION'

    # RDS instance details
    rds_instance_id = 'YOUR_RDS_INSTANCE_ID'

    # Define thresholds for metrics
    cpu_threshold = 80  # CPU utilization threshold (percentage)
    memory_threshold = 80  # Memory usage threshold (percentage)
    disk_io_threshold = 1000  # Disk I/O threshold (IOPS)

    # Set up AWS credentials and region
    boto3.setup_default_session(region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Retrieve metrics and generate alerts after five minutes
    get_rds_metrics(rds_instance_id, 'CPUUtilization', 5, cpu_threshold) 
    get_rds_metrics(rds_instance_id, 'FreeableMemory', 5, memory_threshold)
    get_rds_metrics(rds_instance_id, 'DiskReadOps', 5, disk_io_threshold)
    get_rds_metrics(rds_instance_id, 'DiskWriteOps', 5, disk_io_threshold)

if __name__ == "__main__":
    main()
