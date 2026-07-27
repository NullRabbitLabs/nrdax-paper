"""Generate the paper's figures from the committed data files.

Reproducible by construction and immune to the registry moving: the classification
comes from `data/classification.py` (this paper's own per-technique assignment) and
the corpus shape from the pinned snapshot. Both are committed, so a figure cannot
drift from the text and re-running this on a later registry state changes nothing.

Run:  python3 data/make_figures.py

Output is hand-written SVG (no plotting dependency) so the figures are vector,
diffable, and legible in print. Sequential magnitude uses one hue light-to-dark,
which also degrades correctly to greyscale for a printed copy.
"""
from __future__ import annotations
import json, sys, pathlib, collections

FAMILIES = ["memory_amp", "compute_amp", "fault_termination",
            "connection_exhaustion", "response_amp"]
BOUNDS = ["no-bound", "mis-quantified", "late", "mis-scoped", "absent-invariant"]
FAM_LABEL = {"memory_amp": "Retention", "compute_amp": "Computation",
             "fault_termination": "Termination",
             "connection_exhaustion": "Admission", "response_amp": "Egress"}
BOUND_LABEL = {"no-bound": "No bound", "mis-quantified": "Mis-quantified",
               "late": "Late", "mis-scoped": "Mis-scoped",
               "absent-invariant": "Absent invariant"}
# Sequential blue ramp, light->dark (validated steps 100..700).
RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
SURFACE, INK, MUTED, RULE = "#fcfcfb", "#0b0b0b", "#52514e", "#d8d7d2"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def shade(n: int, hi: int) -> str:
    """Light->dark by magnitude; empty cells stay on the surface."""
    if n == 0:
        return SURFACE
    frac = n / hi if hi else 0
    idx = min(len(RAMP) - 1, 1 + int(frac * (len(RAMP) - 2)))
    return RAMP[idx]


def fig_grid(techs, out: pathlib.Path) -> str:
    cur = [t for t in techs if t["classification"] == "curated"]
    cell = collections.Counter((t["family"], t["bound_failure"]) for t in cur)
    hi = max(cell.values())
    cw, ch, lx, ty = 132, 54, 132, 92
    W, H = lx + cw * len(BOUNDS) + 60, ty + ch * len(FAMILIES) + 74
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" font-family="Georgia,serif">',
         f'<rect width="{W}" height="{H}" fill="{SURFACE}"/>',
         f'<text x="0" y="22" font-size="15" font-weight="bold" fill="{INK}">'
         f'Figure 1. The mechanism grid: resource class by bound-failure mode</text>',
         f'<text x="0" y="42" font-size="11.5" fill="{MUTED}">'
         f'{len(cur)} classified techniques. A family is a ROW; a mechanism is a CELL. '
         f'Shading is cell population.</text>',
         f'<text x="0" y="58" font-size="11.5" fill="{MUTED}">'
         f'Empty cells are combinations the corpus has not reproduced, not combinations ruled out.</text>']
    for j, b in enumerate(BOUNDS):
        x = lx + j * cw + cw / 2
        p.append(f'<text x="{x:.0f}" y="{ty-12}" font-size="11" fill="{MUTED}" '
                 f'text-anchor="middle">{esc(BOUND_LABEL[b])}</text>')
    for i, f in enumerate(FAMILIES):
        y = ty + i * ch
        total = sum(v for (ff, _), v in cell.items() if ff == f)
        p.append(f'<text x="{lx-10}" y="{y+ch/2+4:.0f}" font-size="11.5" fill="{INK}" '
                 f'text-anchor="end">{esc(FAM_LABEL[f])} <tspan fill="{MUTED}">({total})</tspan></text>')
        for j, b in enumerate(BOUNDS):
            x, n = lx + j * cw, cell.get((f, b), 0)
            fill = shade(n, hi)
            # 2px surface gap between fills, per mark spec.
            p.append(f'<rect x="{x+1}" y="{y+1}" width="{cw-2}" height="{ch-2}" rx="4" '
                     f'fill="{fill}" stroke="{RULE}" stroke-width="1"/>')
            if n:
                tc = "#ffffff" if n / hi > 0.45 else INK
                p.append(f'<text x="{x+cw/2:.0f}" y="{y+ch/2+5:.0f}" font-size="14" '
                         f'font-weight="bold" fill="{tc}" text-anchor="middle">{n}</text>')
    yb = ty + ch * len(FAMILIES) + 30
    p.append(f'<text x="0" y="{yb}" font-size="11" fill="{MUTED}">'
             f'Termination occupies one cell by definition: a single input that faults the node '
             f'involves no accumulation,</text>')
    p.append(f'<text x="0" y="{yb+15}" font-size="11" fill="{MUTED}">'
             f'so no bound could have failed in any other way. The other four rows span modes as the corpus populates them.</text>')
    p.append("</svg>")
    out.write_text("\n".join(p))
    return f"grid: {len(cur)} techniques over {len(cell)} populated cells of 25"


def fig_hierarchy(techs, out: pathlib.Path) -> str:
    cur = [t for t in techs if t["classification"] == "curated"]
    inst = sum(len(t["instances"]) for t in cur)
    targets = len({i["chain"] for t in cur for i in t["instances"]})
    W, H = 760, 340
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Georgia,serif"><rect width="{W}" height="{H}" fill="{SURFACE}"/>',
         f'<text x="0" y="22" font-size="15" font-weight="bold" fill="{INK}">'
         f'Figure 2. Technique, instance, primitive</text>',
         f'<text x="0" y="42" font-size="11.5" fill="{MUTED}">'
         f'The three levels kept separate, and what each one carries.</text>']
    rows = [
        (72, "TECHNIQUE", f"{len(cur)} classified", "NRDAX-T0205",
         "The mechanism, stated without reference to any implementation.",
         "Carries the permanent identifier, the family and the bound-failure mode.", RAMP[4], "#ffffff"),
        (168, "INSTANCE", f"{inst} on classified techniques", "NRDAX-T0205 on Cosmos",
         f"One occurrence against one of {targets} targets, with fidelity and discovery origin.",
         "Where a CVE attaches, because a CVE is a property of an implementation.", RAMP[2], INK),
        (264, "PRIMITIVE", "the reproduction artefact", "cometbft_mconn_handshake_burn",
         "The executable reproduction and its captured evidence bundle.",
         "Also the key the lineage record uses, because it survives republication.", RAMP[0], INK),
    ]
    for y, title, count, example, l1, l2, fill, tc in rows:
        p.append(f'<rect x="0" y="{y}" width="188" height="76" rx="6" fill="{fill}" '
                 f'stroke="{RULE}"/>')
        p.append(f'<text x="94" y="{y+30}" font-size="13" font-weight="bold" fill="{tc}" '
                 f'text-anchor="middle">{title}</text>')
        p.append(f'<text x="94" y="{y+50}" font-size="10.5" fill="{tc}" '
                 f'text-anchor="middle" opacity="0.85">{esc(count)}</text>')
        p.append(f'<text x="206" y="{y+22}" font-size="11.5" fill="{INK}" '
                 f'font-family="monospace">{esc(example)}</text>')
        p.append(f'<text x="206" y="{y+42}" font-size="11" fill="{MUTED}">{esc(l1)}</text>')
        p.append(f'<text x="206" y="{y+60}" font-size="11" fill="{MUTED}">{esc(l2)}</text>')
    for y in (148, 244):
        p.append(f'<path d="M94 {y} L94 {y+20}" stroke="{MUTED}" stroke-width="2" '
                 f'marker-end="url(#a)"/>')
    p.append(f'<defs><marker id="a" markerWidth="8" markerHeight="8" refX="4" refY="4" '
             f'orient="auto"><path d="M1 1 L7 4 L1 7 z" fill="{MUTED}"/></marker></defs>')
    p.append(f'<text x="0" y="{H-14}" font-size="11" fill="{MUTED}">'
             f'Splitting the three is what lets one mechanism carry evidence from many targets '
             f'without collapsing into unrelated records.</text>')
    p.append("</svg>")
    out.write_text("\n".join(p))
    return f"hierarchy: {len(cur)} techniques, {inst} instances, {targets} targets"


def fig_pipeline(techs, out: pathlib.Path) -> str:
    allt = techs
    repro = [t for t in allt if t["instances"]]
    cur = [t for t in allt if t["classification"] == "curated"]
    oos = [t for t in allt if t.get("out_of_scope")]
    W, H = 900, 250
    steps = [("Candidate", f"{len(allt)} published", "advisory, source review,\nor a prior mechanism"),
             ("Reproduced", f"{len(repro)}", "delivered over the wire,\nevidence captured"),
             ("In scope", f"{len(repro)-len(oos and [t for t in oos if t['instances']])}",
              "network-boundary /\nnode-resource class"),
             ("Classified", f"{len(cur)}", "mechanism read off\nthe reproduction"),
             ("Published", f"{len(cur)}", "permanent id, JSON,\nSTIX, JSON-LD")]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Georgia,serif"><rect width="{W}" height="{H}" fill="{SURFACE}"/>',
         f'<text x="0" y="22" font-size="15" font-weight="bold" fill="{INK}">'
         f'Figure 3. How a technique enters the registry, and where the population falls away</text>',
         f'<text x="0" y="42" font-size="11.5" fill="{MUTED}">'
         f'Classification is gated on reproduction. The gate is one-directional: not every '
         f'reproduction is classified.</text>']
    bw, gap, y0 = 150, 34, 78
    for k, (title, n, sub) in enumerate(steps):
        x = k * (bw + gap)
        fill = RAMP[min(6, 1 + k)]
        tc = "#ffffff" if k >= 2 else INK
        p.append(f'<rect x="{x}" y="{y0}" width="{bw}" height="84" rx="6" fill="{fill}" stroke="{RULE}"/>')
        p.append(f'<text x="{x+bw/2}" y="{y0+26}" font-size="12" font-weight="bold" fill="{tc}" '
                 f'text-anchor="middle">{title}</text>')
        p.append(f'<text x="{x+bw/2}" y="{y0+56}" font-size="20" font-weight="bold" fill="{tc}" '
                 f'text-anchor="middle">{n}</text>')
        for li, line in enumerate(sub.split("\n")):
            p.append(f'<text x="{x+bw/2}" y="{y0+104+li*15}" font-size="10.5" fill="{MUTED}" '
                     f'text-anchor="middle">{esc(line)}</text>')
        if k < len(steps) - 1:
            p.append(f'<path d="M{x+bw+6} {y0+42} L{x+bw+gap-6} {y0+42}" stroke="{MUTED}" '
                     f'stroke-width="2" marker-end="url(#b)"/>')
    p.append(f'<defs><marker id="b" markerWidth="8" markerHeight="8" refX="4" refY="4" '
             f'orient="auto"><path d="M1 1 L7 4 L1 7 z" fill="{MUTED}"/></marker></defs>')
    p.append(f'<text x="0" y="{H-16}" font-size="11" fill="{MUTED}">'
             f'{len(allt)-len(repro)} techniques are recorded from a public advisory with no reproduction, '
             f'so no mechanism can be read and none is inferred.</text>')
    p.append("</svg>")
    out.write_text("\n".join(p))
    return f"pipeline: {len(allt)} -> {len(repro)} reproduced -> {len(cur)} classified"


def load() -> list[dict]:
    """Join the pinned snapshot with this paper's own classification assignment.

    The snapshot predates the classification migration, which is deliberate: it is
    the state the paper's numbers were verified against and it does not move. The
    assignment lives in classification.py and is equally fixed."""
    root = pathlib.Path(__file__).resolve().parent
    techs = json.loads((root / "registry-snapshot-2026-07-24.json").read_text())["techniques"]
    ns: dict = {}
    exec((root / "classification.py").read_text(), ns)
    assigned = {r[0]: r for r in ns["CLASSIFICATION"]}
    tombstoned = {r[0] for r in ns["TOMBSTONE"]}
    for t in techs:
        row = assigned.get(t["id"])
        t["classification"] = "curated" if row else "pending"
        t["family"] = row[1] if row else None
        t["surface"] = row[2] if row else None
        t["bound_failure"] = row[3] if row else None
        if t["id"] in tombstoned:
            t["out_of_scope"] = True
    return techs


def main() -> None:
    techs = load()
    figs = pathlib.Path("figures"); figs.mkdir(exist_ok=True)
    print(fig_grid(techs, figs / "fig1-mechanism-grid.svg"))
    print(fig_hierarchy(techs, figs / "fig2-identifier-hierarchy.svg"))
    print(fig_pipeline(techs, figs / "fig3-pipeline.svg"))


if __name__ == "__main__":
    main()
