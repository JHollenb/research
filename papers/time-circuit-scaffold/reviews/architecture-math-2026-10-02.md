---
title: "Mathematical account of the time-scaffold architecture"
type: coordinator-math
date: 2026-10-02
companion: architecture-brief-2026-10-02.md
sources: saturn/experiments/2026-10-01-scaffold-graph-identification/MATH.md; saturn/experiments/2026-10-02-mamba-operation-clock-debugger/MATH.md; research/demos/docs/scene-generator-paper.md; research/papers/space-and-time-circuits/paper.md §2.2–3.1; saturn/docs/CAUSAL-CONTEXT-VM.md; primary FINDINGS cited inline
---

# Mathematical account: dynamic circuits looping through a stable time scaffold

Status labels used throughout:
- **[Thm]** is a statement proved here or in MATH.md.
- **[Id]** is an exact algebraic identity.
- **[Meas]** is a measured number, cited with its primary record.
- **[Pred]** is a consequence derived here, followed by whether data agree.

Every [Meas] number below was re-read in its primary FINDINGS on 2026-10-02.

## 1. The object

### 1.1 Low-level system

A model m executes a deterministic computation on an ordered time index $\mathcal T_m$:

| Family | Time index | Carried state $X_t$ |
|---|---|---|
| Diffusion | denoising call $k=0..T$ | latent $s_k$ plus scheduler history |
| AR transformer | partial order on (layer $\ell$, position $i$) | residual $x_{\ell,i}$; committed K/V cache $\{(k_{\ell,j},v_{\ell,j})\}_{j\le i}$ |
| SSM | (layer $\ell$, step $t$) | channel states $h_{\ell,t}$ plus conv buffer |

Write the dynamics as $X_{t+1}=F_\theta(X_t,z_{t+1})$ and the readout as $Y=G_\theta(X_T,q)$, where $z$ is the exogenous input at each step and $q$ the query/consumer context.

### 1.2 High-level role machine

The architecture is a small recurrent machine over **roles**: $\mathcal R=\{$source $s$, operation/address $u$, reader/transition $A$, writer $W$, carried state $z$, consumer $C\}$:

$$a_t=A_m(s,u_t,z_t),\quad w_t=W_m(s,u_t,z_t,a_t),\quad z_{t+1}=T_m(z_t,w_t),\quad y_t=C_m(z_{t+1},u_t).$$

### 1.3 Lowering and the meaning of "static"

A **lowering** $L_m:\mathcal R\to 2^{\text{sites}}$ assigns each role a set of low-level sites. The assignment may be partial and many-to-many; a role may lower to a band or a span. An **alignment** $\pi_m$ reads role values off low-level state at those sites.

**Definition (scaffold, i.e. the static part).** $(L_m,\pi_m)$ is a scaffold over a context set $\mathcal C$, an operation set $\mathcal U$ and time $\mathcal T_m$ if, for every role $r$ and every pair $c,c'\in\mathcal C$, the low-level interchange intervention commutes with the high-level one up to $\varepsilon$:

$$\Pr_{c,c',u}\Big[\,Y\big(c,u;\;\mathrm{do}(L_m(r)\leftarrow L_m(r)[c'])\big)\;\approx\;Y^{\text{high}}\big(c,u;\;\mathrm{do}(r\leftarrow r[c'])\big)\Big]\ \ge\ 1-\varepsilon .$$

This is interchange-intervention accuracy (causal abstraction, Geiger et al.). The key word is *fixed*: $L_m$ and $\pi_m$ do not depend on $c$, $u$ or $t$.

**Definition (dynamic circuit).** For a given $(c,u)$, the dynamic circuit is:
- the **active edge set** $G(c,u)=\{e:\ \text{interventional effect of }e\text{ on }Y\neq0\}$;
- together with the realized **values**: source rows, address $a_t$, payload $w_t$, dose, timing.

**Thesis, formally.** There exists one fixed $(L_m,\pi_m)$ with high IIA across broad $\mathcal C\times\mathcal U$, while $G(c,u)$ and the realized values vary with $(c,u)$.

Two consequences:
1. **"Static" means a fixed alignment, not a fixed layer index.** A role lowering to a band $B$ satisfies the definition even if the layer with the largest single effect moves inside $B$ from context to context (§9.1).
2. **Coordinates are not unique.** For any invertible reparameterization $\phi$, $(\phi\circ L_m,\pi_m\circ\phi^{-1})$ is an equally valid scaffold, so there is no intrinsically unique graph (MATH.md). Claims are therefore about interventional *behavior at declared sites*, never about a canonical wiring diagram.

## 2. Complete state, sufficiency and the VM

**[Thm] Complete-state equality** (MATH.md). If $X_t$ is complete (Markov) and two runs share $X_t$ and all future inputs, their futures are equal.
- Proof: induction on $F_\theta$.

**Corollary 1 (VM exactness).** Fork, export, resume and replay of a complete StateCut reproduce native continuation exactly. **[Meas]** Exact for Qwen (CausalContextVM) and for Mamba (MambaStateVM).
- The VM is therefore the complete-state theorem made executable.
- A **swap** is a low-level interchange intervention on $L_m(r)$. The VM's swap success rate *is* the IIA in §1.3.

**Corollary 2 (contrapositive, the stale writer).** Two runs whose immediate outputs agree but whose carried states differ need not agree later. **[Meas]** In the SDXL stale-writer control, the immediate output matches and later steps diverge.

**Definition (ε-sufficient interface).** A site set $I$ is ε-sufficient for variable $V$ if transplanting $I[c']$ into $c$ yields $c'$'s value of $V$ with probability $\ge1-\varepsilon$, with the rest of $c$ native.

**Where sufficiency is architectural vs learned.** This is the distinction that makes results non-trivial.

- **Diffusion source.** The prompt enters the denoiser only through the text-encoder output, projected into per-site $K_\ell=EW^K_\ell$, $V_\ell=EW^V_\ell$, plus pooled conditioning. The compiled source $S=C(p,n)$ is therefore complete *by construction*, and

  $$R\big(\Phi_\theta^{T}(s_0,\,C(p,n))\big)=G(p,n,\xi)$$

  is a custody check (no hidden prompt path), not a discovery. **[Meas]** 21/21 RGB endpoints across 7 specimens and 5 families; 3 unused SDXL prompts byte-exact. The science in diffusion is (a) the per-site K/V factorization (§4), (b) time-indexed authority (§7) and (c) temporal closure (§7).
- **AR late band.** A narrow late K/V band is *not* sufficient by construction:
  - the residual at the source position continues past the band;
  - every later position can attend at every layer.

  So ε-sufficiency of a narrow learned band is an empirical property of trained weights. **[Meas] E20:**
  - Qwen 1.5B: block 0.924, rescue 0.871, wrong-identity 37/42.
  - Replicated on Gemma, SmolLM2 and held-out Qwen.
  - Qwen2.5-7B: rescue 0.770, wrong −0.026.
  - It is a property of the weights: v_proj row permutation collapses it, and trained vs random/shuffled networks differ (§8).

## 3. Formation in time

### 3.1 Formation over depth is structural

In an AR transformer,

$$k_{\ell,i}=W_K^\ell\,\mathrm{LN}(x_{\ell,i}),\qquad x_{\ell,i}=x_{0,i}+\sum_{j<\ell}\big(\mathrm{attn}_j+\mathrm{mlp}_j\big)(i),$$

so the content of the store at layer $\ell$ is a function of all depth before $\ell$ and of all positions $\le i$.

**[Pred] Early-layer absence is the expected result.** A K/V transplant at early $\ell$ moves projections of an *unformed* residual, so it should not rescue. Seeding the *residual* early and letting native layers run *should* rescue. This is not a falsifier; it is the definition of formation.

**[Meas] Both halves hold:**
- **Seeding.** An L11/L12 residual seed followed by native layers rescues identity in 16/16 generated reads (`qwen-scaffold-context-poc/FINDINGS.md:62`).
- **Formed store.** Installing the recipient-formed L22–27 anchor rescues 16/16. Blocking it restores donor identity in 14/14 available reads.
- **Generality.** The same source → formed store → answer path holds for Python return values and literal copying (`qwen-formation-replay`).
- **Earlier band fails.** Early-band (L16–21) fact-span patches give donor identity 0/15 and donor color 0/16.

### 3.2 Where the formation happens (formation-over-time test, 2026-10-02)

This test was prereg-frozen. Qwen job-eaf503028c04, Gemma job-9acb76a12273; canaries exact. **[Meas]**

1. **No single band layer carries the store.** The best single layer reaches 0.732 (Qwen) and 0.804 (Gemma) of full-band rescue, below the 0.90 threshold. The commit is distributed across the band.
2. **The band's own computation is not needed.** Freezing the band's attention and MLP leaves rescue intact (Qwen 0.904, Gemma 1.023). The content is present in $x_{\ell_0,i}$ at band entry; each band layer's $W_K^\ell,W_V^\ell$ projects it into the readable store.
3. **The consumer reads at the subject position.** Cutting consumer→subject attention collapses rescue (0.871→0.010; 0.985→0.015). Cutting consumer→other positions does not.
4. **Prereg disclosure.** The decisive "band builds the store" prediction (P2a) FAILED in both families and its falsifier F2 FIRED. P3b failed and F3b fired: blocking the subject's reads of earlier positions leaves rescue intact (Qwen loses a small ~0.06). P1c failed: the ramp is non-monotone and non-additive. The prereg passes were P1a, P1b, P2c, P3a-i and P3a-ii. So the test refuted "built inside the band" and supported "committed at the band, formed before it".
5. **Correction (2026-10-02 validity review).** An earlier draft of this item cited "pre-band L13–21 freeze cuts Qwen 0.871→0.675" as formation-over-time evidence. That number comes from `2026-10-02-p1-reviewer-experiments` (`rescue_late_freeze_mid`, 0.675 [0.611, 0.713]). There it missed its own 0.20 threshold in Qwen and was a no-op in Gemma (0.990 vs 0.985; F_A4_freeze_noop fired). It is NOT positive evidence for pre-band construction.
   - The positive formed-over-depth evidence is the L11/L12 residual seed run through native layers (16/16 rescue; early-band K/V transplant 0/15), together with items 1–3 here.
   - *Where* in the pre-band depth the content forms is not localized by any run so far.

Role reading:
- writer = depth up to band entry (formation);
- commit = band projections (write port);
- carried state = K/V cache;
- reader = consumer attention at the subject position.

This is the architecture's "formed over ordered execution, committed, later read". It also refines it: the late band is the **commit/read-out zone**, not the formation zone. The formation locus inside the pre-band depth remains open.

### 3.3 Ancestry: state is a function of ordered history, not of the token set

$k^{A\|B}_{\ell,i}$ for $i\in B$ depends on $A$ through attention at every $j<\ell$. Mounting independently formed pages gives $k^{B}_{\ell,i}$ instead.

- **[Pred]** $\mathrm{Mount}(A,B)\neq\mathrm{Prefill}(A\|B)$ unless B's state is invariant to its causal past.
- **[Meas]** 6/6 vs 1/6.
- A "bag of facts" memory predicts equality, so this refutes it.

## 4. Address vs payload: exact attention identities

Single head, slot $s$ with weight $\alpha_s$, output $o=\sum_j\alpha_jv_j$. Let $E=e^{q^\top\Delta k/\sqrt d}$ and $D=1+\alpha_s(E-1)$.

**[Id]**

$$\Delta o^{K}=\frac{\alpha_s(E-1)}{D}(v_s-o),\qquad \Delta o^{V}=\alpha_s\Delta v,\qquad \Delta o^{KV}=\frac{\alpha_s}{D}\big[(E-1)(v_s-o)+E\,\Delta v\big].$$

Subtracting the two single-operand effects gives the interaction:

$$\Delta o^{KV}-\Delta o^K-\Delta o^V=\alpha_s\Delta v\Big(\frac{E}{D}-1\Big)=\frac{\alpha_s(1-\alpha_s)(E-1)}{D}\,\Delta v .$$

Consequences:
- **K is address.** A key change can only re-weight existing payloads. Its effect is bounded by $v_s-o$ and saturates as $E\to\infty$.
- **V is payload.** Its effect is linear in $\Delta v$, gated by the *existing* address weight $\alpha_s$.
- **Superadditivity.** The interaction is nonzero only when both change and $0<\alpha_s<1$. It is positive along $\Delta v$ when the new key raises attention ($E>1$).

**[Pred] → [Meas]** Matched K and V should be superadditive. Neither alone should repair the lesion when the base slot carries the wrong payload: K alone points at the old payload, and V alone is gated by a small old $\alpha_s$.

SDXL factorial (`scene-generator-paper.md` §5.2):

| Arm | α |
|---|---|
| K₀V₀ (base) | 0.72139 |
| K₁V₀ (candidate K only) | 0.66201 |
| K₀V₁ (candidate V only) | 0.71808 |
| K₁V₁ (both) | 1.00000 |

So $\Delta_{K\times V}\alpha=1-0.66201-0.71808+0.72139=0.3413>0$. The sign and pattern agree with the identity.
- Caveat: α is an image-axis projection through many heads, steps and a nonlinear renderer. The identity predicts the qualitative pattern only, not the scalar.

**[Pred] Joint row permutation is exactly invariant.** For softmax attention over a set without positional terms in K, $o$ is invariant to jointly permuting $(k_j,v_j)$ pairs. Token row is therefore a basis coordinate, not the lookup address. The key vector is the address.

**[Meas]** Joint permutation gives α 0.859 with the same semantics but altered composition. K-only gives 0.436 and V-only 0.627; wrong-K 0.358, wrong-V 0.413. FLUX.2 row permutation gives RGB MAE 4.6–22.8, against wrong-source 54.5–94.3 and wrong-sign 60.0–89.3 (`research/demos/artifacts/scene-generator/artifacts/reports/flux2-klein.json`, 3 prompts; an earlier draft cited 7–11 / 57–97 from a different run). FLUX.2 joint attention may give text tokens positions, so exact invariance is not predicted there; the theorem applies to SDXL-style cross-attention.

The residual gap from exact invariance is an **open check**. Candidate causes: not every row-indexed path was jointly permuted (padding/mask, pooled), or reduction-order non-associativity amplified chaotically over the sampling trajectory. Run it fp64 at one site before citing the 0.859 as anything but "near-invariant".

**Link to AR.** In Qwen, key-only transfer is exact (C5), and same-patch query selectivity is the AR version of the address term (§5). Both families lower "address" to K and "payload" to V.

## 5. Context selects participation (the dynamic part)

Define the **authority** of a stored object $z_j$ under query $q$ as an interventional effect:

$$\mathcal A_j(q)=Y(q,z)-Y(q,z_{j\leftarrow z'_j}).$$

Hold the parent state and the patch bytes fixed and vary only $q$. Any change in $\mathcal A_j(q)$ then arises through $\alpha_j(q)$ and the downstream consumer, i.e. through *participation*, not through the content of the store.

- **A content-additive or steering-vector model**, $Y=Y_0+\langle\beta,\Delta z\rangle$ with $\beta$ independent of $q$, predicts $\partial\mathcal A/\partial q=0$.
- **The role machine** predicts $\mathcal A_j(q)\propto\alpha_j(q)$ at first order (from $\Delta o^V=\alpha_s\Delta v$).

**[Meas]** Same parent StateCut and byte-identical K/V patch; only the native question changes (`qwen-scaffold-context-poc/FINDINGS.md` §2):
- query-selective harm: color 3.130 nats, 16/16; position 0.583 nats, 16/16; position→color 3.021 nats, 16/16;
- all 128 digest-pairing checks pass.

The interface is shared while the readers differ:
- **[Meas]** One fixed L22–27 interface hosts color 16/16, position 12/16 and identity 11/11 without reselection.
- **[Meas]** Per-item reader cosine is 0.73–0.99 within an operation and 0.20 across operations.
- **[Meas]** Eye color and eye geometry share 5–7 of the top-8 consumer heads but only 10–15 of 64 source rows.

That is "fixed $L_m$, varying $G(c,u)$" in the measured numbers.

## 6. The loop: written state changes later reads

### 6.1 Four-cell identities

Four-cell table $Y_{ab}=g(H_a,S_{2b})$ (MATH.md), where $H$ is history and $S_2$ the new row.

**[Id]**
- $\tau=Y_{11}-Y_{00}=b_0+r_0+i=b_0+r_1=r_0+b_1$;
- $b_0=Y_{10}-Y_{00}$, $r_0=Y_{01}-Y_{00}$;
- $i=Y_{11}-Y_{10}-Y_{01}+Y_{00}$.

Serial, additive, conjunctive, redundant and counteracting consumers give distinct tables, so the table identifies consumer *form*.

**[Meas]** History×row on 4 held contexts: history +1.279 to +1.576, row −0.152 to −0.014, total +0.957 to +1.425.
- The consumer is history-dominated with an opposing row term. It is not "read the newest row".

### 6.2 Serial vs fork needs a pre-update intervention

**[Thm]** (MATH.md). A serial chain $S_1\to S_2\to Y$ and a fork $S_1\to Y\leftarrow S_2$ give identical observational and post-update tables.
- Only an intervention on $S_1$ *before* the update, with $W_{ab}=f(S_{1b},R_a,z_2)$ and composed contrast $\kappa=Z_{a1;c}-Z_{a0;c}$, separates them.
- **[Meas]** Two-update France→Germany with the visible token fixed; route→write→future key-only transfer exact; L23–27 closure on 3 fresh held contexts.

### 6.3 Composition through a non-identity transition (SSM)

Two Mamba steps give $h_2=\rho_2\rho_1h_0+\rho_2w_1+w_2$. An endpoint-sum model predicts $h_0+\Delta_1+\Delta_2$ and is wrong by $(\rho_2-1)w_1$ plus the $\rho$ terms on $h_0$.

- **[Pred]** Staged composition is exact and endpoint sums fail whenever $\rho\neq1$. This failure is the signature of a carried state through a real transition.
- **[Meas]** Composition 3/3 vs endpoint-sum 0; staged execution exact; S2 closure exact; fresh CPU dog/cat +2.74.

## 7. Time-indexed authority in diffusion

Install source $S_A$ for $k<k_0$ and $S_B$ after. The output is $I(k_0)=R(\Phi^{T-k_0}(\Phi^{k_0}(s_0,S_A),S_B))$.

- **Authority varies with time.** The authority of the source at call $k$ is $\|\partial s_T/\partial S_k\|$, and it is time-dependent.
- **Why the frequency band moves.** At noise level $\sigma_k$ the denoiser predicts the posterior mean given $x_k$. At high σ only coarse structure is unresolved, so the source moves composition. At low σ coarse structure is fixed by the carried latent, so the source can only move fine detail.

**[Pred] → [Meas]**
- Early install changes composition and eye geometry; late install changes iris color with composition kept (12 references across 56 images).
- An SDXL base-K/V lesion at call 0 gives MAE 20.82; the same lesion at call 14 gives 2.15.

**Temporal closure.** The continuation $R(\Phi^{T-k}(s_k,S))$ takes *both* the register $s_k$ and the program $S$ as arguments. By the complete-state theorem only the pair is complete.
- **[Meas]** Program alone 0.712, register alone 0.403, both together exact.
- **[Meas]** Eye-geometry register inserted after $t_0,t_1,t_2,t_3$ retains 0.342 / 0.488 / 0.675 / 1.0 of the final effect. The register is progressively formed, not a one-shot write.

**Static bus, dynamic query.** $K_\ell,V_\ell$ are fixed per prompt, while $Q_{\ell,k}=W_Q^\ell h_{\ell,k}(s_k)$ moves with the carried state.
- **[Meas]** K/V are byte-identical across calls, while the cosine between an edited run's queries and the base run's queries falls from 0.99990 (call 0, block 0) to 0.83993 (call 14, block 0) (`research/demos/artifacts/scene-generator/sources/qkv-findings.md:72,80`). With the prompt K/V fixed, the address diverges as the carried image states diverge: the address is generated by carried state. (An earlier draft misdescribed this as within-run drift.)
- This is the static/dynamic split of §1.3 in one measurement: weights plus compiled K/V are $L_m$; $\alpha(Q_k,K)$ is $G(c,u)$ at time $k$.

## 8. Mamba recurrence and the clock

Per channel, $h_t=\rho_th_{t-1}+\Delta_tb_tu_t$ with $\rho_t=\exp(\Delta_tA)$, read by $s_t=\langle c_t,h_t\rangle+Du_t$. Unrolled:

$$H_T=R_{t_0:T}H_{t_0}+\sum_iR_{i:T}w_i,\qquad R=\exp\!\big(A\textstyle\sum\Delta\big),\quad \text{elapsed clock }=-\log R .$$

**[Id] Matched dose panel:**

| Dose | Retention | Write |
|---|---|---|
| $\Delta\times k$ | $\exp(Ak\Delta)$ | $k\,w$ |
| $A_{\log}\mathrel{+}=\log k$ | $\exp(Ak\Delta)$ | $w$ |
| $b\times k$ | $\exp(A\Delta)$ | $k\,w$ |

A dt dose is therefore a joint clock+write action. Only the A arm isolates the clock.

**[Id] Sensitivity of the carried term to an A-dose.** Scaling the elapsed clock $c=-\log R$ by $k$ multiplies the carried contribution by $e^{-(k-1)c}$.

**[Meas]** The writer's elapsed clock is $c\approx0.03$–$0.07$, against $1$–$8$ at other layers. So $k\in\{0.5,2\}$ changes the carried term by a factor in $[e^{-0.07},e^{0.035}]$, i.e. ≤7%.
- **[Pred]** At $k\in\{0.5,2\}$ the A arm is near-inert *by construction* whether or not the stopped clock is causal. The clock-dose run's small A effects (≤0.40; 0.04 at 2.8B identity) therefore cannot license "clock not causal".
- **The discriminating dose** drives the writer's clock to the control layers' regime, $k\approx c_{\text{ctrl}}/c_{\text{writer}}\sim15$–$150$. A "retention latch carries the commit" hypothesis then predicts collapse.
- **[Meas] The retest used that dose** (`2026-10-02-mamba-clock-retest`, prereg-frozen; jobs 130M ed83b7e7668d, 370M 3f20952d26c9, 2.8B 6225bc854a49). Forcing the writer's survival to the network median needed γ = 15–142, matching the derived range.
  - Release hurts in 0/6 cells.
  - dt acts via retention in 0/6; via the write in 6/6.
  - Writer-specific in 1/6.
  - On identity, releasing retention *raises* the margin.
- **Verdict:** `RETENTION_NOT_COMMIT_LEVER`. In role terms the Mamba commit lowers to the **writer W**, not to the transition's retention. The retention-outlier correlation (survival 0.66–0.90) stands as a measured correlate.
- This does not weaken the architecture: the role machine requires a write that later reads consume, not a particular retention value.

**[Meas] State selectivity.** On byte-identical history, L0→L18–20 gives donkey/Vienna +4.59 / +7.65 nats. Restoring the selected state removes 90.3% / 91.6% of the effect.

## 9. Discriminating tests and why tonight's proxies were misaligned

A test discriminates only if $P(\text{result}\mid\text{thesis})\ne P(\text{result}\mid\text{alternative})$.

### 9.1 Proxies that do not discriminate

**Commit-location SD / FAL-3 argmax locator / 7B commit SD.**
- The statistic is $L^*(c)=\arg\max_{\ell\in B}e_\ell(c)$ with $e_\ell=\bar e_\ell+\eta_\ell(c)$.
- The thesis predicts a near-flat plateau over $B$ (§3.2: best single layer 0.73–0.80 of full). The argmax is then ill-conditioned: for i.i.d. noise on a flat 6-layer band, $\mathrm{SD}(L^*)\to\sqrt{(6^2-1)/12}\approx1.7$ layers.
- A scaffold-free "each context recruits its own layers" model also gives large SD. Both hypotheses predict the same result, so it does not discriminate.
- For scale (arithmetic, not a test): the trained S2 SDs of 1.16 / 1.60 sit at or under the flat-plateau value.
- The right statistic is band-level IIA under fixed $L_m$.

**Lexical-set "fact" variance ratio.** This decomposes the variance of the same ill-conditioned locator by factor, so it inherits the problem above.

**Random and shuffled networks.** They are incompetent: there is no behavior, so $L^*$ is undefined. The contrast tests "learned vs untrained" (property 6), not scaffold structure.
- Secondary result: trained 1.16 / 1.60 vs random 8.56 / 7.28 and shuffled 10.03 / 10.22.

**Pre-band subject-position freeze reported as "construction unsupported".**
- Formation is multi-position and depth-distributed. A null at one position or window is predicted whenever formation sits elsewhere in depth or position.
- The properly designed test (§3.2) moved the conclusion rather than refuting the thesis.

**Sliding-window type swap at sequence length 17.** For $n\le W$ the sliding-window mask equals the causal mask, so the swap is the identity map on the computation. It cannot test anything.

**A-only clock dose at k∈{0.5,2}.** Inert by construction (§8). It was superseded by the aligned retest (γ = 15–142), which measured that the write, not the clock, is the lever.

**Function-vector test.** It probes an additive, query-independent task vector, i.e. the steering-vector alternative of §5. The role machine predicts query-dependent, non-additive authority, so an FV null is uninformative about the scaffold.

### 9.2 Tests that do discriminate

| Alternative | Its prediction | Measured |
|---|---|---|
| Generic bottleneck (any narrow band works) | v_proj permutation leaves rescue; wrong site works | collapse; wrong site −0.133 vs 1.011 |
| Per-input sites (no reuse) | each operation needs its own reselected site | one fixed L22–27 hosts 3 operations; FLUX profile 0.913 same vs 0.734 different organization |
| Steering vector / additive | $\partial\mathcal A/\partial q=0$; endpoint sums compose; no K×V interaction | 16/16 selectivity; 3/3 vs 0; $\Delta_{K\times V}=0.341$ |
| Bag-of-facts memory | Mount = Prefill | 6/6 vs 1/6 |
| Read-off-source (no formation) | early K/V or linear seed-image rescues | no; native-layer seed rescues 16/16 |
| Single-layer write | one layer ≈ full band | best 0.73–0.80 |

## 10. Limits the mathematics forces

- **Identifiability.** A role is identifiable against a generic model only where $(I-P_G)X_R\neq0$ (MATH.md). Where the generic predictor spans the role's contribution, the connected forecast ties an additive rival, as measured.
- **No canonical graph.** Coordinate reparameterization leaves IIA unchanged (§1.3). The complete common cross-family graph is a null, and no unique graph exists to find.
- **Ranking reversal.** Reader rankings can reverse across backgrounds (MATH.md). Per-item reader profiles must be compared within a background.
- **The four-quadrant certificate does not certify mechanism.** It certifies distribution of support: $y=\mathrm{mean}(x)$ passes. It must be paired with isolated swaps and named interventions; in-forward vs isolated differ (Qwen L0 0.99 vs 0.00).
- **Diffusion source sufficiency is architectural (§2).** The 21/21 result is custody/parity and must not be sold as discovery. The discoveries are the factorization, time-indexed authority and closure.
