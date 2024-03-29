import boto3
from typing import Dict, List


def submit_batch_job(
    command: str, job_name: str, dependencies: List[str] = [], tag=None
):
    session = boto3.session.Session()
    batch = session.client("batch")
    job_definition = "sm-job"
    if tag:
        job_definition = f"{job_definition}-{tag}"
    submit_job_response = batch.submit_job(
        jobName=job_name,
        jobQueue="sm-queue",
        jobDefinition=job_definition,
        containerOverrides={"command": command.split(" ")},
        dependsOn=[{"jobId": dep, "type": "N_TO_N"} for dep in dependencies],
    )
    job_id = submit_job_response["jobId"]
    print(f"Submitted job {job_name} {job_id}")
    return job_id


def get_job_status(job_id: str) -> Dict:
    session = boto3.session.Session()
    batch = session.client("batch")
    describe_jobs_response = batch.describe_jobs(jobs=[job_id])
    return describe_jobs_response["jobs"][0]["status"]
