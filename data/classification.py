"""The curated mechanism classification of the reproduced NRDAX corpus.

Each entry is (technique_id, mechanism family, surface, bound-failure mode,
dual_with or None, note or None), assigned against the technique's own recorded
mechanism text in the registry.

A mechanism is the pair (resource exhausted, bound-failure mode). The family names
the resource half; bound_failure names why the node's limit did not apply, and is
the half that carries the audit question. Surface is recorded but never decides a
family: the same mechanism arrives on different surfaces, and grouping by surface
is what separated techniques that share a defect.

`dual_with` marks a technique that is genuinely dual, where no reproduction measured
which resource binds first. Marked rather than forced: a taxonomy that looks cleaner
than its evidence is worse than one that admits the tie.

The 14 techniques outside the network-boundary / node-resource class are NOT here.
They are tombstoned instead, following the economic-defi/bridge precedent.

Convention for surface on shared substrates: QUIC transport defects are p2p-gossip;
HTTP/2 and HTTP/3 codec defects are rpc-api, because that codec fronts the node's
RPC surface.
"""

# (id, family, surface, bound_failure, dual_with, note)
CLASSIFICATION = [
    # ── from producer family memory_amp (35 of 36; T0292 tombstoned) ────────────
    ("NRDAX-T0023", "memory_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0025", "memory_amp", "p2p-gossip", "mis-quantified", None,
     "The size calculation itself overflows 32 bits, so the bound is computed on a wrapped value."),
    ("NRDAX-T0038", "memory_amp", "p2p-gossip", "mis-quantified", "response_amp",
     "count-1 underflows past maxHeadersServe; the node then both allocates and emits without bound."),
    ("NRDAX-T0042", "memory_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0046", "memory_amp", "rpc-api", "mis-quantified", None,
     "Bounded on compressed bytes; the cost is in decompressed bytes."),
    ("NRDAX-T0059", "memory_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0061", "memory_amp", "consensus-ingest", "no-bound", None, None),
    ("NRDAX-T0071", "memory_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0095", "memory_amp", "rpc-api", "no-bound", "compute_amp",
     "Each alias drives a full-chain scan: unbounded in both allocation and cycles."),
    ("NRDAX-T0097", "memory_amp", "rpc-api", "no-bound", None, None),
    ("NRDAX-T0106", "memory_amp", "p2p-gossip", "no-bound", None,
     "Reproduced on Bitcoin, libp2p, Monero and Zcash: the family's clearest chain-agnostic claim."),
    ("NRDAX-T0112", "memory_amp", "rpc-api", "no-bound", None, None),
    ("NRDAX-T0124", "response_amp", "p2p-gossip", "no-bound", None,
     "Reclassified from memory_amp: 50k provoked getheaders replies is egress, not retention."),
    ("NRDAX-T0131", "memory_amp", "p2p-gossip", "no-bound", None,
     "Storage rather than memory: unconditional logging of PoW-invalid blocks fills disk."),
    ("NRDAX-T0156", "memory_amp", "consensus-ingest", "mis-scoped", None,
     "The per-account bound does not cover the pending-eviction path."),
    ("NRDAX-T0182", "response_amp", "p2p-gossip", "no-bound", None,
     "Reclassified from memory_amp: optimistic ACKs drive the victim's own send rate up."),
    ("NRDAX-T0185", "memory_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0187", "memory_amp", "consensus-ingest", "no-bound", None, None),
    ("NRDAX-T0195", "memory_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0196", "memory_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0203", "memory_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0280", "response_amp", "p2p-gossip", "late", None,
     "Reclassified from memory_amp: discv4 FINDNODE/NEIGHBORS reflection, the textbook "
     "connectionless amplifier. The endpoint proof is checked after the reply is emitted."),
    ("NRDAX-T0321", "memory_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0327", "memory_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0351", "memory_amp", "p2p-gossip", "no-bound", None,
     "Persisted rather than held: unvalidated DHT records reach storage."),
    ("NRDAX-T0353", "memory_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0354", "memory_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0355", "memory_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0369", "connection_exhaustion", "rpc-api", "no-bound", "memory_amp",
     "Unbounded task spawn on slow-read: an admission count with a retention shadow."),
    ("NRDAX-T0382", "memory_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0383", "memory_amp", "rpc-api", "mis-quantified", None,
     "The HPACK bound counts encoded bytes; cookie bytes escape the decoded-size accounting."),
    ("NRDAX-T0386", "memory_amp", "rpc-api", "no-bound", None, None),
    ("NRDAX-T0387", "memory_amp", "rpc-api", "no-bound", None, None),
    ("NRDAX-T0388", "memory_amp", "rpc-api", "no-bound", None,
     "Insecure default: maxHeaderListSize defaults to the RFC 9114 ceiling."),
    ("NRDAX-T0408", "compute_amp", "consensus-ingest", "late", "memory_amp",
     "Reclassified from memory_amp: ValidateBasic runs in CheckTx before signature "
     "verification, and the map-operation slowdown propagates to every receiving node."),

    # ── from producer family compute_amp (27 of 27) ─────────────────────────────
    ("NRDAX-T0005", "fault_termination", "p2p-gossip", "absent-invariant", None, None),
    ("NRDAX-T0006", "compute_amp", "rpc-api", "no-bound", None,
     "The BPF VM runs synchronously on the calling Tokio worker; no spawn_blocking interposed."),
    ("NRDAX-T0013", "fault_termination", "p2p-gossip", "absent-invariant", None,
     "Zero divisor: an empty BIP37 filter reaches a modulo in CBloomFilter::Hash()."),
    ("NRDAX-T0076", "compute_amp", "rpc-api", "no-bound", None, None),
    ("NRDAX-T0101", "fault_termination", "p2p-gossip", "absent-invariant", None, None),
    ("NRDAX-T0122", "fault_termination", "consensus-ingest", "absent-invariant", None, None),
    ("NRDAX-T0129", "fault_termination", "consensus-ingest", "absent-invariant", None,
     "The identity point is canonical and spec-permitted, so it parses and then panics."),
    ("NRDAX-T0139", "compute_amp", "consensus-ingest", "no-bound", None,
     "Quadratic legacy-sighash validation with no peer penalty."),
    ("NRDAX-T0148", "compute_amp", "consensus-ingest", "no-bound", None, None),
    ("NRDAX-T0166", "compute_amp", "consensus-ingest", "no-bound", None,
     "Non-termination, not a crash: the process is intact and the work item is killable."),
    ("NRDAX-T0171", "fault_termination", "p2p-gossip", "absent-invariant", None, None),
    ("NRDAX-T0184", "compute_amp", "consensus-ingest", "no-bound", None, None),
    ("NRDAX-T0198", "compute_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0205", "compute_amp", "p2p-gossip", "late", None,
     "Unauthenticated ellswift ECDH + HKDF before any auth or rate limit. Reproduced on nine "
     "substrates: the widest cross-implementation spread in the corpus."),
    ("NRDAX-T0249", "fault_termination", "consensus-ingest", "absent-invariant", "compute_amp",
     "Stack overflow dominates, but deep nesting also costs exponential CPU pre-validation."),
    ("NRDAX-T0254", "compute_amp", "p2p-gossip", "no-bound", "connection_exhaustion", None),
    ("NRDAX-T0328", "memory_amp", "rpc-api", "no-bound", None,
     "Reclassified from compute_amp: attesting_indices is capped only structurally."),
    ("NRDAX-T0342", "compute_amp", "rpc-api", "no-bound", None, None),
    ("NRDAX-T0349", "compute_amp", "p2p-gossip", "no-bound", None,
     "Crafted colliding SCIDs defeat the unseeded hash table's expected constant-time lookup."),
    ("NRDAX-T0384", "compute_amp", "rpc-api", "mis-quantified", None,
     "The guard is size-based, so zero-length CONTINUATION frames never trip it; no count limit exists."),
    ("NRDAX-T0389", "compute_amp", "consensus-ingest", "mis-quantified", None,
     "BLAKE2F rounds are charged flat per round against a cost that is not flat."),
    ("NRDAX-T0394", "compute_amp", "p2p-gossip", "no-bound", None,
     "Non-termination, not a crash: the retirement handler fails to converge."),
    ("NRDAX-T0399", "fault_termination", "p2p-gossip", "absent-invariant", None,
     "Uninitialised state: the AutoNAT v2 per-peer rate-limiter map is never initialised before use."),
    ("NRDAX-T0400", "fault_termination", "p2p-gossip", "absent-invariant", None, None),
    ("NRDAX-T0401", "fault_termination", "consensus-ingest", "absent-invariant", None,
     "Unchecked index: a strict > bounds-check on an attacker-supplied signer slot index."),
    ("NRDAX-T0407", "fault_termination", "consensus-ingest", "absent-invariant", None,
     "Integer width: verify_signatures counts public keys with a u8-width counter."),
    ("NRDAX-T0417", "fault_termination", "p2p-gossip", "absent-invariant", None, None),

    # ── from producer family connection_exhaustion (15 of 16; T0275 tombstoned) ─
    ("NRDAX-T0041", "connection_exhaustion", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0064", "connection_exhaustion", "rpc-api", "no-bound", None,
     "grpc.NewServer without MaxConcurrentStreams and no SETTINGS_MAX_CONCURRENT_STREAMS."),
    ("NRDAX-T0088", "compute_amp", "p2p-gossip", "no-bound", "response_amp", None),
    ("NRDAX-T0099", "connection_exhaustion", "p2p-gossip", "no-bound", "memory_amp",
     "Half-open handshake slots and pinned memory; no reproduction measured which binds first."),
    ("NRDAX-T0100", "compute_amp", "p2p-gossip", "late", None,
     "Reclassified from connection_exhaustion: its own mechanism text records it as "
     "compute-bound and distinct from the connection-slot flood. Same mechanism cell as T0205."),
    ("NRDAX-T0145", "fault_termination", "rpc-api", "absent-invariant", None,
     "Reclassified from connection_exhaustion: a failed body read is treated as unrecoverable."),
    ("NRDAX-T0206", "compute_amp", "p2p-gossip", "late", None,
     "Reclassified from connection_exhaustion: RLPx pre-auth work. Third member of the T0205 cell."),
    ("NRDAX-T0214", "connection_exhaustion", "p2p-gossip", "no-bound", "memory_amp", None),
    ("NRDAX-T0225", "connection_exhaustion", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0246", "connection_exhaustion", "rpc-api", "mis-scoped", None,
     "The per-NodeId quota buckets under the carrier replica's own id, not the sender's."),
    ("NRDAX-T0261", "connection_exhaustion", "rpc-api", "no-bound", "compute_amp", None),
    ("NRDAX-T0291", "connection_exhaustion", "rpc-api", "mis-scoped", None,
     "The subscription cap keys on RemoteAddr(ip:port), so each new source port is a new client."),
    ("NRDAX-T0320", "connection_exhaustion", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0331", "connection_exhaustion", "p2p-gossip", "no-bound", "memory_amp", None),
    ("NRDAX-T0333", "connection_exhaustion", "rpc-api", "no-bound", None, None),

    # ── from producer family consensus_abuse (6 of 13; 7 tombstoned) ────────────
    ("NRDAX-T0024", "fault_termination", "consensus-ingest", "absent-invariant", None,
     "Reachable assertion: FillBlock called twice, assertion, node exit."),
    ("NRDAX-T0056", "fault_termination", "consensus-ingest", "absent-invariant", None, None),
    ("NRDAX-T0143", "compute_amp", "consensus-ingest", "late", None, None),
    ("NRDAX-T0165", "fault_termination", "consensus-ingest", "absent-invariant", None,
     "Zero divisor: PercentageDecisionPolicy.Allow divides with no totalPower == 0 guard."),
    ("NRDAX-T0207", "compute_amp", "consensus-ingest", "late", None,
     "The RLock and queue path runs before deferred signature verification."),
    ("NRDAX-T0211", "fault_termination", "consensus-ingest", "absent-invariant", None,
     "The vote extension is handled before the ValidatorIndex is verified."),

    # ── from producer family gossip_abuse (6 of 10; 4 tombstoned) ───────────────
    ("NRDAX-T0001", "fault_termination", "p2p-gossip", "absent-invariant", None,
     "Accumulates first and terminates second. Rule 1: termination dominates, because "
     "rate-limiting addr still leaves the assertion reachable by a patient attacker."),
    ("NRDAX-T0120", "fault_termination", "p2p-gossip", "absent-invariant", None, None),
    ("NRDAX-T0188", "compute_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0192", "memory_amp", "consensus-ingest", "mis-quantified", "compute_amp",
     "Max transaction size was raised to the full block size after Sapling."),
    ("NRDAX-T0199", "memory_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0326", "connection_exhaustion", "p2p-gossip", "no-bound", None, None),

    # ── from the singleton families (all retired into the mechanism axis) ───────
    ("NRDAX-T0329", "response_amp", "rpc-api", "no-bound", None,
     "No response-size accounting or cost weighting on batched account lookups."),
    ("NRDAX-T0345", "response_amp", "p2p-gossip", "no-bound", None, None),
    ("NRDAX-T0142", "fault_termination", "rpc-api", "absent-invariant", None,
     "Retires rpc_handler_cpu: its only member was a crash, not a CPU mechanism."),
    ("NRDAX-T0248", "compute_amp", "rpc-api", "no-bound", None,
     "Retires subscription_cpu_amp: compute_amp with surface = rpc-api."),
    ("NRDAX-T0352", "fault_termination", "sync-state-import", "absent-invariant", None,
     "Retires state_import_abuse into the mechanism axis; the surface it named is recorded here."),
    ("NRDAX-T0392", "fault_termination", "p2p-gossip", "absent-invariant", None,
     "Retires protocol_logic_exploit: the residual bucket existed only because there was "
     "no fault_termination family to hold this."),
    ("NRDAX-T0396", "compute_amp", "rpc-api", "mis-quantified", "response_amp",
     "Retires rate_limiter_bypass. The limiter counts h2c connections at layer 4 while the "
     "backend honours every multiplexed stream. Filed by what the bypass yields, not by the guard."),
    ("NRDAX-T0398", "compute_amp", "control-plane", "no-bound", None,
     "Retires service_misconfig. No auth, no per-IP limit, no concurrency cap: filed by the "
     "compute the absent admission control yields."),
]

# The 14 outside the network-boundary / node-resource class, with an AADAPT crosswalk
# where an honest equivalent exists and None where it does not. Never fabricated.
TOMBSTONE = [
    ("NRDAX-T0202", None, None, "Timejacking: consensus safety, not node resource loss."),
    ("NRDAX-T0298", "ADT3003", "Chain Reorganization",
     "Timestamp overflow driving a netsplit: consensus safety."),
    ("NRDAX-T0307", None, None, "Transaction malleability: consensus safety."),
    ("NRDAX-T0350", None, None, "Block-download state poisoning: propagation delay, not resource loss."),
    ("NRDAX-T0409", "ADT3007", "Exploit Consensus Logic",
     "Blocked-address validation bypass in x/auth/vesting: application-level access control."),
    ("NRDAX-T0411", "ADT3007", "Exploit Consensus Logic",
     "SIGHASH_SINGLE index gap: block-template divergence between defective and compliant nodes."),
    ("NRDAX-T0414", "ADT3007", "Exploit Consensus Logic",
     "Invalid sighash-type gap: consensus divergence."),
    ("NRDAX-T0050", None, None, "DHT Sybil content censorship: censorship, not resource loss."),
    ("NRDAX-T0295", None, None, "Sync-state poisoning via fake blocks: liveness/logic, not resource loss."),
    ("NRDAX-T0312", None, None, "Transaction-relay throughput jamming: an off-chain relay protocol attack."),
    ("NRDAX-T0403", None, None, "DHT first-record verification bypass: a verification logic gap."),
    ("NRDAX-T0275", None, None, "Single-peer block-discovery stall: propagation delay, not resource loss."),
    ("NRDAX-T0292", None, None, "Sync-height manipulation stall: liveness, not resource loss."),
    ("NRDAX-T0317", "ADT1552", "Unsecured Credentials",
     "Unauthenticated personal namespace with an unlockable account: the outcome is key "
     "compromise and fund theft, not node availability."),
]
