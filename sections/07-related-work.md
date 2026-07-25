# 7. Related work and positioning

The claim this section supports is narrow: for the network-boundary and node-resource class defined in section 2, there is no existing structured index that classifies by mechanism. The frameworks that exist are either at a different layer, in an adjacent domain, or organised on a different axis. We take each in turn, and where a measurement is available we give it rather than asserting the gap.

## 7.1 MITRE ATT&CK: a different layer

ATT&CK is the reference model for adversary behaviour against enterprise, cloud, ICS and mobile environments, organised as tactics (the adversary's objective) and techniques (how the objective is achieved) [MITRE ATT&CK].

Its coverage of the outcome NRDAX catalogues sits under the Impact tactic, principally *Endpoint Denial of Service* (T1499), with sub-techniques *OS Exhaustion Flood* (T1499.001), *Service Exhaustion Flood* (T1499.002), *Application Exhaustion Flood* (T1499.003) and *Application or System Exploitation* (T1499.004), alongside *Network Denial of Service* (T1498).

Those five values are the entire vocabulary ATT&CK offers for this class, and the granularity is the point. Every one of the 97 classified NRDAX techniques would map to T1499.002 or T1499.003, and the mapping would carry no information: it would not distinguish a pre-authentication handshake CPU burn from an unbounded connection-ID map from a UTF-8 decode panic, and it would not tell a defender which of the three to look for in their own code. ATT&CK is not deficient here. It operates at the layer of *what the adversary is doing to the organisation*, and at that layer "the service was exhausted" is the right resolution. NRDAX operates at the layer of *what property of this implementation permitted it*, which is a different question about a different artefact.

The two are complementary rather than competing, and the honest statement of the relationship is that an NRDAX technique refines T1499 downward by roughly twenty-fold in specificity - five ATT&CK values against 97 classified techniques - for one class of target ATT&CK does not model: the node implementation of a decentralised protocol.

## 7.2 MITRE AADAPT: the adjacent domain, and the measured gap

AADAPT (Adversarial Actions in Digital Asset Payment Technologies) is MITRE's ATT&CK-styled framework for digital asset systems, released July 2025 and built from more than 150 government, industry and academic sources [MITRE AADAPT]. It is the closest existing framework to NRDAX's domain, and it is the right place to test whether this registry is redundant.

NRDAX carries an AADAPT crosswalk as first-class data, pinned to an immutable source revision (`cd6a74ca`, retrieved 2025-10-31), served at `/v1/aadapt`, and populated conservatively: a specific AADAPT technique where the match is exact, a parent where the record is a general instance of it, and null where no honest equivalent exists. Crosswalks are never fabricated to fill the column.

The result, read from the live registry on 2026-07-24:

| | |
|---|---:|
| AADAPT techniques with any NRDAX mapping | 12 |
| NRDAX techniques with an AADAPT mapping | 27 of 420 |
| of those, tombstoned as out of NRDAX scope | 16 |
| of those, still in scope | 11 |
| **Classified NRDAX techniques with an AADAPT mapping** | **0 of 97** |

**Not one of the 97 mechanism-classified techniques maps to any AADAPT technique.** Every one of the 27 mapped records is either known-but-not-reproduced or tombstoned.

Because this is the paper's key positioning evidence, the working is worth showing rather than asserting. The crosswalk was built before the reclassification reported in section 3.7 and measured 22 mapped techniques, of which zero were in the reproduced slice. The reclassification then tombstoned 14 techniques (section 2.2), and 5 of those carried an honest AADAPT equivalent that had not previously been recorded: `NRDAX-T0298`, `NRDAX-T0409`, `NRDAX-T0411` and `NRDAX-T0414` to consensus-logic and chain-reorganisation techniques, and `NRDAX-T0317` to `ADT1552` Unsecured Credentials. That is the whole of the 22-to-27 change; no mapping was removed, and none was added to a technique that stayed in scope.

The zero is therefore stable across the reclassification rather than produced by it. It was zero before and it is zero now. The denominator changed rather than the result: the crosswalk was measured against the 111 techniques then carrying one of the producer's fine-grained family labels, which was the slice the reclassification went on to examine, and it is now measured against the 97 that slice yielded. (111 is not the reproduced total, which was and is 118; the difference is the 7 reproduced techniques carrying coarse labels, section 4.3.) What the reclassification changed is the *character* of the mapped set, which went from 50% to 59% tombstoned as NRDAX ceded more ground to the framework that should hold it. The mapped set concentrates exactly where it should: `ADT3012` (Exploit Smart Contract Implementation) with 7, `ADT3007` (Exploit Consensus Logic) with 6, `ADT3016.001` (Cryptographic Protocol Analysis) with 3, and `ADT3003` (Chain Reorganization) with 2.

That distribution is the finding, and it reads in both directions. AADAPT covers smart contracts, consensus logic, cryptographic protocol weaknesses, counterfeit tokens and credential handling thoroughly. It does not model the node implementation as an attack surface in its own right: there is no AADAPT technique for pre-authentication cryptographic work, for allocation without limits in a gossip handler, for an admission cap keyed on an attacker-chosen value, or for a decode panic reachable in one packet. Conversely, the NRDAX records that *do* map to AADAPT are precisely the ones NRDAX has ceded: 16 of the 27 are tombstoned, with the crosswalk serving as a hand-off to the registry that should hold them.

Two registries with adjacent domains and zero overlap on the reproduced corpus is the strongest single piece of evidence we can offer that this class is unclassified rather than merely unclassified-by-us. We note the direction of the inference honestly: it establishes that AADAPT does not cover this class. It does not establish that the class is important, which is an argument from the corpus (section 6) and not from a gap in someone else's index.

## 7.3 Blockchain security surveys: classified by layer, not mechanism

There is a substantial survey literature on blockchain attack surfaces. Saad et al. survey the attack surface comprehensively, attributing viability to cryptographic constructs, distributed architecture, and application context [Saad et al. 2020]. Chen et al. survey Ethereum systems security across vulnerabilities, attacks and defences [Chen et al. 2020]. Both are broad, well-constructed, and organised by *where in the stack* a weakness sits.

Most directly relevant, Zhang, Dou and Li analyse DoS attacks and defence technologies in blockchain systems, organising them by the blockchain architecture hierarchy with emphasis on the contract layer and the consensus layer [Zhang et al. 2026]. This is the nearest prior work to the present paper: same outcome class, explicitly taxonomic, recent. And the emphasis is the gap. A layer-based hierarchy that concentrates on the contract and consensus layers is organising by *target*, and the two layers it concentrates on are the two that section 2 excludes. The network-boundary and node-resource class sits below both, in the implementation of the P2P and RPC surfaces, and a layer axis places every member of it in a single undifferentiated bucket.

The P2P-network literature is different in kind and worth separating: Heilman et al. on eclipse attacks against Bitcoin's peer-to-peer network [Heilman et al. 2015] is exactly the depth of mechanism analysis this class needs. But it is a paper about one mechanism against one implementation, which is the normal and correct unit for a research contribution. What does not exist is the index that accumulates such analyses into a structure where the next one can be predicted.

The distinction we draw against all of this work is not quality. It is that a survey classifies the literature and a registry classifies the artefacts, with permanent identifiers, machine surfaces and an increment-only history. A survey is a snapshot of a field; a registry is a citable substrate other work can point at. Both are useful and they are not substitutes.

## 7.4 CVE and CWE: the defect, and the attack

CVE identifies a vulnerability in a specific product version. It is the right identifier for that, and NRDAX defers to it: 150 CVE references and 56 GHSA references attach to instances, because a CVE is a property of an *implementation*, which in this model is an instance and not a technique (section 4.2). NRDAX does not compete with CVE and does not mint identifiers for things CVE already identifies. Where a technique reproduces a public CVE, the registry says so on the instance, and section 5.3 reports that this is 74% of the classified corpus.

CWE is the more interesting comparison, because CWE-405 *Asymmetric Resource Consumption (Amplification)* [CWE-405] describes almost exactly the asymmetry that section 3.2 uses to define the class, sitting under CWE-400 *Uncontrolled Resource Consumption* [CWE-400] alongside CWE-770 *Allocation of Resources Without Limits or Throttling* [CWE-770]. The overlap is not coincidental: `NRDAX-T0139`, one of the techniques in our corpus, carries CVE-2025-46598, which NVD classifies as CWE-405.

The relationship is a division of labour, not a rivalry, and it is worth stating precisely because the two are easy to conflate.

**CWE classifies the defect. NRDAX classifies the attack.** CWE-770 says a resource was allocated without a limit. It says nothing about who can reach that allocation, over which protocol, whether authentication intervenes first, or what an operator loses. Those are properties of the attack, and they are what decides whether a CWE-770 instance is a critical unauthenticated remote issue or a non-issue behind an admin boundary.

The `fault_termination` family makes the division concrete. CWE-617 (Reachable Assertion), CWE-248 (Uncaught Exception), CWE-369 (Divide By Zero) and CWE-129 (Improper Validation of Array Index) each name a defect. `fault_termination` names the property that an *unauthenticated remote peer can reach that defect with a single message and remove a node from the network*. The same CWE-129 defect behind an authenticated interface is not a member of the family. One defect class, two attack outcomes, and it is the attack outcome a defender prioritises on.

NRDAX's second axis is where the two frameworks come closest. `bound_failure` (section 3.2.3) is defect-flavoured: `no-bound` is close to CWE-770, and `mis-quantified`, `late` and `mis-scoped` are refinements of "a limit exists but does not apply" that CWE does not currently distinguish. We regard that as a contribution to be checked rather than claimed: whether those four modes are the right decomposition is exactly the kind of thing external review should test, and section 8 records that no such review has happened.

## 7.5 Summary of the position

NRDAX is not a replacement for any of the above. It occupies a specific gap:

- **below ATT&CK**, which models organisational impact and offers five values where this class needs a hundred;
- **beside AADAPT**, which models digital asset systems and, as measured, shares zero techniques with this registry's classified corpus;
- **orthogonal to the survey literature**, which classifies by layer and target rather than mechanism, and whose DoS-specific taxonomy concentrates on the two layers this class sits below;
- **downstream of CVE**, which identifies implementations, and which NRDAX references rather than duplicates;
- **complementary to CWE**, which classifies defects where NRDAX classifies the attacks that reach them.
