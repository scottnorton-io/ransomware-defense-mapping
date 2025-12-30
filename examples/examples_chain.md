# Example Ransomware Kill Chain – lab-1

This example shows how to use the resolver to understand ransomware defense coverage for the **lab-1** environment.

We model a simplified three-step ransomware kill chain:

1. **Initial access via valid accounts** – ATT&CK `T1078`
2. **Lateral movement via remote services** – ATT&CK `T1021`
3. **Data encryption and inhibited recovery** – ATT&CK `T1486` and `T1490`

## 1. Techniques in scope

From `data/attack_techniques.json`:

- `T1078` – **Valid Accounts** (Initial Access)
- `T1021` – **Remote Services** (Lateral Movement)
- `T1486` – **Data Encrypted for Impact** (Impact)
- `T1490` – **Inhibit System Recovery** (Impact)

## 2. Defensive techniques (D3FEND subset)

From `data/d3fend_techniques.json` and `data/attack_to_d3fend.jsonl`:

- For `T1078` (Valid Accounts):
  - `D3-AUTH-0001` – Multi-Factor Authentication
  - `D3-LOG-0001` – Centralized Authentication Logging
- For `T1021` (Remote Services):
  - `D3-NET-0001` – Network Segmentation and Isolation
- For `T1486` (Data Encrypted for Impact):
  - `D3-BACKUP-0001` – Immutable and Offline Backups
- For `T1490` (Inhibit System Recovery):
  - `D3-BACKUP-0001` – Immutable and Offline Backups
  - `D3-RECOVERY-0001` – Automated Recovery Procedures

## 3. Controls mapped to D3FEND

From `controls/controls.jsonl`:

- `ctrl.auth.mfa.critical-systems` → MFA for critical systems (D3-AUTH-like)
- `ctrl.logging.central-auth` → Centralized authentication logging (D3-LOG-like)
- `ctrl.network.segmentation-core` → Core network segmentation controls (D3-NET-like)
- `ctrl.backup.immutable` → Immutable backup storage (D3-BACKUP-like)
- `ctrl.recovery.automated` → Automated recovery runbooks (D3-RECOVERY-like)

## 4. lab-1 environment state

From `controls/env_controls.example.jsonl`:

- `ctrl.auth.mfa.critical-systems` – **partial**, last test **pass**
- `ctrl.logging.central-auth` – **full**, last test **pass**
- `ctrl.network.segmentation-core` – **partial**, last test **fail**
- `ctrl.backup.immutable` – **full**, last test **pass**
- `ctrl.recovery.automated` – **not_present**, no tests run

## 5. Example resolver usage

Once `src/model.py`, `src/resolver.py`, and `src/cli.py` are implemented, you should be able to run commands like:
```bash
python -m src.cli map T1486 --env lab-1
```

Conceptual expected output:

- ATT&CK: `T1486` (Data Encrypted for Impact)
- D3FEND techniques:
  - `D3-BACKUP-0001` – Immutable and Offline Backups
- Controls for `lab-1`:
  - `ctrl.backup.immutable` – deployment_state=`full`, last_test_status=`pass`

Coverage sketch:

- 1 mapped control
- 1 deployed and passing
- **Coverage: 100% of mapped controls are deployed and passing tests** (for this technique in this environment)

### 5.1 Chain-level view

You could also imagine a higher-level command (not required for this repo) that walks the full chain:
```bash
python -m src.cli chain --env lab-1 \
  --techniques T1078 T1021 T1486 T1490
```

Conceptually, this would summarize:

- Where controls are missing entirely (for example, `ctrl.recovery.automated`).
- Where tests are failing (for example, `ctrl.network.segmentation-core`).
- Where coverage is strong (for example, `ctrl.backup.immutable`).

Use this example as a starting point for your own chains and environments.
