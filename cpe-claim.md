Title: Ransomware Defense Mapping with ATT&CK, D3FEND, and Platform0-style Testing

Certification body: <ISACA / ISC² / Other>
CPE category: Technical Information Security / Threat and Vulnerability Management
Activity type: Authoring technical publication + open-source reference implementation

Date range: 2025-12-XX to 2025-12-XX
Total CPE hours claimed: 8.0
  - Research and design: 2.5 hours
  - Implementation (data model, resolver, CLI, examples): 3.0 hours
  - Writing and publishing article + documentation: 2.5 hours

Learning objectives:
  1. Map ransomware-relevant MITRE ATT&CK techniques to MITRE D3FEND defensive patterns.
  2. Design a small, inspectable data model that connects attack behaviors to testable security controls.
  3. Implement a reference resolver and CLI to compute per-environment coverage for ransomware techniques.
  4. Communicate the pattern through a technical article and example repository suitable for practitioner use.

Description of activity:
  Authored a technical reference implementation and article demonstrating how to connect MITRE ATT&CK
  ransomware techniques to MITRE D3FEND defensive techniques and concrete security controls that can be
  tested using a Platform0-style pattern (stateless jobs + durable evidence). Implemented a small data
  model (ATT&CK subset, D3FEND subset, mappings, controls, environment state), a Python resolver and CLI
  (`map` and `gaps` commands), and example ransomware kill-chain documentation for a lab environment.
  Wrote an article describing the approach, data model, implementation details, and practitioner
  next steps.

Artifacts / evidence:
  - Public GitHub repository: https://github.com/scottnorton-io/ransomware-defense-mapping
  - Article / whitepaper: <ARTICLE_URL>
  - Example CLI output and diagrams: see repository README and `examples/example_chain.md`.

Relevance to certification domain:
  - Demonstrates practical application of threat modeling using MITRE ATT&CK and D3FEND.
  - Shows how to move from descriptive diagrams to evidence-backed control verification for ransomware.
  - Provides reusable patterns for security engineering, risk assessment, and audit preparation.

Attestation:
  I certify that the hours claimed above are accurate and reflect my own participation in this activity.

  Name: Scott Norton
  Date: ______________________
  Signature (if required): ______________________
