#!/usr/bin/env python3
import argparse
import subprocess

STATE_MAP = {
    "BOOT_FAIL": "failed",
    "CANCELLED": "failed",
    "COMPLETED": "success",
    "CONFIGURING": "running",
    "COMPLETING": "running",
    "DEADLINE": "failed",
    "FAILED": "failed",
    "NODE_FAIL": "failed",
    "OUT_OF_MEMORY": "failed",
    "PENDING": "running",
    "PREEMPTED": "failed",
    "RUNNING": "running",
    "RESIZING": "running",
    "SUSPENDED": "running",
    "TIMEOUT": "failed"
}


def fetch_status(batch_id):
    """fetch the status for the batch id"""
    sacct_args = ["sacct", "-j",  batch_id, "-o", "State", "--parsable2",
                  "--noheader"]
    output = subprocess.check_output(sacct_args).decode("utf-8").strip()

    # The first output is the state of the overall job
    # See
    # https://stackoverflow.com/questions/52447602/slurm-sacct-shows-batch-and-extern-job-names
    # for details
    job_status = output.split("\n")[0]

    # If the job was cancelled manually, it will say by who, e.g "CANCELLED by 12345"
    # We only care that it was cancelled
    if job_status.startswith("CANCELLED by"):
        return "CANCELLED"

    # Otherwise, return the status
    return job_status


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("batch_id", type=str)
    args = parser.parse_args()

    status = fetch_status(args.batch_id)

    print(STATE_MAP[status])
