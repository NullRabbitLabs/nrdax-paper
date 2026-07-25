# 6. Evaluation

A taxonomy is not evaluated by whether it is tidy. It is evaluated by whether it supports an inference that its absence does not. The inference this one claims is:

> A mechanism observed against one node implementation predicts exposure in other, independent implementations.

If that holds, the classification does work no per-project CVE list can do, because a per-project list has no representation for "the same mechanism, elsewhere". If it does not hold, the families are a filing convention.

Section 6.1 reports the evidence. Section 6.2 reports what we consider the more informative half of it: where the evidence does not extend.

## 6.1 The same mechanism recurs across independent implementations

Of the 97 classified techniques, **23 carry instances against more than one target** and 74 against exactly one. The 23 span 2 to 9 targets each.

The raw count is not the interesting number, because "target" conflates two different things. The corpus spans 37 targets: 33 independent chain implementations, and 4 shared substrates (QUIC, HTTP/2, HTTP/3, libp2p) that chains embed as libraries. A mechanism recurring across two chains that both use libp2p may be one library defect reached twice. A mechanism recurring across two chains with no shared code is a different and much stronger claim.

Separating them:

| Recurrence pattern | Techniques |
|---|---:|
| Across independent chains only, no shared substrate | 16 |
| Spanning both independent chains and a shared substrate | 7 |
| Within shared substrates only | 0 |
| **Total multi-target** | **23** |

**Sixteen techniques recur across independent chain implementations with no shared substrate in the instance set at all.** These are the cases where the same mechanism was reproduced against separately-written codebases, and they are what the claim rests on. Not one multi-target technique is confined to shared substrates, so no part of the recurrence result is an artefact of counting one library twice.

The strongest individual cases. Read the columns carefully: "targets" is chains plus substrates, so `NRDAX-T0205` at nine targets is eight chains and libp2p, whereas `NRDAX-T0100` at nine targets is nine chains and nothing shared. The distinction is the whole point of the table.

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

`NRDAX-T0100` is the clearest single result: nine independent chain implementations, zero shared substrates. BNB Smart Chain, Celestia, the Ethereum consensus layer, Filecoin, Optimism, Polkadot/Substrate, Polygon PoS, Solana and Sonic/Fantom each perform per-handshake asymmetric cryptography before any admission decision. These are separately-written node implementations in different languages by different teams, and the recurrence is not explained by shared code. It is explained by a shared design pressure: a handshake must do cryptography, and admission control is easier to write after the handshake than before it.

Together with `NRDAX-T0205` (Bitcoin Core, Cosmos, Conflux, XRP, Casper, ICON, Qtum, Polygon PoS, and libp2p) and `NRDAX-T0206` (RLPx, on Ethereum), those three pre-authentication handshake techniques account for reproduced exposure across **18 distinct targets**.

The mechanism cell they belong to, (`compute_amp`, `late`), is wider than the handshake case. It has six members, and the other three generalise it past the handshake to any check that runs after the cost: `NRDAX-T0143` and `NRDAX-T0207` are gossip processed before signature verification, and `NRDAX-T0408` is `ValidateBasic` running in `CheckTx` ahead of the antehandler. The cell's audit question - *what work happens before the first check that could reject the input?* - covers all six, and the six between them span 18 targets.

Those six members were previously distributed across **four different producer families** (`compute_amp`, `connection_exhaustion`, `consensus_abuse` and `memory_amp`), because the old labels mixed a mechanism axis with a surface axis: the handshake ones looked like connection problems and the gossip ones looked like consensus problems. The cell is the paper's central example precisely because it was not visible in the registry at all until the reclassification in section 3.7.

### 6.1.1 What this does for a defender that a CVE list does not

A per-project CVE list represents `NRDAX-T0100` as nine unrelated advisories, each against one project, disclosed at different times by different reporters. Nothing in that representation says the nine are the same thing, and nothing in it tells the tenth project to look.

The mechanism representation makes the query expressible. The cell carries the audit question, inherited from its bound-failure mode (section 3.2.3): for (`compute_amp`, `late`), *what work happens before the first check that could reject the input?* That question is implementation- independent, and it is what turns nine advisories into one thing to check everywhere.

We can state one concrete instance of this working, and we state it narrowly. `NRDAX-T0206` (RLPx pre-authentication packet flood) and the libp2p instance of `NRDAX-T0205` were examined because the mechanism had already been characterised elsewhere in the corpus, not because an advisory pointed at them. That is the mechanism axis doing the work it is supposed to do. It is also a small number of cases, and section 8 declines to generalise from it.

### 6.1.2 Recurrence is uneven across families

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

What survives the confound is the existence claim, which is the one section 6 actually needs: **for at least 16 mechanisms, the same mechanism demonstrably works against multiple independently written implementations, with captured evidence per instance.** That is enough to establish that mechanism-level recurrence in this class is real and worth indexing. It is not enough to establish how common it is, and we do not claim a rate.

Two further limits on the matrix, stated here and developed in section 8:

**All lab fidelity.** Every cell records a reproduction in a controlled environment (198 lab, 1 proxy, no production capture). A cell says the mechanism works against that implementation in a lab, not that a deployed operator of it is exposed. Real deployments sit behind mitigations the corpus does not model.

**No detection claim is made anywhere in this paper.** A companion line of work applied machine learning to detecting attacks in this class and reported the central cross-chain transfer claim as *falsified* at its pre-registered evaluation gate. Nothing here revises that. The taxonomy organises attacks; it is not evidence that they can be detected, and the honest published result on detection is a negative one.
