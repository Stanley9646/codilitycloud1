import boto3
from datetime import datetime, timedelta

def create_database_snapshot(instance_id, snapshot_id):
    rds_client = boto3.client('rds')
    response = rds_client.create_db_snapshot(
        DBSnapshotIdentifier=snapshot_id,
        DBInstanceIdentifier=instance_id
    )
    return response

def delete_database_snapshot(snapshot_id):
    rds_client = boto3.client('rds')
    response = rds_client.delete_db_snapshot(
        DBSnapshotIdentifier=snapshot_id
    )
    return response

def restore_database(instance_id, snapshot_id):
    rds_client = boto3.client('rds')
    response = rds_client.restore_db_instance_from_db_snapshot(
        DBInstanceIdentifier=instance_id,
        DBSnapshotIdentifier=snapshot_id,
        PubliclyAccessible=True,  # Make the restored instance publicly accessible
        AutoMinorVersionUpgrade=True  # Enable automatic minor version upgrades
    )
    return response

def list_database_snapshots(instance_id):
    rds_client = boto3.client('rds')
    response = rds_client.describe_db_snapshots(
        DBInstanceIdentifier=instance_id
    )
    snapshots = response['DBSnapshots']
    return snapshots

def find_latest_snapshot(snapshots):
    if snapshots:
        latest_snapshot = max(snapshots, key=lambda x: x['SnapshotCreateTime'])
        return latest_snapshot
    else:
        return None

def cleanup_old_snapshots(instance_id, retention_days):
    rds_client = boto3.client('rds')
    response = rds_client.describe_db_snapshots(
        DBInstanceIdentifier=instance_id
    )
    snapshots = response['DBSnapshots']
    if snapshots:
        current_time = datetime.now()
        for snapshot in snapshots:
            snapshot_time = snapshot['SnapshotCreateTime']
            age = current_time - snapshot_time.replace(tzinfo=None)
            if age.days >= retention_days:
                delete_database_snapshot(snapshot['DBSnapshotIdentifier'])
                print(f"Old snapshot '{snapshot['DBSnapshotIdentifier']}' deleted.")
    else:
        print("No snapshots found.")

def main():
    # AWS credentials and region
    aws_access_key_id = 'YOUR_AWS_ACCESS_KEY_ID'
    aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY'
    aws_region = 'YOUR_AWS_REGION'

    # Database instance details
    instance_id = 'sample-db-instance'

    # Backup settings
    snapshot_id = f"{instance_id}-snapshot-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
    retention_days = 7  # Number of days to retain snapshots

    # Set up AWS credentials and region
    boto3.setup_default_session(region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Create database snapshot
    create_database_snapshot(instance_id, snapshot_id)
    print(f"Snapshot '{snapshot_id}' created.")

    # Cleanup old snapshots
    cleanup_old_snapshots(instance_id, retention_days)

    # Restore database from the latest snapshot (optional)
    snapshots = list_database_snapshots(instance_id)
    latest_snapshot = find_latest_snapshot(snapshots)
    if latest_snapshot:
        restore_database(instance_id, latest_snapshot['DBSnapshotIdentifier'])
        print(f"Database instance '{instance_id}' restored from snapshot '{latest_snapshot['DBSnapshotIdentifier']}'.")

if __name__ == "__main__":
    main()
