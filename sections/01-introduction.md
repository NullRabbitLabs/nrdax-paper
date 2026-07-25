# 1. Introduction

A node implementation of a decentralised protocol is an unusual piece of software to have to defend. It is required to accept connections from anonymous, unauthenticated peers; to parse attacker-controlled structures before it can decide whether the sender is worth talking to; and to do all of this continuously, because being reachable is what participation means. The attack surface is not a deployment mistake. It is the design.

The consequences accumulate steadily in the public record. A length prefix that pre-allocates a receive buffer before the body arrives (CVE-2015-3641). An un-rate-limited `getheaders` handler which, in our reproduction, drove more than 100 MB/s of upload (CVE-2023-33297). An empty Bloom filter reaching a modulo in a hash function (CVE-2013-5700). Connection identifiers accumulating in an unbounded map on an established QUIC connection (CVE-2024-22189). An `addr` flood overflowing a 32-bit counter into an assertion abort (CVE-2024-52919). Each is catalogued against the project it was found in, patched, and filed.

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

**A mechanism-defined classification.** We define a mechanism as a pair: the resource the node spends disproportionately, and the way its bound on that resource failed to apply. Five resource classes and five bound-failure modes. The resource axis names the families and the bound-failure axis is a second attribute recorded within them, so the taxonomy is five families over a 5x5 mechanism grid, not twenty-five. Each bound-failure mode carries a concrete audit question, which a technique inherits and which transfers to a codebase that has never been examined. Section 3.

The distinction from symptom-based grouping is load-bearing rather than rhetorical, and section 3.7 puts a number on it. We applied the criteria to a corpus of 97 reproduced techniques that had been published under a 13-label scheme assembled operationally. Forty changed family. Twenty-two turned out to share a mechanism the old vocabulary had no name for, scattered across seven labels. Six labels turned out not to be mechanisms at all - three named an entry surface, three named a bypassed guard. Fourteen records turned out to be outside the class entirely. That reclassification is now live in the registry, which is why this paper can be checked against it.

**A reproduction-grounded corpus.** A technique is classified only if it has been reproduced in a controlled environment with captured evidence. Of 420 published techniques, 118 carry a reproduced instance and 97 carry a mechanism family, the 21-technique difference being 14 tombstoned as out of class and 7 reproduced but not yet classified (section 4.3). The 97 carry 199 instances across 37 targets. The 323 without a family are served with an explicit `pending` state and no inferred family, because the alternative - mapping coarse labels onto mechanisms mechanically - is how the scheme we replaced went wrong in the first place. Section 5.

**Permanent identifiers and machine surfaces.** `NRDAX-Tnnnn` identifiers are opaque, stable and never reused, with family as an attribute rather than a component. This is what let 40 techniques change family without breaking a citation. The registry serves JSON, STIX 2.1 and JSON-LD, and is designed to be ingested rather than read. Section 4.

**Evidence that the classification does work.** Sixteen mechanisms recur across independently written chain implementations with no shared library in the instance set. `NRDAX-T0100` alone has reproduced instances against nine separate chains. One mechanism cell accounts for exposure across 18 distinct targets - and until the reclassification its six members sat in four different families, so that grouping was not visible in the registry at all. Section 6.

## 1.3 What this paper does not claim

Stated here rather than only in section 8, because the claims are easy to inflate by omission.

The corpus is **lab fidelity**: 198 of 199 instances. Nothing here is evidence about production impact.

**Seventy-four per cent of classified techniques are reproductions of publicly disclosed CVEs**, not discoveries. The contribution in those cases is the reproduction, the mechanism reading and the index entry.

Coverage is **uneven**, with the top five targets holding half the instances and 18 of 37 targets carrying a single one. An empty cell in the coverage matrix means "not examined" far more often than "not exposed", and this confounds the recurrence result in the flattering direction. We report recurrence as an existence claim and decline to report a rate.

The classification is **one team's judgement, externally unreviewed**, with no inter-rater measurement. Thirteen techniques could not be resolved to a single family at all.

And **no detection capability is claimed**. Companion work applied machine learning to detecting attacks in this class and reported its central cross-chain transfer claim as falsified at a pre-registered gate. That negative result stands; this paper does not route around it. A mechanism taxonomy is a prerequisite for asking well-posed detection questions, not evidence that the answers are affirmative.
