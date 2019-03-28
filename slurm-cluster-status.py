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


def fetch_statuses(batch_id):
    """fetch all statuses for the batch id.
    A batch id _may_ have multiple statuses"""
    sacct_args = ["sacct", "-j",  batch_id, "-o", "State", "--parsable"]
    output = subprocess.check_output(sacct_args).decode("utf-8").strip()
    return set(map(lambda x: x.strip("|"), output.split("\n")[1:]))


def final_state(statuses):
    """Get the final state on a list of snakemake statuses"""
    if "failed" in statuses:
        return "failed"
    if "running" in statuses:
        return "running"
    if "success" in statuses:
        return "success"
    raise NotImplementedError


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("batch_id", type=str)
    args = parser.parse_args()

    statuses = fetch_statuses(args.batch_id)
    snakemake_statuses = set(map(lambda x: STATE_MAP[x.upper()], statuses))

    print(final_state(snakemake_statuses))
