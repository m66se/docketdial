"""Build the static DocketDial site and a ZIP suitable for a static web host.

Run from anywhere with: python3 website/build.py OUTPUT_DIRECTORY HOSTING_ZIP
"""
import argparse
import shutil
import zipfile
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = "https://github.com/m66se/docketdial"
PLATFORMS = {
    "copilot": {
        "name": "Microsoft 365 Copilot Cowork",
        "file": "DocketDial.md", "label": "Download Markdown", "format": ".md · Single skill file",
        "manual": "Open Customize → Skills in Cowork. Choose Add → Upload skill and select DocketDial.md. Start a new task and ask DocketDial to draft your dockets.",
        "prompt": f"Help me install DocketDial in Microsoft 365 Copilot Cowork. From {REPO}, fetch copilot/DocketDial.md and check its skill name is docketdial. Import it as a personal skill if you have access. If I need to finish the upload, give me the file and the exact clicks. Verify it is available in a new task before saying it is installed."
    },
    "claude": {
        "name": "Claude Cowork",
        "file": "docketdial.zip", "label": "Download skill ZIP", "format": ".zip · Ready for Claude",
        "manual": "In Claude, open Customize → Skills and upload the ZIP as downloaded. Enable DocketDial, then type /docketdial in Cowork.",
        "prompt": f"Help me install DocketDial in Claude Cowork from {REPO}. Package skills/docketdial as a ZIP containing docketdial/SKILL.md and its companion files. Upload and enable it in Customize → Skills if you have access. Otherwise give me the ready-to-upload ZIP and the remaining clicks. Verify /docketdial is available."
    },
    "codex": {
        "name": "Codex",
        "file": "docketdial.zip", "label": "Download skill ZIP", "format": ".zip · Complete skill folder",
        "manual": "Unzip the download and place the docketdial folder in ~/.agents/skills/. Start your next prompt with $docketdial.",
        "prompt": f"Use $skill-installer to install skills/docketdial from {REPO} as my personal Codex skill. If it is already installed, check the existing copy before replacing it. Verify that $docketdial is available, then give me a first prompt for drafting yesterday’s dockets."
    }
}


def write_archive(destination, members):
    with zipfile.ZipFile(destination, "w") as archive:
        for name, path in sorted(members):
            entry = zipfile.ZipInfo(name)
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, path.read_bytes())


def panel(key, platform):
    p = {field: escape(value, quote=True) for field, value in platform.items()}
    return f'''<section class="install-panel" id="{key}" aria-labelledby="{key}-title">
      <div class="install-copy"><h3 id="{key}-title">{p["name"]}</h3><p>{p["manual"]}</p>
        <a class="button" download="{p["file"]}" href="downloads/{p["file"]}">{p["label"]} <span aria-hidden="true">↓</span></a>
        <div class="filetype">{p["format"]}</div>
      </div>
      <div class="agent-box"><div class="copy-line"><strong>Ask your agent to install it</strong><button type="button" class="copy-btn" hidden>Copy instructions</button></div>
        <p class="prompt">{p["prompt"]}</p><p class="status" role="status"></p>
      </div></section>'''


def build(output, archive_path):
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise SystemExit("Choose an empty output directory so the package contains only site files.")
    for name in ("assets", "fonts"):
        shutil.copytree(HERE / name, output / name)
    for name in ("style.css", "app.js"):
        shutil.copyfile(HERE / name, output / name)
    template = (HERE / "index.html").read_text()
    (output / "index.html").write_text(template.replace("<!-- INSTALL_PANELS -->", "\n".join(panel(k, p) for k, p in PLATFORMS.items())))
    downloads = output / "downloads"
    downloads.mkdir()
    shutil.copyfile(ROOT / "copilot" / "DocketDial.md", downloads / "DocketDial.md")
    skill = ROOT / "skills" / "docketdial"
    write_archive(downloads / "docketdial.zip", [
        ("docketdial/" + p.relative_to(skill).as_posix(), p) for p in skill.rglob("*")
        if p.is_file() and not any(part.startswith(".") for part in p.relative_to(skill).parts)
    ])
    instructions = ["# Install DocketDial", "", f"Official source: {REPO}", "",
                    "Use the section for the visitor’s chosen host. Installation does not require access to client records. If a file upload requires a person, provide the prepared file and identify that step.", ""]
    for p in PLATFORMS.values():
        instructions.extend([f"## {p['name']}", "", p['prompt'], "", p['manual'], ""])
    (output / "install.md").write_text("\n".join(instructions))
    write_archive(archive_path, [(p.relative_to(output).as_posix(), p) for p in output.rglob("*") if p.is_file()])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    build(args.output.resolve(), args.archive.resolve())
