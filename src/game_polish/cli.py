"""Small, dependency-free project configuration and evidence CLI."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import hashlib
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
import uuid

from .reporting import render_report, write_reports

CONFIG = "game-polish.json"


def default_config(name: str) -> dict:
    return {
        "schema_version": 1,
        "project": {"name": name, "engine": "godot", "root": "."},
        "cycle": {"interval_minutes": None, "max_tokens": None},
        "goals": ["Improve player feedback without changing core mechanics"],
        "constraints": ["Preserve input bindings and save compatibility"],
        "checks": {
            "scripts": {"argv": ["gdx", "--project", "{project_root}", "script", "check-all"], "timeout_seconds": 120, "expect_json_ok": True},
        },
        "review": {"required_evidence": ["before screenshot", "after screenshot", "interaction recording"],
                   "acceptance": ["No new errors in configured checks", "Human review of feel, readability, and accessibility"]},
    }


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def strings(value, field: str, nonempty: bool = False) -> None:
    require(isinstance(value, list) and all(isinstance(x, str) and x.strip() for x in value), f"{field} must be an array of nonempty strings")
    require(not nonempty or bool(value), f"{field} must not be empty")


def load_config(path: Path) -> tuple[dict, Path]:
    data = json.loads(path.read_text())
    require(isinstance(data, dict), "configuration must be an object")
    require(type(data.get("schema_version")) is int and data["schema_version"] == 1, "schema_version must be 1")
    project = data.get("project")
    require(isinstance(project, dict), "project must be an object")
    for key in ("name", "engine", "root"):
        require(isinstance(project.get(key), str) and bool(project[key].strip()), f"project.{key} must be a nonempty string")
    root = (path.parent / project["root"]).resolve()
    require(root.is_dir(), f"project root is not a directory: {root}")
    for key in ("goals", "constraints"):
        strings(data.get(key), key)
    cycle = data.get("cycle", {})
    require(isinstance(cycle, dict), "cycle must be an object")
    for key in ("interval_minutes", "max_tokens"):
        value = cycle.get(key)
        require(value is None or (type(value) is int and value > 0), f"cycle.{key} must be null or a positive integer")
    checks = data.get("checks")
    require(isinstance(checks, dict) and bool(checks), "checks must be a nonempty object")
    for name, check in checks.items():
        require(bool(re.fullmatch(r"[a-zA-Z0-9_-]+", name)), f"invalid check name: {name}")
        require(isinstance(check, dict), f"checks.{name} must be an object")
        strings(check.get("argv"), f"checks.{name}.argv", True)
        require(type(check.get("expect_json_ok", False)) is bool, f"checks.{name}.expect_json_ok must be boolean")
        timeout = check.get("timeout_seconds", 60)
        require(type(timeout) is int and 1 <= timeout <= 3600, f"checks.{name}.timeout_seconds must be an integer from 1 to 3600")
    review = data.get("review")
    require(isinstance(review, dict), "review must be an object")
    for key in ("required_evidence", "acceptance"):
        strings(review.get(key), f"review.{key}", True)
    return data, root


def cycle_warnings(config: dict) -> list[str]:
    cycle = config.get("cycle", {})
    messages = []
    if cycle.get("interval_minutes") is not None:
        messages.append("Requested cycle interval is metadata only; no schedule has been created. Configure and verify scheduling in the existing host.")
    if cycle.get("max_tokens") is not None:
        messages.append("Hard token limit is UNSUPPORTED by this CLI; tokens_used remains null. The host must measure and enforce it before a budget-constrained model cycle begins.")
    return messages


def print_cycle_warnings(config: dict) -> None:
    for message in cycle_warnings(config):
        print(f"game-polish warning: {message}", file=sys.stderr)


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n")


def execute(check: dict, root: Path, log: Path) -> dict:
    started = time.monotonic()
    result = {"argv": check["argv"], "status": "error", "exit_code": None, "log": log.name}
    # No shell interpolation. Commands remain executable code and must be reviewed.
    error_log = log.with_suffix(".stderr.log")
    result["stderr_log"] = error_log.name
    with log.open("wb") as output, error_log.open("wb") as errors:
        try:
            proc = subprocess.Popen(check["argv"], cwd=root, stdout=output, stderr=errors,
                                    stdin=subprocess.DEVNULL, start_new_session=os.name == "posix")
            try:
                code = proc.wait(timeout=check.get("timeout_seconds", 60))
                result.update(status="passed" if code == 0 else "failed", exit_code=code)
            except (subprocess.TimeoutExpired, KeyboardInterrupt) as exc:
                try:
                    if os.name == "posix":
                        os.killpg(proc.pid, signal.SIGKILL)
                    else:
                        proc.kill()
                except ProcessLookupError:
                    pass
                proc.wait()
                result["status"] = "interrupted" if isinstance(exc, KeyboardInterrupt) else "timed_out"
        except OSError as exc:
            output.write(str(exc).encode())
            result["error"] = str(exc)
    if result["status"] == "passed" and check.get("expect_json_ok", False):
        try:
            require(log.stat().st_size <= 10_000_000, "JSON result exceeds 10 MB")
            payload = json.loads(log.read_text())
            require(isinstance(payload, dict) and payload.get("ok") is True, "JSON result must contain ok: true")
            result["json_ok"] = True
        except (OSError, UnicodeError, ValueError) as exc:
            result.update(status="failed", json_ok=False, error=str(exc))
    result["duration_seconds"] = round(time.monotonic() - started, 3)
    return result


def source_snapshot(root: Path, destination: Path, prefix: str = "source") -> dict:
    """Best-effort Git identity; never call an untracked tree reproducible."""
    try:
        def git(*args):
            return subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=10, check=True).stdout
        head = git("rev-parse", "HEAD").decode().strip()
        status = git("status", "--porcelain", "--untracked-files=all", "--", ".", ":!.game-polish").decode()
        diff = git("diff", "--no-ext-diff", "--no-textconv", "HEAD", "--binary", "--", ".", ":!.game-polish")
        (destination / f"{prefix}.diff").write_bytes(diff)
        (destination / f"{prefix}.status.txt").write_text(status)
        return {"kind": "git", "head": head, "dirty": bool(status),
                "diff_sha256": hashlib.sha256(diff).hexdigest(),
                "limitations": "Untracked file contents are not captured. Review source.status.txt; evidence is not tamper-proof."}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"kind": "unavailable", "reason": str(exc), "limitations": "Source revision not verified."}


def create_run(config_path: Path, phase: str, execute_commands: bool, selected: list[str] | None, baseline: str | None) -> tuple[Path, dict]:
    config, root = load_config(config_path)
    print_cycle_warnings(config)
    names = selected or list(config["checks"])
    require(all(name in config["checks"] for name in names), "unknown check requested")
    comparison = {"status": "not_provided"}
    if baseline:
        base = Path(baseline).resolve()
        base_data = json.loads((base / "manifest.json").read_text())
        require(base_data.get("phase") == "baseline", "--baseline must point to a baseline run directory")
        require(base_data.get("status") == "passed", "baseline checks must have been executed and passed")
        require(base_data.get("project_root") == str(root), "baseline belongs to a different project root")
        old_config = json.loads((base / "config.snapshot.json").read_text())
        matches = set(base_data["checks"]) == set(names) and all(old_config["checks"].get(name) == config["checks"][name] for name in names)
        comparison = {"status": "matching_checks" if matches else "different_checks", "note": "Matching commands alone do not establish equivalent play conditions."}
        baseline = str(base)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    evidence_root = root / ".game-polish" / "runs"
    require(evidence_root.resolve().is_relative_to(root), "evidence directory must remain inside project root")
    destination = evidence_root / run_id
    destination.mkdir(parents=True, exist_ok=False)
    (destination / "evidence").mkdir()
    write_json(destination / "config.snapshot.json", config)
    checks = {name: {"argv": config["checks"][name]["argv"], "status": "not_run"} for name in names}
    manifest = {"schema_version": 1, "id": run_id, "phase": phase, "project": config["project"]["name"],
                "project_root": str(root), "created_at": datetime.now(timezone.utc).isoformat(),
                "cycle": config.get("cycle", {}), "scheduling": {"status": "not_scheduled_by_cli", "owner": "existing_host"}, "budget": {"tokens_used": None, "enforcement": "unsupported_by_cli", "note": "The existing host must measure and enforce token limits; CLI does not call models or schedule work."},
                "regression": {"status": "not_evaluated", "scope": "Configured command results only (exit codes and JSON ok when requested); visual and gameplay review remain pending."},
                "goals": config["goals"], "constraints": config["constraints"],
                "status": "planned", "baseline": baseline, "comparison": comparison, "source": source_snapshot(root, destination), "review": config["review"], "checks": checks}
    write_json(destination / "manifest.json", manifest)
    write_json(destination / "observations.json", {"review_status": "pending", "hypothesis": "", "changes": [],
                "evidence": [], "observations": [], "regressions": [], "limitations": [], "rollback": [], "decision": "pending"})
    if execute_commands:
        manifest["status"] = "running"
        write_json(destination / "manifest.json", manifest)
        for name in names:
            check = dict(config["checks"][name])
            check["argv"] = [arg.replace("{evidence_dir}", str(destination / "evidence")).replace("{project_root}", str(root)) for arg in check["argv"]]
            checks[name] = execute(check, root, destination / f"{name}.log")
            write_json(destination / "manifest.json", manifest)
            if checks[name]["status"] == "interrupted":
                break
        manifest["status"] = "passed" if all(c["status"] == "passed" for c in checks.values()) else "failed"
    if execute_commands:
        manifest["source_after"] = source_snapshot(root, destination, "source-after")
    if execute_commands and baseline and comparison["status"] == "matching_checks":
        manifest["regression"]["status"] = "no_check_regression" if manifest["status"] == "passed" else "check_regression"
    write_json(destination / "manifest.json", manifest)
    write_reports(destination, manifest)
    return destination, manifest


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="write a starter config, never overwrite")
    init.add_argument("path", nargs="?", default=".", help="existing game project directory")
    init.add_argument("--name")
    validate = sub.add_parser("validate", help="validate config and project root without running commands")
    validate.add_argument("--config", default=CONFIG)
    for verb in ("baseline", "run"):
        cmd = sub.add_parser(verb, help="prepare evidence; execute only with --execute")
        cmd.add_argument("--config", default=CONFIG)
        cmd.add_argument("--execute", action="store_true", help="execute reviewed project commands (not sandboxed)")
        cmd.add_argument("--check", action="append", help="select check; repeat to select several")
        if verb == "run":
            cmd.add_argument("--baseline", help="path to an executed baseline run directory")
    report = sub.add_parser("report", help="regenerate report from recorded check results")
    report.add_argument("run_dir")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            root = Path(args.path).resolve()
            require(root.is_dir(), "project directory must already exist")
            path = root / CONFIG
            with path.open("x") as file:
                json.dump(default_config(args.name or root.name), file, indent=2)
                file.write("\n")
            print(path)
        elif args.command == "validate":
            config, root = load_config(Path(args.config).resolve())
            print_cycle_warnings(config)
            print(f"Valid: {config['project']['name']} ({root}); commands not executed")
        elif args.command in ("baseline", "run"):
            destination, manifest = create_run(Path(args.config).resolve(), args.command, args.execute, args.check, getattr(args, "baseline", None))
            print(f"{manifest['status']}: {destination}")
            if manifest["status"] == "failed":
                return 1
        else:
            directory = Path(args.run_dir).resolve()
            manifest = json.loads((directory / "manifest.json").read_text())
            write_reports(directory, manifest)
            print(directory / "report.html")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"game-polish: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
