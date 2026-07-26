# 1. Introduction

A node implementation of a decentralised protocol is an unusual piece of software to have to defend. It is required to accept connections from anonymous, unauthenticated peers; to parse attacker-controlled structures before it can decide whether the sender is worth talking to; and to do all of this continuously, because being reachable is what participation means. The attack surface is not a deployment mistake. It is the design.

The consequences accumulate steadily in the public record. A length prefix that pre-allocates a receive buffer before the body arrives (CVE-2015-3641 \cite{cve-2015-3641}). An un-rate-limited `getheaders` handler which, in our reproduction, drove more than 100 MB/s of upload (CVE-2023-33297 \cite{cve-2023-33297}). An empty Bloom filter reaching a modulo in a hash function (CVE-2013-5700 \cite{cve-2013-5700}). Connection identifiers accumulating in an unbounded map on an established QUIC connection (CVE-2024-22189 \cite{cve-2024-22189}). An `addr` flood overflowing a 32-bit counter into an assertion abort (CVE-2024-52919 \cite{cve-2024-52919}). Each is catalogued against the project it was found in, patched, and filed.

Read as a list of advisories, those are five unrelated bugs in five codebases. Read as mechanisms, the first and fourth are the same failure - an attacker-controlled quantity accumulating against no bound - reached through different protocol features, and the third and fifth are the same failure as each other: a single input violating an assumption the code never checked, with the node process as the cost.

That second reading is the one that generalises, and there is currently no shared vocabulary in which to write it down.

## 1.1 The gap

The class we mean is specific: **network-boundary and node-resource attacks against node implementations**. A small or malformed input from an unauthenticated peer forcing disproportionate consumption of memory, CPU, admission capacity or egress bandwidth, or an unrecoverable fault. Pre-authentication cryptographic burn, protocol-frame exhaustion, mempool and pool abuse, response amplification, one-packet panics. Section 2 defines the boundary and, as importantly, what falls outside it.

This class is systematically under-classified, and not for lack of frameworks. It falls between them.

MITRE ATT&CK models adversary behaviour against enterprise environments, and its entire vocabulary for this outcome is *Endpoint Denial of Service* (T1499) with four sub-techniques. Every technique in our corpus would land in one of two of them, which tells a defender nothing about what to look for in their code. (Unlike the AADAPT result below, this one is an argument from ATT&CK's granularity rather than a published crosswalk: we have not built an ATT&CK mapping.)

MITRE AADAPT models digital asset systems and does so well, but its centre is smart contracts, consensus logic and cryptographic protocol weaknesses. We built the crosswalk and measured it: of the 97 mechanism-classified techniques in our registry, **zero map to any AADAPT technique**. Twenty-seven records do map, and not one of them is classified: 16 we have tombstoned as outside our own scope, and the other 11 are unreproduced.

The blockchain security survey literature is substantial and organises by layer and target. The nearest prior work, a hierarchical analysis of DoS attacks in blockchain systems, concentrates on the contract and consensus layers - which are the two layers this class sits below.

CVE identifies the vulnerability in the product version, correctly and usefully, and has no representation for "the same mechanism, in another implementation". CWE classifies the defect, which is a different object from the attack that reaches it: CWE-129 behind an authenticated admin interface and CWE-129 reachable by one packet from any peer are the same weakness and not remotely the same problem.

So the symptom is catalogued per project, the defect is catalogued per weakness class, and the mechanism - the thing that recurs, and the only level at which a finding against one implementation says anything about the next - is catalogued nowhere.

## 1.2 Contributions

1. **A model of mechanism as a pair.** We define an attack in this class by the
   resource the node spends disproportionately and the way its bound on that
   resource failed to apply. Neither half alone is predictive: the resource is
   the symptom and the bound failure is the defect class CWE already indexes.
   Section 3.2, with the derivation and its limits in section 3.2.5.

2. **A classification over that model.** Five resource classes name the
   families, five bound-failure modes are recorded within them, and a mechanism
   is a cell of the resulting grid rather than a family. Eleven of the twenty-five
   cells are populated. Each bound-failure mode states an audit question phrased
   to be askable of a codebase we have not examined. Section 3.3.

3. **Its application to a real corpus, reported with what it got wrong.**
   Applied to 97 reproduced techniques previously published under a thirteen-label
   scheme, it moved 40 of them: 22 into a mechanism the old vocabulary could not
   name, 6 out of surface-defined families, 2 out of guard-defined ones, 1 out of
   a surface-qualified singleton, and 9 corrected within the resource axis.
   Fourteen further records proved to be outside the declared class and were
   tombstoned. Section 3.7.

4. **An identifier scheme in which family is an attribute.** `NRDAX-Tnnnn` is
   opaque, stable and never reused, and the classification rides alongside the
   technique rather than inside its identity. That is what let 40 techniques
   change family without breaking a citation. Section 4.

5. **A registry, a crosswalk and the datasets behind both.** The corpus is served
   as JSON, STIX 2.1 and JSON-LD with an OpenAPI description generated from the
   serving code; a MITRE AADAPT crosswalk pinned to an immutable source revision
   is published as data, and shares zero techniques with the classified corpus.
   The per-technique assignment and the registry snapshot every figure was
   computed from ship with this paper. Sections 4.4, 7.2 and 9.

We state the limits of each in section 1.3 and at length in section 8. In
particular, contribution 2's audit questions are demonstrated to transfer in two
cases and are not established as a general property, and contribution 3 is one
team's unreviewed judgement.

**Scale and evidence.** Of 421 published techniques, 118 carry a reproduced instance and 97 carry a mechanism family; the 21-technique difference is 14 tombstoned as out of class and 7 reproduced but not yet classified (section 4.3). The 97 rest on 199 instances across 37 targets. The 324 without a family are served with an explicit `pending` state and no inferred value, because the alternative - mapping coarse labels onto mechanisms mechanically - is how the scheme we replaced went wrong.

As evidence that the classification does work, 23 mechanisms recur across more than one chain deployment, and one mechanism cell accounts for exposure across 18 distinct targets, a grouping invisible before the reclassification because its six members sat in four different families. Working the headline case by hand, `NRDAX-T0100` reaches nine chain deployments over four independently written handshake stacks; the registry records no implementation lineage for most instances, so chain counts overstate independence and we report the smaller number.

## 1.3 What this paper does not claim

Stated here rather than only in section 8, because the claims are easy to inflate by omission.

The corpus is **lab fidelity**: 198 of 199 instances. Nothing here is evidence about production impact.

**Seventy-four per cent of classified techniques are reproductions of publicly disclosed CVEs**, not discoveries. The contribution in those cases is the reproduction, the mechanism reading and the index entry.

Coverage is **uneven**, with the top five targets holding half the instances and 18 of 37 targets carrying a single one. An empty cell in the coverage matrix means "not examined" far more often than "not exposed", and this confounds the recurrence result in the flattering direction. We report recurrence as an existence claim and decline to report a rate.

The classification is **one team's judgement, externally unreviewed**, with no inter-rater measurement. Thirteen techniques could not be resolved to a single family at all.

And **no detection capability is claimed**. Companion work applied machine learning to detecting attacks in this class and reported its central cross-chain transfer claim as falsified at a pre-registered gate. That negative result stands; this paper does not route around it. A mechanism taxonomy is a prerequisite for asking well-posed detection questions, not evidence that the answers are affirmative.
