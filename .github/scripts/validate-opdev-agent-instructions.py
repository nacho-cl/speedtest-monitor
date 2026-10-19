import os
import re
import sys
from hashlib import sha256
from pathlib import Path

expected = os.environ.get("OPDEV_AGENT_RULES_SHA256")
if len(sys.argv) > 2:
    expected = sys.argv[2]
if not expected:
    print("OPDEV_AGENT_RULES_SHA256 is not set", file=sys.stderr)
    sys.exit(2)

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
agents_path = root / "AGENTS.md"
if not agents_path.is_file():
    print("AGENTS.md is missing", file=sys.stderr)
    sys.exit(1)

agents = agents_path.read_text(encoding="utf-8")
pattern = re.compile(
    r"<!-- OPDEV-COMMON-AGENT-RULES -->\s*(.*?)\s*"
    r"<!-- /OPDEV-COMMON-AGENT-RULES -->",
    re.DOTALL,
)
blocks = pattern.findall(agents)
if len(blocks) != 1:
    print(
        f"Expected one managed rules block in AGENTS.md; found {len(blocks)}",
        file=sys.stderr,
    )
    sys.exit(1)

actual = sha256(blocks[0].strip().encode("utf-8")).hexdigest()
if actual != expected:
    print(
        f"OPDev agent rules are outdated or modified: expected {expected}, found {actual}",
        file=sys.stderr,
    )
    sys.exit(1)

for filename in ("CLAUDE.md", ".github/copilot-instructions.md"):
    path = root / filename
    if not path.is_file() or "AGENTS.md" not in path.read_text(encoding="utf-8"):
        print(f"{filename} must reference the repository's AGENTS.md", file=sys.stderr)
        sys.exit(1)

print(f"OPDev agent instructions are consistent ({actual})")
