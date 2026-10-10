#!/usr/bin/env python3
# humanize:ignore-file
import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

STYLE_EXT = {".css", ".scss", ".sass", ".less"}
MARKUP_EXT = {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro"}
SCRIPT_EXT = {".js", ".ts", ".mjs", ".cjs"}
UI_EXT = STYLE_EXT | MARKUP_EXT | SCRIPT_EXT

SKIP_DIRS = {
    "node_modules", ".git", ".next", ".nuxt", ".svelte-kit", "dist", "build", "out",
    ".turbo", ".vercel", ".cache", "coverage", "__pycache__", ".venv", "venv", "vendor",
}
IGNORE_MARKER = "humanize:ignore-file"
MAX_SIZE = 2_000_000
LABELS = {"error": "erreur", "warn": "attention", "info": "info"}

HEX = re.compile(r"#([0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")
RGB = re.compile(r"rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)")
HSL = re.compile(r"hsla?\(\s*[\d.]+(?:deg)?[\s,]+([\d.]+)%")
TW_COLOR = re.compile(
    r"\b(?:red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d{2,3}\b"
)
NAMED_VIVID = re.compile(
    r"\b(?:magenta|fuchsia|cyan|aqua|lime|violet|purple|hotpink|deeppink|blueviolet|indigo)\b", re.I
)
GLOW_VAR = re.compile(r"var\(--[\w-]*(?:neon|glow|accent|primary|brand|purple|violet)", re.I)

GLOW_PROP = re.compile(r"\b(box-shadow|text-shadow)\s*:\s*([^;}{]+)", re.I)
DROP_SHADOW = re.compile(r"drop-shadow\(\s*0(?:px)?\s+0(?:px)?\s+(\d+)px([^)]*\)?)", re.I)
ZERO_OFFSET_BLUR = re.compile(r"(?:^|,)\s*(?:inset\s+)?0(?:px)?\s+0(?:px)?\s+(\d+)px")
TW_GLOW = re.compile(
    r"\b(?:shadow-\[0_0_[^\]]+\]|(?:shadow|drop-shadow)-(?:red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d{2,3}(?:/\d+)?)"
)

GRADIENT_BG = re.compile(r"\bbackground(?:-image)?\s*:\s*([^;}{]*(?:linear|radial|conic)-gradient[^;}{]*)", re.I)
TW_GRADIENT = re.compile(r"\bbg-(?:gradient|linear|radial|conic)-[\w\[\]-]+")
TW_STOP = re.compile(r"\b(?:from|via|to)-(?:indigo|violet|purple|fuchsia|pink|rose|blue|cyan|sky|teal|emerald)-\d{2,3}")
GRADIENT_TEXT = re.compile(r"(?:-webkit-)?background-clip\s*:\s*text|\bbg-clip-text\b", re.I)

BACKDROP = re.compile(r"backdrop-filter\s*:\s*[^;]*blur|\bbackdrop-blur(?:-\w+)?\b", re.I)
BIG_BLUR = re.compile(r"(?<!drop-)(?<!backdrop-)\bfilter\s*:\s*[^;]*blur\(\s*(\d+)px", re.I)
TW_BIG_BLUR = re.compile(r"(?<![\w-])blur-(?:2xl|3xl|\[\d{2,}px\])")

AI_PURPLE = re.compile(
    r"#(?:8b5cf6|7c3aed|6d28d9|a855f7|9333ea|c084fc|6366f1|4f46e5|818cf8|ec4899|db2777|d946ef|c026d3|06b6d4)\b"
    r"|\b(?:purple|violet|indigo|fuchsia)-(?:300|400|500|600|700)\b",
    re.I,
)

INFINITE = re.compile(r"\banimation(?:-iteration-count)?\s*:\s*([^;}{]*\binfinite\b[^;}{]*)", re.I)
TW_LOOP = re.compile(r"\banimate-(?:pulse|bounce|ping)\b")
REDUCED_MOTION = re.compile(r"prefers-reduced-motion|motion-safe:|motion-reduce:|useReducedMotion")
ANY_MOTION = re.compile(r"@keyframes|\banimation\s*:|\btransition\s*:|\banimate-|\btransition-|framer-motion|gsap", re.I)

OUTLINE_NONE = re.compile(r"\boutline\s*:\s*(?:none|0)\b", re.I)
TW_OUTLINE_NONE = re.compile(r"\b(?:focus:)?outline-none\b")
FOCUS_VISIBLE = re.compile(r":focus-visible|focus-visible:|:focus\b|focus:ring|focus:outline-(?!none)", re.I)

SPACING_PROP = re.compile(
    r"\b(?:margin|padding|gap|row-gap|column-gap|inset|top|right|bottom|left)(?:-(?:top|right|bottom|left|inline|block)(?:-(?:start|end))?)?\s*:\s*([^;}{]+)",
    re.I,
)
PX_VALUE = re.compile(r"(?<![\w.#-])(\d+(?:\.\d+)?)px\b")
TW_ARBITRARY_SPACE = re.compile(r"\b-?(?:[pm][trblxy]?|gap(?:-[xy])?|space-[xy]|inset|top|left|right|bottom)-\[(\d+(?:\.\d+)?)px\]")

FONT_SIZE = re.compile(r"\bfont-size\s*:\s*(\d+(?:\.\d+)?)(px|rem)\b", re.I)
TW_TINY = re.compile(r"\btext-\[(\d+(?:\.\d+)?)(px|rem)\]")
UPPER_TRACKING = re.compile(r"\buppercase\b[^\"'`\n]*\btracking-(?:wider|widest|\[)|\btracking-(?:wider|widest|\[)[^\"'`\n]*\buppercase\b")
SECTION_NUMBER = re.compile(r">\s*(?:\[\s*)?0\d\s*(?:\]|/|\.|—|-|·)\s*[A-ZÀ-Ýa-zà-ÿ]")

CLOCK = re.compile(
    r"toLocaleTimeString|timeZoneName|Intl\.DateTimeFormat\([^)]*\{[^}]*(?:hour|timeZone)"
    r"|\b(?:local|current)\s*time\b|heure\s+locale|\bGMT\s*[+-]\s*\d|\bUTC\s*[+-]\s*\d"
    r"|setInterval\([^)]*(?:new Date|Date\.now)",
    re.I,
)
FILLER_TEXT = re.compile(
    r"scroll\s+(?:to|pour)\s+(?:explore|explorer|discover|d[ée]couvrir)|made with\s*(?:❤|♥|love)"
    r"|all systems operational|currently (?:building|available)|available for (?:work|freelance|projects)"
    r"|disponible pour (?:missions|projets|freelance)|\best\.\s*20\d\d|\bbuild\s+20\d\d"
    r"|\d{1,2}\.\d{2,}°\s*[NS]",
    re.I,
)

KEY_HANDLER = re.compile(r"\b(?:keydown|keyup|keypress|onKeyDown|onKeyUp|useHotkeys|hotkeys\()")
META_KEY = re.compile(r"\bmetaKey\b")
CTRL_KEY = re.compile(r"\bctrlKey\b")
RESERVED_SHORTCUT = re.compile(
    r"(?:metaKey|ctrlKey|mod\+|meta\+|ctrl\+|cmd\+)[^\n;]{0,80}?(?:key\s*===?\s*[\"']([tTwWnNlLrRqQpP])[\"']|\+([twnlrqp])\b)"
    r"|key\s*===?\s*[\"']([tTwWnNlLrRqQ])[\"'][^\n;]{0,80}?(?:metaKey|ctrlKey)",
)
SINGLE_KEY = re.compile(r"\.key\s*===?\s*[\"'](?:[a-z/?.]|\s)[\"']")
TYPING_GUARD = re.compile(r"isContentEditable|tagName|closest\(\s*[\"'][^\"']*(?:input|textarea)|instanceof\s+HTML(?:Input|TextArea)Element|enableOnFormTags")
HARDCODED_KBD = re.compile(r"[\"'>`]\s*(?:⌘|Cmd\s*\+|Ctrl\s*\+)\s*[A-Za-z0-9,/.]\s*[\"'<`]")
PLATFORM_CHECK = re.compile(r"navigator\.(?:platform|userAgentData|userAgent)|isMac|isApple|platform", re.I)

EMOJI_UI = re.compile("[\U0001F300-\U0001FAFF✨✅⚡]")


@dataclass
class Finding:
    line: int
    col: int
    level: str
    message: str
    excerpt: str = ""


def excerpt(line, start, end):
    a = max(0, start - 30)
    b = min(len(line), end + 30)
    text = line[a:b].strip()
    return ("..." if a > 0 else "") + text + ("..." if b < len(line) else "")


def is_vivid(text):
    for m in HEX.finditer(text):
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        if max(r, g, b) - min(r, g, b) > 60:
            return True
    for m in RGB.finditer(text):
        r, g, b = (float(x) for x in m.groups())
        if max(r, g, b) - min(r, g, b) > 60:
            return True
    for m in HSL.finditer(text):
        if float(m.group(1)) > 35:
            return True
    return bool(TW_COLOR.search(text) or NAMED_VIVID.search(text) or GLOW_VAR.search(text))


def add(findings, lines, idx, m, level, message, group=0):
    line = lines[idx]
    start, end = m.span(group)
    findings.append(Finding(idx + 1, start + 1, level, message, excerpt(line, start, end)))


def scan_line(lines, idx, ext, findings):
    line = lines[idx]
    is_markup = ext in MARKUP_EXT
    is_script = ext in SCRIPT_EXT

    for m in GLOW_PROP.finditer(line):
        value = m.group(2)
        blurs = [int(b) for b in ZERO_OFFSET_BLUR.findall(value)]
        if blurs and max(blurs) >= 8 and is_vivid(value):
            add(findings, lines, idx, m, "warn", f"Halo néon ({m.group(1)} coloré sans décalage) : ombre neutre décalée vers le bas, ou rien")
    for m in DROP_SHADOW.finditer(line):
        if int(m.group(1)) >= 6 and is_vivid(m.group(0)):
            add(findings, lines, idx, m, "warn", "drop-shadow coloré qui fait un glow")
    for m in TW_GLOW.finditer(line):
        add(findings, lines, idx, m, "warn", "Ombre colorée ou glow Tailwind")

    for m in GRADIENT_BG.finditer(line):
        if is_vivid(m.group(1)):
            add(findings, lines, idx, m, "warn", "Dégradé coloré en fond : fond uni, sauf voile de lisibilité ou charte de marque")
        else:
            add(findings, lines, idx, m, "info", "Dégradé neutre en fond : vérifier qu'il sert (voile sur image, fondu de défilement)")
    tw_grad = TW_GRADIENT.search(line)
    if tw_grad:
        level = "warn" if TW_STOP.search(line) else "info"
        add(findings, lines, idx, tw_grad, level, "Dégradé Tailwind en fond")
    for m in GRADIENT_TEXT.finditer(line):
        add(findings, lines, idx, m, "warn", "Texte en dégradé : couleur de texte normale, la graisse ou la taille font la hiérarchie")

    for m in BACKDROP.finditer(line):
        add(findings, lines, idx, m, "info", "Flou d'arrière-plan : à garder seulement pour une barre qui passe au-dessus d'un contenu qui défile")
    for m in BIG_BLUR.finditer(line):
        if int(m.group(1)) >= 20:
            add(findings, lines, idx, m, "warn", "Grosse tache floue décorative")
    for m in TW_BIG_BLUR.finditer(line):
        add(findings, lines, idx, m, "warn", "Grosse tache floue décorative")

    for m in AI_PURPLE.finditer(line):
        add(findings, lines, idx, m, "info", "Couleur de la palette IA par défaut (violet, indigo, fuchsia) : vient-elle de la marque ?")

    for m in INFINITE.finditer(line):
        if not re.search(r"spin|rotate|load|skeleton|shimmer", m.group(1), re.I):
            add(findings, lines, idx, m, "warn", "Animation infinie : une animation répond à une action puis s'arrête")
    for m in TW_LOOP.finditer(line):
        add(findings, lines, idx, m, "warn", "Animation en boucle décorative")

    for m in OUTLINE_NONE.finditer(line):
        add(findings, lines, idx, m, "outline", "outline supprimé")
    for m in TW_OUTLINE_NONE.finditer(line):
        if not re.search(r"focus-visible:(?:ring|outline)|focus:ring", line):
            add(findings, lines, idx, m, "warn", "outline-none sans anneau focus-visible sur le même élément")

    if ext in STYLE_EXT or is_markup:
        for m in SPACING_PROP.finditer(line):
            for v in PX_VALUE.finditer(m.group(1)):
                n = float(v.group(1))
                if n > 2 and n % 4:
                    start = m.start(1) + v.start()
                    findings.append(Finding(idx + 1, start + 1, "info", f"Espacement hors grille de 4 px ({v.group(0)})", excerpt(line, start, start + len(v.group(0)))))
        for m in TW_ARBITRARY_SPACE.finditer(line):
            n = float(m.group(1))
            if n > 2 and n % 4:
                add(findings, lines, idx, m, "info", "Espacement arbitraire hors grille de 4 px")
        for m in FONT_SIZE.finditer(line):
            px = float(m.group(1)) * (16 if m.group(2) == "rem" else 1)
            if px < 12:
                add(findings, lines, idx, m, "warn", f"Texte de {px:g} px : illisible, et souvent un texte inutile")
        for m in TW_TINY.finditer(line):
            px = float(m.group(1)) * (16 if m.group(2) == "rem" else 1)
            if px < 12:
                add(findings, lines, idx, m, "warn", f"Texte de {px:g} px : illisible, et souvent un texte inutile")

    if is_markup:
        for m in UPPER_TRACKING.finditer(line):
            add(findings, lines, idx, m, "info", "Petites majuscules espacées : sur-titre ou étiquette décorative ?")
        for m in SECTION_NUMBER.finditer(line):
            add(findings, lines, idx, m, "info", "Numéro de section décoratif (01 / ...)")
        for m in EMOJI_UI.finditer(line):
            add(findings, lines, idx, m, "warn", "Emoji dans l'interface")

    if is_markup or is_script:
        for m in CLOCK.finditer(line):
            add(findings, lines, idx, m, "warn", "Heure locale ou fuseau affiché : texte décoratif à retirer, sauf si l'heure est le sujet")
        for m in FILLER_TEXT.finditer(line):
            add(findings, lines, idx, m, "warn", "Texte de remplissage (statut, signature, méta, instruction évidente)")
        for m in RESERVED_SHORTCUT.finditer(line):
            add(findings, lines, idx, m, "error", "Raccourci réservé au navigateur ou au système (⌘/Ctrl + T, W, N, L, R, Q, P)")
        for m in HARDCODED_KBD.finditer(line):
            add(findings, lines, idx, m, "kbd", "Raccourci affiché en dur")


def scan_file(text, ext):
    findings = []
    lines = text.split("\n")
    for idx in range(len(lines)):
        scan_line(lines, idx, ext, findings)

    has_focus_visible = bool(FOCUS_VISIBLE.search(text))
    has_platform = bool(PLATFORM_CHECK.search(text))
    resolved = []
    for f in findings:
        if f.level == "outline":
            if has_focus_visible:
                continue
            f.level, f.message = "error", "outline supprimé sans style :focus-visible dans le fichier : le clavier ne voit plus le focus"
        elif f.level == "kbd":
            if has_platform:
                continue
            f.level, f.message = "info", "Raccourci affiché en dur : ⌘ sur Mac, Ctrl ailleurs, selon la plateforme"
        resolved.append(f)
    findings = resolved

    if ext in MARKUP_EXT | SCRIPT_EXT and KEY_HANDLER.search(text):
        has_meta, has_ctrl = bool(META_KEY.search(text)), bool(CTRL_KEY.search(text))
        if has_meta != has_ctrl:
            which = "metaKey" if has_meta else "ctrlKey"
            other = "Windows et Linux" if has_meta else "Mac"
            m = (META_KEY if has_meta else CTRL_KEY).search(text)
            line_no = text.count("\n", 0, m.start()) + 1
            findings.append(Finding(line_no, 1, "warn", f"Raccourci testé sur {which} seulement : il ne marche pas sur {other}", lines[line_no - 1].strip()[:80]))
        single = next(
            (m for m in SINGLE_KEY.finditer(text)
             if not re.search(r"metaKey|ctrlKey|altKey", lines[text.count("\n", 0, m.start())])),
            None,
        )
        if single and not TYPING_GUARD.search(text):
            line_no = text.count("\n", 0, single.start()) + 1
            findings.append(Finding(line_no, 1, "warn", "Raccourci à une touche sans vérifier si l'utilisateur tape dans un champ", lines[line_no - 1].strip()[:80]))

    if ANY_MOTION.search(text) and (INFINITE.search(text) or TW_LOOP.search(text) or "@keyframes" in text) and not REDUCED_MOTION.search(text):
        findings.append(Finding(0, 0, "info", "Animations sans prise en compte de prefers-reduced-motion dans ce fichier"))

    return findings


def iter_files(targets):
    for target in targets:
        p = Path(target)
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and f.suffix.lower() in UI_EXT and not any(part in SKIP_DIRS for part in f.parts):
                    yield f


def print_findings(name, findings, show_info):
    shown = [f for f in findings if show_info or f.level != "info"]
    if not shown:
        return
    print(name)
    for f in sorted(shown, key=lambda f: (f.line, f.col)):
        loc = f"{f.line}:{f.col}"
        tail = f"  {f.excerpt}" if f.excerpt else ""
        print(f"  {loc:<8} {LABELS[f.level]:<9} {f.message}{tail}")
    print()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Repère les marqueurs visuels d'une interface générée par IA.")
    parser.add_argument("paths", nargs="+", help="fichiers ou dossiers, ou - pour lire l'entrée standard")
    parser.add_argument("--ext", default=".tsx", help="extension à supposer pour l'entrée standard")
    parser.add_argument("--all", action="store_true", help="affiche aussi les signaux faibles")
    args = parser.parse_args()

    totals = {"error": 0, "warn": 0, "info": 0}
    files_with_issues = 0

    if args.paths == ["-"]:
        sources = [("<stdin>", sys.stdin.read(), args.ext)]
    else:
        sources = []
        for path in iter_files(args.paths):
            if path.stat().st_size > MAX_SIZE:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            sources.append((str(path), text, path.suffix.lower()))

    for name, text, ext in sources:
        if IGNORE_MARKER in "\n".join(text.split("\n", 20)[:20]):
            continue
        findings = scan_file(text, ext)
        visible = [f for f in findings if args.all or f.level != "info"]
        if visible:
            files_with_issues += 1
            print_findings(name, findings, args.all)
        for f in findings:
            totals[f.level] += 1

    hidden = "" if args.all else f" ({totals['info']} signal(aux) faible(s), --all pour les voir)"
    print(f"{totals['error']} erreur(s), {totals['warn']} avertissement(s) dans {files_with_issues} fichier(s){hidden}")
    sys.exit(1 if totals["error"] else 0)


if __name__ == "__main__":
    main()
