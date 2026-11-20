"""Run the Job Board Aggregator Actor on Apify and print the jobs it returns.

Setup:
    pip install apify-client
    export APIFY_TOKEN=<your Apify API token>   # read from the environment, never hard-coded
    python call_actor.py
"""
import json
import os
from pathlib import Path

from apify_client import ApifyClient

ACTOR_ID = "bardach_technologies/public-job-boards-aggregator"


def main() -> None:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        raise SystemExit("Set the APIFY_TOKEN environment variable first.")

    run_input = json.loads((Path(__file__).parent / "input.json").read_text())

    client = ApifyClient(token)
    run = client.actor(ACTOR_ID).call(run_input=run_input)

    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        if item.get("type") != "job":
            continue  # "source" rows only report how each board went (free)
        print(f'{item["title"]} | {item.get("company")} | {item["sourceName"]} | {item["url"]}')


if __name__ == "__main__":
    main()
