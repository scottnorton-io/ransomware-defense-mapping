"""Core data models for ransomware defense mapping.

These models mirror the JSON / JSONL structures in the data/ and controls/
folders and provide typed structures for the resolver to work with.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class AttackTechnique:
    id: str
    name: str
    tactic: str
    description: str
    ransomware_relevance: bool


@dataclass
class D3fendTechnique:
    id: str
    name: str
    category: str
    description: str


@dataclass
class AttackToD3fendMapping:
    attack_id: str
    d3fend_id: str
    justification: str


@dataclass
class Control:
    id: str
    name: str
    category: str
    scenario_id: str
    evidence_schema_ref: str


@dataclass
class EnvControlState:
    env_id: str
    control_id: str
    deployment_state: str  # e.g., "not_present", "partial", "full"
    last_test_time: Optional[datetime]
    last_test_status: str  # e.g., "pass", "fail", "unknown"


@dataclass
class ControlWithState:
    control: Control
    state: Optional[EnvControlState]


@dataclass
class TechniqueCoverage:
    attack: AttackTechnique
    d3fend_techniques: List[D3fendTechnique]
    controls: List[ControlWithState]
    coverage_score: Optional[float] = None  # 0.0–1.0 or None if not computed
