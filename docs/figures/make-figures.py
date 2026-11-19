#!/usr/bin/env python3
"""Draw the README's figure from the tree. Standard library only.

    python3 -I docs/figures/make-figures.py           write docs/figures/*.svg
    python3 -I docs/figures/make-figures.py --check   exit 1 if a committed figure is out of date

Each figure is written twice, <name>-light.svg and <name>-dark.svg, for a
<picture> element. The files stand alone (no external CSS, fonts or scripts).
The visual system (palette, fonts, label measurement against font-metrics.json)
is first-bite's docs/img/build.py. Every name, version and count in the figure
is read from this tree: first-bite.ref, .github/workflows/, dictionaries/ and
deployments/.
"""
import json
import math
import os
import re
import sys
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))


def read_text(path):
    """The text of the file at `path`."""
    with open(path, encoding="utf-8") as fh:
        return fh.read()


METRICS = json.loads(read_text(os.path.join(HERE, "font-metrics.json")))
W = 760
FONT = '"Helvetica Neue", Helvetica, Arial, "Liberation Sans", sans-serif'
MONO = 'Menlo, Consolas, "Liberation Mono", "Courier New", monospace'
MIN_SIZE = 13

PALETTE = {
    "light": {
        "ink": "#16191f", "quiet": "#515a66", "rule": "#dfe3e8", "line": "#7d8899",
        "paper": "#ffffff", "panel": "#f4f6f8",
        "accent": "#1f4fbf", "accent-soft": "#e6edfb", "on-accent": "#ffffff",
        "good": "#24703a", "good-bg": "#e3f4e7", "warn": "#8a5300", "warn-bg": "#fcefd6",
        "info": "#5b4bb0", "info-bg": "#eeebfa", "mute": "#5a606a", "mute-bg": "#eeeeec",
    },
    "dark": {
        "ink": "#e6e9ee", "quiet": "#a3abb8", "rule": "#2c333d", "line": "#7a8594",
        "paper": "#0f1317", "panel": "#171b21",
        "accent": "#8fb0ff", "accent-soft": "#172544", "on-accent": "#0f1317",
        "good": "#6cc487", "good-bg": "#172b1e", "warn": "#e3b04f", "warn-bg": "#31281a",
        "info": "#b3a6f5", "info-bg": "#221d3d", "mute": "#9aa2ad", "mute-bg": "#23262b",
    },
}

CSS = """
text{font-family:%(font)s}
.m{font-family:%(mono)s}
.t{fill:%(ink)s}.q{fill:%(quiet)s}.a{fill:%(accent)s}.g{fill:%(good)s}.w{fill:%(warn)s}.i{fill:%(info)s}.mu{fill:%(mute)s}.on{fill:%(on-accent)s}
.bg{fill:%(paper)s;stroke:%(rule)s;stroke-width:1}
.bx{fill:%(paper)s;stroke:%(line)s;stroke-width:1.25}
.bxp{fill:%(panel)s;stroke:%(rule)s;stroke-width:1.25}
.bxa{fill:%(accent-soft)s;stroke:%(accent)s;stroke-width:1.25}
.bxg{fill:%(good-bg)s;stroke:%(good)s;stroke-width:1.25}
.bxw{fill:%(warn-bg)s;stroke:%(warn)s;stroke-width:1.25}
.bxm{fill:%(mute-bg)s;stroke:%(mute)s;stroke-width:1.25;stroke-dasharray:2 4}
.bxd{fill:%(paper)s;stroke:%(line)s;stroke-width:1.25;stroke-dasharray:5 4}
.ln{stroke:%(line)s;stroke-width:1.25;fill:none}
.lnk{stroke:%(ink)s;stroke-width:3;fill:none}
.lna{stroke:%(accent)s;stroke-width:2;fill:none}
.lnd{stroke:%(line)s;stroke-width:1.25;fill:none;stroke-dasharray:6 5}
.lnr{stroke:%(rule)s;stroke-width:1;fill:none}
.fa{fill:%(accent)s}.fl{fill:%(line)s}.fk{fill:%(ink)s}.fg{fill:%(good)s}.fp{fill:%(panel)s}.fr{fill:%(rule)s}
.f0{fill:%(accent-soft)s}.f1{fill:%(warn-bg)s}.f2{fill:%(info-bg)s}.f3{fill:%(good-bg)s}
.s0{stroke:%(accent)s}.s1{stroke:%(warn)s}.s2{stroke:%(info)s}.s3{stroke:%(good)s}
.c0{fill:%(accent)s}.c1{fill:%(warn)s}.c2{fill:%(info)s}.c3{fill:%(good)s}
.pp{fill:%(paper)s}
path,line{stroke-linejoin:round}
"""


def tw(s, size, bold=False, mono=False):
    """Width of a label in user units, with headroom."""
    if mono:
        return len(s) * 0.602 * size * 1.04
    table = METRICS["bold" if bold else "regular"]
    return sum(table.get(ch, 600) for ch in s) / 1000 * size * 1.06


def n(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


def thousands(v):
    return f"{v:,}"


class Fig:
    def __init__(self, name, title, desc, height, show_title=True):
        """show_title=False: a large-type figure whose own headings carry the message."""
        self.name, self.title, self.desc, self.h = name, title, desc, height
        self.out = []
        self.out.append(f'<rect class="bg" x="0.5" y="0.5" width="{W - 1}" height="{height - 1}" rx="12"/>')
        if show_title:
            self.text(24, 38, title, 18, bold=True, role="title")

    # -- text ---------------------------------------------------------------
    def text(self, x, y, s, size=13, bold=False, cls="t", anchor="start", mono=False,
             halo=False, role=None, maxw=None):
        if size < MIN_SIZE:
            raise SystemExit(f"{self.name}: {s!r} is below the minimum size")
        w = tw(s, size, bold, mono)
        x0 = x if anchor == "start" else x - w / 2 if anchor == "middle" else x - w
        if x0 < 8 or x0 + w > W - 8 or y - size < 4 or y + size * 0.3 > self.h - 6:
            raise SystemExit(f"{self.name}: {s!r} leaves the canvas ({x0:.0f}..{x0 + w:.0f}, y {y:.0f})")
        if maxw is not None and w > maxw:
            raise SystemExit(f"{self.name}: {s!r} is {w:.0f} wide, more than the {maxw:.0f} it has")
        if halo:   # a paper patch behind the label, so a line passing under it does not cross the text
            self.out.append(f'<rect x="{n(x0 - 4)}" y="{n(y - size)}" width="{n(w + 8)}" height="{n(size * 1.35)}" class="pp" data-lint="halo"/>')
        c = cls + (" m" if mono else "")
        a = "" if anchor == "start" else f' text-anchor="{anchor}"'
        b = ' font-weight="700"' if bold else ""
        r = f' data-role="{role}"' if role else ""
        if halo:
            r += ' data-lint="halo"'
        self.out.append(f'<text x="{n(x)}" y="{n(y)}" font-size="{n(size)}"{b}{a}{r} class="{c}">{escape(s)}</text>')
        return w

    def rich(self, x, y, parts, size=13, maxw=None, role="note"):
        """One line made of (text, bold, class) runs."""
        w = sum(tw(s, size, b) for s, b, _ in parts)
        if x < 8 or x + w > W - 8:
            raise SystemExit(f"{self.name}: {parts!r} leaves the canvas")
        if maxw is not None and w > maxw:
            raise SystemExit(f"{self.name}: {parts!r} is {w:.0f} wide, more than {maxw:.0f}")
        spans = "".join(
            f'<tspan class="{c}"{" font-weight=" + chr(34) + "700" + chr(34) if b else ""}>{escape(s)}</tspan>'
            for s, b, c in parts)
        self.out.append(f'<text x="{n(x)}" y="{n(y)}" font-size="{n(size)}" data-role="{role}" class="t" xml:space="preserve">{spans}</text>')

    # -- shapes -------------------------------------------------------------
    def rect(self, x, y, w, h, cls="bx", rx=8):
        self.out.append(f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{n(rx)}" class="{cls}"/>')

    def box(self, x, y, w, h, lines, cls="bx", rx=8, align="middle", pad=10):
        """A box with centred lines. lines: (text, size, bold, class[, mono])."""
        self.rect(x, y, w, h, cls, rx)
        lead = [ln[1] + 5 for ln in lines]
        total = sum(lead) - 5
        if total > h - 12:
            raise SystemExit(f"{self.name}: box at {x},{y} is too short for its text")
        cy = y + (h - total) / 2
        for ln, ld in zip(lines, lead):
            s, size, bold, c = ln[:4]
            mono = len(ln) > 4 and ln[4]
            base = cy + size * 0.80
            tx = x + w / 2 if align == "middle" else x + pad
            self.text(tx, base, s, size, bold, c, anchor=align if align == "middle" else "start",
                      mono=mono, maxw=w - 2 * pad)
            cy += ld

    def line(self, pts, cls="ln", head=None, start_head=False, nohead=False, hcls=None):
        """Polyline. head: fill class of an arrowhead at the last point."""
        pts = [tuple(map(float, p)) for p in pts]
        heads = ""

        def arrow(tip, prev):
            (x2, y2), (x1, y1) = tip, prev
            length = math.hypot(x2 - x1, y2 - y1)
            ux, uy = (x2 - x1) / length, (y2 - y1) / length
            hl, hw = 10, 5
            bx, by = x2 - ux * hl, y2 - uy * hl
            p1, p2 = (bx - uy * hw, by + ux * hw), (bx + uy * hw, by - ux * hw)
            path = f'<path d="M{n(x2)} {n(y2)}L{n(p1[0])} {n(p1[1])}L{n(p2[0])} {n(p2[1])}z" class="{head}"/>'
            return (bx + ux, by + uy), path

        draw = list(pts)
        if head:
            draw[-1], h1 = arrow(pts[-1], pts[-2])
            heads += h1
            if start_head:
                draw[0], h0 = arrow(pts[0], pts[1])
                heads += h0
        d = "M" + "L".join(f"{n(x)} {n(y)}" for x, y in draw)
        lint = ' data-lint="nohead"' if (nohead or not head) else ""
        self.out.append(f'<path d="{d}" class="{cls}"{lint}/>' + heads)

    def disc(self, cx, cy, r, cls, label=None, lcls="on"):
        self.out.append(f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" class="{cls}"/>')
        if label is not None:
            self.text(cx, cy + 4.6, str(label), 13, True, lcls, "middle")

    def raw(self, s):
        self.out.append(s)

    # -- output -------------------------------------------------------------
    def render(self, theme):
        pal = dict(PALETTE[theme], font=FONT, mono=MONO)
        css = (CSS % pal).strip().replace("\n", "")
        tid, did = f"{self.name}-title", f"{self.name}-desc"
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {self.h}" width="{W}" height="{self.h}" '
            f'role="img" aria-labelledby="{tid} {did}" aria-label="{escape(self.title)}">\n'
            f'<title id="{tid}">{escape(self.title)}</title>\n<desc id="{did}">{escape(self.desc)}</desc>\n'
            f'<style>{css}</style>\n' + "\n".join(self.out) + "\n</svg>\n")




# ---------------------------------------------------------------------------
# Facts, read from the tree
# ---------------------------------------------------------------------------
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def facts():
    pin = read_text(os.path.join(ROOT, "first-bite.ref")).strip()
    if len(pin) != 40:
        raise SystemExit("first-bite.ref does not hold a full sha")
    version = None
    for line in read_text(os.path.join(ROOT, ".github", "workflows", "check.yml")).splitlines():
        if line.strip().startswith("FIRST_BITE_VERSION:"):
            version = line.split(":", 1)[1].strip().strip('"')
    dicts = []
    for name in sorted(os.listdir(os.path.join(ROOT, "dictionaries"))):
        d = os.path.join(ROOT, "dictionaries", name, "dictionary")
        if not os.path.isdir(d):
            continue
        meta = json.loads(read_text(os.path.join(d, "dictionary.json")))
        iface = [e for e in sorted(os.listdir(d)) if os.path.isdir(os.path.join(d, e, "messages"))][0]
        im = json.loads(read_text(os.path.join(d, iface, "metadata.json")))
        files = {e[:-5] for e in os.listdir(os.path.join(d, iface, "messages")) if e.endswith(".json")}
        order = [v for _, v in sorted(im["message_type"]["values"].items(), key=lambda kv: int(kv[0]))]
        msgs = [m for m in order if m in files]
        dicts.append({"name": meta["name"], "version": meta["version"], "doc": meta["source"]["document"],
                      "rev": meta["source"]["revision"], "iface": iface, "msgs": msgs})
    sites = sorted(e for e in os.listdir(os.path.join(ROOT, "deployments"))
                   if os.path.isdir(os.path.join(ROOT, "deployments", e)))
    site = sites[0]
    subs = read_text(os.path.join(ROOT, "deployments", site, "subscribers.yml"))
    transport = re.search(r"^\s+transport:\s*(\S+)", subs, re.M).group(1)
    min_tls = re.search(r'^\s+min_tls:\s*"?([\d.]+)', subs, re.M).group(1)
    sinks = re.findall(r"^\s+- name:\s*(\S+)", subs, re.M)
    workflows = sorted(os.path.splitext(e)[0] for e in os.listdir(os.path.join(ROOT, ".github", "workflows"))
                       if e.endswith(".yml"))
    return {"pin": pin, "version": version, "dicts": dicts, "site": site, "sites": sites,
            "transport": transport, "min_tls": min_tls, "sinks": sinks, "workflows": workflows}


# ---------------------------------------------------------------------------
# overlay: first-bite at a pinned commit, plus what a deployment owns
# ---------------------------------------------------------------------------
def overlay():
    F = facts()
    short = F["pin"][:7]
    dnames = " and ".join(d["name"] for d in F["dicts"])
    title = "A deployment is first-bite at a pinned commit, plus an overlay it owns"
    desc = ("first-bite (public) supplies the software: bite, the decoder, and mind, the capture and publish "
            "process. This repository, first-bite-env, is the overlay: first-bite.ref pins first-bite commit %s "
            "(release v%s); bite checks its dictionaries %s with make check; mind runs its site %s, which sends "
            "Cursor-on-Target to a TAK server and records to an archive, over TLS %s. Every document, dictionary, "
            "address and name in it is invented. A private overlay is made from it as a template, with the same "
            "shape." % (short, F["version"], dnames, F["site"], F["min_tls"]))
    f = Fig("overlay", title, desc, 618)
    f.text(24, 60, "This repository is the overlay, with invented content. Yours is a private copy of it.", 13,
           cls="q")

    # first-bite, the software
    f.rect(24, 80, 712, 84, "bxp", 10)
    f.text(40, 110, "USAREUR-AF/first-bite", 15, True)
    f.text(40, 130, "public: the software", 13, cls="q")
    f.text(40, 148, "release v%s" % F["version"], 13, cls="q")
    f.box(300, 94, 196, 56, [("bite", 15, True, "t", True), ("the decoder", 13, False, "q")])
    f.box(520, 94, 196, 56, [("mind", 15, True, "t", True), ("capture and publish", 13, False, "q")])

    # the three relations across the gap
    oy = 228
    f.line([(150, oy), (150, 164)], "lna", head="fa")
    f.text(162, 190, "first-bite.ref pins", 13, True, "a", mono=False)
    f.text(162, 208, "commit %s (v%s)" % (short, F["version"]), 13, cls="q")
    f.text(408, 196, "make check", 13, mono=True)
    f.text(628, 196, "check.sh", 13, mono=True)

    # the overlay
    f.rect(24, oy, 712, 296, "bxa", 12)
    f.text(40, oy + 26, "first-bite-env: the overlay", 15, True, "a")
    f.text(40, oy + 46, "everything a deployment owns, none of the code", 13, cls="q")

    # dictionaries
    f.rect(40, 292, 428, 160, "bx", 10)
    f.text(56, 316, "dictionaries/", 13, True, mono=True)
    f.text(176, 316, "one per interface document", 13, cls="q")
    cw, gap = 190, 16
    for i, d in enumerate(F["dicts"][:2]):
        x = 56 + i * (cw + gap)
        f.rect(x, 330, cw, 108, "bxp", 8)
        f.text(x + 12, 354, d["name"], 14, True, mono=True, maxw=cw - 24)
        f.text(x + 12 + tw(d["name"], 14, True, True) + 8, 354, d["version"], 13, cls="q")
        f.text(x + 12, 374, "from %s rev %s" % (d["doc"], d["rev"]), 13, cls="q", maxw=cw - 24)
        rows, line = [], d["iface"] + ":"
        for m in d["msgs"]:
            t = line + " " + m + ("," if m != d["msgs"][-1] else "")
            if tw(t, 13) <= cw - 24:
                line = t
            else:
                rows.append(line)
                line = m + ("," if m != d["msgs"][-1] else "")
        rows.append(line)
        if len(rows) > 2:
            raise SystemExit("overlay: the messages of %s need more than two lines" % d["name"])
        for j, r in enumerate(rows):
            f.text(x + 12, 398 + j * 18, r, 13, maxw=cw - 24)

    # the site
    f.rect(484, 292, 236, 160, "bx", 10)
    f.text(500, 316, "deployments/", 13, True, mono=True)
    f.text(500, 338, F["site"], 14, True, mono=True)
    f.text(500, 358, "security: %s, TLS %s" % (F["transport"], F["min_tls"]), 13, cls="q", maxw=204)
    out = [("Cursor-on-Target", "to a TAK server"), ("records", "to an archive, HTTPS")]
    for j, (a, b) in enumerate(out):
        y = 384 + j * 40
        f.line([(500, y - 4), (514, y - 4)], "ln", head="fl")
        f.text(522, y, a, 13, True, maxw=190)
        f.text(522, y + 18, b, 13, cls="q", maxw=190)

    # bite checks the dictionaries, mind runs the site (drawn over the overlay's fill)
    f.line([(398, 150), (398, 292)], "ln", head="fl")
    f.line([(618, 150), (618, 292)], "ln", head="fl")

    # the gates
    f.rect(40, 464, 680, 44, "bxp", 8)
    f.rich(56, 491, [("On every pull request: ", True, "t"), (", ".join(F["workflows"]), False, "q")], 13,
           maxw=650)

    # your private copy
    f.line([(380, 524), (380, 558)], "lnd", head="fl")
    f.text(392, 546, "Use this template", 13, True)
    f.rect(24, 558, 712, 48, "bxd", 10)
    f.rich(40, 587, [("Your private overlay: ", True, "t"),
                     ("the same shape, your documents' dictionaries, your sites", False, "q")], 13, maxw=680)
    return f


FIGURES = [overlay]


def main():
    check = "--check" in sys.argv[1:]
    stale = []
    for make in FIGURES:
        fig = make()
        for theme in ("light", "dark"):
            path = os.path.join(HERE, "%s-%s.svg" % (fig.name, theme))
            svg = fig.render(theme)
            if check:
                if not os.path.exists(path) or read_text(path) != svg:
                    stale.append(os.path.basename(path))
            else:
                with open(path, "w", encoding="utf-8") as out:
                    out.write(svg)
    if check and stale:
        raise SystemExit("out of date, run python3 -I docs/figures/make-figures.py: " + ", ".join(stale))
    print(("checked" if check else "wrote") + " %d files" % (len(FIGURES) * 2))


if __name__ == "__main__":
    main()
