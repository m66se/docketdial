"""Build the Microsoft 365 import and, optionally, both release downloads."""

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "docketdial"
COPILOT = ROOT / "copilot" / "DocketDial.md"


def copilot_bytes():
    source = (SKILL / "SKILL.md").read_bytes()
    section = (ROOT / "scripts" / "copilot-section.md").read_bytes().strip()
    # The host-specific guidance belongs after the introduction, before the workflow.
    boundary = b"\n## Establish the working set\n"
    if source.count(boundary) != 1:
        raise SystemExit("Expected one 'Establish the working set' heading in SKILL.md.")
    return source.replace(boundary, b"\n" + section + b"\n" + boundary)


def build_downloads(directory, copilot):
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "DocketDial.md").write_bytes(copilot)
    with ZipFile(directory / "docketdial.zip", "w") as archive:
        for path in sorted(SKILL.rglob("*")):
            if path.is_file():
                member = ZipInfo(path.relative_to(SKILL.parent).as_posix())
                member.create_system = 3
                member.external_attr = (0o100755 if path.stat().st_mode & 0o111 else 0o100644) << 16
                archive.writestr(member, path.read_bytes(), compress_type=ZIP_DEFLATED)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the checked-in Copilot import is stale.")
    parser.add_argument("--output", type=Path, help="Write DocketDial.md and docketdial.zip to this directory.")
    args = parser.parse_args()
    generated = copilot_bytes()
    if args.check:
        if not COPILOT.is_file() or COPILOT.read_bytes() != generated:
            raise SystemExit("Copilot import is stale. Run python3 scripts/build.py and commit the result.")
    else:
        COPILOT.write_bytes(generated)
    if args.output is not None:
        build_downloads(args.output, generated)


if __name__ == "__main__":
    main()
