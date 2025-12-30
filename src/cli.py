"""Simple CLI for ransomware defense mapping.

Usage examples (from the repo root):

    python -m src.cli map T1486 --env lab-1

"""

from __future__ import annotations

import argparse
from pathlib import Path

from .resolver import DataStore, load_datastore, resolve_defenses


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ransomware defense mapping CLI",
    )

    parser.add_argument(
        "--base-dir",
        type=str,
        default=".",
        help="Base directory of the repository (defaults to current directory)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    map_parser = subparsers.add_parser(
        "map",
        help="Show defenses and controls for a single ATT&CK technique in an environment",
    )
    map_parser.add_argument("attack_id", type=str, help="ATT&CK technique ID (e.g., T1486)")
    map_parser.add_argument("--env", dest="env_id", type=str, required=True, help="Environment ID (e.g., lab-1)")

    # gaps command is currently an alias for map with a slightly different heading
    gaps_parser = subparsers.add_parser(
        "gaps",
        help="Highlight gaps for a single ATT&CK technique in an environment",
    )
    gaps_parser.add_argument("attack_id", type=str, help="ATT&CK technique ID (e.g., T1486)")
    gaps_parser.add_argument("--env", dest="env_id", type=str, required=True, help="Environment ID (e.g., lab-1)")

    return parser


def _load_store(base_dir: str) -> DataStore:
    return load_datastore(Path(base_dir))


def cmd_map(store: DataStore, attack_id: str, env_id: str) -> None:
    coverage = resolve_defenses(store, attack_id=attack_id, env_id=env_id)

    print(f"ATT&CK: {coverage.attack.id} - {coverage.attack.name} [{coverage.attack.tactic}]")
    print()

    print("D3FEND techniques:")
    for d in coverage.d3fend_techniques:
        print(f"  - {d.id}: {d.name} ({d.category})")
    print()

    print(f"Controls in environment '{env_id}':")
    for cw in coverage.controls:
        state = cw.state
        if state is None:
            print(f"  - {cw.control.id}: {cw.control.name} [no state for env]")
        else:
            print(
                f"  - {cw.control.id}: {cw.control.name} "
                f"(deployment={state.deployment_state}, last_test_status={state.last_test_status})"
            )

    print()
    if coverage.coverage_score is None:
        print("Coverage score: n/a (no in-scope controls)")
    else:
        pct = round(coverage.coverage_score * 100, 1)
        print(f"Coverage score: {pct}% of in-scope controls are fully deployed and passing tests")


def cmd_gaps(store: DataStore, attack_id: str, env_id: str) -> None:
    coverage = resolve_defenses(store, attack_id=attack_id, env_id=env_id)

    print(f"Gaps for ATT&CK {coverage.attack.id} in env '{env_id}':")

    missing_or_partial = []
    for cw in coverage.controls:
        s = cw.state
        if s is None or s.deployment_state != "full" or s.last_test_status != "pass":
            missing_or_partial.append(cw)

    if not missing_or_partial:
        print("  - No gaps: all in-scope controls are fully deployed and passing tests.")
        return

    for cw in missing_or_partial:
        s = cw.state
        if s is None:
            print(f"  - {cw.control.id}: {cw.control.name} [no state for env]")
        else:
            print(
                f"  - {cw.control.id}: {cw.control.name} "
                f"(deployment={s.deployment_state}, last_test_status={s.last_test_status})"
            )


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    store = _load_store(args.base_dir)

    if args.command == "map":
        cmd_map(store, attack_id=args.attack_id, env_id=args.env_id)
    elif args.command == "gaps":
        cmd_gaps(store, attack_id=args.attack_id, env_id=args.env_id)
    else:
        parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":  # pragma: no cover
    main()
