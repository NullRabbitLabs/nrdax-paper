# 3. The classification

All figures in this section were read from the live registry at
`https://api.nrdax.com/v1` on 2026-07-24 and can be re-read there.
Every technique cited is resolvable at
`https://nrdax.com/techniques/<id>`.

## 3.1 What a mechanism-defined family has to do

Most catalogues of node-level denial-of-service group findings by
one of two things. Either by **target**, which produces families
like "P2P attacks", "RPC attacks", "consensus attacks", or by
**symptom**, which produces families like "memory exhaustion",
"CPU exhaustion", "crash". Both groupings are stable and easy to
apply, and neither supports the inference the class actually
needs: given a technique observed against one implementation,
which other implementations are exposed, and what property of
their code decides it.

Target-defined families fail this because the same defect appears
behind different entry points. Symptom-defined families fail it
because the same symptom is reached by unrelated routes. A node
that exhausts memory because a length prefix pre-allocates a
receive buffer (`NRDAX-T0106`) and a node that exhausts memory
because a header-size guard counts encoded rather than decoded
bytes (`NRDAX-T0383`) share an outcome and share nothing that
would let a reader predict the second from the first. The fix
classes differ, the affected code differs, and the set of exposed
implementations differs.

We therefore require a family to satisfy four tests.

1. **Mechanism determinacy.** Membership is decided by the route
   from attacker input to resource loss, not by which port the
   input arrived on and not by which counter went to zero.
2. **Predictive transfer.** Family membership implies a concrete
   audit question that can be asked of an unrelated codebase. If
   knowing a technique's family tells a reader nothing to go and
   check, the family is a label rather than a class.
3. **Chain-agnosticism.** No family may be definable only in terms
   of one chain's protocol vocabulary. Families whose defining
   mechanism is stated in terms of `addr` messages or `cmpctblock`
   are per-project categories in disguise.
4. **Disjointness under a stated tie-break.** Every technique has
   exactly one family, and where a technique plausibly satisfies
   two definitions there is a written rule that decides it. Without
   the tie-break, disjointness is an accident of who did the
   filing.

Section 3.7 reports what happened when these tests were applied to
a corpus that had been assembled without them.

## 3.2 Mechanism as a two-part construct

The observation that makes this class tractable is that every
technique in it is an **asymmetry**: the attacker spends less to
send the input than the node spends to process it. Where there is
no asymmetry there is only bandwidth, and volumetric flooding is
not what this registry catalogues.

An asymmetry requires two things simultaneously. It requires a
**resource** that the node spends disproportionately, and it
requires the node's **bound on that resource to fail to apply**.
Node implementations are not naive; nearly all of them have limits
on message size, connection count, and request rate. A technique
exists because a specific limit did not cover a specific quantity
at a specific moment. That is the mechanism, and it is a pair:

> **mechanism = (exhausted resource, bound failure mode)**

Neither half is sufficient. The resource alone is the symptom, and
grouping by it produces the "memory exhaustion" bucket that fails
test 2. The bound failure alone is the defect class, which is what
CWE already indexes, and grouping by it detaches the technique
from what an operator actually loses. Taken together they are
predictive: they name the code property to audit and the
consequence of finding it.

The registry serves both halves on every technique, as `family`
and `bound_failure`.

### 3.2.1 The resource axis

Five resource classes cover the corpus. The first four are
exhaustion proper, in which the attacker's cost accumulates in the
victim; the fifth is availability loss with no accumulation at all.

**R1 - Retention.** Memory or persistent storage that the node
allocates and holds. Terminal state is allocator pressure, OOM
kill, or disk fill. The distinguishing feature is that the cost
survives the request that created it.

**R2 - Computation.** CPU cycles or thread occupancy consumed
during processing. Terminal state is processing stall, missed
deadlines, or blocked runtimes. The cost is spent and released;
what harms the node is the rate at which it can be re-imposed.

**R3 - Admission capacity.** A bounded count of accept-side slots:
sockets, streams, peer slots, subscriptions, concurrency permits.
The scarce quantity is a count, not bytes or cycles, and the harm
is denial of entry to legitimate peers rather than degradation of
the node itself. A node under R3 attack can be entirely healthy
and still useless.

**R4 - Egress.** Response traffic the node emits, in excess of
what the request justifies. The victim may be the node's own
uplink or, where the request is spoofable, a third party. This is
the only class where the node is a weapon as well as a target.

**R5 - Termination.** The node process ends, or enters an
unrecoverable state, as a direct consequence of processing a
single input. Nothing accumulates. The asymmetry is not a ratio
but a discontinuity: one packet, one node.

R5 sits alongside the exhaustion classes rather than inside them
because it inverts their economics. Defences that work against
R1 through R4, which are fundamentally about rate limits, quotas,
and admission control, do not work against R5 at all, because
there is no rate to limit. Conversely a bug that faults on a
malformed field is invisible to capacity planning.

### 3.2.2 The bound failure axis

Five bound failure modes account for the corpus. B1 through B4 are
the modes by which an existing or absent limit fails to contain an
accumulating cost; B5 is the mode in which no limit is relevant.
Registry values are given in brackets.

**B1 - No bound** (`no-bound`, 57 techniques). The accumulating
quantity has no limit. The node stores what it is sent for as long
as it is sent. *Audit question: which attacker-controlled
collections grow without a cap?*

**B2 - Mis-quantified bound** (`mis-quantified`, 8). A limit
exists, is enforced, and counts the wrong quantity. The classic
shapes are counting encoded bytes when the cost is in decoded
bytes, counting frame size when the cost is per-frame, and
counting connections when the cost is per-stream. *Audit question:
for each limit, is the counted quantity the same quantity that
generates the cost?*

**B3 - Late bound** (`late`, 7). The limit is correct and is
enforced after the cost has already been paid. Every
pre-authentication and pre-validation code path is a candidate.
*Audit question: what work happens before the first check that
could reject the input?*

**B4 - Mis-scoped bound** (`mis-scoped`, 3). The limit is correct
and is keyed on the wrong identity or granularity: per-connection
where the resource is global, or keyed on a value the attacker
chooses. *Audit question: for each quota, can the attacker mint
new keys?*

**B5 - Absent invariant** (`absent-invariant`, 22). No
accumulation is involved. An attacker-supplied value violates an
assumption the code did not check, and the process faults: an
unchecked index, a zero divisor, a non-UTF-8 byte sequence, an
unhandled enum variant. *Audit question: which attacker-controlled
values reach an operation that can panic?*

These five audit questions are the concrete discharge of test 2. A
family that inherits one of them tells a reader what to go and
look for in a codebase that has never been examined.

The registry enforces the one implication that holds between the
axes: `fault_termination` always carries `absent-invariant`, and
`absent-invariant` never appears on any other family. Nothing
accumulates in R5, so there is no bound that could have failed in
any other way.

### 3.2.3 The surface axis is not the family axis

Where the input arrives matters operationally: it determines who
can reach the defect and what mitigations are available at the
perimeter. The registry records it, as an attribute, over five
values: **P2P and gossip** (50 techniques), **RPC and public API**
(24), **consensus ingest** (21), **sync and state import** (1),
and **control plane** (1).

It is not the family axis, and the corpus shows why. `NRDAX-T0205`
(Bitcoin Core BIP-324 v2 transport, unauthenticated `ellswift`
ECDH plus HKDF-SHA256 before any rate limit), `NRDAX-T0100` (QUIC
INITIAL flood driving per-handshake x25519 and ed25519 before any
admission decision) and `NRDAX-T0206` (RLPx pre-auth packet flood)
are one mechanism cell, (R2, B3): an unauthenticated peer forces
asymmetric public-key work ahead of admission control. They arrive
on different transports against different chains.

Before this classification the three were split across two
families, because the labels in use mixed a mechanism axis with a
surface axis. A reader who patched one had no reason to look for
the others. They are now adjacent, and the audit question
generalises to every handshake in the corpus. Section 3.7 gives
the full account.

## 3.3 The families

Five mechanism families, each a region of the
(resource, bound failure) space. Populations are the live registry
as of 2026-07-24: 97 classified techniques.

---

### 3.3.1 memory_amp (33 techniques)

**Mechanism.** (R1, B1|B2|B3). Attacker input causes the node to
allocate memory or storage it does not release, at a cost to the
attacker far below the cost to the node.

**Discriminating criterion.** The cost **survives the request**.
If the allocation is freed when processing completes and the harm
is the rate of re-allocation, the technique is `compute_amp`. The
test is whether an attacker who stops sending leaves the node
degraded: for R1, yes.

**Representative techniques.**

- `NRDAX-T0106` header-length-preallocation-oom (B1): a declared
  length field pre-allocates the receive buffer before the body
  arrives. Reproduced on Bitcoin, libp2p, Monero and Zcash, which
  makes it the clearest instance of the family's chain-agnostic
  claim.
- `NRDAX-T0383` hpack-decoded-size-accounting-bypass (B2): the
  HPACK decoder bounds the header block on encoded bytes only,
  and cookie bytes escape the decoded-size accounting.
- `NRDAX-T0321` unbounded-connection-id-storage (B1): a flood of
  `NEW_CONNECTION_ID` frames on one established QUIC connection.
- `NRDAX-T0355` unvalidated-relay-map-memory-exhaustion (B1):
  pre-0.13.0 Bitcoin Core alert messages stored in an unbounded
  map.
- `NRDAX-T0131` invalid-message-log-flood (B1): storage rather
  than memory. Unconditional logging of PoW-invalid blocks fills
  disk, which is the same mechanism against a slower resource.

**Boundary.** Against `connection_exhaustion`: an attacker
occupying a connection slot also consumes per-connection memory,
so most R3 techniques have an R1 shadow. The tie-break is which
limit had to fail for the technique to work. If the connection
count limit was sufficient and the per-connection memory was not,
it is `memory_amp`; if the count limit itself was absent or
bypassable, it is `connection_exhaustion`.

---

### 3.3.2 compute_amp (24 techniques)

**Mechanism.** (R2, B1|B2|B3). Attacker input causes computation
disproportionate to the cost of sending it.

**Discriminating criterion.** The cost is **spent and released**.
The node recovers fully when the input stops. Against `memory_amp`
the test is the survival test above; against `response_amp` the
test is whether the disproportion is in cycles or in emitted
bytes.

**Representative techniques.**

- `NRDAX-T0205` pre-handshake-crypto-cpu-burn (B3): reproduced
  across nine substrates including Bitcoin, Cosmos, libp2p, XRP
  and Polygon PoS. The widest cross-implementation spread in the
  corpus, and the strongest single piece of evidence that the
  mechanism axis generalises.
- `NRDAX-T0139` legacy-sighash-quadratic-cpu-blowup (B1):
  many legacy-sighash inputs give quadratic validation cost with
  no peer penalty (CVE-2025-46598).
- `NRDAX-T0384` http2-continuation-frame-flood (B2): the
  header-list guard is size-based, so zero-length CONTINUATION
  frames never trip it and no count limit exists.
- `NRDAX-T0349` unseeded-hash-collision-dos (B1): QUIC Source
  Connection IDs crafted to collide in the server's unseeded hash
  table (CVE-2025-47200).
- `NRDAX-T0389` precompile-gas-underpricing-cpu-burn (B2): the
  BLAKE2F `rounds` field is charged flat per round against a cost
  that is not flat.

**Boundary.** Against R5: `NRDAX-T0166` (Move verifier fixpoint
non-termination) and `NRDAX-T0394` (connection-ID retirement
infinite loop) end in an unresponsive node, which resembles a
crash. They remain R2 because the node process is intact and the
condition is in principle recoverable by killing the work item.
A technique is R5 only when the process itself ends or enters an
unrecoverable state.

---

### 3.3.3 fault_termination (22 techniques)

**Mechanism.** (R5, B5). A single well-formed-enough input drives
the node into an unrecoverable fault, with no resource
accumulation required.

**Discriminating criterion.** **Nothing accumulates.** One message
is sufficient, and a defender who rate-limits the message still
has the fault reachable by a patient attacker. This is what
separates the family from every exhaustion family and why it is
worth naming: rate limits, quotas and admission control, which are
the standard mitigations for R1 through R4, do not touch it.

**Representative techniques**, spanning the range of unchecked
assumption:

- **Unchecked index.** `NRDAX-T0401`
  (boundary-check-off-by-one-index-oob-panic): a proposal-ingest
  path bounds-checks an attacker-supplied `signer` slot index with
  a strict `>` against the validator-set size. Reproduced on
  Cosmos and Nimiq.
- **Zero divisor.** `NRDAX-T0013`
  (bloom-filter-divide-by-zero-crash): an empty BIP37 bloom filter
  reaches a modulo in `CBloomFilter::Hash()` (CVE-2013-5700).
  `NRDAX-T0165` is the same shape in `x/group`
  `PercentageDecisionPolicy.Allow` with no `totalPower == 0` guard.
- **Type or encoding assumption.** `NRDAX-T0392`
  (invalid-utf8-decode-panic): a QUIC CONNECTION_CLOSE reason
  phrase is opaque bytes per RFC 9000 section 19.19, and is
  decoded directly into a Rust `str`. `NRDAX-T0417` is a malformed
  RLP field length in the conflux-rust light protocol.
- **Integer width.** `NRDAX-T0407`
  (signature-count-integer-overflow-panic): `Tx::verify_signatures`
  counts public keys with a u8-width counter.
- **Uninitialised state.** `NRDAX-T0399`: the libp2p AutoNAT v2
  server never initialises its per-peer rate-limiter map before
  use, and any well-formed inbound `DialRequest` panics on it.
- **Reachable assertion.** `NRDAX-T0024`
  (compact-block-fillblock-duplicate-crash): `FillBlock` called
  twice, assertion, node exit.

**Relationship to CWE.** It is easy to mistake this family for a
CWE re-labelling, and the distinction matters. CWE-617 (Reachable
Assertion), CWE-248 (Uncaught Exception), CWE-369 (Divide By Zero)
and CWE-129 (Improper Validation of Array Index) each name the
**defect**. `fault_termination` names the **attack**: the property
that an unauthenticated remote peer can reach that defect with one
message and remove a node from the network. The same CWE-129
defect behind an authenticated administrative interface is not a
member. Section 7 develops this.

**Boundary.** Against the exhaustion families, rule 1 of the
assignment procedure governs: termination dominates. `NRDAX-T0001`
(an `addr` flood overflowing a 32-bit `nIdCount` to an assertion
abort) accumulates first and terminates second, and is R5, because
rate-limiting `addr` leaves the assertion reachable.

---

### 3.3.4 connection_exhaustion (13 techniques)

**Mechanism.** (R3, B1|B4). The attacker occupies a bounded count
of accept-side slots, denying entry to legitimate peers.

**Discriminating criterion.** The scarce quantity is a **count of
admissions**, and the harm is exclusion rather than degradation.
A node fully exhausted in this sense may show normal CPU and
memory and still serve nobody.

**Representative techniques.**

- `NRDAX-T0320` unbounded-connection-flood (B1): unlimited
  CometBFT P2P connection requests, reproduced on seven
  substrates.
- `NRDAX-T0291` subscription-permit-exhaustion (B4): CometBFT
  caps subscription clients but keys the cap on
  `clientID = RemoteAddr(ip:port)`, so each new source port is a
  new client.
- `NRDAX-T0246` rate-limit-key-confusion (B4): a per-NodeId quota
  buckets under the carrier replica's own id rather than the
  sender's.
- `NRDAX-T0064` endpoint-concurrency-cap-exhaustion (B1):
  `grpc.NewServer` without `MaxConcurrentStreams`.

**Boundary.** Against `memory_amp`, see 3.3.1. Against
`compute_amp`: a handshake flood consumes both a slot and CPU. The
tie-break is which resource is exhausted first at the attacker's
achievable rate; where the reproduction measured this, the
measurement governs. Five of this family's members carry a
`dual_with` marking against `memory_amp` for exactly this reason.

---

### 3.3.5 response_amp (5 techniques)

**Mechanism.** (R4, B1|B2|B3). The node emits response traffic
disproportionate to the request that provoked it.

**Discriminating criterion.** The disproportion is measured in
**bytes leaving the node**. Where the request is spoofable and the
protocol is connectionless, the node becomes a reflector and the
victim is a third party; where it is not, the victim is the node's
own uplink. Both are R4.

**Representative techniques.**

- `NRDAX-T0280` spoofed-endpoint-proof-bypass-amplification (B3):
  discv4 FINDNODE-to-NEIGHBORS reflection, the textbook
  connectionless amplifier, with the endpoint proof checked after
  the reply is emitted.
- `NRDAX-T0345` unrated-getheaders-response-flood (B1):
  un-rate-limited `getheaders` producing in excess of 100 MB/s of
  upload (CVE-2023-33297).
- `NRDAX-T0329` unbounded-rpc-response-amplification (B1):
  batched account-lookup RPC with no response-size accounting,
  reproduced across seven chains.
- `NRDAX-T0182` optimistic-ack-congestion-window-manipulation
  (B1): optimistic ACKs drive the victim's own send rate up. The
  node is made to spend its egress against itself.

This is the smallest family, and three of its five members
(`NRDAX-T0124`, `NRDAX-T0182`, `NRDAX-T0280`) were previously
filed under `memory_amp`. Section 3.7 records why.

---

## 3.4 Assignment procedure

Where a technique satisfies more than one definition, the
following rules decide it, applied in order. They are stated as a
procedure rather than as guidance so that assignment is
reproducible by a reader.

1. **Termination dominates.** If the node process ends or enters
   an unrecoverable state, the family is `fault_termination`,
   regardless of what was consumed on the way.
2. **Binding constraint decides among R1 to R4.** Where several
   resources are consumed, the family is the one whose limit is
   reached first at the attacker's achievable rate. Where the
   reproduction measured this, the measurement governs.
3. **Survival test separates R1 from R2.** If an attacker who
   stops sending leaves the node degraded, R1. If the node
   recovers, R2.
4. **Exclusion test separates R3.** If the node is healthy on
   every internal metric and still cannot serve new peers, R3.
5. **Guard bypass never decides a family.** It is recorded as a
   bound failure mode (B2, B3 or B4). The family is decided by
   what the bypass yields.
6. **Surface never decides a family.** It is recorded on the
   `surface` attribute.
7. **Unresolved ties are recorded, not broken.** Thirteen of the
   97 classified techniques carry a `dual_with` marking: they are
   genuinely dual under rules 2 to 4 and no reproduction measured
   which resource binds first. `NRDAX-T0099`
   (half-open-handshake-slowloris, described in its own mechanism
   text as a "memory pin") consumes a handshake slot and pins
   memory. Forcing such a technique would make the taxonomy look
   cleaner than the evidence supports.

## 3.5 Coverage and what is not classified

Of 420 published techniques, 97 carry a mechanism family and 323
do not. The registry serves the unclassified ones as
`family: null` with `classification: "pending"`, and never infers
a mechanism from any other field. The 323 divide into two groups.

**309 are known-but-not-reproduced.** They enter the registry from
a public advisory naming a defect in a node implementation, with
no reproduction on file. A mechanism is read off a reproduction:
what a technique exhausts, and which bound failed, are observed
during the reproduction and not restated from the advisory text.
Without one there is no mechanism evidence to classify on, so
these carry only the producing pipeline's coarse class
(`network-p2p`, `network-rpc`, `consensus` and six others). The
registry enforces this: a classification for a technique with no
instance fails the build. This is what "grounded in reproduction
rather than report" means operationally, and it is the reason the
classified corpus is a fifth of the published one.

**14 are out of scope**, and section 3.7 covers them.

We report the gap as a number rather than closing it by mapping
the coarse classes onto mechanism families. Such a map would be
mechanical and, for the surface-defined labels, silently wrong,
which is the failure this classification exists to correct.

## 3.6 Worked boundary cases

**Three techniques, one mechanism, previously two families.**
`NRDAX-T0205`, `NRDAX-T0100` and `NRDAX-T0206` are all (R2, B3):
unauthenticated public-key work ahead of admission control. They
were filed under `compute_amp`, `connection_exhaustion` and
`connection_exhaustion` respectively. `NRDAX-T0100`'s own recorded
mechanism describes it as "compute-bound, distinct from the
connection-slot flood" - it disclaimed the family it was filed
under. Under rules 2 and 6 all three are `compute_amp`, which is
what the registry now serves.

**One name, two resources.** `NRDAX-T0408` was filed under
`memory_amp` and named
`unbounded-address-list-validation-cpu-exhaustion`. Its mechanism
is an unbounded address list de-duplicated via a map during
`ValidateBasic()` in `CheckTx`, before antehandler signature
verification: a clean B3. Rule 2 governs, because the mempool
map-operation slowdown is what propagates to every node that
receives the transaction, so it is `compute_amp` with `dual_with:
memory_amp`. Symmetrically `NRDAX-T0328` was filed under
`compute_amp` and named `unbounded-request-body-memory-exhaustion`;
it is R1.

**Amplification filed as retention.** `NRDAX-T0280` (discv4
reflection), `NRDAX-T0124` (an INV flood provoking 50k
`getheaders` replies) and `NRDAX-T0182` (optimistic-ACK congestion
window growth) were all in `memory_amp`. All three are R4, and
moving them more than doubled `response_amp`.

**Crash filed as CPU.** `NRDAX-T0142`
(malformed-bytecode-index-panic) was the sole member of a family
named `rpc_handler_cpu`, which asserts a CPU mechanism. Its
mechanism is an index panic crashing the RPC service: R5. A family
of one, whose one member contradicted its name.

## 3.7 What the reclassification found

The 97 classified techniques were assigned against each
technique's own recorded mechanism text, not against its existing
label. Forty landed in a different family from the one they had
been filed under. The pattern in those forty is the substantive
result of this section, because it says what a taxonomy assembled
without the tests in 3.1 gets wrong.

**A mechanism class with no name (22 techniques).** Every
`fault_termination` member came from somewhere else, distributed
across seven families:

| Previous family | Moved to `fault_termination` |
|---|---:|
| `compute_amp` | 12 |
| `consensus_abuse` | 4 |
| `gossip_abuse` | 2 |
| `connection_exhaustion` | 1 |
| `rpc_handler_cpu` | 1 |
| `state_import_abuse` | 1 |
| `protocol_logic_exploit` | 1 |
| **Total** | **22** |

The old vocabulary had no name for "one input, one dead node",
so each such technique was filed under whichever resource family
its incidental details most resembled, and one was filed in a
residual bucket that existed for no other purpose. Twenty per cent
of the classified corpus shares a mechanism, and a defender
reading the old taxonomy could not have discovered that.

**Mixed axes (13 techniques).** Three of the old families were
defined by entry surface (`gossip_abuse`, `consensus_abuse`,
`state_import_abuse`) and three by a guard rather than a resource
(`auth_bypass`, `rate_limiter_bypass`, `service_misconfig`). The
surface-defined ones admitted anything arriving on that surface,
whatever the mechanism: `gossip_abuse` held members in R1, R2, R3
and R5. The guard-defined ones held exactly one technique each,
which is what happens when a category sits on a different axis
from everything around it: nothing can join it without leaving its
own resource class. A bypass is a meta-mechanism, so it is now a
`bound_failure` value and each technique is filed by what the
bypass yields. `NRDAX-T0396` (h2c multiplexing rate-limit bypass)
is B2 on the limiter and `compute_amp` in what it delivers.

**Corrections within the resource axis (5 techniques).** The three
egress techniques above, plus `NRDAX-T0408` and `NRDAX-T0328`
swapping places.

**Out of the class entirely (14 techniques).** Reproduced,
published, but their harm is consensus divergence
(`NRDAX-T0307` transaction malleability, `NRDAX-T0411` a
SIGHASH_SINGLE index gap producing a block-template divergence
between defective and spec-compliant nodes), censorship
(`NRDAX-T0050` DHT Sybil content censorship), propagation delay,
or credential compromise (`NRDAX-T0317`, an unauthenticated
`personal` namespace, whose outcome is fund theft rather than node
availability). Seven came from `consensus_abuse` and four from
`gossip_abuse` - again, what a surface-defined family does.

They are tombstoned rather than removed, following the same
precedent as the economic and bridge classes: the identifier stays
resolvable, every export flags it, and a MITRE AADAPT crosswalk
points at the right registry where an honest equivalent exists
(`NRDAX-T0317` to ADT1552 Unsecured Credentials; the
consensus-divergence records to ADT3007 Exploit Consensus Logic).
Thirty-one techniques are now tombstoned in total. A tombstoned
technique carries no mechanism family, because it is outside the
class the taxonomy classifies: a category error, not a gap.

### 3.7.1 What this supports, and what it does not

The mechanism axis classified 97 of 97 in-scope reproduced
techniques without extension, resolved every boundary case in 3.6
by a written rule, and produced cross-implementation groupings
that no per-project CVE list produces: `NRDAX-T0205` across nine
substrates, `NRDAX-T0320` across seven, `NRDAX-T0106` across four.
Section 6 develops those groupings.

It does not support a claim of settled coverage. Three quarters of
the published registry carries no mechanism family, because three
quarters of it has not been reproduced. Five families is a small
taxonomy, and a corpus five times the size would likely need more.
Thirteen techniques could not be resolved to a single family at
all and are marked dual. And the classification is one team's
reading of its own reproductions, which section 8 addresses
directly.

What the reclassification does establish is that the criteria in
3.1 have teeth. They were sharp enough to find a mechanism class
that 22 techniques shared and no label named, six categories that
were not mechanisms at all, five misfiled resource assignments,
and fourteen records outside the declared class - in a corpus that
had been assembled, published and served without them.
