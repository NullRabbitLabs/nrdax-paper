# 6. Evaluation

A taxonomy is not evaluated by whether it is tidy. It is evaluated by whether it supports an inference that its absence does not. The inference this one claims is:

> A mechanism observed against one node implementation predicts exposure in other implementations.

If that holds, the classification does work no per-project CVE list can do, because a per-project list has no representation for "the same mechanism, elsewhere". If it does not hold, the families are a filing convention.

Section 6.1 reports the evidence. Section 6.2 reports what we consider the more informative half of it: where the evidence does not extend.

## 6.1 The same mechanism recurs across independent deployments

Of the 97 classified techniques, **23 carry instances against more than one target** and 74 against exactly one. The 23 span 2 to 9 targets each.

The raw count is not the interesting number, because a mechanism reproduced against two chains that embed the same networking library may be one library defect reached twice. What the argument needs is recurrence across implementations that do not share the relevant code.

We report two levels, and the gap between them is the finding.

### 6.1.1 Level one: distinct chain deployments

The first level is what the registry's own target field supports. Of the 23 multi-target techniques, 16 have no shared substrate recorded as a target, 7 span both chains and a substrate, and none is confined to substrates.

| Recurrence pattern | Techniques |
|---|---:|
| Across chain deployments only, no substrate recorded as a target | 16 |
| Spanning both chain deployments and a recorded substrate | 7 |
| Within recorded substrates only | 0 |
| **Total multi-target** | **23** |

**This is a weaker result than it looks, and the earlier drafts of this paper overstated it.** The test asks whether a shared substrate appears in the *target* field. It does not ask whether the chains reached that substrate through an embedded dependency, and a chain that vendors libp2p is recorded under its own name, not under libp2p. So "no shared substrate recorded" does not mean "no shared code", and the 16 must not be read as sixteen independent implementations.

### 6.1.2 Level two: independent protocol stacks, worked for the headline case

`NRDAX-T0100` was presented in earlier drafts as the strongest single result: nine chains, no shared substrate, therefore nine separately-written implementations. That claim was wrong, and the registry's own data refutes it. The primitive identifiers name the handshake stack each instance was reproduced against:

| Handshake stack | Deployments |
|---|---|
| RLPx / devp2p (go-ethereum lineage) | BNB Smart Chain, Polygon PoS, Sonic/Fantom |
| libp2p Noise | Celestia, Ethereum consensus layer, Filecoin, Optimism |
| litep2p Noise (Rust reimplementation) | Polkadot/Substrate |
| Solana TPU QUIC | Solana |

Nine chain deployments over **four handshake stacks**, and arguably three if litep2p is treated as a libp2p reimplementation rather than an independent one. Three of the nine share go-ethereum's RLPx handshake; four share libp2p's Noise handshake. The recurrence is substantially explained by shared code, which is precisely the confound section 6.1.1 sets up and which the earlier claim failed to control for.

What survives is still worth stating, and it is a different claim: **the same mechanism appears in four independently written handshake implementations** - RLPx, libp2p Noise, litep2p Noise and Solana's TPU QUIC path - which were written in different languages by different teams and share no handshake code between the four groups. Four is a real result for a mechanism that admits an obvious defence. Nine was not.

It also has a sharper defensive reading than the inflated version did. Where recurrence is stack-level, the fix is stack-level: patching libp2p's Noise handshake protects every embedder at once, and the registry's job is to say which mechanism affects which stack, not to imply nine independent bugs where there are four.

### 6.1.3 What the registry now records, and what it still does not

The stack analysis above is no longer a hand calculation in a paper. The registry carries lineage as data: each instance may record the stack it exercised, and a separate curated table declares which stacks share the code that matters, with a written rationale per row. The independence count is derived from the two and served on every technique.

Two rules keep the derived figure honest, and they are enforced rather than intended:

- **an unknown lineage never counts as independent**, and
- **where anything is unknown the figure is published as a lower bound** with an upper bound beside it, assuming each unknown instance turns out to be its own new group.

Coverage is the limit, and it is severe. Of 226 instances, 9 carry curated lineage - `NRDAX-T0100`'s, which is why that case can be stated exactly. A further 64 carry a lineage *proposed* by pattern-matching the primitive identifier; those are marked `inferred` and count toward nothing until a human confirms each against its bundle, because treating an inference as a fact is the mistake that produced the mixed family taxonomy. The remaining 153 record no stack at all.

So the position is now:

- **23 techniques recur across more than one chain deployment.** Measured, and it stands.
- **`NRDAX-T0100` recurs across four independent stacks.** Curated, derived, and served.
- **For every other multi-target technique the independence count is a lower bound**, usually zero, with an upper bound equal to its deployment count. `NRDAX-T0205` reports "at least 0, at most 9" rather than 9, which is the honest reading of nine uncurated instances.

The remedy is no longer a schema change but a curation queue, and the registry now says exactly how long it is.

The strongest individual cases by deployment count, with the same caveat applying to every row:

| Technique | Family | Chains | Substrates | Targets |
|---|---|---:|---:|---:|
| `NRDAX-T0100` handshake-crypto-cpu-burn | `compute_amp` | 9 | 0 | 9 |
| `NRDAX-T0205` pre-handshake-crypto-cpu-burn | `compute_amp` | 8 | 1 | 9 |
| `NRDAX-T0329` unbounded-rpc-response-amplification | `response_amp` | 7 | 0 | 7 |
| `NRDAX-T0320` unbounded-connection-flood | `connection_exhaustion` | 5 | 2 | 7 |
| `NRDAX-T0099` half-open-handshake-slowloris | `connection_exhaustion` | 5 | 0 | 5 |
| `NRDAX-T0064` endpoint-concurrency-cap-exhaustion | `connection_exhaustion` | 4 | 1 | 5 |
| `NRDAX-T0328` unbounded-request-body-memory-exhaustion | `memory_amp` | 4 | 0 | 4 |
| `NRDAX-T0006` async-runtime-blocking-vm-execution | `compute_amp` | 4 | 0 | 4 |
| `NRDAX-T0106` header-length-preallocation-oom | `memory_amp` | 3 | 1 | 4 |

The "Chains" column counts chain deployments, not independent implementations. `NRDAX-T0100`'s nine chains are four stacks; the others have not been worked.

### 6.1.4 What this does for a defender that a CVE list does not

A per-project CVE list represents `NRDAX-T0100` as nine unrelated advisories, each against one project. Nothing in that representation says the nine are the same thing, that four stacks underlie them, or which other embedders of those stacks to check.

The mechanism representation makes the query expressible. The cell carries the audit question, inherited from its bound-failure mode (section 3.2.3): for (`compute_amp`, `late`), *what work happens before the first check that could reject the input?* That question is implementation- independent, and it is what turns nine advisories into one thing to check everywhere.

We can state one concrete instance of this working, and we state it narrowly. `NRDAX-T0206` (RLPx pre-authentication packet flood) and the libp2p instance of `NRDAX-T0205` were examined because the mechanism had already been characterised elsewhere in the corpus, not because an advisory pointed at them. That is the mechanism axis doing the work it is supposed to do. It is also a small number of cases, and section 8 declines to generalise from it.

### 6.1.5 Recurrence is uneven across families

| Family | Multi-target | Total | Rate |
|---|---:|---:|---:|
| `connection_exhaustion` | 7 | 13 | 54% |
| `compute_amp` | 6 | 24 | 25% |
| `fault_termination` | 5 | 22 | 23% |
| `memory_amp` | 4 | 33 | 12% |
| `response_amp` | 1 | 5 | 20% |

`connection_exhaustion` recurs at more than four times the rate of `memory_amp`, and the asymmetry is interpretable. Admission capacity is a design-level concern: every node must decide how many peers to accept and how to key that limit, and the wrong answers are a small set that many implementations reach independently. Retention defects are code-level: a specific unbounded collection in a specific handler, which the next implementation may simply not have written.

If that reading is right, it says something useful about where the taxonomy's predictive value is concentrated: a `connection_exhaustion` finding is worth checking everywhere, a `memory_amp` finding often is not. We offer it as a hypothesis the corpus is consistent with, not as a result. Twenty-three multi-target techniques across five families is not enough to support a claim about rates, and the confound in section 6.2 is severe enough that we would not make one from this data.

## 6.2 What the coverage matrix cannot support

The coverage matrix is technique by target, with a cell where a reproduced instance exists. It is derived, never stored, and empty cells are the majority.

**An empty cell is not evidence of absence.** The corpus is deep on a few implementations and one-shot on half the rest: the top five targets hold 102 of 199 instances, and 18 of 37 targets carry exactly one instance each. When `NRDAX-T0100` shows nine targets and `NRDAX-T0106` four, the difference is partly about the mechanisms and substantially about where we looked.

This is the confound that limits section 6.1, and it runs in the direction that flatters the result. A technique reproduced on nine chains was *pursued* across nine chains, generally because an early instance suggested it would generalise. A technique with one instance may be equally general and simply never followed up. So the 23 multi-target techniques are better read as *23 mechanisms we checked and found to recur* than as *23 of 97 mechanisms that recur*, and the 74 single-target techniques carry almost no information about generality either way.

What survives is an existence claim, and a narrower one than earlier drafts made: **23 mechanisms demonstrably work against more than one chain deployment, with captured evidence per instance, and at least one of them works against four independently written implementations of the same protocol step.** That is enough to establish that mechanism-level recurrence in this class is real and worth indexing. It is not enough to establish how common it is, nor how much of it is stack-level rather than implementation-level, and we claim neither.

Two further limits on the matrix, stated here and developed in section 8:

**All lab fidelity.** Every cell records a reproduction in a controlled environment (198 lab, 1 proxy, no production capture). A cell says the mechanism works against that implementation in a lab, not that a deployed operator of it is exposed. Real deployments sit behind mitigations the corpus does not model.

**No detection claim is made anywhere in this paper.** A companion line of work applied machine learning to detecting attacks in this class and reported the central cross-chain transfer claim as *falsified* at its pre-registered evaluation gate. Nothing here revises that. The taxonomy organises attacks; it is not evidence that they can be detected, and the honest published result on detection is a negative one.
