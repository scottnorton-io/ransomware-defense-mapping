`gaps` command example

```bash
(.venv) scott@scotts-MacBook-Pro ransomware-defense-mapping % python3 -m src.cli gaps T1486 --env lab-1
Gaps for ATT&CK T1486 in env 'lab-1':
  - ctrl.auth.mfa.critical-systems: MFA for critical systems (deployment=partial, last_test_status=pass)
  - ctrl.network.segmentation-core: Core network segmentation controls (deployment=partial, last_test_status=fail)
  - ctrl.recovery.automated: Automated recovery runbooks (deployment=not_present, last_test_status=unknown)
(.venv) scott@scotts-MacBook-Pro ransomware-defense-mapping %
```
