# Preparing a judge demonstration

Start the API and frontend using the README. With a real backend Gemma key configured, run:

```powershell
.\.venv\Scripts\python.exe scripts/prepare_judge_demo.py
.\.venv\Scripts\python.exe scripts/check_judge_demo.py
```

The first command creates a seven-source fictional Nova Internship investigation, runs actual Gemma extraction, and prepares separately labeled authored controls. It writes local URLs, original evidence and results under the ignored data/judge-demo directory. Each run creates a new case and may call the cloud provider.

The second command uses the analyst-review API to normalize a repeated registration obligation and a numeric eligibility criterion against the authored sources. It preserves original extraction and records explicit review history, then checks simulation, profiles, hashes and reports. Provider challenge is separate; errors must never be relabeled as success. To prepare exports without repeating a challenge request, use --skip-challenge.

The local app accepts ?investigation=<UUID>&provider=gemma to open a prepared case. Local investigation IDs and original evidence are not published by these scripts.

A strong timed route is original images -> evidence pair and conservative scope checks -> calculator -> Journey and dated change -> hypothetical PromiseLab -> connected evidence graph -> dossier and MIT-licensed original engine. Longer demos can show eligibility, conditions, claim corrections, analyst decisions, clarification drafts, receipt comparisons, explicit providers, batch ingestion, and negative controls.

Disclose the fictional sources, saved run timing, any analyst corrections, approximate image quotations, and authored fixture provenance. A model output or accepted review does not authenticate a source. A dated revision is not necessarily a simultaneous contradiction. A byte-identical receipt does not prove authorship. Keep the reviewed saved case intact and use a fresh investigation for a live inference rerun.
