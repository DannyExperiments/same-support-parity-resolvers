# Q820: Keeping exactly the same transitions does not preserve an almost-sure resolver

## Source and exact question

Thomas A. Henzinger, Keya Prakash and K. S. Thejaswini, *Resolving Nondeterminism with Randomness*, MFCS 2025, [§6, first question, printed p. 57:16 (PDF p. 16)](https://drops.dagstuhl.de/storage/00lipics/lipics-vol345-mfcs2025/LIPIcs.MFCS.2025.57/LIPIcs.MFCS.2025.57.pdf#page=16):

> Are almost-sure resolvers in stochastically resolvable settings indifferent to the exact probability distribution?

The [author preprint record](https://arxiv.org/abs/2502.12872) lists only v1. Its [§6 (PDF p. 19)](https://arxiv.org/pdf/2502.12872v1#page=19) retains the same question. In the stochastic setting the complete infinite input word is fixed independently of the random choices; an almost-sure resolver must accept each word of the nondeterministic automaton's language with probability one.

## Four-state counterexample

The alphabet is {a,#}, the states are S,R,D1,D2, and the initial state is D1. Parity uses the maximum priority appearing infinitely often. Here is the complete list of transitions, with no parallel edges:

| Source | On a, successors (priority 0) | On #, successors | Priority of both # edges |
|---|---|---|---|
| S | S,D1,D2 | S,R | 2 |
| R | R,D1 | S,R | 1 |
| D1 | D1 | S,R | 0 |
| D2 | D2 | S,R | 0 |

Resolver G chooses uniformly at every row of state and letter except (S,a), where it gives probabilities (1/2,1/4,1/4) to (S,D1,D2). Resolver U chooses uniformly everywhere. Both are memoryless, and every transition has positive probability under both.

A word with finitely many # symbols has eventually only priority 0, so is accepted certainly by both. If there are infinitely many # symbols, ignore the prefix through the first # for parity. Each following block consists of n≥0 a's followed by #. The random choice of successor at the preceding # is uniform in S,R, independent of the source and all previous random choices. The priority on that preceding # is determined by its source and does not depend on its chosen successor. Consequently complete blocks have independent emitted priorities: to generate the priority for a block use only the coin at the preceding # and the independent choices on its a's. Under G the probabilities of priority 2 and of priority 1 are both (1/2)2^(−n). If the sum for one is finite, both are finite and each of these priorities occurs only finitely often almost surely, by the first Borel–Cantelli lemma. If the sum diverges, priority 2 occurs infinitely often almost surely, by the second Borel–Cantelli lemma. In both cases the run accepts almost surely. This works for every fixed word, including consecutive # symbols. It also implies the underlying nondeterministic language is universal, as a set of accepting runs of probability one is nonempty.

Under U the block probability for priority 1 stays (1/2)2^(−n), but that for 2 is (1/2)3^(−n). Use the fixed infinite word starting with # and then, for each n=1,2,… in order, 2^n copies of a^n#. The sum for priority 1 is ∑_n 1/2=∞, while that for priority 2 is (1/2)∑_n(2/3)^n<∞. Thus priority 1 occurs infinitely often and 2 only finitely often, almost surely. U rejects this accepted word with probability one. This disproves support-only invariance and also disproves uniform reweighting as a way to keep the same successful support.
