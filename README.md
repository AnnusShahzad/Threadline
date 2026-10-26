# Threadline

An open-source, Maltego-style link-analysis framework for OSINT investigations. Start from one
entity — a domain, IP address, email or username — run transforms on it, and explore the graph
that comes back.

Maltego popularised this workflow but is proprietary and built around a closed transform
ecosystem. Open-source alternatives such as SpiderFoot, theHarvester and Recon-ng automate
collection without centring on interactive graph pivoting. Threadline fills that gap: local,
inspectable, and extensible through a transform format anyone can implement.

## Status

Proposal stage. No application code yet; the plan below is what this repository is being built
toward over one month, by one developer.

## What the MVP covers

- Typed entities and edges in SQLite, reusing Maltego-style type names where practical.
- Transforms discovered from a local `transforms/` folder, each a manifest plus an executable.
- An asynchronous runner with timeouts, concurrency limits, per-source rate limiting and clear
  error reporting.
- Six to eight starter transforms over keyless sources (certificate transparency, DNS, WHOIS)
  and keyed sources (for example Shodan and VirusTotal).
- API keys entered, changed and removed inside the application; keyed transforms stay disabled
  until a key exists.
- A web graph canvas: add entities, run transforms from a context menu, expand, filter, delete
  and inspect properties.
- A reproducible demonstration investigation, documented end to end.

## Architecture

Four components, all on the investigator's machine, so investigation data never depends on a
third-party service:

| Component | Responsibility |
| --- | --- |
| Storage | entities, edges and investigation metadata in SQLite |
| Transform engine | discovers, validates and executes transforms |
| Backend | FastAPI + asyncio API for investigations, entities, transforms and settings |
| Client | Cytoscape.js graph canvas |

Transform execution is a subprocess boundary: one entity arrives as JSON on stdin, a JSON list
of entities and edges leaves on stdout. Only JSON crosses it, so the format stays
language-agnostic even though Python is the only implementation shipped this milestone.

A transform is a folder:

    transforms/
      domain_to_subdomains/
        manifest.json
        run.py

with a manifest declaring what it accepts, produces and needs:

```json
{
  "name": "Domain to Subdomains (crt.sh)",
  "version": "0.1.0",
  "input_type": "Domain",
  "output_types": ["Domain"],
  "requires_api_key": false,
  "timeout_seconds": 30,
  "command": ["python", "run.py"]
}
```

## Not in this milestone

- A hosted transform registry, or any remote transform distribution.
- Maltego compatibility: neither acting as a remote transform server nor importing/exporting
  Maltego GraphML graphs.
- Multi-user collaboration, authentication and shared investigations.
- Very large graphs (tens of thousands of nodes) and GPU-accelerated rendering.
- Automated reporting, machine-learning entity resolution and scheduled monitoring.
- Transform SDKs for languages other than Python, and AI-assisted investigation.

## Intended use

Lawful investigation only, using public information or sources the investigator is licensed or
authorized to use.
