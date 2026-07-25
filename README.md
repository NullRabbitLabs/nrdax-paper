# NRDAX taxonomy paper

A mechanism-defined taxonomy for network-boundary and node-resource attacks on decentralised infrastructure. Target venue: arXiv cs.CR.

Start at [`paper.md`](paper.md) for the abstract and contents; sections are in [`sections/`](sections/).

## Verifying the figures

Every number in the paper is read from the live registry and can be re-read there. The paper does not rely on any figure that a reader cannot check:

```
curl 'https://api.nrdax.com/v1/techniques?limit=500'
curl 'https://api.nrdax.com/v1/aadapt?limit=500'
```

Classified techniques are those with `classification: "curated"`. The mechanism family is `family`; the producing pipeline's own operational label is `producer_family`. The two are never merged.

`data/` holds the per-technique mechanism assignment behind section 3 (`classification.py`, `mechanism-audit.csv`) and the registry snapshot the figures were computed from (`registry-snapshot-2026-07-24.json`), so a reader who disagrees with an assignment can raise it against a specific identifier.

## Status

Working draft, 2026-07-24, against registry version v0.2.

The classification described in section 3 is live: the registry serves it, and the reclassification reported in section 3.7 (40 techniques moved, 22 into a new family, 14 tombstoned) was applied before this draft was written, so the paper and the registry agree.

## Related work by the same authors

The substrate paper reports a machine-learning methodology for detecting attacks in this class, whose central cross-chain transfer claim was **falsified** at its pre-registered evaluation gate. This paper makes no detection claim and does not revise that result. See section 8.9.
