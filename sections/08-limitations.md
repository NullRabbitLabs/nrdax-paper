# 8. Limitations

Every figure below is from the live registry on 2026-07-24 and can be checked there. We have tried to state each limitation at the strength it actually has, rather than in the softened form that would be easier to publish.

## 8.1 The corpus is lab fidelity, not production

Of 199 instances on classified techniques, **198 are `lab` and one is `proxy`. None is production-captured or production-derived.**

A lab instance means the attack was delivered over a real network stack against a real build of the target software in a controlled environment, and the effect was observed and captured. It does not mean a deployed operator of that software is exposed. Production deployments sit behind rate limiters, load balancers, peer reputation systems, connection caps set by operators, and sometimes CDN or DDoS-mitigation frontends, none of which the corpus models. They also carry real peer populations and background contention, which can make a mechanism either harder or easier to exercise than the lab suggests.

The fidelity scale exists precisely because this distinction matters, and the corpus currently occupies one point on it. No claim in this paper about a mechanism "working" should be read as a claim about production impact.

## 8.2 Three quarters of the classified corpus reproduces public CVEs

Per technique, taking all its instances together: **72 of 97 classified techniques are reverse-engineered from public CVEs only**, 14 are original research only, and 11 are mixed.

These 72 are not discoveries. The defect was already public, with a CVE, GHSA or vendor advisory, and generally with a patch. What this work added is a reproduction, captured evidence, a mechanism reading and a place in a structured index. That is a real contribution to a registry and it is a different contribution from finding the vulnerability, and the paper's value should be assessed on the former.

This also constrains what the corpus can be evidence *about*. It is, in substantial part, a re-indexing of the public advisory record for this class, and it therefore inherits that record's biases: toward implementations with active security programmes, toward defects severe enough to warrant a CVE, and toward projects with the resources to run disclosure processes.

## 8.3 Coverage is uneven, and empty cells mean "not examined"

The 199 instances are distributed across 37 targets, but not evenly: the top five (Ethereum, QUIC, Bitcoin, Cosmos, libp2p) hold **102 of 199**, and **18 of the 37 targets carry exactly one instance**.

The practical consequence is stated in section 6.2 and repeated here because it is the most likely way for this registry to be misread: **an empty cell in the coverage matrix is overwhelmingly "we did not look", not "not exposed".** Nobody should infer that an implementation is safe from a mechanism because the matrix has no cell for it.

The same skew confounds section 6's recurrence result in the flattering direction. Multi-target techniques are largely techniques that were *pursued* across targets. We therefore report recurrence as an existence result (23 mechanisms demonstrably recur across more than one chain deployment) and explicitly decline to report a rate. Section 8.4 covers the separate and larger problem that a chain deployment is not an independent implementation.

Two surfaces are effectively unexamined: `sync-state-import` and `control-plane` carry one classified technique each. Their populations say nothing about their exposure.

## 8.4 The registry records no implementation lineage, so recurrence is overstated by construction

An instance records a chain, a primitive id, a bundle reference, a fidelity and a discovery origin. It does **not** record which networking stack the target embeds, and nothing in the schema distinguishes a chain that vendors libp2p from one that wrote its own transport.

The consequence runs through section 6. Counting distinct chains as distinct implementations inflates every recurrence figure by an unknown factor, because a chain reaching a shared library through a dependency is recorded under its own name. Section 6.1.2 works the single case where the primitive naming happens to make the lineage legible: `NRDAX-T0100`'s nine chain deployments are four handshake stacks, three of them sharing go-ethereum's RLPx and four sharing libp2p's Noise. Earlier drafts of this paper presented those nine as nine independent implementations. They are not, and a reviewer familiar with the ecosystem would have seen it at once.

We have corrected the headline case and cannot correct the corpus: for most techniques the primitive identifiers name no stack, so the analysis is not repeatable without new data. The reported figure of 16 techniques recurring "with no shared substrate recorded as a target" is therefore a statement about the target field and not about implementation independence, and section 6.1.1 now says so in those words.

Adding a lineage field to the instance schema is the remedy, and it is specified rather than merely gestured at: the instance records which stack it exercised, a separate curated table groups stacks that share the relevant code, and the independence count is derived from the two. Where lineage is unknown the derived figure is published as a lower bound with an upper bound beside it, so an unknown can never read as independence. The bootstrap is partial - 75 of 226 instances carry a primitive identifier naming a stack, and those are proposals requiring confirmation, not answers.

It is not built. Until it is, no recurrence count in this registry should be read as an independent-implementation count.

## 8.5 Most of the registry is unclassified, and 232 records have no reference

Of 420 published techniques, **97 carry a mechanism family and 323 do not**. The taxonomy this paper presents covers 23% of the registry.

Most of that gap is want of evidence: 302 of the 323 have no reproduced instance, so there is no mechanism to read. But **7 of them do have a reproduced instance, are in scope, and are simply not classified yet** (`NRDAX-T0009`, `NRDAX-T0096`, `NRDAX-T0110`, `NRDAX-T0111`, `NRDAX-T0332`, `NRDAX-T0338`, `NRDAX-T0381`). They arrived carrying one of the producing pipeline's coarse class labels rather than a fine-grained one, so they fell outside the slice the reclassification examined. That is an oversight in our procedure rather than a limit on the evidence, and it is the one gap in this paper that could be closed immediately.

A reviewer will ask why it was not. The reason is that every figure in this paper is read from a single registry state, 2026-07-24 at version v0.2, and stated so that it can be re-read there. Classifying the 7 mid-draft would have moved the counts in sections 3, 5 and 6 away from anything a reader could verify, for a gain of seven techniques. We would rather publish a checkable 97 with a named gap than an unverifiable 104. The 7 are the first item of work after this draft, and the identifiers are listed so that anyone can confirm the gap has closed.

Separately, **232 of 420 techniques carry no external reference at all**. That gap is heavily concentrated in the unreproduced slice: 215 of the 323 pending techniques have no reference, against 17 of the 97 classified ones. A known-but-not-reproduced technique with no reference on file is a weak record - it asserts that a defect exists without a resolvable pointer to the disclosure that motivated it - and there are a lot of them.

We report the unclassified count rather than closing it by mapping the producing pipeline's coarse labels onto mechanism families, because that map would be mechanical and, for the surface-defined labels, silently wrong. But "we declined to guess" is not the same as "we know", and a reader should treat the 323 as unindexed rather than as classified-elsewhere.

## 8.6 The `first_seen` field will not support a temporal claim

**330 of 420 techniques carry a January-1 date**, and 191 carry exactly `2020-01-01`. These are placeholders from the import path, not disclosure dates.

The problem is much smaller on the classified slice (16 of 97), but registry-wide the field is not fit for temporal analysis. No claim in this paper depends on it, and we state the defect explicitly rather than quietly avoiding the subject, because a reviewer querying the API finds it in a minute. Anyone wanting a timeline for this class should use the CVE and GHSA references, which carry real dates, and not the registry's own `first_seen`.

One consequence is worth stating because it touches a machine surface the paper advertises. The Atom feed at `/v1/feed.xml` orders on `first_seen` descending. Its head is sound: recently added techniques carry real dates, and none of the newest 25 entries is a placeholder, so a subscriber watching for new techniques sees an accurate sequence. The placeholders sit in the tail, where they collapse a decade of disclosures onto a handful of January-1 dates. The feed is therefore reliable for "what is new" and unreliable as a chronology, which is the same caveat as the field itself.

## 8.7 The classification is one team's judgement, unreviewed

The mechanism assignments in section 3 were made by the same team that produced the reproductions, reading each technique's own recorded mechanism text. There has been **no external review, no second-rater exercise, and no inter-rater agreement measurement.**

This matters more than it would for a purely descriptive catalogue, because section 3 argues that the boundaries between families are principled. That argument is currently supported by a written assignment procedure (section 3.4) and by the corpus being consistent with it, but consistency with a procedure applied by its own authors is weak evidence that the procedure is reproducible. A second rater applying section 3.4 to the same 97 techniques could disagree materially, and we do not know by how much.

The obvious next step is exactly that exercise, and it has not been done. We publish the full per-technique assignment with the corpus so that a disagreement can be raised against a specific identifier rather than against the scheme in general.

Related, and honestly a symptom of the same thing: **13 of the 97 techniques could not be resolved to a single family** and carry a dual marking, because no reproduction measured which resource binds first. Rule 7 of the assignment procedure records the tie rather than breaking it, which we believe is the right choice, but 13% unresolved is a real rate.

## 8.8 Five families may be the wrong number

The taxonomy has five mechanism families over 97 techniques. Section 3.7 reports that this replaced a 13-label scheme that mixed three axes, and the reduction is a genuine improvement in coherence. It is not evidence that five is right.

Two specific risks. First, `memory_amp` holds 33 techniques, a third of the corpus, and a family that large is a candidate for being under-discriminated: the retention mechanisms behind a pre-allocating length prefix and a flow-control accounting leak may deserve separation. Second, `response_amp` holds five, and a family that small has not been tested against enough cases for its boundary to have been probed.

A corpus five times the size would very likely need more families, and the honest expectation is that this taxonomy will need revision rather than extension. The identifier design makes that cheap (section 4.1) and the migration reported in section 3.7 is a demonstration that it can be done without breaking citations, but the reader should expect it to happen.

## 8.9 No DOI, and a single-team, single-pipeline provenance

**No DOI has been minted.** The registry is versioned (v0.2) and every identifier resolves, but there is no archival deposit, so a citation cannot currently be pinned to an immutable artefact independent of the serving infrastructure. Entry pages carry a cite block with the version and URL, which is weaker than what a citing author should ideally have.

The static feed artefacts described in section 4.4 (`registry.jsonl`, per-technique JSON files, `families.json`, `coverage-matrix.json`) are emitted and golden-tested but **are not served at a public URL**. A consumer wanting the whole corpus must page the JSON API. That is a gap in the "designed to be ingested" claim, and it compounds the missing DOI: there is currently no single immutable file a citation can point at.

All reproductions come from one pipeline operated by one team. There is no independent replication of any instance in the corpus. The determinism guarantees in section 5.5 mean a reader can verify that the registry consistently reports what it reports; they do not mean anyone outside this team has verified that a reproduction does what its bundle says.

## 8.10 No detection capability is claimed

This paper makes no claim that attacks in this class can be reliably detected, and nothing in it should be cited as evidence that they can.

A companion line of work applied machine learning to detecting attacks in this class and reported its central cross-chain mechanism-transfer claim as **falsified** at a pre-registered evaluation gate. That negative result stands and is published. This paper does not revise it, weaken it, or route around it.

The relationship between the two is worth stating plainly, because it would be easy to imply a stronger one. A mechanism-defined taxonomy is a prerequisite for asking well-posed detection questions - it gives you a label set whose members are supposed to share observable structure. It is not a demonstration that detectors built on that label set work. On current evidence, one did not.

## 8.11 Scope boundaries are judgement calls at the margin

Section 2.2's exclusions are firm in the centre and negotiable at the edge. The 14 techniques tombstoned in section 3.7 were reproduced, published node-implementation defects that we subsequently judged out of class; another team could reasonably have kept several. `NRDAX-T0411` (a SIGHASH_SINGLE validation gap) is a defect in a node implementation reachable by a remote party, and we excluded it because its harm is consensus divergence rather than node loss. That is a defensible line and it is a line, not a fact.

Tombstoning rather than deleting is our mitigation: the records remain resolvable and flagged, so a reader who disagrees with the boundary can still find and use them, and the AADAPT crosswalk points at where they belong if not here.
