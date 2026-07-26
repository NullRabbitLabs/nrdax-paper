# 10. Conclusion

The hypothesis this work is organised around is narrow enough to be wrong:
**mechanism, and not implementation, is the unit that transfers across node
implementations of decentralised protocols.**

If it holds, a finding against one codebase carries information about others, and
the right thing to index is the mechanism. If it fails, the class really is a
list of per-project bugs, and a per-project bug tracker was the correct
representation all along.

Our contribution is not a proof of the hypothesis. It is a definition sharp
enough to test it, and a registry that operationalises the definition in a form
other people can check.

**The definition.** A mechanism is a pair: the resource a node spends
disproportionately, and the way its bound on that resource failed to apply.
Neither half suffices. The resource alone is the symptom that per-project
advisories already record; the bound failure alone is the defect class CWE
already indexes. Together they name both what an operator loses and the code
property that permitted it, and the second is what an engineer can go and look
for somewhere else.

**What the corpus supports.** Applying that definition to 97 reproduced
techniques moved 40 of them, surfaced a mechanism 22 techniques shared that the
previous vocabulary could not name, and grouped three techniques spanning 18
targets into a single cell that had been split across two families. Twenty-three
mechanisms recur across more than one chain deployment. Those are real results
and they are the strongest ones we have.

**What it does not support.** It does not support a rate. Multi-target techniques
are largely the ones we pursued across targets, which confounds recurrence in the
flattering direction (section 6.2). It does not support an independence count
beyond a single curated case: `NRDAX-T0100`'s nine chain deployments proved to be
four independently written handshake stacks, and for every other technique the
registry reports a lower bound because lineage is uncurated (sections 6.1.2,
8.4). And it does not support a claim that the audit questions transfer as a
matter of course: two techniques were found because a mechanism had been
characterised elsewhere, which is an existence proof and not a property
(section 6.1.4).

**What would test it properly.** Not more analysis of this corpus. The confounds
are structural and no amount of re-cutting the same 199 instances removes them.
The test is prospective: take one cell's audit question, apply it to an
implementation that is not in the corpus and was not chosen because it looked
promising, and report the outcome either way. A pre-registered prediction, a
codebase picked before the prediction, and a published negative if it fails. We
have not run that test, and until someone does, mechanism-as-transferable-unit
remains a hypothesis that the corpus is consistent with rather than one the
corpus establishes.

We have tried throughout to leave the registry in a state where that test is
possible for someone other than us: permanent identifiers that survive
reclassification, both taxonomy axes served separately so neither has to be
inferred, gaps published as numbers rather than closed by inference, and the
per-technique assignment shipped as data so a disagreement can be raised against
a specific identifier. A companion line of work applying machine learning to
detection in this class reported its central claim falsified at a pre-registered
gate, and that result stands unrevised in section 8.10. We would rather this
paper's central claim were tested the same way and failed than repeated
untested.
