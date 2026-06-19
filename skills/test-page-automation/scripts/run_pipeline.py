#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import subprocess


KNOWN_SLUGS = [
    "hard-or-change",
    "be-controlled",
    "sensitive-type",
    "hot-or-steady-love",
    "money-talent",
    "life-script",
    "wrong-person",
    "strong-or-growth-love",
    "like-signals",
    "love-clarity",
]


def run(cmd, cwd):
    print("$ " + " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, text=True, check=False)


def prepare(project):
    if (project / "generate_10_hot_tests.py").exists():
        result = run(["python3", "generate_10_hot_tests.py"], project)
        if result.returncode:
            raise SystemExit(result.returncode)
    result = run(["python3", "publish_to_github_pages.py"], project)
    if result.returncode:
        raise SystemExit(result.returncode)
    site = project / "site"
    if site.exists():
        run(["cp", "-R", "site/.", "."], project)
    validate(project)


def validate(project):
    base = project / "tests"
    missing = []
    for slug in KNOWN_SLUGS:
        config_path = base / slug / "test_config.json"
        html_path = base / slug / "index.html"
        if not config_path.exists() or not html_path.exists():
            missing.append(slug)
            continue
        data = json.loads(config_path.read_text(encoding="utf-8"))
        questions = data.get("questions", [])
        option_sets = [tuple(o.get("text", "") for o in q.get("options", [])) for q in questions]
        repeated_first = len(option_sets) > 1 and option_sets[0] == option_sets[1]
        print(f"{slug}: {len(questions)} questions, first two option sets same={repeated_first}")
    if missing:
        raise SystemExit("Missing tests: " + ", ".join(missing))


def diagnose(project):
    run(["git", "status", "-sb"], project)
    run(["git", "remote", "-v"], project)
    print("\nChecking GitHub credential record for shufan-art...")
    p = subprocess.run(
        ["git", "credential-osxkeychain", "get"],
        cwd=project,
        input="protocol=https\nhost=github.com\nusername=shufan-art\n\n",
        text=True,
        capture_output=True,
        check=False,
    )
    visible = "\n".join(line for line in p.stdout.splitlines() if not line.startswith("password="))
    print(visible or "No visible credential record found.")


def links(base_url):
    base_url = base_url.rstrip("/")
    for slug in KNOWN_SLUGS:
        print(f"{base_url}/tests/{slug}/index.html")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--mode", choices=["prepare", "diagnose", "links"], default="prepare")
    parser.add_argument("--base-url", default="https://shufan-art.github.io/shufan/")
    args = parser.parse_args()
    project = Path(args.project).expanduser().resolve()

    if args.mode == "prepare":
        prepare(project)
    elif args.mode == "diagnose":
        diagnose(project)
    else:
        links(args.base_url)


if __name__ == "__main__":
    main()
