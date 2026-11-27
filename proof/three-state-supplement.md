# Q820 supplement: a three-state counterexample

This improves the four-state witness in the original project packet #43. It is a refinement of the same result, not a new numbered solve, a first resolution of the qualitative question, or a minimality claim.

## Exact target

Henzinger, Prakash and Thejaswini, *Resolving Nondeterminism with Randomness*, [MFCS 2025 final, §6, p. 57:16 (PDF p. 16)](https://drops.dagstuhl.de/storage/00lipics/lipics-vol345-mfcs2025/LIPIcs.MFCS.2025.57/LIPIcs.MFCS.2025.57.pdf#page=16): “Are almost-sure resolvers in stochastically resolvable settings indifferent to the exact probability distribution?” The same question appears in [author v1, §6, p. 19](https://arxiv.org/pdf/2502.12872v1#page=19). The word is fixed independently of resolver randomness; no adaptive opponent is used.

## Construction

States: S, R, D, initially D. Alphabet: a and #. Maximum priority seen infinitely often determines parity, accepting if even. Both resolvers use all edges, independent random choices on successive transitions, and no extra memory.

- On a the successor lists from S, R and D are (S,R,D), (R,D) and (D). Every such edge has priority 0.
- On # every state resets fairly to S or R. Both edges from S have priority 2, both from R priority 1, and both from D priority 0.
- U is uniform on every row. G differs only in the (S,a) row, where the probabilities of (S,R,D) are (2/3,1/6,1/6). Every listed edge has positive probability under both.

For any fixed word with finitely many # symbols, the tail uses only priority 0. For infinitely many separators, discard the first separator and write subsequent blocks as a^n# with n≥0. The closing priority of each such block depends only on the fair reset at its start and the independent a-choices inside the block; the separator at its end uses the source state, not the fresh reset. Thus the closing-priority variables of these blocks are independent, including consecutive separators.

Under G the row distribution (1/2,1/2) on S and R is a left eigenvector of the surviving two-state substochastic matrix [[2/3,1/6],[0,1/2]], with eigenvalue 2/3. Hence the probabilities of closing with priorities 2 and 1 are both (2/3)^n/2. If their common sum over blocks is finite, both priorities occur only finitely often by the first Borel–Cantelli lemma, leaving priority 0. If the sum is infinite, priority 2 occurs infinitely often almost surely by independence and the second lemma. This proves probability-one acceptance for each fixed word; in particular a supported accepting run exists for every word.

Under U, after n a's, let s_n and r_n be the S and R masses. Then s_(n+1)=s_n/3 and r_(n+1)=s_n/3+r_n/2 with initial masses 1/2,1/2. Solving gives s_n=3^(−n)/2 and r_n=3·2^(−n)/2−3^(−n)≥2^(−n)/2. On the fixed word starting with # and then containing 2^n blocks a^n# for successive n=1,2,…, the sum of priority-2 probabilities is finite, while the sum of priority-1 probabilities diverges. The two Borel–Cantelli lemmas imply almost-sure rejection. Thus U fails despite sharing the full support of G and changing only one row.

## Prior work and scope

The original [tagged release](https://github.com/DannyExperiments/same-support-parity-resolvers/releases/tag/v1.0.0) remains unchanged. Its [public literature audit](https://github.com/DannyExperiments/same-support-parity-resolvers/blob/v1.0.0/audits/public_safe_reports/LITERATURE.md) explains why the broad negative answer is already derivable from [Baier, Bertrand and Größer, Lemmas 3.6 and 3.9 and Theorem 3.12](https://arxiv.org/html/0907.4760), using the [support-preserving zero–one construction](https://wwwtcs.inf.tu-dresden.de/ALGI/PUB/thesis_groesser.pdf) and a Boolean product and finite parity monitor. In brief: choose two common-support parameter values with different positive languages; obtain zero–one Rabin languages without changing support between parameter choices; use the product objective “first accepts or second rejects.” Equal parameters then accept every fixed word almost surely, whereas appropriate unequal parameters reject a word in the difference. This yields the qualitative counterexample, not the three-state, single-row, uniform-resolver parameters above. The contribution here is the smaller explicit example and its exact analysis. No novelty or smallest-size certification. Checked November 27, 2026 UTC.
