---
title: "Dynamic circuits as state-dependent routing around a time scaffold"
type: theory-review
date: 2026-10-02
author: "Opus 5.5 theorist subagent, for Jacob Hollenbeck"
companion: architecture-math-2026-10-02.md
builds_on: architecture-math-2026-10-02.md; architecture-brief-2026-10-02.md; ../paper.md §2–6; saturn/experiments/2026-10-01-scaffold-graph-identification/MATH.md
consumers: saturn/experiments/2026-10-02-qwen-address-symbol-table/PREREG.md (theory_addenda); saturn/experiments/2026-10-02-sdxl-address-symbol-table/ (panel only at time of writing)
checks: small exact/symbolic checks only (sympy, toy matrices ≤ 8×8, 1-D ODE); no model loads
---

# Dynamic circuits as state-dependent routing around a time scaffold

## Labels and evidence discipline

Every statement carries one of these labels:
- **[Thm]** is proved here, possibly under a stated model assumption.
- **[Id]** is an exact algebraic identity.
- **[Pred]** is a derived, falsifiable prediction.
- **[Conj]** is a conjecture with a stated reason.
- **[Meas — path]** is a number I read in the named primary record on 2026-10-02.
- **[Comp — path]** is a number I computed from numbers in that primary record.

Paths are relative to `~/domains`. Toy checks are in my session scratchpad (`checks.py`). That script is a scratch artifact, not a project file; its outputs are quoted where used.

One correction to the existing account comes first, because §5 depends on it. The SDXL figure "Q cosine 0.9999 → 0.8399" is cited in `architecture-math §7` as one trajectory's query drifting over time. The primary record says something different: it is the cosine between the **candidate-run Q and the base-run Q** at the same site, measured at call 0 and at call 14. [Meas — `research/demos/artifacts/scene-generator/sources/qkv-findings.md`]
- At call 0, block 0, the cosine is 0.99990.
- At call 14 it is 0.83993 (block 1: 0.82159).
- Attention-map cosine is 0.78819 at call 0 and 0.80640 at call 14.

So the measurement shows that **the address diverges as the carried states of two runs diverge**, while K/V stay byte-identical. That is stronger evidence for the thesis below than a single-trajectory drift would be. I use the corrected reading throughout.

---

## 0. The model in one page

**Core model.** A dynamic circuit is the routing signature $\Gamma(c,t)$ that the carried state generates at each step. It has three parts:
- attention distributions $\alpha(q(z_t),K)$;
- MLP and SSM gates;
- normalisation gains.

The scaffold is the fixed weights plus the fixed lowering of roles to sites. Payloads enter **linearly given $\Gamma$**. Every non-additive effect, including bindings, relations and K×V conjunctions, passes through a change in $\Gamma$. $\Gamma$ is a function of the carried state, so the carried state both stores content and selects what is read next. That is the formal reason it carries the load for relations.

Five results organise the document:

1. **Conditional linearity [Thm, §2.3].** Freeze the routing signature (attention probabilities, gates, normalisation scales). The network is then affine in every payload, and every 4-cell interaction between source edits is exactly zero. Interactions are routing-mediated by construction.
2. **Single-read lemma [Id, §3.2].** In one attention read with a fixed query:
   - the content of row $b$ cannot change the *relative* selection among other rows;
   - V-only edits of distinct rows are exactly additive.

   Pointer-following ("C refers to A", "the colour of the thing on the left", transport) therefore needs the query to have been written by an earlier read. That write lives in some position's or region's carried state.
3. **Layer-0 and causal-encoder locality [Thm, §3.3].** Every function of two or more tokens is computed into a residual stream. In a causal text encoder (CLIP for SDXL; Qwen), a modifier–head binding can only live at the head-word row or later rows. In SDXL cross-attention the image token $i$ sees the carried state only through $z_i$. Spatial relations between image regions are therefore image-side carried-state conjunctions by architecture.
4. **Time-indexed authority [Thm in a linear-Gaussian model, §5].** In rectified flow with a Gaussian prior of variance $\lambda$, a register inserted at time $t$ retains $\rho=\sqrt{\mathrm{SNR}/(1+\mathrm{SNR})}$ of the target, with $\mathrm{SNR}=(1-t)^2\lambda/t^2$. The current program supplies exactly $1-\rho$. High-variance (coarse, layout-coupled) components lock first. The reachable set of any deterministic system shrinks monotonically along its trajectory (§5.1). The AR analogue is depth: pointers formed at other positions before the late band lock relational reads earlier than attribute reads.
5. **Symbol-table coordinates [§4].** A table entry is not a token row. It is a tuple:
   - a site set;
   - a time or depth window;
   - an address class, meaning the key modulo what the window's live queries can distinguish, under the gauge-invariant query-covariance metric;
   - a payload class, meaning the value modulo the consumer null space;
   - a precondition region of carried state.

   Attributes are separable entries whose precondition is already locked. Relations are entries whose precondition is written by other entries. Those are production rules over carried state, which is why a prompt-keyed table "got decent results but it was hard to define everything".

---

## 1. Setup and notation

AR transformer, pre-norm, at layer $\ell$ and position $i$ (Qwen2.5: RMSNorm, GQA, SwiGLU, RoPE). Write $N(\cdot)$ for the normalisation, $h$ for heads and $R_j$ for the RoPE rotation at position $j$:

$$
x^{\ell+1}_i = y^\ell_i + m^\ell(y^\ell_i),\qquad y^\ell_i=x^\ell_i+\sum_h W_O^h o^{h}_i,\qquad o^h_i=\sum_{j\le i}\alpha^h_{ij}v^h_j,
$$
$$
\alpha^h_{ij}=\operatorname{softmax}_j\!\Big(\tfrac{q^{h\top}_i k^h_j}{\sqrt d}+\mu_{ij}\Big),\quad q^h_i=W^h_Q N(x^\ell_i),\quad k^h_j=R_jW^{g(h)}_K N(x^\ell_j),\quad v^h_j=W^{g(h)}_V N(x^\ell_j).
$$

**Diffusion (SDXL).** One scheduler call is $z_{k+1}=\Psi_k(z_k,\hat\epsilon_\theta(z_k,S,k))$, where $\Psi_k$ is affine in its arguments for DDIM/Euler. Inside $\hat\epsilon_\theta$:
- cross-attention reads the static source $S=\{K_\ell,V_\ell\}$ with queries $Q_{\ell,k}=W_Q h_{\ell,k}(z_k)$;
- self-attention, convolutions and GroupNorm mix image tokens.

**SSM (Mamba).** $H_t=\rho(u_t)\odot H_{t-1}+\Delta(u_t)b(u_t)u_t$, read as $s_t=c(u_t)^\top H_t+Du_t$. The coefficients are functions of the current input $u_t$ (residual plus conv buffer), not of $H$.

**Roles** are as in `architecture-math §1.2`. The **routing signature** at $(c,t)$ is

$$
\Gamma(c,t)=\big(\{\alpha^{h,\ell}_{ij}\},\ \{\text{MLP/SSM gate values}\},\ \{\text{normalisation scales}\}\big)
$$

evaluated on input $c$ at step $t$.

---

## 2. Q1 — A dynamic circuit is state-dependent routing

### 2.1 The per-step map is bilinear in (routing, payload)

Hold the normalisation scale fixed. The attention sub-step is $\sum_h W_O^h V^{h\top}\alpha^h(z)$: **linear in the payload table $V$ for fixed $\alpha$**, with $\alpha$ a smooth function of the carried state $z$. The MLP is linear in its input for fixed gate values. Only the routing signature is nonlinear in the state. [Id]

### 2.2 Jacobian decomposition

**[Id] Normalisation gain.** For RMSNorm $N(x)=g\odot\sqrt d\,x/\|x\|$:

$$
J_N(x)=\frac{\sqrt d\,\operatorname{diag}(g)}{\|x\|}\big(I-\hat x\hat x^\top\big),\qquad \hat x=x/\|x\|.
$$

Every read of a residual has gain $\propto 1/\|x\|$, and the radial direction is projected out. This is used in §5.5.

**[Id] Attention Jacobian (one head, reader $i$, source position $m$).** With $\bar k_i=\sum_j\alpha_{ij}k_j$:

$$
\frac{\partial o_i}{\partial x_m}=
\underbrace{\alpha_{im}W_VJ_N(x_m)}_{\text{value path}}
+\underbrace{\tfrac{1}{\sqrt d}\,\alpha_{im}(v_m-o_i)\,q_i^\top R_mW_KJ_N(x_m)}_{\text{key path (address of the source)}}
+\underbrace{\delta_{mi}\,\tfrac{1}{\sqrt d}\,\mathrm{Cov}_{\alpha_i}(v,k)\,W_QJ_N(x_i)}_{\text{query path (address from the reader's own state)}},
$$
$$
\mathrm{Cov}_{\alpha_i}(v,k)=\sum_j\alpha_{ij}(v_j-o_i)(k_j-\bar k_i)^\top .
$$

*Derivation.* $\partial\alpha_j/\partial q=\alpha_j(k_j-\bar k)/\sqrt d$. Then $\partial o/\partial q=\sum_j v_j\alpha_j(k_j-\bar k)^\top/\sqrt d$. Subtracting $o\sum_j\alpha_j(k_j-\bar k)^\top=0$ gives the covariance. The key path follows the same way from $\partial\alpha_j/\partial k_m$. Checked against finite differences on a 7-row toy: max error $2.3\times10^{-10}$ (`checks.py`).

**[Id] Two-candidate reduction.** If the reader splits mass $\alpha,1-\alpha$ between two rows,

$$
\mathrm{Cov}_\alpha(v,k)=\alpha(1-\alpha)\,(v_1-v_2)(k_1-k_2)^\top .
$$

This is rank 1, with gain $\alpha(1-\alpha)$. Checked to $2\times10^{-16}$.

**[Thm] Properties of the address path.**
- (a) $\operatorname{rank}\mathrm{Cov}_{\alpha}\le\min(d_h,|\operatorname{supp}\alpha|-1)$.
- (b) If a fraction $\varepsilon$ of the mass leaks off the top row, $\|\mathrm{Cov}_\alpha\|=O(\varepsilon)$. In expanded form, every term is $O(\varepsilon)$: the top row contributes $(1-\varepsilon)\cdot O(\varepsilon)\cdot O(\varepsilon)$ and each other row $\alpha_j\cdot O(1)\cdot O(1)$ with $\sum\alpha_j=\varepsilon$.

So the reader's own state steers its read only while the read is **undecided**. Once attention commits to a row, the carried state stops re-routing that read and only the value path remains.

**[Id] MLP Jacobian (SwiGLU).** $m(x)=W_d[\operatorname{silu}(W_gN)\odot W_uN]$ gives

$$
\partial m/\partial x=W_d\big[\operatorname{diag}(\operatorname{silu}(g))W_u+\operatorname{diag}(u\odot\operatorname{silu}'(g))W_g\big]J_N.
$$

The first term is linear given the gate. The second is the gate-routing term.

**[Id] Composition over depth.** Over positions, layer $\ell$'s Jacobian is block lower-triangular:

$$
\mathcal J^\ell=I+\mathcal V^\ell+\mathcal K^\ell+\mathcal Q^\ell+\mathcal M^\ell .
$$

The end-to-end Jacobian $\prod_\ell\mathcal J^\ell=I+\sum_\ell\Delta^\ell+\sum_{\ell<\ell'}\Delta^{\ell'}\Delta^\ell+\dots$ expands into paths. The second-order products $\mathcal Q^{\ell'}\mathcal V^{\ell}$ and $\mathcal K^{\ell'}\mathcal V^{\ell}$ are the Q- and K-composition terms: a payload written at $\ell$ changes an address read at $\ell'$. These are the only places where carried state re-routes.

### 2.3 Conditional linearity: interactions are routing

**[Thm] Conditional payload-linearity.** Fix $\Gamma$ to the values of a reference run:
- replace each softmax by the reference probabilities;
- replace each gate by its reference value;
- replace each normalisation by the linear map $x\mapsto g\odot x/\mathrm{rms}_{\mathrm{ref}}$.

Every layer is then linear in its input, and the whole forward pass, and in diffusion the affine scheduler loop, is affine in all additive source edits: embeddings, residual seeds, V rows. Consequently, for any two edits $\delta_a,\delta_b$ the 4-cell interaction $i=Y_{11}-Y_{10}-Y_{01}+Y_{00}$ is exactly 0 under frozen $\Gamma$.
- *Proof.* A composition of affine maps is affine, and the mixed second difference of an affine function vanishes. ∎
- *Toy check.* Two sequential reads with Q-composition: live interaction norm 0.0098, frozen-routing interaction $2.4\times10^{-16}$ (`checks.py`).

**[Thm] Corollary: where interactions come from.** Write the live output as $Y(\delta)=F(\Gamma(\delta),\delta)$, with $F(\Gamma,\cdot)$ affine for each $\Gamma$. Then

$$
i=\Delta_a\Delta_b\big[F(\Gamma(\delta),\delta)-F(\Gamma_{\mathrm{ref}},\delta)\big],
$$

and to second order

$$
i\approx\Big\langle\tfrac{\partial F}{\partial\Gamma},\tfrac{\partial^2\Gamma}{\partial\delta_a\partial\delta_b}\Big\rangle+\Big\langle\tfrac{\partial^2F}{\partial\Gamma\,\partial\delta},\ \tfrac{\partial\Gamma}{\partial\delta_b}\otimes\delta_a+\tfrac{\partial\Gamma}{\partial\delta_a}\otimes\delta_b\Big\rangle+\tfrac{\partial^2F}{\partial\Gamma^2}\Big[\tfrac{\partial\Gamma}{\partial\delta_a},\tfrac{\partial\Gamma}{\partial\delta_b}\Big].
$$

Every term carries a derivative of $\Gamma$. Because $\Gamma$ is a function of carried state ($q=W_QN(x)$, gates, norms), **every conjunction is mediated by carried state.** That is the formal content of "the carried state both stores and selects".

### 2.4 Definition of the dynamic circuit, and when it is sparse

**Definition (dynamic circuit at $(c,t)$).** It is the triple $\big(\Gamma(c,t),\ L_{c,t},\ \mathcal R_{c,t}\big)$:
- $L_{c,t}=D_SY|_{\Gamma\text{ frozen at }c}$ is the **frozen-routing operator**: the exact linear map from source perturbations to output, at the routing that $c$ realises.
- $\mathcal R_{c,t}=D_S\Gamma$ is the **routing sensitivity**.
- The **active subspace** is the top singular subspace of $L_{c,t}$, weighted over a declared perturbation family.

The active edge set $G(c,u)$ of `architecture-math §1.3` is the support of $L$ plus the support of $\mathcal R$ at nonzero interventional effect. This refines that definition without replacing it. The scaffold is $\theta$ plus the lowering. The dynamic circuit is $\Gamma$, which the scaffold computes from the carried state.

**[Thm] When it is low-rank and sparse.** $L$ is low-rank and sparse when:
- (i) attention is concentrated (low entropy), so the value path selects few rows and the address path has gain $O(\varepsilon)$;
- (ii) gates are far from their switching points;
- (iii) few heads align with the consumer, i.e. $\|J_{\text{cons}}W_O^h\|$ is concentrated;
- (iv) the residual norm is large relative to the write (normalisation gain $\propto1/\|x\|$).

**[Thm] When it is not.** $L$ and $\mathcal R$ are high-rank or dense when:
- (i) attention is diffuse, e.g. early, high-noise diffusion calls, where $\mathrm{Cov}_\alpha$ has many terms;
- (ii) the read sits at a decision point, $\alpha\approx\tfrac12$ between competitors, where the address gain $\alpha(1-\alpha)$ is maximal;
- (iii) many heads carry near-collinear $W_OV$ directions (functionally low-rank, component-dense; Hydra/self-repair).

**[Thm] Coordinate dependence.** The score perturbation that live queries see is $Q\,\Delta K^\top$, with rank $\le\dim\operatorname{span}(Q_\tau)$ regardless of how many rows $\Delta K$ touches. A source program can therefore be dense in token rows and low-rank in key space.

[Meas — `research/demos/artifacts/anime-sprite-register/identity-program/evidence/prior/eye-geometry-findings.md`] This is what the FLUX eye program shows:
- top-1 and top-4 contextual rows were near null (0.001 and 0.007);
- top-16 rows reached 0.212 and top-64 reached 0.323;
- the complement still carried 0.172, against 0.463 for all text;
- the shared eight-head set carried 0.832 / 0.868 of the local attention branch.

The pattern is dense in rows and concentrated in heads.

### 2.5 Family specialisations

- **Diffusion [Id].** $K,V$ are prompt-static, so in cross-attention the only routing variable is $Q(z_k)$. The SDXL record shows K/V byte-identical between calls 0 and 14. Candidate-vs-base Q cosine falls from 0.99990 to 0.83993, and attention-map cosine is 0.78819 at call 0. [Meas — `research/demos/artifacts/scene-generator/sources/qkv-findings.md`] The dynamic circuit is the trajectory-dependent map $\alpha_k$ (image location × prompt row).
- **Mamba [Id].** Selectivity enters through $u_t$, not through $H$. Within one mixer, carried state cannot re-route its own read. Routing by carried state therefore needs depth: the residual output of layer $\ell$ sets $\Delta,b,c$ at $\ell+1$. That is why relations in Mamba appear as staged transition composition: $h_2=\rho_2\rho_1h_0+\rho_2w_1+w_2$ ≠ an endpoint sum (`architecture-math §6.3`). It also fits the retest finding that the commit lever is the write, not the retention [Meas — `saturn/experiments/2026-10-02-mamba-clock-retest/FINDINGS.md`]:
  - dt acts via the write in 6/6 cells and via retention in 0/6;
  - the verdict is `RETENTION_NOT_COMMIT_LEVER`.

---

## 3. Q2 — Why relations live in the carried state, not the source

### 3.1 Two kinds of binding

Formalise a binding of a role $r$ to a filler $f$ as a conjunction. There are two computationally distinct kinds.

- **Selection-by-content (pointer).** The output is $v_{\pi(c_b)}$: which row is read depends on the *content* of another row $b$. Examples are "C refers to A", "the colour of the animal on the left", induction and transport ("the chair that was at L").
- **Conjunction-of-contents.** The output is $g(c_a,c_b)$, not additive in $(c_a,c_b)$. Examples are role⊗filler tensors, and a colour painted on a support whose shape is $c_b$.

### 3.2 The single-read lemma

Fix the query $q$ of one attention read over rows $\{(k_j,v_j)\}$.

**[Id] (a) Payloads of distinct rows add.** $\partial^2o/\partial v_a\partial v_b=0$. For finite V-only edits of rows $a\ne b$ the 4-cell interaction is exactly 0. Toy: $1.1\times10^{-16}$.

**[Id] (b) No row can steer the relative selection of others.** For $b\notin\{a,c\}$:

$$
\frac{\partial}{\partial k_b}\big(\log\alpha_a-\log\alpha_c\big)=\frac{\partial}{\partial v_b}\big(\log\alpha_a-\log\alpha_c\big)=0,
$$

because $\log\alpha_a-\log\alpha_c=q^\top(k_a-k_c)/\sqrt d$. Changing $k_b$ rescales every other row's weight by the *same* factor.

**[Id] (c) Key edits only reallocate.** For K-only finite edits on rows $a,b$, the interaction lies exactly in $\operatorname{span}\{v_a-o_{\text{rest}},\,v_b-o_{\text{rest}}\}$, where $o_{\text{rest}}$ is the read over the untouched rows. All four cell outputs lie in the affine hull of $\{v_a,v_b,o_{\text{rest}}\}$, and the 4-cell coefficients sum to zero. Toy relative residual: $1.4\times10^{-14}$.

**[Thm] Pointer-following requires carried state.** Suppose a read $r$ implements selection-by-content, so the relative weight of rows $a,c$ depends on the content of row $b$. Then the query $q_r$ depends on row $b$'s content.
- In a transformer, $q_r=W_QN(x_r)$, and $x_r$ at layer 0 is the reader's own token embedding. The dependence must therefore have been written into the reader's residual by an earlier read of $b$ (Q-composition).
- Alternatively, it was written into $a$'s residual by $a$ reading $b$ (K-composition). The binding then lives in $a$'s carried row.
- *Proof.* This is Lemma (b) plus the definition of $q_r$. ∎

**[Thm] Conjunction-of-contents requires a nonlinearity acting on carried state.** By Lemma (a) and conditional linearity, a non-additive $g(c_a,c_b)$ cannot arise from the payload path alone. It arises in one of three ways:
- a routing change: K×V within one row, or Q-composition across rows;
- a gate acting on a residual that already holds both contents (MLP, consumer);
- consumer curvature.

All three act on carried state.

### 3.3 Locality theorems

**[Thm] Layer-0 locality.** At layer 0 each residual is a function of one token and its position. Every function of two or more tokens, at any site, was computed by mixing (attention, SSM, convolution) into some position's carried state.

**[Thm] Causal-encoder binding.** In a causal encoder, a binding between a token at $p$ and a token at $p'>p$ can be represented only at rows $\ge p'$.
- The SDXL text encoders are causal. The installed `transformers` `CLIPTextTransformer` builds `create_causal_mask(...)` and passes `is_causal=True`; I read this in the local `modeling_clip.py`.
- So in "…with **blue eyes**…", the binding *blue→eyes* cannot be in the "blue" row. It can only be in the "eyes" row and later rows, including EOS and padding rows, which see the whole prompt.
- The same holds for Qwen prefixes ("On the left is a red fox"): *left⊗fox⊗red* is formed at the "fox" row and later. This is consistent with identity having a decisive animal anchor while colour and position support is spread over the fact span. [Meas — `saturn/experiments/2026-10-01-qwen-scaffold-context-poc/FINDINGS.md`]

**[Thm] Diffusion spatial binding is image-side.** SDXL cross-attention at image token $i$ is $o_i=\sum_j\alpha_{ij}(Q_i(z_i))V_j$, so it depends on the carried state only through $z_i$ at that site. Interactions between two image regions $R_1,R_2$ (a nonzero $\partial^2Y/\partial z_{R_1}\partial z_{R_2}$) pass only through self-attention, convolution, GroupNorm statistics and the carried latent. Any relation between image regions (left-of, occlusion, transport) is therefore realised in carried image state. The source can only request it.

### 3.4 Second-order anatomy of an interaction

For edits $\delta_a,\delta_b$ to two source entries, $i\approx\delta_a^\top H\delta_b$ with [Id]

$$
H=H_{K\times V}+H_{\text{comp}}+H_{Q\circ V}+H_{\text{cons}} .
$$

The four terms are:
- **$H_{K\times V}$:** same read, same row (address and payload of one entry);
- **$H_{\text{comp}}$:** same read, different rows (pure reallocation, Lemma (c));
- **$H_{Q\circ V}$:** a payload written by one entry changes a later query that reads the other (pointer, transport, support-dependence);
- **$H_{\text{cons}}$:** consumer curvature on a carried state holding both.

For two different source rows, $H_{K\times V}=0$. Any non-competitive interaction is then $H_{Q\circ V}+H_{\text{cons}}$, i.e. carried state.

**[Id] The K×V term (`architecture-math §4`).** In finite form:

$$
\Delta o^{KV}-\Delta o^K-\Delta o^V=\frac{\alpha_s(1-\alpha_s)(E-1)}{D}\Delta v,\qquad D=1+\alpha_s(E-1).
$$

(Re-verified symbolically.)

**[Id] Where the K×V term peaks.** As a function of the base weight $\alpha_s$ it is maximised at

$$
\alpha_s^*=\frac1{1+\sqrt E}
$$

This reduces to ½ as $E\to1$. Solved symbolically and checked numerically at $E\in\{0.25,1.5,4,9\}$.

**[Thm] One factor governs both binding mechanisms.** The K×V interaction and the query-path gain (§2.2, $\alpha(1-\alpha)$) share the factor $\alpha(1-\alpha)$. Both mechanisms are strongest where the read is undecided and vanish once it is committed.

**[Id] Sign law for donor-row edits.** Take a single head and slot, with V effect $J^\top\alpha_s\Delta v$ and interaction $J^\top\alpha_s(1-\alpha_s)\tfrac{E-1}{D}\Delta v$. Then

$$
\frac{I}{V}=\frac{(1-\alpha_s)(E-1)}{1+\alpha_s(E-1)}\in(-1,0)\iff E<1,
$$

and $I/V>0\iff E>1$. $E<1$ means the live query scores the donor key *lower* than the recipient key, i.e. the query already carries recipient-specific content.

**[Comp — `saturn/experiments/2026-10-01-qwen-head-edge-topology/analysis/joint_kv_interactions.csv`]** I applied this law to the 13 single-group K/V rows where the joint or the V-only effect exceeds 0.05 nat in magnitude:
- 8/13 lie in the single-slot band $(-1,0)$; for example identity L23/KV0 gives $I/V=0.998/(-1.448)=-0.69$.
- 3/13 lie below −1 (−1.50, −1.00, −1.25). These are single-slot violations, expected because each cut spans several positions and six query heads.
- 2/13 are positive.

This is a post-hoc consistency check, not a test. Read this way, Qwen's late readers mostly score the donor key *below* the recipient key. That is the signature of queries whose content was formed from the recipient's own prefix. This is the same mechanism as the alias limit (§3.7).

### 3.5 Evidence that conjunctions are carried-state objects

The records below are each described by one of the terms above.

**FLUX eye colour × shape conjunction.** [Meas — `research/demos/artifacts/anime-sprite-register/identity-program/evidence/prior/eye-geometry-findings.md`]
- *Where the residual sits.* $I=$joint−colour−shape+base is exactly zero in the `joint.0@t0` image pre-state, because the noise is shared. In the text pre-state it is already 0.647 of the joint text delta.
- *Image-program deletions.* Removing the text+image program interaction left 0.184 of joint progress; removing the image-program interaction alone left 0.310.
- *Text-side deletion.* Removing the text-program interaction alone left 0.855. Under fresh seeds and grammars the range was 0.885–0.990.
- *Register deletion.* Removing the register interaction left 0.824.
- *Reading.* The source-side (text) conjunction exists but is not load-bearing. The image-side carried conjunction is. This is the §3.3 diffusion theorem made visible.
- *The vector is not stable, the contract is.* Under rephrasing, the register interaction's projection changed from −0.369..−0.237 to −0.001..0.026. The dose law was stable: λ = −1, 0, 0.5, 1, 1.5 gives −0.220, 0, 0.532, 1, 1.138, and a norm-preserving roll gives −0.009.

**Chair transport (spatial and temporal conjunction).** [Meas — `saturn/experiments/2026-09-20-flux2-transport-temporal-carrier/FINDINGS.md`; Comp]
- Source-only departure −0.3530; target-only departure −0.0022, arrival 0.7049; both: departure 0.9982, arrival 0.7418.
- The departure 4-cell interaction is $0.9982+0.3530+0.0022=1.353$, larger than the total effect. That is a pure conjunction.
- Late steps 2–3 alone: departure 0.0006, arrival 0.0002. The relation is locked by step 2 (§5).

**Early × late installs (scene editing).** [Comp — `research/demos/scene-editing.md` §5 table] The 4-cell over (install at calls 0+1) × (install at calls 2+3) on whole-image $P$:

| Edit | $i=P_{\text{all}}-P_{\text{early}}-P_{\text{late}}$ | Late authority given the early-edited state ($P_{\text{all}}-P_{\text{early}}$) | Late alone | Ratio |
|---|---:|---:|---:|---:|
| framing | +0.149 | 0.162 | 0.012 | 13.0× |
| rear view | +0.267 | 0.305 | 0.037 | 8.2× |
| eye colour | +0.241 | 0.310 | 0.069 | 4.5× |
| eye shape | +0.153 | 0.185 | 0.032 | 5.8× |

All four interactions are positive. A late source has 4.5–13× more authority on a carried state that the early source prepared. Additive steering predicts $i=0$, and so does the linear-Gaussian model of §5. The excess is $H_{Q\circ V}$ across time: later reads act on the state that earlier writes formed.

**SDXL Q×K×V.** [Meas — `research/demos/artifacts/scene-generator/sources/qkv-findings.md`]
- Under the live candidate Q, the K×V interaction is 0.34130.
- Candidate K+V with *base* Q reaches 0.98497. At call 0 the source distinction is carried by K/V, with $Q_{\text{cand}}\approx Q_{\text{base}}$ (cos 0.99990).
- Reversing query spatial order with candidate K/V gives 0.84473 (MAE 16.4047). Q decides *where* the matched program binds.

### 3.6 Why a prompt-keyed table is incomplete

**[Thm] (complete-state theorem).** $Y=R(\Phi^{T-k}(z_k,S))$. A source-keyed table edits only $S$. If a recipient's $z_k$ differs from the target's, installing $S_{\text{tgt}}$ gives

$$
Y(z_k^{\text{rec}},S_{\text{tgt}})-Y(z_k^{\text{tgt}},S_{\text{tgt}})\approx-\,\partial_{z_k}Y\,(z_k^{\text{tgt}}-z_k^{\text{rec}})\ne0
$$

unless the register difference is invisible to the consumer.

**[Thm] (linear-Gaussian closure partition, rectified flow; proof in §5.2).** For a scalar component with prior variance $\lambda$, consider switching the program at time $t$:
- the register-only arm has progress $\rho(t)=\sqrt{\mathrm{SNR}_t/(1+\mathrm{SNR}_t)}$;
- the program-only arm has progress $1-\rho(t)$;
- their 4-cell interaction is exactly 0;
- "both" is exact.

A source-keyed table therefore misses, at minimum, the fraction $\rho$ of every component that the register had already locked. $\rho$ is largest for high-variance (coarse, layout-coupled, relational) components.

**[Comp — `research/demos/artifacts/scene-editing/artifacts/closure/temporal-closure-summary.json`]** Program-only is 0.7124 and register-only is 0.4035, so $i/\tau=1-0.7124-0.4035=-0.116$.
- The near-unit sum is what the linear partition predicts.
- The small negative interaction is redundancy between the parents.
- "Both exact" is the complete-state theorem.

The table gets "decent results" on the $1-\rho$ part and cannot reach the $\rho$ part.

**[Meas — eye-geometry-findings] The payload is a function of the carried state.**
- A population body atlas built at seed 60660 reached 0.679 and 0.732 on sealed characters. At seed 7217 it reached only 0.097 / 0.146, against self ceilings of 0.904 / 0.891.
- The `single.0` differential increment installed alone retained only 0.115 / 0.194 at `single.19`.

So a seed-invariant prompt-keyed payload does not exist for these operations: the right payload is conditioned on $z_0$ and the residual.

**Why it was "hard to define everything".** The table's key space (prompt rows) has no coordinate for the precondition of a relational entry. That precondition is a region of carried state, which depends on seed and history. Every attempt to enumerate relations by prompt keys must therefore either:
- install early, where the entry is not separable because early authority is broad (the eye-colour early arm reaches $P=0.5772$ while leaving the eyes blue [Meas — `research/demos/scene-editing.md`]); or
- install late, where the relation is already locked ($\rho\to1$; chair late departure 0.0006).

### 3.7 The Qwen alias limit in the same terms

[Meas — `saturn/experiments/2026-10-01-qwen-formation-replay/results/qwen-formation-703f2394860c/report.json`, row `alias-explicit-target-second`]
- **Prompt.** "B stores the animal cat. A stores the animal fox. C refers to A." The donor has *bird* for A. The query is "The animal stored by C is".
- **Native runs.** The clean run says fox; the donor run says bird.
- **Residual seed at the A anchor, dose 1.** Seeding at L3, L7, L11, L15 or L19 gives **fox**. Seeding at L23 gives **cat**. Seeding at L26 gives **bird**.
- **Dose 0.5 at any layer ≤ L23.** Gives **cat**.
- **K/V transfers.** Late K/V anchor rescue (L22–27) gives **cat**. Early K/V anchor rescue gives **bird**.
- **Other arms.** The norm-matched random seed gives bird.

**[Thm-level explanation, mechanism Conj] The stale pointer.** The read "C → A → value" is pointer-following, so by §3.2 the query that finally reads A's value carries an address written by earlier reads. Those reads sit at the C-clause and query positions, at layers below the read.

1. **Seeding at ≤ L19.** The downstream positions re-form their states from the clean anchor at every later layer, so pointer and row agree and the answer is fox.
2. **Seeding at L23, or late K/V rescue.** The downstream pointers were formed against the *donor* anchor at layers < 22–23, while A's late key is now the clean one. The live query scores A's new key below its old key ($E<1$). By the key identity $\Delta o^K=\alpha(E-1)/D\,(v_A-o)$, mass moves *away* from A's row toward the competitor row, B (cat). The predicted failure is therefore *the other binding*, not the donor value and not noise, and that is what is observed.
3. **Dose 0.5.** An off-manifold anchor matches no pointer. $E<1$ for every reader, so the read falls to the competitor at every depth: cat.
4. **Seeding at L26.** The read has already happened at L22–25, so the donor value is retained: bird.

**Corroboration in the B-store line.** [Meas — `saturn/experiments/2026-10-01-qwen-frozen-reference-payload/FINDINGS.md`; `.../2026-10-01-qwen-b-store-layer-support/FINDINGS.md`; `.../2026-10-02-qwen-b-store-middle-split/FINDINGS.md`]
- **Direct reads need only the late band.** A late B-value row (L22–27) changes the direct B read in 4/4; the middle scope alone changes 0/4.
- **Indirect reads need middle layers too.** Adding L12–21 to the late band repairs a C-refers-to-B read that late-only and late+early (0–11) leave stale. It also creates a C-refers-to-A collateral error. The direct read lowers late; the pointer-mediated read needs the source at the depth where the pointer is dereferenced.
- **The collateral is an $E>1$ effect.** The transplanted row's middle-layer key now attracts queries that were not addressing it. By the same identity, $\Delta o^K\propto\alpha(E-1)/D$ with $E>1$.
- **A broken payload also falls to the competitor.** Under shuffled-V (donor K, rolled V), B returns *red*, A's value, in 4/4 under each scope.

**[Meas — `research/demos/qwen-causal-programs.md` (demo record)] Payload-dominant installs work with the recipient's address.**
- Donor-free generated V with base K succeeds 4/4; generated K with base V succeeds 0/4.
- Operation-specific localisation: V at L20 alone suffices for square/maximum (4/4), K at L12 alone for odd parity (2/2).

Address-type content lowers earlier in depth than payload-type content, as §5.5 predicts.

---

## 4. Q3 — The right coordinates for a symbol table

### 4.1 Token rows are not addresses

**[Id] Symmetries of the read.** Softmax attention over a set has three symmetries:
- **Joint row permutation.** $o$ is invariant to jointly permuting the rows $(k_j,v_j)$. This needs no positional term in the keys; a mask must be permuted with the rows.
- **Common key offset.** It is invariant to $k_j\mapsto k_j+c$ for all $j$, since every score shifts by $q^\top c$.
- **Head-space gauge.** It is invariant to $(W_Q,W_K)\mapsto(W_QA^{\top},A^{-1}W_K)$ for any invertible $A$, since $q^\top k$ is unchanged.

Row index, absolute key position and the K-space basis are therefore not functional coordinates. Only $q^\top k$ over the live queries is.

[Meas — `research/demos/artifacts/scene-generator/sources/qkv-findings.md`] In the SDXL factorial organism, a coherent K/V token permutation gives $\alpha=0.97298$ with a binding-output relative difference of **0.00164**. A K-only permutation gives 0.66304. That is much closer to exact invariance than the whale-panel 0.859 [Meas — `research/demos/docs/scene-generator-paper.md` §5.3]. The open fp64 check in `architecture-math §4` should be run at the factorial site first.

### 4.2 The address is a score functional, indexed by time

Define the live-query distribution of a site in window $\tau$ (diffusion calls, or AR depth band × reader positions) as $\mathcal Q_\tau$, and $\Sigma_\tau=\mathbb E_{q\sim\mathcal Q_\tau}[qq^\top]$.

**Definition (address metric).** $d_\tau(k,k')^2=(k-k')^\top\Sigma_\tau(k-k')/d_h=\mathbb E_{q\sim\mathcal Q_\tau}\big[(q^\top(k-k'))^2\big]/d_h$.

**[Thm] Gauge invariance.** $d_\tau$ is invariant under the gauge $A$. With $q'=A^\top q$ and $k'=A^{-1}k$, $\Sigma'=A^\top\Sigma A$ and the quadratic form is unchanged. Two keys with $d_\tau=0$ produce identical scores for every live query in $\tau$: they are the same address in that window.

**[Thm] The same key is a different address at different times.** Because $\mathcal Q_\tau$ moves with the carried state, the same static key has different address classes in different windows. In SDXL the queries of two runs diverge from cos 0.99990 to 0.83993 between calls 0 and 14, while K/V are byte-identical. A symbol-table key must therefore carry the window $\tau$.

### 4.3 Proposed key for a symbol-table entry

$$
e=\big\langle\ \mathcal H_e\ (\text{site set: layers/heads or KV-groups}),\ \ \tau_e\ (\text{time or depth window}),\ \ [k]_e\in K/{\sim_{d_{\tau}}},\ \ \mathcal R_e\subset\mathcal Z\ (\text{precondition region of carried state}),\ \ [v]_e\in V/\ker(J_{\tau}W_O)\ \big\rangle .
$$

The components are:
- $[k]_e$ is a cluster in the $\Sigma_\tau$-whitened key space.
- $\mathcal R_e=\{z:\alpha_e(q(z))\ge\theta\}$ is the set of carried states whose readers actually address the entry.
- $[v]_e$ is the payload modulo directions the window's consumer cannot see.

**Readout semantics.** For $t\in\tau_e$ and a reader in state $z$, the contribution is $W_O[v]_e\,\alpha_e(q(z))$. It is exactly linear in the payload given $\alpha$ (§2.3).

### 4.4 Which entries are separable

**[Thm] Separability (second order).** Two entries $e_1,e_2$ have zero second-order interaction if three conditions hold:
- **(i) No competition.** No live query in $\tau_1\cup\tau_2$ places non-negligible mass on both address classes. This kills $H_{\text{comp}}$.
- **(ii) No composition.** Neither entry's write moves any reader of the other across its precondition boundary: $\partial\alpha_{e_2}(q(z))/\partial v_{e_1}=0$ along the trajectory, and symmetrically. This kills $H_{Q\circ V}$.
- **(iii) No consumer curvature** between their write directions. This kills $H_{\text{cons}}$.

$H_{K\times V}=0$ because they are different entries. ∎

**Attributes are separable when their precondition is already locked.** An attribute of a region whose support is already fixed (by earlier locked state) has:
- one address cluster, read by the region's queries (i);
- a write that does not change where any other entry is read (ii).

Example [Pred]: eye colour and hair colour of one character. They are read by disjoint image regions, and neither defines the other's support, so they should be **additive**.

**Relations violate (ii) by definition.** A relational entry's precondition region is written by another entry: "C refers to A", the chair's departure versus arrival, and colour painted on a support that the shape entry is changing.

[Meas — eye-geometry-findings] FLUX colour and shape head-output directions had cosine 0.021 (near-orthogonal), yet the native joint output differed from their sum by 0.485 of the joint norm. Independent colour+shape addition at the terminating boundary reached only 0.304 of joint progress; the joint program is exact. Shape moves the eye support that colour's readers sit on, a violation of (ii). The interaction should therefore be **asymmetric**: shape → colour, not colour → shape. That gives an order prediction (§6, P5).

### 4.5 Why eye colour and eye geometry share consumer heads but not source rows

[Meas — eye-geometry-findings]
- At a fresh seed, eye shape and eye colour shared 7/8 top heads at `single.0`, and 5–7/8 at `single.1..4`.
- Their top-64 K/V rows overlapped only 15, 11, 10, 11 and 11 of 64 across `single.0..4`.
- Frozen shape rows on the correct colour heads gave 0.053, against 0.376 for locally selected colour rows.

**[Thm-sketch] Head participation factorises.** Head $h$'s effect on region $\mathcal R$ for entry $e$ is $J_{\mathcal R}W_O^h\,\alpha^h_{\mathcal R,e}\,\Delta v^h_e$. It factorises into three parts:
- query-side readiness, set by the queries of the image tokens in $\mathcal R$ through $W_Q^h$;
- address match $\alpha^h_{\mathcal R,e}$;
- consumer alignment $J_{\mathcal R}W_O^h$.

Two attributes of the *same region* share the first and third factors. Two attributes with *different content* differ in $[k]_e$.

**[Conj] Consequence.** Consumer-head overlap is governed by *where the readers are* (the precondition region). Source-row overlap is governed by *what is read* (the address class). The pair of eye colour and eye geometry is same-region and different-address, which is exactly the measured pattern.

### 4.6 What a table must store for relations

A relational entry is a **production rule over carried state**: if $z\in\mathcal R_a$ (state written by entry $a$) and $\tau$, then read $[k]_b$ and write $[v]$. Its key is $(\mathcal R_a,\tau)$, a region of state space, not a prompt row. Such regions:
- depend on seed and history (§3.6);
- are combinatorially many;
- are not enumerable from the prompt.

**[Conj]** A practical table should therefore have two tiers:
- **Static tier.** Attribute entries keyed $(\mathcal H,\tau,[k])$ with locked preconditions. These transfer across prompts and templates.
- **Dynamic tier.** Relational entries stored as *programs* evaluated against the live carried state, not as payload vectors. Examples are the chair's coordinated source-and-destination field over steps 0–1, and a C→A pointer re-derived from the recipient's own formation.

The Mamba relation operator that "escaped the lookup table" fits this tier. A coordinate-wise affine map from the held prompt's own relation node is reported to have built carriers for unseen `above` and `inside` relations, where a closed carrier bank could not. That is reported in `obsidian/blog/2026-09-03-213738-the-relation-operator-escaped-the-lookup-table.md`. I cite it qualitatively only and quote no numbers, because I did not read its primary record.

---

## 5. Q4 — Time: why early installs change composition and late installs change colour

### 5.1 A general principle: monotone loss of reachability

**[Thm] Reachable sets shrink along the trajectory.** Let $\mathrm{Reach}(z_k)=\{R(\Phi_{k:T}(z_k;S_k,\dots,S_{T-1})):S_j\in\mathcal S\}$ be the outputs reachable by any source schedule from $z_k$. If $z_{k+1}=\Phi_k(z_k;S_k)$ for some admissible $S_k$, then

$$
\mathrm{Reach}(z_{k+1})\subseteq\mathrm{Reach}(z_k).
$$

*Proof.* Prepend $S_k$ to any schedule from $z_{k+1}$. ∎

This holds for any deterministic system: diffusion calls, AR depth with per-layer source writes, SSM steps. The content of "coarse-to-fine" is *which* components leave the reachable set first. That needs a model of the dynamics.

### 5.2 Linear-Gaussian rectified flow: a quantitative ordering

**Model.** Take one eigen-component of the data with prior $x_0\sim\mathcal N(\mu,\lambda)$, and the rectified-flow path $x_t=(1-t)x_0+t\epsilon$. The program sets the conditional mean $\mu$ (A before the switch time $t_s$, B after). The marginal is $x_t\sim\mathcal N((1-t)\mu,\ (1-t)^2\lambda+t^2)$. The 1-D probability-flow ODE preserves the standardised value, so

$$
x_0=\mu_B+\sqrt{\frac{\lambda}{(1-t_s)^2\lambda+t_s^2}}\ \big(x_{t_s}-(1-t_s)\mu_B\big).
$$

From the same noise, $x^{\text{tgt}}_{t_s}-x^{\text{rec}}_{t_s}=(1-t_s)(\mu_B-\mu_A)$.

**[Thm] Register retention and program authority.**

$$
\rho(t_s)=\frac{Y_{10}-Y_{00}}{Y_{11}-Y_{00}}=\sqrt{\frac{\mathrm{SNR}}{1+\mathrm{SNR}}},\qquad \mathrm{SNR}=\frac{(1-t_s)^2\lambda}{t_s^2},\qquad \frac{Y_{01}-Y_{00}}{Y_{11}-Y_{00}}=1-\rho,\qquad i=0 .
$$

Here $Y_{10}$ is the target register with the recipient program, and $Y_{01}$ the recipient register with the target program. For VE/VP samplers with noise $\sigma$, the same derivation gives $\rho=\sqrt{\lambda/(\lambda+\sigma^2)}$.
- *Numerical check.* A 20k-step Euler integration of the PF-ODE at $(\lambda,t_s)\in\{(0.5,0.6),(2,0.3),(0.1,0.8)\}$ gives register progress 0.42639 / 0.95702 / 0.07881, against the formula's 0.42640 / 0.95702 / 0.07881. Program progress is the exact complement (`checks.py`).

**[Thm] Corollary: coarse-to-fine by prior variance.** $\rho$ is increasing in $\lambda$ and in $1-t$. Components with large prior variance, conditional on what is already locked, lock first. Late sources keep authority only over low-variance components. Two consequences:
- **Composition and framing** are the highest-variance components of an image, so they lock first.
- **Eye geometry** is coupled to face and layout geometry: the FLUX self-delta assembles eye shape from both eye tokens and the surrounding face ring, and the union is stronger than either alone [Meas — eye-geometry-findings]. It is effectively a high-variance, layout-conditioned component and locks early. Iris colour is a small-variance, nearly layout-independent component and stays free until late.

This is the noise-level argument of `architecture-math §7`, made exact in the linear model.

**[Thm] Corollary: whole-image distance misranks attribute edits.** Early installs move the high-$\lambda$ components, which dominate pixel distance. An early edit therefore scores high on whole-image progress even when it misses a low-variance target. [Meas — `research/demos/scene-editing.md` §5.3] Eye colour early $P=0.5772$ with the eyes still blue; late $P=0.0689$ with violet irises.

### 5.3 Diffusion evidence for time-indexed authority

All of the following come from primary records:

- **SDXL base-K/V lesion.** MAE 20.8215 at call 0 versus 2.1535 at call 14 (ratio 9.67). [Meas — `research/demos/artifacts/scene-generator/sources/qkv-findings.md`]
- **Scene-editing early/late table.** Late-only $P$ is ≤ 0.0689 for all four edits; early-only $P$ is 0.5772–0.7841. [Meas — `research/demos/scene-editing.md`]
- **FLUX eye-register insertion.** Retained after $t_0..t_3$: 0.342 / 0.488 / 0.675 / 1.0 (blue medic) and 0.149 / 0.255 / 0.542 / 1.0 (red violinist). The direction at $t_0/t_1$ is already aligned with $t_2$: 0.436 / 0.757 and 0.389 / 0.656. [Meas — eye-geometry-findings]
- **Ownership transfers from text to image state.** Text-only replacement at `single.0` reaches `single.19` projection 1.005, 0.826, 0.463, 0.134 at $t_0..t_3$. Both-stream final RGB leverage rises from 0.149 at $t_0$ to 0.707 at $t_3$. [Meas — eye-geometry-findings]
- **Chair transport.** Late steps alone give departure 0.0006; steps 0–1 alone give 0.9978. [Meas — chair FINDINGS]

**[Comp] A single-λ test on the eye-register curve.** Invert $\rho$ into $u=\log\frac{\rho^2}{1-\rho^2}=\log\mathrm{SNR}_{\text{eff}}$:

| | after $t_0$ | after $t_1$ | after $t_2$ |
|---|---:|---:|---:|
| $\mathrm{SNR}_{\text{eff}}$, blue | 0.132 | 0.313 | 0.837 |
| $\mathrm{SNR}_{\text{eff}}$, red | 0.023 | 0.070 | 0.416 |
| $u_{\text{blue}}-u_{\text{red}}$ | 1.76 | 1.50 | 0.70 |

- *What the model predicts.* A single-component linear-Gaussian model predicts that the curves of two characters differ by a constant shift $\log(\lambda_{\text{blue}}/\lambda_{\text{red}})$ at every step.
- *What the data show.* The shift is not constant, so the eye register is not one Gaussian component. It is at least a mixture.
- *Reading.* This fits the record's own reading: "progressive formation plus prompt-local repair". The monotone increase itself is predicted. I report this as a measured *limit* of the linear model, not a confirmation.

**[Conj] Binding locks early because early reads are undecided.** At high noise, queries carry little image structure, so cross-attention is diffuse. That makes $\alpha(1-\alpha)$ large, and with it both binding gains of §3.4. As the carried state sharpens, reads commit and the address path's gain falls as $O(\varepsilon)$ (§2.2). Two kinds of support:
- this is consistent with chair transport being done by steps 0–1;
- it is consistent with the K×V conjunction being measured at call 0 of SDXL.

Direct test: P9.

### 5.4 The AR analogue: depth is the time axis

- **[Id] Normalisation gain falls with residual norm.** The read gain is $\propto1/\|x^\ell\|$ (§2.2). As the residual norm grows over depth, a write of fixed norm moves every later normalised read less.
- **[Conj] Depth-SNR.** Define $\mathrm{SNR}_\ell\sim\|x^\ell\|^2/\|\delta\|^2$. It plays the role of the diffusion SNR: an earlier write locks more of the downstream computation.
- **[Thm] (§5.1 specialised to depth).** A source write at layers $\ge\ell$ cannot change any read that other positions performed at layers $<\ell$. Pointers formed at the C-clause and query positions before the late band are therefore locked by the time the band is written. **Relational reachability closes at an earlier depth than direct-attribute reachability.**
- **[Meas] Direct versus indirect reads.**
  - *Alias.* Recovery holds for seeding at ≤ L19 and fails at L23, falling to the competitor (`qwen-formation-replay` report).
  - *B-store.* The direct B read is reachable from L22–27 alone (4/4). The indirect C read needs L12–21 (B-store FINDINGS).
- **[Meas — `research/demos/qwen-causal-programs.md`] Address versus payload in depth.** Address-type parity sits at K@L12; payload-type square/maximum sits at V@L20.
- **[Meas — `saturn/experiments/2026-10-02-formation-over-time/results/FOT_analysis.json`] Formation-over-time.** This is the attribute (identity) case:
  - freezing the whole band's attention+MLP at the subject leaves rescue at 0.904 (Qwen) and 1.023 (Gemma);
  - the best single band layer reaches 0.732 / 0.804;
  - cutting consumer→subject attention drops rescue to 0.010 / 0.015;
  - blocking the subject row's reads of earlier positions *inside the band* leaves rescue at 0.810 / 1.046 (F3b fired).

  So the identity store is formed **token-locally** in the subject's own residual before the band, then committed and read at the subject position. This fits §4.4: a single-entity attribute is a single-address entry with a locked precondition. The theory predicts the contrast case: for relational queries the cross-position block *should* matter (P8).
- **Mamba.** The commit is the write, not the retention: release hurts 0/6, dt-via-write 6/6, dt-via-retention 0/6 [Meas — clock retest FINDINGS]. Relations need staged composition across transitions (§2.5).

### 5.5 The general principle

**[Thm] Monotone loss of controllability.** The carried state progressively constrains what later sources can change (§5.1).

**[Thm, linear-Gaussian] Variance ordering.** The order is by prior variance conditional on what is already locked (§5.2).

**[Conj] Binding before payload, for networks.** Address and binding decisions, being high-variance and undecided reads, lock before payload decisions. In diffusion that is layout and geometry, then colour. In AR depth it is pointers at other positions, then attribute payloads in the late band. In Mamba it is staged transitions, then the late writer. This links the eye-geometry/colour timing, the alias depth profile, the B-store depth split and the K@L12 / V@L20 program split.

**[Meas] Ownership transfers to the carried state.** Over the trajectory, the dominant parent of each step's update moves from the source to the carried state: text ownership 1.005 → 0.134; scheduler-register share at $t_2$ is 0.283 / 0.217 against action 0.717 / 0.784 (eye-geometry-findings).

---

## 6. Q5 — Predictions that separate this model from simpler ones

### 6.1 The alternatives

| Model | What it asserts | Signature predictions |
|---|---|---|
| **Source-keyed symbol table (STab)** | Behaviour is a function of installed prompt-row entries $(k,v)$ | K+V ≥ K-only, V-only; effect independent of recipient carried state and of install order; rows are addresses |
| **Additive steering (Add)** | $Y=Y_0+\sum_e\beta_e$ | $i=0$ everywhere; dose-linear; sign-symmetric; query-independent |
| **Fixed per-attribute circuit (FixC)** | Each attribute has a fixed set of heads, rows and time, possibly with a fixed conjunction unit | Consumer and source sets fixed per attribute; interactions survive frozen routing (they are computed by fixed units); timing independent of preceding state |
| **This model (Route)** | Payload-linear given $\Gamma$; $\Gamma=\Gamma(z)$; relations are $H_{Q\circ V}$ in carried state; time-indexed authority | Below |

### 6.2 Predictions

Each prediction gives its derivation, how it discriminates, a protocol on existing Saturn machinery, and a falsifier.

**P1 — Frozen-routing additivity. Most important.**
- **Derivation.** §2.3.
- **Prediction.** For any 4-cell of source edits:
  - with $\Gamma$ frozen to the base cell's routing (attention probabilities at every self- and cross-attention call, gates and norm scales), $|i_{\text{frozen}}|\le0.25\,|i_{\text{live}}|$;
  - the single-factor main effects persist, at a reduced magnitude.
- **Freezing only cross-attention** (SDXL) or only one band's attention (Qwen) apportions $i$ between those routing sites and the rest.
- **What each alternative predicts.**
  - Route: interaction collapses.
  - FixC with a fixed conjunction unit: the interaction survives.
  - Add: $i_{\text{live}}=0$ already.
  - STab: says nothing about the mechanism; if entries are self-contained, freezing α should not destroy the joint entry's effect.
- **SDXL protocol.**
  - Use the panel's subject × eye_color and eye_color × hair_color 4-cells.
  - Capture the base cell's attention probabilities at all calls with a probability-replay attention processor at the scene-generator per-site hook. The Q×K×V factorial already holds Q fixed and swaps K/V per site, so the hook point exists.
  - Replay edited V with frozen probabilities and frozen GroupNorm statistics.
  - Measure $i$ on the factor-specific axis.
- **Qwen protocol.** Composed `A|P` 4-cell (colour edit × position-binding edit). Freeze L16–27 attention probabilities by an eager-attention probability override; route-write-future already overwrote L22 probabilities.
- **Falsifier.** $|i_{\text{frozen}}|\ge0.75|i_{\text{live}}|$ → the conjunction is computed by a fixed nonlinear unit on payloads (FixC), not by state-dependent routing.

**P2 — The stale-pointer signature for relational installs.** Qwen.
- **Derivation.** §3.2, §3.7.
- **Prediction.** Split donors into **binding-changing** (which entity is where, or what C refers to) and **payload-only** (same binding, different value). For binding-changing donors on relational or composed queries, late-band installs at the source row should behave as follows:
  - (a) K-only and K+V return the **competitor binding** more often than the donor or clean value;
  - (b) V-only recovers the requested value at least as often as K+V;
  - (c) query→requested-row attention mass falls under K-only and K+V ($E<1$) and is unchanged under V-only, within ±0.05;
  - (d) for payload-only donors, K+V works with no alias limit.
- **What each alternative predicts.** STab predicts K+V ≥ V-only, with no dependence on donor type. Add predicts no competitor-specific failure.
- **Protocol.** `alias-explicit` and B-store organisms, plus the Qwen symbol-table panel's composed queries, with the existing per-(layer, KV-head, position) overwrite.
- **Falsifier.** V-only < K+V in binding-changing rows, *or* the failure mode is not the competitor.

**P3 — Joint-swap invariance.** Qwen T2, SDXL.
- **Derivation.** §4.1. Swap entity0 and entity1 band records.
  - **K-only.** It moves the composed answer toward entity1, and attention moves.
  - **V-only.** It moves the answer toward entity1, and attention does not move.
  - **K+V jointly.** It is a row relabelling, so the answer is approximately unchanged: $|\Delta|\le0.25\times$ the K-only effect. The interaction is therefore $i\approx-(\Delta_K+\Delta_V)$.
- **Deviations from exact invariance** can come only from three sources:
  - RoPE relative-position terms;
  - mask asymmetry;
  - copies already carried in pre-band residuals, the §3.7 mechanism.

  To isolate content address, swap **pre-RoPE** K and re-rotate at the destination.
- **What each alternative predicts.** A row-addressed STab predicts that K+V moves the answer fully.
- **Falsifier.** K+V joint swap ≥ 0.75 of the K-only effect with pre-RoPE swapping.

**P4 — The time law for attributes.** SDXL panel.
- **Derivation.** §5.1–5.2.
- **Install-time sweep.** Install each factor's target source only for calls ≥ $k_0$, and only for calls < $k_0$, with $k_0$ on a grid. Predictions:
  - (a) Register-retention $\rho_f(k_0)$ (the target register at $k_0$ with recipient program after) is monotone non-decreasing in $k_0$.
  - (b) Program-only + register-only progress $\approx1$ with $|i/\tau|\le0.2$; the measured FLUX value is −0.116.
  - (c) Ordering of the half-authority call: $k_{1/2}(\text{background})<k_{1/2}(\text{subject})\le k_{1/2}(\text{hair})<k_{1/2}(\text{eye colour})$.
  - (d) Single-λ check: $u_f(k)-\log\mathrm{SNR}_{\text{sched}}(k)$ is constant in $k$ for a one-component feature. Its failure counts components; it is expected to fail for eye features, per §5.3.
  - (e) Early×late $i>0$, with late authority amplified by the early-prepared state, as in the FLUX 4.5–13×.
- **What each alternative predicts.** FixC with a static time profile predicts $i=0$ and no amplification. Add predicts $i=0$.
- **Falsifier.**
  - Crossing $k_{1/2}$ order, e.g. eye colour locks before background.
  - $i\le0$ in early×late.
  - Non-monotone $\rho$.

**P5 — Sequencing composes, simultaneity interacts. Most important for the symbol table.**
- **Derivation.** §4.4 (ii), §5.2.
- **Install orders.** For a same-object pair where one attribute defines the other's support (FLUX colour × shape, or SDXL subject × eye_color), compare four installs:
  - A: shape (or subject) program at early calls only, then colour program at late calls only;
  - B: the reverse;
  - C: simultaneous independent addition;
  - D: native joint.
- **Prediction.** Progress(A) ≥ 0.8 and > progress(C) + 0.3; progress(B) ≤ 0.5. For a disjoint-support pair (eye_color × hair_color), A ≈ B ≈ C, within 0.1.
- **What each alternative predicts.**
  - STab and Add predict order independence.
  - FixC predicts that C reproduces D whenever the per-attribute circuits are installed.
- **Protocol.** The existing early/late install machinery (scene-editing 4-call schedule in FLUX; any call split in SDXL).
- **Falsifier.**
  - A ≤ C.
  - A ≈ B for the support-defining pair.
  - A ≠ C for the disjoint pair.

**P6 — Consumer overlap follows reader region; source overlap follows address.** SDXL panel.
- **Derivation.** §4.5.
- **Prediction.** Top-8 consumer-head overlap is higher for two edits of the *same* region (eye colour c1→c2 versus c1→c3) than for *different* regions (eye colour versus hair colour), by ≥ 2/8. Source-cluster overlap (in $\Sigma_\tau$ metric) is governed by attribute content, not region.
- **What each alternative predicts.** FixC predicts consumer heads fixed per attribute *type*: all colour edits share heads regardless of region.
- **Falsifier.** Same-region overlap ≤ cross-region overlap.

**P7 — The address is low-rank in key space and not row-sparse.** SDXL and Qwen Part A.
- **Derivation.** §2.4, §4.2.
- **Prediction.** Project the full contrast $\Delta K$ onto the top-$r$ eigendirections of $\Sigma_\tau$ and install it, keeping all rows. This recovers ≥ 0.7 of the K-only attention effect at $r\le8$ per head, while the top-$r$ *rows* recover ≤ 0.3.
- **Clustering prediction.** k-means in $\Sigma_\tau$-whitened K gives higher role-cNMI than raw L2-normalised K.
- **What each alternative predicts.** A row-keyed STab predicts that row subsets suffice.
- **Falsifier.** Top-$r$ rows ≥ rank-$r$ projection.

**P8 — The hop-depth law.** Qwen, new experiment.
- **Derivation.** §5.4.
- **Chains.** 0-hop (direct "A stores X"), 1-hop ("C refers to A"), 2-hop ("D refers to C").
- **Prediction.** The last residual-seed layer at the source anchor that still recovers the requested value, $\ell^*_k$, is strictly decreasing in the hop count $k$. The minimal source K/V depth band needed for transfer moves earlier with $k$. The cross-position block during formation (FOT test 3b) should matter for $k\ge1$, though it did not for identity (F3b fired at 0.810 / 1.046).
- **What each alternative predicts.** STab and FixC predict one depth for all.
- **Falsifier.** $\ell^*_1\ge\ell^*_0$.

**P9 — Interaction concentrates at undecided reads.** SDXL.
- **Derivation.** §3.4.
- **Prediction.** Run per-site, per-call K×V factorials, as in the existing Q×K×V factorial but swept over sites and calls. The image-level interaction should be concentrated at (site, call) cells whose touched-slot attention $\alpha_s$ is near $1/(1+\sqrt E)$, and at early calls where cross-attention entropy is highest. The Spearman correlation between per-cell $|i|$ and $\alpha_s(1-\alpha_s)|E-1|/D$ should be ≥ 0.5.
- **What each alternative predicts.** FixC predicts that the interaction tracks fixed sites regardless of α.
- **Falsifier.** Correlation ≤ 0.

**P10 — Causal-encoder binding lives at the head word. Cheap SDXL test.**
- **Derivation.** §3.3. CLIP is causal, so *blue→eyes* cannot be in "blue"'s row.
- **Prediction.** Installing only the colour word's K/V rows (template A "blue eyes") transfers the colour with **more off-target leakage** (hair, clothes, background chroma) than installing the colour word plus the "eyes" row plus the EOS/padding rows. The latter has ≥ 2× better target/off-target ratio.
- **Template B.** "black-haired …": the hair-colour binding sits at "haired" and later.
- **What each alternative predicts.** A token-keyed STab predicts that the colour row alone suffices.
- **Falsifier.** The colour-word row alone gives target/off-target ratio ≥ the bound-set ratio.

The three most important are **P1** (it tests the core claim that interactions are routing through carried state), **P2** (it explains the alias limit and predicts its failure mode) and **P5** (it turns time-indexed authority into a composition rule a symbol table can use).

### 6.3 Mapping to the two experiments being preregistered

**Qwen — `saturn/experiments/2026-10-02-qwen-address-symbol-table/PREREG.md`** (read 2026-10-02):

| Prereg test | Relation to this theory | Cheap addendum recommended |
|---|---|---|
| Part A: K clusters by role, not token (raw L2-normalised K, k-means k=8) | Tests §4.2's "address ≠ token". Prediction agrees with P-A | Repeat clustering in $\Sigma_\tau$-whitened K, with $\Sigma_\tau$ from the band's live consumer queries (P7). Report entity-slot cNMI separately: bindings formed pre-band (§3.3) predict entity-slot cNMI > 0. Note that raw post-RoPE K mixes position into the geometry |
| T1: attribute edit by address cluster | §4.4: single-entity attributes with locked preconditions are separable. Predict P-T1a,b,c pass for colour and size | None needed |
| T2: K-only rebinds, V-only changes content | P3 agrees on K-only and V-only | **Add a prediction for the "both" arm:** joint K+V swap ≈ invariant (≤ 0.25 × K-only), with interaction ≈ −(K+V). Swap pre-RoPE K if feasible, otherwise report RoPE as a confound |
| T3: K/V-only under-transfers and mis-binds relations; residual completes | P2 agrees on direction but **refines the condition**: the alias limit should appear only for *binding-changing* donors. Payload-only donors should transfer by K/V | (i) Tag each T3 row as binding-changing versus payload-only. (ii) Add a **V-only** arm; predict V-only ≥ K+V on binding-changing rows. (iii) Record whether the wrong answer is the *competitor* entity. (iv) **Warning:** the band-entry (L21→22) seed may itself under-transfer on binding-changing relational rows (alias: L19 works, L23 fails). Add an L12 seed arm so that P-T3c is not falsely failed |
| T4: query selectivity of entries | Consistent with the role machine. The theory adds that selectivity ∝ the queried read's $\alpha$ on the entry | Optional: log $\alpha$ on the entry's rows per query |

Not tested by the Qwen prereg, and needing new runs: P1 (frozen routing), P8 (hop-depth), and the depth analogue of P4.

**SDXL — `saturn/experiments/2026-10-02-sdxl-address-symbol-table/`.** At the time of writing this holds `panel.json`, `code/make_panel.py` and `proof-sheets/`, and **no PREREG**. The panel is:
- subject × eye_color × hair_color × background, for 96 prompts (74 development, 22 held out);
- template A (canonical order) for table construction;
- template B (reordered) as an address-versus-token stress set.

The panel's own comments label background "coarse / early", hair "mid" and eye colour "fine / late".

- **What the panel can test directly.**
  - P4 (time law, ordering of $k_{1/2}$, closure partition, early×late $i$);
  - P5 for subject × eye_color (support-defining) versus eye_color × hair_color (disjoint);
  - P6 (consumer overlap by region);
  - P7 (A→B transfer of K-cluster entries; low-rank versus top-rows);
  - P10 (causal-encoder binding: colour word versus colour + "eyes" + EOS/padding rows);
  - P9 (per-site, per-call K×V);
  - P1 (frozen-routing 4-cells), if a probability-replay processor is added.
- **What it cannot test.**
  - There are no inter-object relations in the panel: one character, and every factor is an attribute or a background. P2/P3-style relational predictions in diffusion need a new two-object panel, e.g. "a knight to the left of a witch" with left/right swaps, or a chair-type transport organism.
  - A source-only table on this panel is expected to look *good*, because the factors are attributes with near-locked preconditions. That should not be read as evidence that tables suffice for relations.
- **Recommendation for the SDXL PREREG.**
  - Freeze P4(c), P5 and P10 as primary predictions, with their falsifiers.
  - Include a disjoint-support control pair (eye × hair).

---

## 7. Q6 — What cannot be known with current interventions

1. **[Thm] There is no canonical coordinate system.** For any invertible $\phi$ on carried state, $(\phi\circ L_m,\pi_m\circ\phi^{-1})$ is an equally valid scaffold (`architecture-math §1.3`). Inside attention the gauge $A\in GL(d_h)$ and the common key offset leave every score unchanged (§4.1). Consequences:
   - k-means in raw K coordinates is a basis-dependent statistic;
   - only score-level quantities ($d_\tau$, attention, causal effects) are functional;
   - a symbol-table key is an *equivalence class*, $[k]$ modulo $d_\tau=0$ and $[v]$ modulo $\ker(J W_O)$, never a vector.
2. **[Thm] Addresses outside the live query span cannot be identified.** Key components orthogonal to every live query in window $\tau$ have no effect in $\tau$. They are unidentifiable until a later window's queries reach them. No intervention restricted to $\tau$ can distinguish $k$ from $k+n$ with $\Sigma_\tau n=0$.
3. **[Thm] Lowering is many-to-many, so minimal sets are not identifiable.** Redundant and counteracting paths ($Y=h\lor s$; $Y=2h-s$, MATH.md) make minimal site sets non-unique. Single-cut signs can oppose the coalition: Qwen L25/KV0 is +0.726 and +0.356 against a strongly negative coalition [Meas — head-edge FINDINGS]. Block-and-rescue identifies sufficiency and necessity *of the declared set*, not uniqueness.
4. **[Thm] The role subspace must not be spanned by generic features.** Role features add identifiable prediction only along $(I-P_G)X_R\neq0$ (MATH.md). A symbol table's gain over generic features (attention mass, norms, layer, position) is identifiable only on that residual. If the table's keys are linear functions of attention mass and position, it cannot be distinguished from a generic predictor.
5. **[Thm] Local Jacobians are not identified.** $c'=c+v$, $d'=d-A^\top v$ give identical natural responses (MATH.md). Without spanning independent interventions on the carried state, the split "history authority versus new-row authority" is not identified.
6. **[Thm] A finite grid cannot rule out dependence outside the grid.** A 4-cell certifies consumer *form* on the tested support only. $g(h,s)=s+hs(s-1)$ is serial on $\{0,1\}$ and history-dependent at $s=2$ (MATH.md). "Separable" (§4.4) is always "separable on the tested doses".
7. **[Thm] Endpoints cannot separate K×V from consumer curvature.** Any finite endpoint table is implementable by a feedforward consumer (MATH.md). Attributing a measured $i$ to $H_{K\times V}$ versus $H_{\text{cons}}$ needs the *internal* read output $o$ measured at the site, not only the image or logit.
8. **[Thm] Frozen routing is an off-manifold intervention.** P1 identifies "interaction mediated by changes of the frozen quantities, given everything else frozen". Freezing α while gates live, and vice versa, does not uniquely apportion $i$, because the routing variables are coupled: gates read the post-attention residual. Only nested freezes (α only; α+gates; α+gates+norms) bound the shares.
9. **[Thm] Authority is a property of the trajectory and the perturbation family.** $\|\partial s_T/\partial S_k\|$ depends on the norm, the perturbation direction and the trajectory. By §5.1 it changes with every earlier intervention. "The authority curve of eye colour" is defined only for a declared trajectory and edit family. The fitted $\lambda_f$ of §5.2 is an effective parameter; the eye-register curve already rejects a single shared λ, so components are only partly identifiable from four time points.
10. **[Thm] A relation has no unique vector.** A relation is a property of the carried-state trajectory. Its Möbius residual $I$ depends on the reference corner and the factorisation. Its direction changed under rephrasing while the dose law stayed fixed [Meas — eye-geometry-findings]. What is identifiable is the **contract**: dose law, sign, address-roll control and consumer response. The vector is not.
11. **Mechanism of the query is not yet observable.** Current tooling patches K/V, residuals and attention probabilities. It does not yet patch $q$ at the consumer independently of the consumer's residual. Without a q-only intervention, the stale-pointer account (§3.7) is supported by the competitor outcome, the depth profile and the $I/V$ sign law, but not directly identified. **[Pred] P2(c) closes this gap.** It measures query→row attention under K-only versus V-only; a q-transplant arm from the clean run would test it directly.
12. **Diffusion source sufficiency is architectural.** Because $S$ is complete by construction, no source-side experiment can localise a relation in $S$. By §3.3 the relation is not in $S$. Localising it requires carried-state interventions (register, image pre-state), and those are high-dimensional and seed-dependent (point 10).

---

## 8. Summary of what is new relative to `architecture-math-2026-10-02.md`

**[Thm] Conditional payload-linearity (§2.3).** Every interaction is routing, and routing is a function of carried state.

**[Id] Query-path covariance and the two-candidate reduction (§2.2).** The address path is $\mathrm{Cov}_\alpha(v,k)$, with gain $\alpha(1-\alpha)$. It is the same factor as the K×V interaction, which peaks at $\alpha^*=1/(1+\sqrt E)$.

**[Id]/[Thm] Single-read lemma (§3.2).** It yields the pointer theorem, the layer-0 and causal-encoder locality theorems, and the image-side relation theorem for diffusion.

**[Comp] Re-reads of existing data that support routing-through-state:**
- the Qwen $I/V$ sign law;
- positive early×late interactions with 4.5–13× late amplification;
- the closure partition $i/\tau=-0.116$;
- the chair departure interaction of 1.353;
- the alias depth profile (L≤19 / L23 / L26 → fox / cat / bird, with the competitor as the predicted failure).

**[Thm] Gauge-invariant address metric $d_\tau$ and the symbol-table entry tuple (§4).** It gives a separability theorem and a two-tier table: static attributes plus dynamic relational production rules.

**[Thm] Nested reachability and the exact linear-Gaussian rectified-flow retention law (§5).** The law is verified numerically. Its single-λ form is rejected by the existing eye-register data, which is reported as a limit.

**Correction to the SDXL "Q drift" reading.** It is a cross-trajectory divergence of the address, not a single trajectory's drift (top of document).

**Ten predictions (P1–P10)**, mapped to the two preregistrations, with addenda for the Qwen T2 and T3 arms.
