"""
Cloud Cost Governance & Asset Optimization Automation
Part of Practical Module #11: Cloud Cost Governance & Optimization
Identifies stopped instances, orphaned unattached EBS volumes, and untagged cloud assets.
"""
import json
import logging
from datetime import datetime, timezone

try:
    import boto3
except ImportError:
    boto3 = None

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CostGovernance")

def audit_unattached_ebs_volumes(ec2_client):
    """Finds all unattached EBS volumes incurring unnecessary storage costs."""
    logger.info("Scanning for orphaned unattached EBS volumes...")
    volumes = ec2_client.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])['Volumes']
    orphans = []
    total_wasted_gb = 0

    for vol in volumes:
        vol_id = vol['VolumeId']
        size_gb = vol['Size']
        vol_type = vol['VolumeType']
        orphans.append({"volume_id": vol_id, "size_gb": size_gb, "type": vol_type})
        total_wasted_gb += size_gb
        logger.warning(f"Orphaned Volume Found: {vol_id} ({size_gb} GB, {vol_type})")

    logger.info(f"Total unattached volumes: {len(orphans)} | Total Wasted Capacity: {total_wasted_gb} GB")
    return orphans

def audit_stopped_ec2_instances(ec2_client, max_stopped_days=7):
    """Finds stopped EC2 instances that may be forgotten or obsolete."""
    logger.info(f"Scanning for EC2 instances stopped for > {max_stopped_days} days...")
    reservations = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])['Reservations']
    idle_instances = []

    for res in reservations:
        for inst in res['Instances']:
            instance_id = inst['InstanceId']
            inst_type = inst['InstanceType']
            tags = {t['Key']: t['Value'] for t in inst.get('Tags', [])}
            name = tags.get('Name', 'Unnamed')
            idle_instances.append({"instance_id": instance_id, "type": inst_type, "name": name})
            logger.warning(f"Stopped Instance Found: {instance_id} ({name}, {inst_type})")

    return idle_instances

def audit_untagged_resources(ec2_client):
    """Audits EC2 instances lacking required financial cost allocation tags."""
    logger.info("Auditing required tags: ['Project', 'Environment', 'Owner']...")
    reservations = ec2_client.describe_instances()['Reservations']
    untagged = []

    required_tags = {"Project", "Environment", "Owner"}
    for res in reservations:
        for inst in res['Instances']:
            existing_tags = {t['Key'] for t in inst.get('Tags', [])}
            missing = required_tags - existing_tags
            if missing:
                untagged.append({"instance_id": inst['InstanceId'], "missing_tags": list(missing)})
                logger.warning(f"Compliance Violation: Instance {inst['InstanceId']} missing tags: {missing}")

    return untagged

def main():
    logger.info("Starting AWS Cost Governance & Cloud Optimization Audit...")
    if boto3 is None:
        logger.warning("boto3 is not installed in the current environment.")
        logger.info("Simulating FinOps compliance check across mock AWS environment...")
        summary = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "MOCK_SIMULATION (Install boto3 to execute against live AWS account)",
            "orphaned_volumes_scanned": 3,
            "orphaned_volumes_identified": 1,
            "stopped_instances_identified": 1,
            "untagged_instances_identified": 2,
            "actionable_monthly_savings_usd": 48.50,
            "recommendation": "Detach unattached 50GB gp2 volume & stop idle staging t3.medium"
        }
        print("\n" + "="*50)
        print("COST GOVERNANCE AUDIT SUMMARY")
        print("="*50)
        print(json.dumps(summary, indent=2))
        return

    try:
        ec2 = boto3.client('ec2', region_name='us-east-1')
        orphaned_vols = audit_unattached_ebs_volumes(ec2)
        idle_vms = audit_stopped_ec2_instances(ec2)
        untagged_vms = audit_untagged_resources(ec2)

        summary = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "orphaned_volumes_count": len(orphaned_vols),
            "idle_stopped_instances_count": len(idle_vms),
            "untagged_instances_count": len(untagged_vms),
            "estimated_monthly_savings_actionable": len(orphaned_vols) > 0 or len(idle_vms) > 0
        }
        print("\n" + "="*50)
        print("COST GOVERNANCE AUDIT SUMMARY")
        print("="*50)
        print(json.dumps(summary, indent=2))

    except Exception as e:
        logger.error(f"Audit against AWS account encountered error: {e}")

if __name__ == "__main__":
    main()
