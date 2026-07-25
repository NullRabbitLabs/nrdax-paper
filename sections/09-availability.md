# 9. Availability

Every URL below was checked on 2026-07-24. Figures quoted in this paper are from the registry as served on that date, at registry version **v0.2**.

## 9.1 The registry

| | |
|---|---|
| Human dashboard | `https://nrdax.com` |
| Technique page | `https://nrdax.com/techniques/<NRDAX-Tnnnn>` |
| Families | `https://nrdax.com/families` |
| Read API | `https://api.nrdax.com/v1` |
| Technique record | `https://api.nrdax.com/v1/techniques/<NRDAX-Tnnnn>` |

Read access is unauthenticated. Public submission of candidate techniques and instances is also unauthenticated, into a quarantined review queue; the only authenticated boundary is admin review and promotion.

## 9.2 Machine surfaces

| Surface | Endpoint |
|---|---|
| Technique list, filterable and paginated | `/v1/techniques` |
| Family taxonomy, both axes, with the pending count | `/v1/families` |
| Instances | `/v1/instances` |
| Coverage matrix (technique × target) | `/v1/coverage` |
| Search | `/v1/search?q=` |
| MITRE AADAPT crosswalk | `/v1/aadapt` |
| Lookup by CVE or advisory id | `/v1/cve/<reference>` |
| STIX 2.1 bundle | `/v1/techniques?format=stix` |
| JSON-LD knowledge pack | `/v1/knowledge-pack.jsonld` |
| Atom feed of new techniques | `/v1/feed.xml` |
| OpenAPI 3.1 description | `/v1/openapi.json`, `/v1/openapi.yaml` |
| Interactive API documentation | `/v1/docs` |

The OpenAPI document is generated from the serving code and guarded against drift by a test, so it describes the API that is actually running.

STIX is also available by content negotiation with `Accept: application/stix+json`.

## 9.3 Reproducing the figures in this paper

The section 3 population counts, section 5 provenance and fidelity tables, section 6 recurrence analysis and section 7 crosswalk result are all derivable from two requests:

```
curl 'https://api.nrdax.com/v1/techniques?limit=500'
curl 'https://api.nrdax.com/v1/aadapt?limit=500'
```

Classified techniques are those with `classification: "curated"`. Note that this is a narrower set than "reproduced": 118 techniques carry at least one instance, 104 of those are in scope (the figure the public dashboard shows as "reproduced"), and 97 of those carry a mechanism family. Section 4.3 reconciles the three counts. The mechanism family is `family`, the producing pipeline's own label is `producer_family`, and the two are never merged. The section 6 chain-versus-substrate split treats `quic`, `http2`, `http3`, `libp2p` and `ipfs` as shared substrates and every other target as an independent chain implementation.

The per-technique mechanism assignment underlying section 3, including the notes recording why a technique was moved from its producer label, is published with this paper as `data/mechanism-audit.csv` and `data/classification.py`, alongside the registry snapshot the figures were computed from (`data/registry-snapshot-2026-07-24.json`). A reader disagreeing with a specific assignment can raise it against an identifier.

## 9.4 Client library

`nrdax` on PyPI: `https://pypi.org/project/nrdax/`

A Python client and CLI over the same API. It ships code only and fetches the dataset explicitly; no snapshot is bundled into the package, so a consumer's data cannot be silently stale. Usage documentation is at `https://nrdax.com/cli`.

## 9.5 Research briefs

Twelve techniques carry `nr-brief` references to long-form write-ups at `https://nullrabbit.ai/research/<slug>`, backlinked from the technique record. These give the reproduction detail that the registry's one-paragraph mechanism field cannot.

The instrumentation analysis motivating section 2.3 is at `https://nullrabbit.ai/research/why-syscall-tooling-cannot-see-p2p-infrastructure`.

## 9.6 What is not available

Stated here so the section is not read as a fuller offer than it is.

**No DOI.** No archival deposit has been made. Citations can pin a registry version and a resolvable URL, but not an immutable artefact independent of the serving infrastructure.

**No public static feed.** `registry.jsonl`, per-technique JSON files, `families.json` and `coverage-matrix.json` are emitted and golden-tested but are not served at a public URL. Bulk consumers must page the API.

**No reproduction bundles.** Instances reference the artefacts that produced them by `bundle_ref`, and those artefacts are not published. A reader can see that a reproduction exists and what it recorded; they cannot re-run it. This is the most significant gap in the availability story, and it is why section 8.8 records that no instance in the corpus has been independently replicated.

**License.** Registry data is published under CC-BY-4.0, stated in the STIX export as an object marking on every object.
