# Job Board Aggregator

One clean job feed from four public job boards: **Jobicy**, **Remote OK**, **JobTech Sweden** and the **Hacker News "Who is hiring"** thread (with YC job posts). Every job comes back in the same schema (title, company, place, remote flag, salary where published, posting date, description, source board and link to the job). A job listed on two boards comes back once, with both links. Phone numbers and e-mail addresses in descriptions are masked. No login, no cookies, no CAPTCHA handling.

[![Run on Apify](https://img.shields.io/badge/Run%20on-Apify-97D700?logo=apify&logoColor=white)](https://apify.com/bardach_technologies/public-job-boards-aggregator)

**[Run on Apify: apify.com/bardach_technologies/public-job-boards-aggregator](https://apify.com/bardach_technologies/public-job-boards-aggregator)**

## Who it is for

- You want remote jobs, startup hiring posts and Swedish public-sector ads in one dataset, filtered by keyword, place, remote and age.
- You run a daily feed and want only jobs not delivered before (`onlyNewSinceLastRun`).
- You build a job board or newsletter and need each row to carry its source and a link back.

It does not read LinkedIn, Indeed, Glassdoor or Google Jobs, and not the career sites of single companies.

## Input

```json
{"sources": ["jobicy", "remoteok", "jobtech"], "keywords": ["engineer"], "maxJobs": 10}
```

Empty input reads all four boards and delivers up to 100 jobs. Add `"onlyNewSinceLastRun": true` for a daily feed. See [examples/input.json](examples/input.json).

## Output

One row per job (a real row from a run on 19.11.2026):

```json
{"type": "job", "id": "hackernews:50545238", "source": "hackernews", "sourceName": "Hacker News",
 "url": "https://news.ycombinator.com/item?id=50545238",
 "applyUrl": "https://www.ycombinator.com/companies/evidence/jobs/1xb9PpP-founding-gtm-lead",
 "title": "Evidence (YC S21) Is Hiring", "company": "Evidence (YC S21)", "location": null, "country": null, "remote": null,
 "employmentTypes": [], "categories": ["Hacker News job post"], "level": null, "salary": null,
 "postedAt": "2026-11-18T12:00:16Z", "description": null, "contactsMasked": 0, "alsoListedOn": [],
 "credit": "Posts of the monthly Who is hiring thread and the YC job posts, from the official Hacker News API.",
 "scrapedAt": "2026-11-18T20:36:40Z"}
```

Free `source` rows say how each board went (status, postings read, delivered).

## Pricing

Pay per event: **USD 0.002 per delivered job** (USD 2.00 per 1,000 jobs), plus Apify's start event of USD 0.00005 per run. Source rows, blocked or failed boards and jobs already delivered cost nothing. Your maximum charge stops the run exactly.

## Use it from your code

Install the official client and put your API token in the environment (never in the code):

```bash
pip install apify-client
export APIFY_TOKEN=<your Apify API token>
python examples/call_actor.py
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("bardach_technologies/public-job-boards-aggregator").call(
    run_input={"sources": ["jobicy", "remoteok"], "keywords": ["engineer"], "maxJobs": 10}
)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    if item.get("type") == "job":
        print(item["title"], item["url"])
```

Full script: [examples/call_actor.py](examples/call_actor.py).

## Credit and terms

Each row has a `credit` field with what the source board asks for when you republish. Read a board's current terms before you publish its data.

## License

MIT, see [LICENSE](LICENSE). The Actor itself runs on the Apify platform; this repository holds the documentation and usage examples.
