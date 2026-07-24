# 4. Identifiers and structure

A taxonomy that cannot be cited is a document. What makes NRDAX a
registry is that each unit has a permanent identifier, a stable
URL, and a machine representation, and that the design decides in
advance which properties of a technique may change and which may
not.

## 4.1 NRDAX-T as a permanent identifier

Identifiers have the form `NRDAX-Tnnnn`. Four properties are
enforced:

**Opaque.** The identifier encodes nothing. It does not encode the
family, the chain, the year, or the severity. This is the property
that made the reclassification in section 3.7 possible: 40 of 97
techniques changed family and not one citation broke, because no
citation ever depended on the family.

**Stable.** An identifier never changes meaning. `NRDAX-T0205` is
the same mechanism it was on the day it was minted.

**Never reused.** A retired identifier is not reassigned. The
registry enforces increment-only: a published entry is never
edited into a different technique and never deleted. A technique
that leaves scope is tombstoned, retained and flagged, so the
identifier keeps resolving; 31 identifiers are in that state.

**Resolvable.** Every identifier resolves at
`https://nrdax.com/techniques/<id>` for a reader and at
`https://api.nrdax.com/v1/techniques/<id>` for a machine, and both
work for tombstoned identifiers.

The consequence worth stating for a citing author: **family is an
attribute, not part of identity.** Cite `NRDAX-T0100` and the
citation survives the technique moving from `connection_exhaustion`
to `compute_amp`, which it did. Cite "the connection-exhaustion
technique in NRDAX" and it does not.

## 4.2 Technique, primitive, instance

Three levels, often conflated in vulnerability catalogues, kept
separate here.

A **technique** is the mechanism, stated independently of any
implementation: *an unauthenticated peer forces asymmetric
public-key work before admission control*. It is what carries the
identifier and what the taxonomy classifies. It has no chain, no
version and no CVE of its own.

An **instance** is that mechanism realised against one target:
`NRDAX-T0205` on Bitcoin, on Cosmos, on XRP, on libp2p, and on
five more. Each instance records its target, its fidelity, its
discovery origin, and any external references specific to it. An
instance is where a CVE attaches, because CVEs are assigned to
implementations, not to mechanisms.

A **primitive** is the executable artefact that produced an
instance: the reproduction itself, identified by
`primitive_id` and a `bundle_ref` pointing at its captured
evidence. Primitives are the layer below publication, produced by
a separate pipeline; the registry references them so a claim can
be traced to what produced it.

The three-level split is what lets one mechanism carry evidence
from nine implementations without collapsing into nine unrelated
records, and it is what section 6's argument rests on. It also
explains an asymmetry a reader will notice: 97 techniques carry
199 instances, so most techniques have one or two and a few have
many.

## 4.3 Reproduced versus known

The registry holds 420 published techniques. Ninety-seven have at
least one reproduced instance. Three hundred and twenty-three do
not: they are recorded from a public advisory naming a defect in a
node implementation, with no reproduction on file.

The distinction is not presentational. It governs three things.

**What may be claimed.** A known technique asserts that an
advisory exists. A reproduced technique asserts that the mechanism
was observed to work in a controlled environment, with captured
evidence.

**Whether it may be classified.** Only reproduced techniques carry
a mechanism family. What a technique exhausts, and which bound
failed, are read off the reproduction; an advisory frequently
states the symptom and the fix without stating either. The
registry enforces this at the write boundary: a classification for
a technique with no instance fails the build. A known technique is
served `family: null` with `classification: "pending"`.

**How the gap is reported.** The 323 are counted and published as
a number (`unclassified` on the families endpoint), not filled in
by inference from the producing pipeline's coarse labels. Such a
map would be mechanical, and for the surface-defined labels it
would be silently wrong - which is the failure section 3.7
describes. The registry states the gap rather than closing it
plausibly.

We regard the ratio as the honest current state of the corpus, not
as a target that has been met. Section 8 returns to it.

## 4.4 Machine surfaces

The registry is designed to be **ingested, not read**. A human
dashboard exists, but the primary consumers we design for are
scanners, agents, and survey tooling that needs the corpus as
data. Every surface below serves the same underlying snapshot, and
a contract test suite pins the response shape per endpoint so they
cannot drift apart.

**JSON API** at `https://api.nrdax.com/v1`, described by an
OpenAPI 3.1 document generated from the serving code at
`/v1/openapi.json` and `/v1/openapi.yaml`, with interactive
documentation at `/v1/docs`. Generated rather than hand-written,
and drift-guarded by a test, so the description cannot fall behind
the implementation. Read endpoints are unauthenticated.

**Static feed, emitted but not yet published.** The registry has an
emitter producing `registry.jsonl` (one technique per line, stable
order), per-technique JSON keyed on the identifier,
`families.json`, and `coverage-matrix.json`. These are byte-for-
byte deterministic and golden-tested: the same registry state
always emits the same bytes, so a consumer could diff two
snapshots and see only real change.

We state plainly that **these artefacts are not currently served at
a public URL.** The emitter runs as part of the publish path, and
a bulk consumer today must page the JSON API rather than fetch a
snapshot file. Hosting them is straightforward and has not been
done; section 8 counts it as a limitation rather than section 9 as
an availability.

**STIX 2.1.** Each technique is an `attack-pattern` carrying its
identifier as an external reference and the classification as
extension properties (`x_nrdax_family`, `x_nrdax_surface`,
`x_nrdax_bound_failure`, `x_nrdax_producer_family`,
`x_nrdax_classification`). Available by content negotiation
(`Accept: application/stix+json`) or `?format=stix`. This is the
surface for existing threat-intelligence pipelines.

**JSON-LD.** A single self-contained `@graph` at
`/v1/knowledge-pack.jsonld` for one-fetch agent ingestion, with
the family taxonomy as a `DefinedTermSet` and each technique as a
`DefinedTerm`. A pending technique states `classification:
"pending"` explicitly rather than omitting the property, so an
ingesting agent cannot mistake an absent classification for an
assertion about the mechanism.

**Client library.** `nrdax` on PyPI, a client and CLI over the
same API. It ships code only and fetches the dataset explicitly;
no snapshot is bundled into the package, so a consumer's data is
never silently stale.

Two design decisions are worth stating because they are not the
obvious ones.

*The gap is a first-class value.* Every machine surface carries
the pending state and the unclassified count. A consumer that
wants only classified techniques filters on it; a consumer that
wants to know how much of the corpus is unclassified is told,
rather than having to derive it.

*Both taxonomy axes are served, on separate keys.* `family` is the
published mechanism taxonomy; `producer_family` is the producing
pipeline's own clustering label, retained for provenance. They are
never merged, because a name like `memory_amp` means one thing on
each axis and the counts differ.

## 4.5 Versioning and citation

The registry carries a version identifier, currently **v0.2**, and
every API response includes it alongside the results, so a
retrieved result set can be pinned to the state that produced it.
Releases are increment-only.

**No DOI has been minted.** Entry pages carry a cite block with
the version and the resolvable URL, and that is the citation we
can currently support. A DOI-backed archival deposit is the
appropriate next step and has not been done; section 8 lists it
among the limitations rather than section 9 among the
availabilities. We note it here because "permanent identifier"
and "archivally deposited" are different guarantees, and this
registry currently provides the first and not the second.
