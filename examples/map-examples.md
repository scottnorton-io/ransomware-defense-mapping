`map` command example 1

```bash
(.venv) scott@scotts-MacBook-Pro ransomware-defense-mapping % python3 -m src.cli map T1486 --env lab-1
ATT&CK: T1486 - Data Encrypted for Impact [Impact]

D3FEND techniques:
  - D3-BACKUP-0001: Immutable and Offline Backups (Resilience)

Controls in environment 'lab-1':
  - ctrl.auth.mfa.critical-systems: MFA for critical systems (deployment=partial, last_test_status=pass)
  - ctrl.logging.central-auth: Centralized authentication logging (deployment=full, last_test_status=pass)
  - ctrl.network.segmentation-core: Core network segmentation controls (deployment=partial, last_test_status=fail)
  - ctrl.backup.immutable: Immutable backup storage (deployment=full, last_test_status=pass)
  - ctrl.recovery.automated: Automated recovery runbooks (deployment=not_present, last_test_status=unknown)

Coverage score: 40.0% of in-scope controls are fully deployed and passing tests
(.venv) scott@scotts-MacBook-Pro ransomware-defense-mapping %
```

