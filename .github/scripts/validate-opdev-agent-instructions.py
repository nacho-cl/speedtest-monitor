import argparse
import os
import re
import sys
from hashlib import sha256
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
parser.add_argument("expected_hash", nargs="?")
args = parser.parse_args()

expected = os.environ.get("OPDEV_AGENT_RULES_SHA256")
if args.expected_hash:
    expected = args.expected_hash
if not expected:
    sys.stderr.write("OPDEV_AGENT_RULES_SHA256 is not set\n")
    sys.exit(2)

root = args.root.resolve()
agents_path = root / "AGENTS.md"
if not agents_path.is_file():
    sys.stderr.write("AGENTS.md is missing\n")
    sys.exit(1)

agents = agents_path.read_text(encoding="utf-8")
pattern = re.compile(
    r"<!-- OPDEV-COMMON-AGENT-RULES -->\s*(.*?)\s*"
    r"<!-- /OPDEV-COMMON-AGENT-RULES -->",
    re.DOTALL,
)
blocks = pattern.findall(agents)
if len(blocks) != 1:
    sys.stderr.write(
        f"Expected one managed rules block in AGENTS.md; found {len(blocks)}\n"
    )
    sys.exit(1)

actual = sha256(blocks[0].strip().encode("utf-8")).hexdigest()
if actual != expected:
    sys.stderr.write(
        f"OPDev agent rules are outdated or modified: expected {expected}, "
        f"found {actual}\n"
    )
    sys.exit(1)

for filename in ("CLAUDE.md", ".github/copilot-instructions.md"):
    path = root / filename
    if not path.is_file() or "AGENTS.md" not in path.read_text(encoding="utf-8"):
        sys.stderr.write(f"{filename} must reference the repository's AGENTS.md\n")
        sys.exit(1)

sys.stdout.write(f"OPDev agent instructions are consistent ({actual})\n")
