"""Resolver functions for ransomware defense mapping.

This module loads data from JSON / JSONL files and computes technique-level
coverage for a given environment.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import json

from .model import (
    AttackTechnique,
    AttackToD3fendMapping,
    Control,
    ControlWithState,
    D3fendTechnique,
    EnvControlState,
    TechniqueCoverage,
)


@dataclass
class DataStore:
    attacks: Dict[str, AttackTechnique]
    d3fend: Dict[str, D3fendTechnique]
    attack_to_d3fend: List[AttackToD3fendMapping]
    controls: Dict[str, Control]
    env_states: List[EnvControlState]


def _load_json_array(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _load_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def load_datastore(base_dir: Path) -> DataStore:
    """Load all reference data from the given base directory.

    Expected structure:
      base_dir/data/attack_techniques.json
      base_dir/data/d3fend_techniques.json
      base_dir/data/attack_to_d3fend.jsonl
      base_dir/controls/controls.jsonl
      base_dir/controls/env_controls.example.jsonl
    """

    attacks_raw = _load_json_array(base_dir / "data" / "attack_techniques.json")
    d3fend_raw = _load_json_array(base_dir / "data" / "d3fend_techniques.json")
    mappings_raw = _load_jsonl(base_dir / "data" / "attack_to_d3fend.jsonl")
    controls_raw = _load_jsonl(base_dir / "controls" / "controls.jsonl")
    env_states_raw = _load_jsonl(base_dir / "controls" / "env_controls.example.jsonl")

    attacks = {
        row["id"]: AttackTechnique(**row)
        for row in attacks_raw
    }

    d3fend = {
        row["id"]: D3fendTechnique(**row)
        for row in d3fend_raw
    }

    attack_to_d3fend = [AttackToD3fendMapping(**row) for row in mappings_raw]

    controls = {
        row["id"]: Control(**row)
        for row in controls_raw
    }

    env_states = [EnvControlState(**row) for row in env_states_raw]

    return DataStore(
        attacks=attacks,
        d3fend=d3fend,
        attack_to_d3fend=attack_to_d3fend,
        controls=controls,
        env_states=env_states,
    )


def resolve_defenses(
    store: DataStore,
    attack_id: str,
    env_id: str,
) -> TechniqueCoverage:
    """Resolve D3FEND techniques and controls for an ATT&CK technique in an env.

    This function intentionally keeps scoring simple. You can refine the
    coverage_score logic as needed.
    """

    attack = store.attacks.get(attack_id)
    if not attack:
        raise ValueError(f"Unknown attack_id: {attack_id}")

    # Find mappings for this technique
    mappings = [m for m in store.attack_to_d3fend if m.attack_id == attack_id]
    d3fend_ids = {m.d3fend_id for m in mappings}

    d3fend_techniques = [store.d3fend[d_id] for d_id in d3fend_ids if d_id in store.d3fend]

    # For this minimal reference, we map controls to D3FEND techniques conceptually
    # via naming / documentation rather than a strict relation table. A more
    # complete implementation could add an explicit control_to_d3fend mapping.

    control_list: List[ControlWithState] = []
    env_states_by_control = {
        s.control_id: s for s in store.env_states if s.env_id == env_id
    }

    for control in store.controls.values():
        state = env_states_by_control.get(control.id)
        control_list.append(ControlWithState(control=control, state=state))

    coverage_score = _compute_coverage_score(control_list)

    return TechniqueCoverage(
        attack=attack,
        d3fend_techniques=d3fend_techniques,
        controls=control_list,
        coverage_score=coverage_score,
    )


def _compute_coverage_score(controls: List[ControlWithState]) -> Optional[float]:
    """Very simple coverage score based on deployment and test status.

    - Only controls with a non-null state are considered "in scope".
    - Score is the fraction of in-scope controls that are fully deployed and
      have a last_test_status of "pass".
    """

    in_scope = [c for c in controls if c.state is not None]
    if not in_scope:
        return None

    good = [
        c
        for c in in_scope
        if c.state.deployment_state == "full" and c.state.last_test_status == "pass"
    ]

    return len(good) / len(in_scope)
