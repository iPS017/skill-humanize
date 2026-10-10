#!/usr/bin/env python3
# humanize:ignore-file
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "humanize-ui" / "scripts"))

import scan
import scan_ui

MAX_LINES = 20


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    file_path = (payload.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0
    path = Path(file_path)
    if not path.is_file() or path.stat().st_size > scan.MAX_SIZE:
        return 0
    if any(part in scan.SKIP_DIRS for part in path.parts):
        return 0
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return 0
    if scan.IGNORE_MARKER in "\n".join(text.split("\n", 20)[:20]):
        return 0

    ext = path.suffix.lower()
    kind = scan.kind_for(path, None)
    findings = []
    if kind == "code":
        findings += [f for f in scan.scan_text(text, kind, ext, None) if f.level != "info"]
    elif kind == "prose":
        findings += [f for f in scan.scan_text(text, kind, ext, None) if f.level == "error"]
    if ext in scan_ui.UI_EXT:
        findings += [f for f in scan_ui.scan_file(text, ext) if f.level != "info"]
    name_issue = scan.check_filename(path)
    if name_issue:
        findings.append(scan.Finding(0, 0, "warn", name_issue, path.name))
    if not findings:
        return 0

    findings = list({(f.line, f.col): f for f in sorted(findings, key=lambda f: (f.line, f.col))}.values())
    out = [f"humanize : {len(findings)} marqueur(s) d'écriture IA dans {path.name}. Corrige le fichier maintenant :"]
    for f in findings[:MAX_LINES]:
        tail = f"  {f.excerpt}" if f.excerpt else ""
        out.append(f"  {f.line}:{f.col} {f.message}{tail}")
    if len(findings) > MAX_LINES:
        out.append(f"  ... et {len(findings) - MAX_LINES} autre(s)")
    out.append(
        "Supprime les commentaires (seules les licences et directives d'outils restent), donne aux classes et aux "
        "variables un nom qui dit leur rôle, utilise les balises sémantiques au lieu des div. Un effet visuel signalé "
        "reste seulement s'il vient de la charte du projet ou d'une demande explicite."
    )
    print("\n".join(out), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
