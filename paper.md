# NRDAX: a mechanism-defined taxonomy for network-boundary and node-resource attacks on decentralised infrastructure

**Author**: Simon Morley, NullRabbit

**Status**: working draft, 2026-07-24

**Registry version**: v0.2, read 2026-07-24

---

# Abstract

Node implementations of decentralised protocols face a class of attack that is well documented case by case and unclassified as a class: a small or malformed input from an unauthenticated peer forcing disproportionate consumption of memory, CPU, admission capacity or egress bandwidth, or an unrecoverable fault. Pre-authentication cryptographic burn, protocol-frame exhaustion, mempool abuse, response amplification, one-packet panics. Existing frameworks do not cover it. MITRE ATT&CK offers five values for the entire outcome, at the layer of organisational impact. MITRE AADAPT covers the adjacent digital-asset domain and, on the crosswalk we publish and measure, shares **zero techniques with our mechanism-classified corpus**. The survey literature, including the nearest DoS-specific taxonomy, organises by architectural layer and concentrates on the contract and consensus layers, which this class sits below. CVE identifies implementations; CWE classifies defects. The mechanism, which is the only level at which a finding against one implementation says anything about the next, is indexed nowhere.

We present NRDAX, a chain-agnostic registry that classifies by mechanism, where a mechanism is a pair: **the resource the node spends disproportionately, and the way its bound on that resource failed to apply**. The two axes are not symmetric in how they are used: the five resource classes name the families and the five bound-failure modes are a second attribute within them, so a family is a row of the 5x5 grid and a mechanism is a cell. The family is the navigation unit; the cell is what predicts exposure elsewhere, and the recurrence results below are cell-level. Each bound-failure mode carries a concrete audit question that transfers to a codebase never examined. The distinction from symptom-based grouping is measurable rather than rhetorical: applying these criteria to 97 reproduced techniques previously published under a 13-label scheme moved 40 of them. Twenty-two shared a mechanism the old vocabulary had no name for, scattered across seven labels; six labels turned out not to be mechanisms at all, three naming an entry surface and three a bypassed guard; and fourteen records fell outside the class entirely and were tombstoned. That reclassification is live, so every figure in this paper can be checked against the running registry.

Classification is gated on reproduction, though the gate is one-directional: of 420 published techniques 118 carry a reproduced instance and only 97 carry a mechanism family. Those 97 rest on 199 instances across 37 targets; the wider reproduced set of 118 reaches 38, the extra one being IPFS on a technique we tombstoned. Of the 21 reproduced techniques without a family, 14 are tombstoned as out of class and 7 are simply not classified yet.

The 323 techniques with no mechanism family are served `family: null` with an explicit state and no inferred value, and they are not one population: 285 are known but never reproduced, 31 are tombstoned as outside the class, and 7 are reproduced, in scope and unassigned. Only the last two groups can be read as work outstanding, and only the 7 as work we could do today - a tombstoned technique will never carry a mechanism family, because it is outside what the taxonomy classifies. Identifiers are opaque, stable and never reused, with family as an attribute rather than a component, which is what allowed 40 techniques to change family without breaking a citation. The registry is served as JSON, STIX 2.1 and JSON-LD, designed to be ingested rather than read.

As evidence that the classification does work, sixteen mechanisms recur across independently written chain implementations with no shared library in the instance set; `NRDAX-T0100` has reproduced instances against nine separate chains and no shared substrate at all (`NRDAX-T0205`, the next widest, also reaches nine targets, but one of those is libp2p and so counts as eight chains), and a single mechanism cell - (`compute_amp`, `late`) - accounts for exposure across eighteen targets - a grouping that was invisible before the reclassification, because its six members sat in four different families.

We state the limits directly. The corpus is lab fidelity (198 of 199 instances); nothing here is evidence about production impact. Seventy-four per cent of classified techniques are reproductions of publicly disclosed CVEs rather than discoveries. Coverage is uneven enough that an empty cell in the coverage matrix means "not examined" far more often than "not exposed", which confounds the recurrence result in the flattering direction, so we report recurrence as an existence claim and not a rate. The classification is one team's judgement with no external review or inter-rater measurement, and thirteen techniques could not be resolved to a single family. No detection capability is claimed: companion work applying machine learning to this class reported its central cross-chain transfer claim as falsified at a pre-registered gate, and that negative result stands unrevised.

---

## Contents

1. [Introduction](sections/01-introduction.md)
2. [Scope and definitions](sections/02-scope.md)
3. [The classification](sections/03-classification.md)
4. [Identifiers and structure](sections/04-identifiers.md)
5. [Corpus and method](sections/05-corpus.md)
6. [Evaluation](sections/06-evaluation.md)
7. [Related work and positioning](sections/07-related-work.md)
8. [Limitations](sections/08-limitations.md)
9. [Availability](sections/09-availability.md)

References: [bibliography.bib](bibliography.bib)

Supporting data: [`data/`](data/) - the per-technique mechanism assignment (`mechanism-audit.csv`, `classification.py`) and the registry snapshot the figures were computed from (`registry-snapshot-2026-07-24.json`).

---

## Reproducing the figures

Every number in this paper derives from two requests against the live registry:

```
curl 'https://api.nrdax.com/v1/techniques?limit=500'
curl 'https://api.nrdax.com/v1/aadapt?limit=500'
```

Classified techniques are those with `classification: "curated"`. The mechanism family is `family`; the producing pipeline's own label is `producer_family`; the two are never merged. Section 9.3 gives the details, including the chain-versus-substrate split used in section 6.
