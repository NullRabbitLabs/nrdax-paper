# 2. Scope and definitions

## 2.1 The class

NRDAX catalogues one class of attack, stated as narrowly as we can state it:

> A network-reachable input, small or malformed relative to its effect, that forces a **node implementation** of a decentralised protocol into disproportionate consumption of memory, CPU, admission capacity or egress bandwidth, or into an unrecoverable fault.

Three parts of that definition do the work.

**Node implementation.** The target is the software a participant runs to take part in the network: a full node, validator, RPC provider, light client, or the transport and gossip libraries they embed. It is not the protocol as specified, and it is not the application layer built on top. Two implementations of the same protocol can differ entirely in exposure, which is the point: the class is about code, not about consensus rules.

**Network-reachable, and generally unauthenticated.** The input arrives over the network from a party the node has not authenticated, or has authenticated only as a peer. Peer authentication does not remove a technique from the class: a completed handshake makes the sender a peer, not a trusted one, and several techniques in the corpus are post-handshake.

We do not put a number on how many are strictly pre-authentication, because the registry does not record reachability as a field and we will not report a figure we cannot show. What the registry does record is the bound-failure mode, and the 7 techniques marked `late` (section 3.2.3) are by definition those where the cost is paid before the check that could have rejected the input.

**Disproportionate.** There is an asymmetry between what the attacker spends and what the node spends. Volumetric flooding, where the attacker simply out-sends the victim's link, is out. Section 3.2 develops the asymmetry into the mechanism definition.

## 2.2 What is deliberately out

The boundary is what makes the classification useful, so we state the exclusions positively rather than by omission. Each has been enforced against the corpus, not merely declared: 31 published techniques are tombstoned as out of class, and section 3.7 records the 14 that were removed from the reproduced slice on exactly these grounds.

**Application and contract level.** Defects in smart contracts, their compilers, or the applications deployed on a chain. Reentrancy, access-control errors in a contract, and signature replay against an application are all excluded, however severe. The node is not the target; the contract is. MITRE AADAPT covers this ground and covers it well (section 7).

**Economic and MEV.** Attacks whose mechanism is incentive manipulation rather than resource consumption: oracle manipulation, liquidation griefing, sandwiching, AMM value extraction. The node behaves correctly throughout; the harm is economic. Seventeen techniques in the economic-DeFi and bridge classes were tombstoned on this basis before the work reported here.

**Consensus safety.** Attacks whose outcome is divergence between honest nodes rather than loss of a node: chain reorganisation, long-range attacks, netsplits, transaction malleability, and validation gaps that cause a defective node to accept what a compliant node rejects. This exclusion is the one most often crossed in practice, because a consensus-safety attack and a node-resource attack can share a delivery path. Seven techniques were tombstoned here, including `NRDAX-T0307` (transaction malleability) and `NRDAX-T0411`, where a SIGHASH_SINGLE index gap produces a block-template divergence. The test we apply: if the harm is that *two honest nodes now disagree*, it is out; if the harm is that *one node is now gone or degraded*, it is in.

**Censorship and eclipse.** Attacks on what a node can see rather than on what it can do. `NRDAX-T0050` (DHT Sybil content censorship) was tombstoned on this basis.

**Supply chain.** Compromise of build, distribution or dependency infrastructure. A different threat model with a different defence surface.

**Credential compromise.** Attacks whose outcome is key or fund theft. `NRDAX-T0317`, an exposed and unauthenticated `personal` RPC namespace with an unlockable account, was tombstoned here: it is a serious defect on a node, but what it yields is theft, not unavailability.

**Host and enterprise intrusion.** Lateral movement, persistence, privilege escalation on the machine hosting a node. MITRE ATT&CK's domain, at a different layer (section 7).

Tombstoning rather than deletion is deliberate. An identifier that has been cited must keep resolving, so an out-of-class record is retained, flagged in every export, demoted from the default view, and where a genuine equivalent exists, crosswalked to the registry that should hold it.

## 2.3 Why this class needs separate treatment

The class is not merely uncovered by existing frameworks (section 7 works through which frameworks and why). It is also poorly served by the tooling that would otherwise discover and classify its members, and the two facts are related: a class that standard instrumentation cannot observe does not accumulate the structured evidence from which taxonomies are usually built.

The specific instrumentation gap is analysed technique by technique in *What syscall-layer tooling cannot see in P2P infrastructure* \cite{nullrabbit2026blindspot}, and we do not restate the analysis here. Its result is what matters for this paper. Taking five techniques from this corpus - pre-authentication handshake CPU burn (`NRDAX-T0205`), HTTP/2 rapid reset (`NRDAX-T0112`), gRPC/HTTP2 multiplexing OOM (`NRDAX-T0097`), mempool pending-eviction flood (`NRDAX-T0156`) and unbounded response amplification (`NRDAX-T0329`) - it finds that **none of the five can be expressed as a syscall-layer detection rule**, for three structural reasons: the rule language cannot aggregate events over a time window, resource cost has no observable field, and the discriminating frame-level facts are unparsed and frequently encrypted.

Five techniques is a small sample and the brief does not claim otherwise. But the three reasons it identifies are properties of the instrumentation boundary rather than of those five cases, which is why we treat the gap as characteristic of the class rather than incidental to it.

Two consequences follow for how this registry is built.

First, **evidence has to be captured at the protocol layer**, which is why the corpus is built from reproductions carrying protocol-level capture rather than from advisory text (section 5).

Second, **the taxonomy cannot be derived from observed telemetry**, because the telemetry that would ground it does not exist at scale. It has to be derived from mechanism, read off the reproduction. That is a constraint, and it shapes what the registry can honestly claim: section 8 states what follows from having 97 classified techniques rather than 97,000 observations.

## 2.4 Terms

Used consistently throughout, and defined against the registry's own model in section 4.

**Technique.** The citable unit: a mechanism, independent of any particular implementation. Carries a permanent `NRDAX-Tnnnn` identifier.

**Instance.** One occurrence of a technique against one specific target, evidenced by a reproduction. A technique's instances are what support its cross-implementation claim.

**Target.** What an instance runs against. We use this rather than "chain" because the corpus contains both: 33 independent chain implementations and 4 shared substrates (QUIC, HTTP/2, HTTP/3, libp2p) that chains embed. Section 6 keeps the two apart, because recurrence across independent chains and recurrence within a shared library are different evidence.

**Mechanism.** The pair (resource exhausted, bound-failure mode). Section 3.2.

**Family.** A region of the mechanism space; the classification a technique is published under. Five of them, section 3.3.

**Surface.** Where the attacker's input enters the node. An attribute, never a family; section 3.2.4 says why.

**Reproduced** and **known**. A reproduced technique has at least one instance captured in a controlled environment. A known technique is recorded from a public advisory with no reproduction on file. The distinction governs what may be claimed about a technique and, in this registry, whether it may be classified at all: 97 techniques are classified, 323 are not, and the boundary between those two numbers is reproduction (section 3.5).
