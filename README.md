# Ransomware Defense Mapping with ATT&CK, D3FEND, and Platform0-style Testing

> Map ransomware-relevant MITRE ATT&CK techniques to MITRE D3FEND defensive patterns and Platform0-style control tests, using a small data model, a resolver CLI, and an example ransomware kill chain.

## 1. Overview

This repository is a small, opinionated reference implementation for **operationalizing ransomware threat modeling**.

Instead of stopping at ATT&CK diagrams, it links:

- **ATT&CK techniques** (ransomware-relevant subset)
- **D3FEND defensive techniques**
- **Concrete security controls** that can be **tested** via Platform0-style jobs

The goal is to help practitioners answer questions like:

- *“For this ransomware technique, what defenses do we have, and are they tested?”*
- *“For this control, which ransomware behaviors does it actually help with?”*

This is **not** a complete ATT&CK or D3FEND implementation. It is a **minimal, inspectable model** you can fork and adapt.

---

## 2. Concept: ATT&CK, D3FEND, and Platform0-style testing

At the core of this repo is a simple mapping:
```plain
ATT&CK Technique ──▶ D3FEND Technique(s) ──▶ Control(s) + Test(s)
```

- **MITRE ATT&CK** describes what adversaries do.
- **MITRE D3FEND** describes defensive techniques that can mitigate those behaviors.
- **Platform0-style testing** treats each control check as a **stateless job** that writes **durable evidence** into storage.

By connecting these three layers, we can:

- Express **ransomware kill chains** as sequences of ATT&CK techniques.
- Map each technique to **defensive patterns** (D3FEND).
- Map defensive patterns to **controls** we can actually deploy and test.
- Compute a **coverage view per environment** from test results.

---

## 3. Data model

All core data lives in a few JSON / JSONL files.

### 3.1 ATT&CK techniques (subset)

`data/attack_techniques.json`

- Small subset of ransomware-relevant techniques.
- Each entry includes:
```json
{
  "id": "T1486",
  "name": "Data Encrypted for Impact",
  "tactic": "Impact",
  "description": "Adversaries encrypt data on a single or multiple systems...",
  "ransomware_relevance": true
}
```

### 3.2 D3FEND defensive techniques

`data/d3fend_techniques.json`

- Subset of D3FEND entries that are useful for ransomware defense.
```json
{
  "id": "D3-EXFIL-001",
  "name": "File Content Inspection",
  "category": "Detection",
  "description": "Inspect file contents for malicious patterns or anomalies..."
}
```

### 3.3 ATT&CK → D3FEND mappings

`data/attack_to_d3fend.jsonl`

- Many-to-many links between ATT&CK and D3FEND, one JSON object per line.
````json
{"attack_id": "T1486", "d3fend_id": "D3-EXFIL-001", "justification": "Detects anomalous encryption or exfil content patterns."}
````

### 3.4 Controls and environment state

`controls/controls.jsonl`

- Logical controls that can be tested via Platform0-style jobs.
```json
{
  "id": "ctrl.backup.immutable",
  "name": "Immutable backup storage",
  "category": "backup",
  "scenario_id": "scn.backup.immutable.check",
  "evidence_schema_ref": "schemas/backup_immutable.json"
}
```

`controls/env_controls.example.jsonl`

- Example environment state showing which controls are deployed and tested.
```json
{
  "env_id": "lab-1",
  "control_id": "ctrl.backup.immutable",
  "deployment_state": "full",
  "last_test_time": "2025-12-30T08:00:00Z",
  "last_test_status": "pass"
}
```

---

## 4. Quickstart

> These steps assume you are working locally with Python 3.11+ and a standard virtualenv or poetry setup. Adjust paths as needed.

1. **Clone the repo**
```bash
git clone <REPO_URL>
cd ransomware-defense-mapping
```

2. **Create and activate a virtual environment** (example using `python -m venv`):
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

3. **Install dependencies**

If you use a `requirements.txt`:
```bash
pip install -r requirements.txt
```

4. **Run a sample mapping query**

Once the CLI is implemented, you should be able to run something like:
```bash
python -m src.cli map T1486 --env lab-1
```

Expected behavior (conceptually):

- Prints basic info about ATT&CK technique `T1486`.
- Lists mapped D3FEND techniques.
- Lists mapped controls and their deployment / test status in `env_id=lab-1`.
- Summarizes coverage (for example, percentage of mapped controls that are deployed and passing tests).

---

## 5. Example ransomware kill chain

The `examples/example_chain.md` file walks through a **small ransomware kill chain**, for example:

1. **Initial access**
2. **Privilege escalation / lateral movement**
3. **Data encryption for impact**

For each step, the example shows:

- ATT&CK technique(s)
- Mapped D3FEND defensive techniques
- Mapped controls
- How you would use the resolver CLI to see coverage for a specific environment

Once the data files and resolver are populated, the example chain becomes a concrete, copyable pattern for your own lab or environment.

---

## 6. Project structure

A typical layout for this repo looks like:
```plain
ransomware-defense-mapping/
├─ data/
│  ├─ attack_techniques.json
│  ├─ d3fend_techniques.json
│  └─ attack_to_d3fend.jsonl
├─ controls/
│  ├─ controls.jsonl
│  └─ env_controls.example.jsonl
├─ src/
│  ├─ **init**.py
│  ├─ model.py
│  ├─ resolver.py
│  └─ cli.py
├─ examples/
│  └─ example_chain.md
├─ README.md
└─ LICENSE
```

- `data/` — ATT&CK / D3FEND subsets and mappings.
- `controls/` — control catalog and example per-environment state.
- `src/` — Python models, resolver logic, and CLI entrypoints.
- `examples/` — worked kill chain example(s).

---

## 7. Limitations and future work

This repository is intentionally small and incomplete.

### 7.1 What this repo is **not**

- Not a comprehensive ATT&CK or D3FEND implementation.
- Not a full ransomware simulation framework.
- Not a drop-in replacement for your internal risk register or GRC tooling.

### 7.2 What you can extend

- **Technique coverage** — add more ATT&CK techniques and D3FEND mappings.
- **Control catalog** — add controls that match your tooling and platforms.
- **Environments** — model multiple environments (`prod`, `staging`, lab tenants) with their own control states.
- **Scoring and reporting** — refine how coverage is computed and how gaps are prioritized.

If you build something interesting on top of this, consider contributing back examples or improvements so others can benefit.
