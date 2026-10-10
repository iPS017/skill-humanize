#!/usr/bin/env python3
# humanize:ignore-file
import argparse
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path

PROSE_EXT = {".md", ".mdx", ".txt", ".rst"}
C_LIKE_EXT = {
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".astro",
    ".go", ".rs", ".java", ".kt", ".swift", ".c", ".h", ".cpp", ".cs", ".php",
    ".scss", ".less", ".dart",
}
CSS_EXT = {".css"}
HASH_EXT = {".py", ".rb", ".sh", ".bash", ".zsh", ".yml", ".yaml", ".toml", ".ps1"}
HTML_EXT = {".html", ".htm"}
MARKUP_EXT = {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro"}
JS_EXT = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".astro"}
CODE_EXT = C_LIKE_EXT | CSS_EXT | HASH_EXT | HTML_EXT | {".json"}

SKIP_DIRS = {
    "node_modules", ".git", ".next", ".nuxt", ".svelte-kit", "dist", "build", "out",
    ".turbo", ".vercel", ".cache", "coverage", "__pycache__", ".venv", "venv", "vendor",
}
IGNORE_MARKER = "humanize:ignore-file"
MAX_SIZE = 2_000_000

EM_DASH = re.compile("\u2014")
SPACED_EN_DASH = re.compile(r"(?<=\S)\s\u2013\s(?=\S)")
ELLIPSIS = re.compile("\u2026")
ARROWS = re.compile("[\u2190-\u21FF\u27F0-\u27FF\u2794-\u27BF]")
INVISIBLE = re.compile("[\u200B\u200C\u200D\u2060\uFEFF]")
NBSP = re.compile("[\u00A0\u202F]")
CURLY = re.compile("[\u2018\u2019\u201C\u201D]")
EN_CURLY_DOUBLE = re.compile("[\u201C\u201D]")
EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF\u2600-\u2793\u2B00-\u2BFF\u2705\u274C\u2728]"
)
EN_SPACE_BEFORE_PUNCT = re.compile(r"(?<=[\w)\]*_`])[ \u00A0\u202F]+(?=[:;!?](\s|$))")
BOLD_LABEL = re.compile(r"^\s*(?:[-*+]|\d+\.)?\s*\*\*[^*\n]{1,50}\*\*\s*:")

FR_PHRASES = [
    r"dans un monde o[uù]", r"[àa] l'[èe]re (du|de l')", r"dans le paysage", r"plong(eons|er|ez) dans",
    r"le vif du sujet", r"il est (important|essentiel|crucial) de (noter|souligner|rappeler)",
    r"il convient de (noter|souligner)", r"force est de constater", r"il va sans dire",
    r"n'h[ée]sitez pas", r"en conclusion", r"en somme", r"en d[ée]finitive", r"pour r[ée]sumer",
    r"j'esp[èe]re que (cela|ça|ceci)", r"excellente question", r"\bv[ée]ritable", r"incontournable",
    r"\bcrucial", r"r[ée]volution(ner|ne|naire)", r"\bsublim(er|e)\b", r"\bboost(er|e)\b", r"\bpropuls",
    r"(lib[ée]rer|exploiter|d[ée]bloquer) (tout )?(le|son|votre|leur) (plein )?potentiel",
    r"tirer parti", r"r[ée]silience", r"bienveillan", r"authenticit[ée]", r"synergie", r"\blevier",
    r"impactant", r"\bvibrant", r"tapisserie", r"symphonie", r"pierre angulaire", r"cl[ée] de vo[uû]te",
    r"que vous soyez", r"^\s*imaginez", r"le meilleur dans tout [çc]a", r"bonne nouvelle\s*:",
    r"spoiler\s*:", r"le r[ée]sultat\s*\?", r"(^|\. |\ble )r[ée]sultat\s*:", r"\ben outre\b", r"de surcro[iî]t",
    r"faire du sens", r"en termes de", r"ce n'est pas (seulement |juste |qu')?[^.]{1,60}?, c'est",
    r"plus qu'une? [^.]{1,40}?, une? ", r"il ne s'agit pas (seulement|uniquement|juste) de",
    r"dans cet article,? nous", r"au c(œ|oe)ur de", r"atout majeur", r"valeur ajout[ée]e",
]
EN_PHRASES = [
    r"\bdelv(e|es|ing)\b", r"\btapestry\b", r"\btestament to\b", r"\bnavigat(e|ing) the\b",
    r"\blandscape\b", r"\brealm\b", r"\bleverag(e|es|ing)\b", r"\bseamless(ly)?\b", r"\brobust\b",
    r"\belevat(e|es|ing)\b", r"\bunlock(s|ing)?\b", r"\bunleash", r"\bharness(es|ing)?\b",
    r"\bgame[- ]chang(er|ing)\b", r"\bcutting[- ]edge\b", r"\bgroundbreaking\b", r"\bvibrant\b",
    r"\bbustling\b", r"\bmeticulous(ly)?\b", r"\bpivotal\b", r"\bcrucial\b", r"\bparamount\b",
    r"\bembark", r"\bfoster(s|ing)?\b", r"\bunderscor(e|es|ing)\b", r"\bshowcas(e|es|ing)\b",
    r"in today's (fast[- ]paced|digital|ever)", r"ever[- ]evolving", r"it(')?s worth noting",
    r"it is worth noting", r"it(')?s important to (note|remember)", r"needless to say",
    r"at the end of the day", r"\bin conclusion\b", r"\bin summary\b", r"feel free to",
    r"i hope this helps", r"great question", r"let'?s dive", r"\bdive into\b", r"deep dive",
    r"whether you're", r"here's the thing", r"\bnot just [^.]{1,60}?,? (it's|but)\b",
    r"\bmoreover\b", r"\bfurthermore\b", r"\badditionally\b", r"happy coding",
]
FR_RE = [re.compile(p, re.IGNORECASE) for p in FR_PHRASES]
EN_RE = [re.compile(p, re.IGNORECASE) for p in EN_PHRASES]

ALLOWED_COMMENT = re.compile(
    r"eslint|@ts-|prettier-ignore|biome-ignore|noqa|type:\s*ignore|istanbul|c8 ignore|pragma|"
    r"webpackChunkName|@vite-ignore|stylelint|jshint|@license|licen[cs]e|copyright|spdx|"
    r"#region|#endregion|@jsx|@refresh|-\*-\s*coding|humanize:|^\s*!|@preserve|pylint|mypy",
    re.IGNORECASE,
)
GENERIC_JS = re.compile(
    r"\b(?:const|let|var|function|class)\s+("
    r"data\d*|temp\d*|tmp\d*|foo|bar|baz|res|result\d*|obj\d*|item\d+|stuff|thing\d*|info|"
    r"myVar\w*|newData|value\d+|handleClick\d+|MyComponent\w*|helper\d*|doStuff|func\d*|"
    r"\w+(?:V2|v2|New|Old|Final|Copy|Temp|Updated|Fixed)"
    r")\b"
)
GENERIC_PY = re.compile(
    r"^\s*(?:def\s+(helper\d*|func\d*|do_stuff|process_data)\b|"
    r"(data\d+|temp\d*|tmp\d*|foo|bar|obj\d*|stuff|thing\d*|result\d+)\s*=[^=])"
)
CONSOLE = re.compile(r"\bconsole\.(log|debug|info)\s*\(")
DIV_CLICK = re.compile(r"<div\b[^>]*\bon(Click|click|:click)\b")
DIV_TAG = re.compile(r"<div\b")
SEMANTIC_TAG = re.compile(
    r"<(header|nav|main|section|article|aside|footer|button|ul|ol|li|figure|form|a|h[1-6]|p|label)\b"
)
CLASS_ATTR = re.compile(r"\bclass(?:Name)?\s*=\s*[\"'{`]([^\"'`}]*)")
BAD_CLASS = re.compile(
    r"^(?:(div|box|block|item|section|container|wrapper)\d+|container-wrapper|inner-wrapper|"
    r"wrapper-inner|text-wrapper|(big|small|red|blue|green|bold)-(text|title|box|button))$"
)
BAD_ALT = re.compile(r"\balt\s*=\s*[\"'](image|img|photo|picture|icon|logo|placeholder)[\"']", re.I)
BAD_FILENAME = re.compile(
    r"(^|[-_. ])(final|new|old|copy|backup|bak|temp|tmp|untitled|misc|stuff|fixed|updated)\d*($|[-_. ])"
    r"|^(utils|helpers?|test|component|file|index|page|styles?|script|main|app)[-_ ]?\d+$"
    r"|\(\d+\)| ",
    re.IGNORECASE,
)

LABELS = {"error": "erreur", "warn": "attention", "info": "info"}


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
    text = line[a:b].strip().replace("\r", "")
    return ("..." if a > 0 else "") + text + ("..." if b < len(line) else "")


def detect_lang(text):
    low = " " + re.sub(r"\s+", " ", text.lower()) + " "
    fr = sum(low.count(w) for w in (" le ", " la ", " les ", " des ", " est ", " une ", " pour ", " que ", " avec "))
    en = sum(low.count(w) for w in (" the ", " and ", " is ", " of ", " to ", " that ", " with ", " for "))
    return "fr" if fr >= en else "en"


def mask_markdown(lines):
    masked, in_fence = [], False
    for line in lines:
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            masked.append("")
            continue
        if in_fence:
            masked.append("")
            continue
        line = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)
        line = re.sub(r"<!--.*?-->", lambda m: " " * len(m.group(0)), line)
        line = re.sub(r"\]\([^)]*\)", lambda m: " " * len(m.group(0)), line)
        masked.append(line)
    return masked


def scan_chars(lines, findings, code):
    for n, line in enumerate(lines, 1):
        for m in INVISIBLE.finditer(line):
            findings.append(Finding(n, m.start() + 1, "error", "Caractère invisible", excerpt(line, m.start(), m.end())))
        for m in EM_DASH.finditer(line):
            findings.append(Finding(n, m.start() + 1, "error", "Tiret cadratin (—)", excerpt(line, m.start(), m.end())))
        for m in SPACED_EN_DASH.finditer(line):
            findings.append(Finding(n, m.start() + 2, "error", "Demi-cadratin utilisé en incise (–)", excerpt(line, m.start(), m.end())))
        for m in ARROWS.finditer(line):
            findings.append(Finding(n, m.start() + 1, "warn", "Flèche décorative", excerpt(line, m.start(), m.end())))
        for m in EMOJI.finditer(line):
            findings.append(Finding(n, m.start() + 1, "warn", "Emoji", excerpt(line, m.start(), m.end())))
        for m in ELLIPSIS.finditer(line):
            findings.append(Finding(n, m.start() + 1, "warn", "Caractère … (utiliser ... ou reformuler)", excerpt(line, m.start(), m.end())))
        if code:
            for m in CURLY.finditer(line):
                findings.append(Finding(n, m.start() + 1, "warn", "Guillemet ou apostrophe courbe dans du code", excerpt(line, m.start(), m.end())))
            for m in NBSP.finditer(line):
                findings.append(Finding(n, m.start() + 1, "warn", "Espace insécable dans du code", excerpt(line, m.start(), m.end())))


def scan_prose(text, lines, findings, lang):
    masked = mask_markdown(lines)
    scan_chars(masked, findings, code=False)
    phrases = FR_RE if lang == "fr" else EN_RE
    bold_labels = []
    for n, line in enumerate(masked, 1):
        norm = line.replace("\u2019", "'")
        for rx in phrases:
            for m in rx.finditer(norm):
                findings.append(Finding(n, m.start() + 1, "warn", f"Tournure typée IA : « {m.group(0).strip()} »", excerpt(line, m.start(), m.end())))
        if lang == "en":
            for m in EN_SPACE_BEFORE_PUNCT.finditer(line):
                findings.append(Finding(n, m.start() + 1, "error", "Espace avant la ponctuation (anglais)", excerpt(line, m.start(), m.end() + 1)))
            for m in NBSP.finditer(line):
                findings.append(Finding(n, m.start() + 1, "warn", "Espace insécable dans un texte anglais", excerpt(line, m.start(), m.end())))
        else:
            for m in EN_CURLY_DOUBLE.finditer(line):
                findings.append(Finding(n, m.start() + 1, "warn", "Guillemets anglais dans un texte français (utiliser « »)", excerpt(line, m.start(), m.end())))
        if BOLD_LABEL.match(line):
            bold_labels.append(n)
    if len(bold_labels) >= 3:
        findings.append(Finding(bold_labels[0], 1, "warn", f"{len(bold_labels)} lignes « **Étiquette** : texte », à rédiger en phrases"))

    body = " ".join(
        l for l in masked
        if l.strip() and not re.match(r"^\s*(#|[-*+]\s|\d+\.\s|\||>)", l)
    )
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", body) if len(s.split()) >= 2]
    if len(sentences) >= 8:
        counts = [len(s.split()) for s in sentences]
        mean = statistics.mean(counts)
        cv = statistics.pstdev(counts) / mean if mean else 0
        if cv < 0.35:
            findings.append(Finding(1, 1, "warn", f"Rythme monotone : phrases de {mean:.0f} mots en moyenne, très peu de variation"))


def find_comments(text, ext):
    spans = []
    if ext in HTML_EXT or ext in {".vue", ".svelte", ".astro"}:
        for m in re.finditer(r"<!--.*?-->", text, re.S):
            spans.append((m.start(), m.end(), m.group(0)))
    if ext in HTML_EXT:
        return spans

    hash_style = ext in HASH_EXT
    line_comments = ext in C_LIKE_EXT
    i, n = 0, len(text)
    state, quote, start = "code", "", 0
    while i < n:
        c = text[i]
        if state == "code":
            if hash_style and c == "#" and (i == 0 or text[i - 1] in " \t\n"):
                if not (i == 0 and text.startswith("#!")):
                    state, start = "line", i
            elif not hash_style and c == "/" and text.startswith("/*", i):
                state, start = "block", i
                i += 1
            elif line_comments and c == "/" and text.startswith("//", i) and (i == 0 or text[i - 1] != ":"):
                state, start = "line", i
                i += 1
            elif hash_style and text.startswith(('"""', "'''"), i):
                state, quote = "string", text[i:i + 3]
                i += 2
            elif c in "\"'`":
                if c == "'" and ext in {".jsx", ".tsx", ".vue", ".svelte", ".astro"} and i > 0 and text[i - 1].isalpha():
                    pass
                else:
                    state, quote = "string", c
        elif state == "line":
            if c == "\n":
                spans.append((start, i, text[start:i]))
                state = "code"
        elif state == "block":
            if text.startswith("*/", i):
                spans.append((start, i + 2, text[start:i + 2]))
                state = "code"
                i += 1
        elif state == "string":
            if c == "\\":
                i += 1
            elif text.startswith(quote, i):
                i += len(quote) - 1
                state = "code"
            elif c == "\n" and quote in "\"'":
                state = "code"
        i += 1
    if state == "line":
        spans.append((start, n, text[start:n]))
    return spans


def classify_comment(body):
    if ALLOWED_COMMENT.search(body):
        return None
    if body.startswith("/**"):
        return ("info", "JSDoc : à garder seulement si le projet documente son API")
    if re.search(r"\b(TODO|FIXME|XXX)\b", body):
        return ("warn", "TODO laissé dans le code")
    return ("warn", "Commentaire : à supprimer s'il paraphrase le code")


def line_col(text, index):
    line = text.count("\n", 0, index) + 1
    col = index - (text.rfind("\n", 0, index) + 1) + 1
    return line, col


def scan_code(text, lines, findings, ext):
    scan_chars(lines, findings, code=True)
    for start, _, body in find_comments(text, ext):
        verdict = classify_comment(body)
        if verdict:
            ln, col = line_col(text, start)
            short = body.strip().splitlines()[0][:70] if body.strip() else body
            findings.append(Finding(ln, col, verdict[0], verdict[1], short))
    for n, line in enumerate(lines, 1):
        if ext in JS_EXT:
            for m in GENERIC_JS.finditer(line):
                findings.append(Finding(n, m.start(1) + 1, "warn", f"Nom générique : {m.group(1)}", excerpt(line, m.start(), m.end())))
            for m in CONSOLE.finditer(line):
                findings.append(Finding(n, m.start() + 1, "warn", "console.log de debug", excerpt(line, m.start(), m.end())))
        if ext == ".py":
            m = GENERIC_PY.search(line)
            if m:
                name = m.group(1) or m.group(2)
                findings.append(Finding(n, line.find(name) + 1, "warn", f"Nom générique : {name}", excerpt(line, 0, len(line))))
        if ext in MARKUP_EXT:
            for m in DIV_CLICK.finditer(line):
                findings.append(Finding(n, m.start() + 1, "warn", "div cliquable (utiliser button ou a)", excerpt(line, m.start(), m.end())))
            for m in CLASS_ATTR.finditer(line):
                for token in m.group(1).split():
                    if BAD_CLASS.match(token):
                        findings.append(Finding(n, m.start() + 1, "warn", f"Classe mal nommée : {token}", excerpt(line, m.start(), m.end())))
            for m in BAD_ALT.finditer(line):
                findings.append(Finding(n, m.start() + 1, "warn", "alt générique (décrire l'image ou alt=\"\")", excerpt(line, m.start(), m.end())))
    if ext in MARKUP_EXT:
        divs = len(DIV_TAG.findall(text))
        semantic = len(SEMANTIC_TAG.findall(text))
        if divs >= 10 and divs / (divs + semantic) > 0.85:
            findings.append(Finding(1, 1, "warn", f"Div soup : {divs} div pour {semantic} balises sémantiques"))


def strip_comments(text, ext):
    spans = [
        (s, e) for s, e, body in find_comments(text, ext)
        if (verdict := classify_comment(body)) and verdict[0] != "info"
    ]
    if not spans:
        return text
    out, last, touched = [], 0, set()
    for s, e in spans:
        before = text[last:s]
        j = len(before.rstrip(" \t"))
        k = e
        while k < len(text) and text[k] in " \t":
            k += 1
        if j and before[j - 1] == "{" and k < len(text) and text[k] == "}":
            before = before[: j - 1]
            e = k + 1
        out.append(before)
        touched.add(len("".join(out)))
        last = e
    out.append(text[last:])
    result = "".join(out)

    new_lines = result.split("\n")
    marks, pos = set(), 0
    for idx, line in enumerate(new_lines):
        end = pos + len(line)
        if any(pos <= t <= end for t in touched):
            marks.add(idx)
        pos = end + 1
    cleaned = []
    for idx, line in enumerate(new_lines):
        if idx in marks:
            stripped = line.rstrip(" \t\r")
            if not stripped.strip():
                continue
            line = stripped + ("\r" if line.endswith("\r") else "")
        cleaned.append(line)
    return "\n".join(cleaned)


def apply_fixes(text, kind, ext, lang):
    text = INVISIBLE.sub("", text)
    if kind == "code":
        text = ELLIPSIS.sub("...", text)
        text = NBSP.sub(" ", text)
        if ext not in MARKUP_EXT:
            text = re.sub("[\u2018\u2019]", "'", text)
            text = re.sub("[\u201C\u201D]", '"', text)
    elif lang == "en":
        text = EN_SPACE_BEFORE_PUNCT.sub("", text)
        text = NBSP.sub(" ", text)
    return text


def kind_for(path, forced):
    if forced:
        return forced
    ext = path.suffix.lower()
    if ext in PROSE_EXT:
        return "prose"
    if ext in CODE_EXT:
        return "code"
    return None


def check_filename(path):
    stem = path.stem if path.suffix else path.name
    if path.name.startswith("."):
        return None
    if BAD_FILENAME.search(stem):
        return "Nom de fichier à revoir (version, copie, fourre-tout ou espace)"
    if re.search(r"[^\x00-\x7F]", path.name):
        return "Nom de fichier avec accent ou caractère spécial"
    return None


def iter_files(targets):
    for target in targets:
        p = Path(target)
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and not any(part in SKIP_DIRS for part in f.parts):
                    yield f


def scan_text(text, kind, ext, lang):
    findings = []
    lines = text.split("\n")
    if kind == "prose":
        scan_prose(text, lines, findings, lang or detect_lang(text))
    else:
        scan_code(text, lines, findings, ext)
    return findings


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
    parser = argparse.ArgumentParser(description="Repère les marqueurs d'écriture IA dans du texte et du code.")
    parser.add_argument("paths", nargs="+", help="fichiers ou dossiers, ou - pour lire l'entrée standard")
    parser.add_argument("--lang", choices=["fr", "en"], help="langue de la prose (détectée sinon)")
    parser.add_argument("--as", dest="kind", choices=["prose", "code"], help="forcer le type de contenu")
    parser.add_argument("--ext", default=".ts", help="extension à supposer pour l'entrée standard en mode code")
    parser.add_argument("--fix", action="store_true", help="corrige les cas sans ambiguïté (caractères invisibles, …, guillemets courbes dans le code, espaces avant ponctuation en anglais)")
    parser.add_argument("--strip-comments", action="store_true", help="supprime les commentaires de code, sauf licences et directives d'outils")
    parser.add_argument("--all", action="store_true", help="affiche aussi les informations mineures")
    args = parser.parse_args()

    totals = {"error": 0, "warn": 0, "info": 0}
    files_with_issues = 0

    if args.paths == ["-"]:
        text = sys.stdin.read()
        kind = args.kind or "prose"
        findings = scan_text(text, kind, args.ext, args.lang)
        print_findings("<stdin>", findings, args.all)
        for f in findings:
            totals[f.level] += 1
        files_with_issues = 1 if findings else 0
    else:
        for path in iter_files(args.paths):
            findings = []
            name_issue = check_filename(path)
            if name_issue:
                findings.append(Finding(0, 0, "warn", name_issue, path.name))
            kind = kind_for(path, args.kind)
            if kind and path.stat().st_size <= MAX_SIZE:
                try:
                    with open(path, encoding="utf-8", newline="") as fh:
                        text = fh.read()
                except UnicodeDecodeError:
                    continue
                if IGNORE_MARKER in "\n".join(text.split("\n", 20)[:20]):
                    continue
                ext = path.suffix.lower()
                lang = args.lang or (detect_lang(text) if kind == "prose" else None)
                if args.fix or args.strip_comments:
                    fixed = apply_fixes(text, kind, ext, lang) if args.fix else text
                    if args.strip_comments and kind == "code":
                        fixed = strip_comments(fixed, ext)
                    if fixed != text:
                        with open(path, "w", encoding="utf-8", newline="") as fh:
                            fh.write(fixed)
                        print(f"corrigé : {path}")
                        text = fixed
                findings.extend(scan_text(text, kind, ext, lang))
            if findings:
                files_with_issues += 1
                print_findings(str(path), findings, args.all)
                for f in findings:
                    totals[f.level] += 1

    print(f"{totals['error']} erreur(s), {totals['warn']} avertissement(s) dans {files_with_issues} fichier(s)")
    sys.exit(1 if totals["error"] else 0)


if __name__ == "__main__":
    main()
