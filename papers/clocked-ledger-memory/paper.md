---
title: "A Clocked Ledger: Exact, Time-Aware Memory for a Frozen Language Model"
type: research-paper
status: draft
date: 2026-09-23
updated: 2026-09-23
tags: [memory, long-context, retrieval, babilong, longmemeval, binding, frozen-llm, spf]
---

# A Clocked Ledger: Exact, Time-Aware Memory for a Frozen Language Model

**Append-only records, exact integer time and entity ⊗ role binding keys let a frozen 1.5B model chain facts, know which fact is current, and never repeat an expired one, where retrieval and long context cannot**

Jacob Hollenbeck

*2026-09-23 (draft; §4.7 awaiting the same-reader LongMemEval baselines)*

> Every number in this paper is measured on one RTX 4080 and traceable to a file in `evidence/` (hashes in `evidence/SHA256SUMS`). Assertions that are not measured are marked ASSERTED.

---

## Abstract

Language models answer questions about long histories in two ways: they read the history (long context) or they read what a retriever ranks as similar (RAG). Both hand the model a *mixture*. It must work out for itself which fact is newest, which has expired, and how facts chain. Neither mixture carries time as anything but text.

We test a different split. A small learned front end reads sentences and marks events. An exact back end files them in an append-only ledger with an integer clock and optional lifetimes. The back end then reads by exact selection: the latest record under a key, a second hop through the entity that record names, and an integer expiry test. In the strongest variant, facts are stored under **binding keys**, a phase sum `φ(entity) + φ(role) mod 2³²`, so that "where is the football?" is resolved by the memory itself and the reader sees one decisive sentence.

With the reader held fixed (frozen Qwen2.5-1.5B-Instruct), BABILong two-fact chaining at 128k tokens rises to **0.91–0.97**. The comparisons on the same questions:
- retrieval: 0.11–0.15
- long context: 0.24
- the unbound ledger: 0.57–0.61

These scores hold with every test name, object and room absent from training. On event phrasings written and frozen before any training change, chains score **0.90–0.92**. A hand-written template rule scores **0.00** on held-out phrasing.

On "where is X now" after idle gaps of up to 10⁸ ticks, the ledger scores **0.92–0.93**; the next best LLM arm scores 0.63. On facts with lifetimes, the ledger gives **no stale answers after expiry**, where every LLM arm gives a stale answer 72–79% of the time.

On LongMemEval-S (500 real chat questions, 4-bit Qwen2.5-7B reader), the ledger answers single-session facts at 0.73–0.83, knowledge updates at 0.68 and abstentions at 0.80. It is weak on preferences, cross-session counts and relative-time questions. §4.7 isolates how much of that gap is the memory and how much the reader.

---

## 1. The problem

Ask a model "where is Mary?" over a 128,000-token book in which Mary moved six times. Long context hands the model all six moves plus the book. Retrieval hands it the five sentences most *similar* to the question, which need not include the latest move. In both cases the model must pick the newest of several candidates from their text alone. Small models do this badly: in our measurements, picking the latest of four dated records costs about 20 points (§4.2).

Two further questions are harder still:
- **Chaining:** "where is the football?" needs *who has it*, then *where that person is now*.
- **Validity:** "is this fact still true?" needs arithmetic against a stated lifetime.

Retrieval ranks by similarity. It has no notion of "latest" or "expired", and it cannot follow a chain whose second step shares no words with the question.

Our design rule comes from earlier work on exact phase formats (SPF): **keep things separate, select exactly, never blend**. Every failure above is a blend: several candidates superposed in one context, left to a soft reader to disentangle. The ledger removes the blend. Learning is used only where language requires it, to decide that a sentence is an event and who and what it is about. Everything after that is exact integer bookkeeping.

---

## 2. The clocked ledger

### 2.1 Write path (learned, small, trained without any test entity)

Each sentence passes through the first 14 layers of the frozen reader (Qwen2.5-1.5B-Instruct), and small heads read those states:

| component | input | output | trained on |
|---|---|---|---|
| mention tagger | token states | entity-mention spans | training names and objects, generic syntax (leading clauses, passives) |
| write gate | mean-pooled sentence state | event vs narrative | training-name events vs narrative and WikiText |
| relation head (bound variant) | mean-pooled state | move / take / drop / give / other | training templates plus narrative negatives |
| role taggers (bound variant) | token states | agent / object / place / recipient | as above; **places exclude every bAbI room** (E8b) |

Each head is a 2-layer MLP of width 256. Training names, objects and places are disjoint from every test entity:
- test names: Mary, John, Sandra, Daniel, …
- test objects: football, apple, milk
- test rooms: kitchen, hallway, …

### 2.2 The record

`Record(t, text, keys, ttl)`:
- `t` is an integer tick (sentence position, or a stated time).
- `ttl` is an optional lifetime, parsed by the same numeral pattern the rule baseline uses.

Records are append-only; nothing is overwritten or averaged. Keys index into a hash table, so a lookup is O(1) and has no ties.

### 2.3 Read path (exact, no learning)

- **Plain ledger (h2m1):**
  - hop 1 takes the latest valid record for each question key
  - hop 2 takes the latest valid records for every other entity those records mention, up to now and up to the hop-1 time

  The selected records, in time order, are the reader's entire context.
- **Expiry:** a record is valid at time `T` iff `t ≤ T` and `T − t < ttl`. This is an integer test. Expired records are never selected, and if nothing valid remains the memory abstains.
- **Bound ledger:** each event updates typed state under binding keys `bind(e, r) = (φ(e) + φ(r)) mod 2³²`, where φ is a 32-bit hash:
  - move: `agent⊗loc ← place`
  - take: `object⊗holder ← agent`
  - give: `object⊗holder ← recipient`
  - drop: `object⊗holder ← ∅` and `object⊗at ← agent's location at that tick`, an exact read at write time

  "Where is O?" returns the holder's latest location if O is held, otherwise O's drop location. The reader sees only the one or two records that decide it. We also report `bound-direct`, the bound value with no reader at all.

The binding key is the conjunctive-binding idea in its exact form. An entity and a role are combined by phase addition on an integer ring, giving one address per pair. Nothing is superposed, so there is no crosstalk between Mary's location and Mary's possessions. With oracle roles the resolver scores 1.00 on all generated chain documents (§4.4).

---

## 3. Setup

- **Reader:** frozen Qwen2.5-1.5B-Instruct (bf16) for BABILong and the generated tasks; frozen Qwen2.5-7B-Instruct (4-bit NF4) for LongMemEval. No weights are tuned.
- **Metric (BABILong, generated tasks):** restricted-label cloze. The answer is the argmax over the task's closed label set at the answer position, after an answer cue that gives baselines their strongest shot (§A.1).
- **Seeds:** 3 writer seeds (17, 29, 43). 95% intervals are bootstrap intervals over questions, about ±0.07–0.10 at n = 100.

**Baselines** (same reader, prompt and scorer):

| arm | context |
|---|---|
| no memory | question only |
| long context | the most recent 32k tokens of the document, with the instruction and examples kept intact (§5.1) |
| RAG dense | bge-small top 5 sentences, in document order, with positions |
| RAG BM25 | BM25 top 5 |
| RAG timestamps | dense top 8, re-ranked by recency, top 5 |
| hand rule | regex over the training templates: latest move per name, TTL check |

**Held-out discipline:**
1. Every test name, object and (in E8b) room is absent from writer training.
2. E4 generates chain and time documents from a true simulator, rendered with the training templates, with a held-out phrasing set (PARA), and with a second held-out set (PARA2). PARA2 was written after PARA results were seen and before any training change, then frozen.
3. Filler is WikiText, split so that training and test halves never share a sentence. BABILong filler is PG19.

---

## 4. Results

### 4.1 BABILong: chaining facts that retrieval cannot

Accuracy on 100 questions per cell. Ledger arms show 3 seeds; baselines are single runs. Long context uses the corrected truncation (§5.1).

| task | length | long context | RAG dense | RAG timestamps | plain ledger (gated) | **bound ledger (E8b, rooms held out)** |
|---|---|---|---|---|---|---|
| qa1, 1 fact | 64k | 0.56 | 0.82–0.89 | 0.69–0.78 | 0.94–1.00 | **0.96–0.98** |
| | 128k | 0.44 | 0.81–0.83 | 0.69–0.71 | 0.92–0.99 | **0.96–0.98** |
| qa2, 2 facts | 64k | 0.31 | 0.13–0.15 | 0.14–0.16 | 0.55–0.60 | **0.91–0.97** |
| | 128k | 0.24 | 0.11–0.14 | 0.13–0.15 | 0.57–0.61 | **0.91–0.97** |
| qa3, 3 facts | 64k | 0.30 | 0.24–0.26 | 0.15–0.16 | 0.64–0.65 | (not implemented) |
| | 128k | 0.37 | 0.17–0.22 | 0.14–0.19 | 0.59–0.65 | (not implemented) |

RAG ranges span the two baseline runs that used different chunkers.

- **Chaining is the gap.** On two-fact questions, retrieval scores at the no-memory level (0.13–0.16). The second fact shares no words with the question, so similarity cannot reach it.
- **The plain ledger's second hop reaches it:** one-hop reads score 0.16, two-hop reads 0.55–0.61.
- **Binding closes most of the rest:** 0.91–0.97 at 128k.
- **qa4** (spatial relations, "what is the hallway east of?") is out of scope. The plain ledger's tagger ignores locations and scores 0.16, below RAG's 0.23–0.29.
- **qa5** (three-argument transfers): the plain ledger scores 0.61–0.73, RAG 0.61–0.68.
- **Filler collisions.** At 128k, the plain ledger without the write gate fell to 0.71–0.80 on qa1, because book filler reuses first names ("Mary Linden…") and those sentences became later records. The learned write gate passes 99–100% of held-out event sentences and 0–0.3% of narrative, which restores 0.92–0.99.

### 4.2 Knowing which fact is current, and when it expired

These are generated documents: a person's location is stated, then idle gaps of 10³–10⁸ ticks pass. Expiry documents attach "valid for N ticks".

| task (n) | plain ledger, latest only | ledger, last 4 records | long context | RAG | RAG timestamps | hand rule |
|---|---|---|---|---|---|---|
| "where is X now" (60) | **0.92–0.93** | 0.70–0.73 | 0.63 | 0.40 | 0.48 | 1.00 |
| expiry accuracy (80) | **0.88–0.95** | 0.88–0.95 | 0.51 | 0.54 | 0.54 | 1.00 |
| stale answers after expiry | **0.00** | 0.00 | 0.72 | 0.79 | 0.79 | 0.00 |
| correct refusals after expiry | **1.00** | 1.00 | 0.28 | 0.21 | 0.21 | 1.00 |

- Handing the reader the last four records instead of the latest one costs 20 points (0.92 to 0.72). The reader cannot reliably find "latest" among dated sentences; the ledger's exact selection does it for the reader.
- Expiry is solved by the integer test, with no stale answer in three seeds.
- The hand rule is perfect here only because these documents use its templates. §4.3 removes that advantage.

### 4.3 Phrasing the memory never saw

E4 uses the same simulator rendered three ways:
- training templates
- PARA ("Soon Mary was in the hallway", "The milk was collected by Bill")
- PARA2, frozen before any training change ("strolled into", "got rid of", "ended up in the hands of")

| arm | chains, training phrasing | chains, PARA | **chains, PARA2** | time, PARA |
|---|---|---|---|---|
| long context | 0.29 | 0.29 | — | 0.60 |
| RAG (best) | 0.19 | 0.21 | — | 0.53 |
| hand rule | n/a | n/a | n/a | **0.00** |
| plain ledger | 0.48–0.53 | 0.42–0.50 | 0.50–0.52 | **0.68–0.72** |
| **bound ledger (E8b)** | **0.96–0.995** | 0.68–0.78 | **0.90–0.92** | — |

Chain documents n = 200, time n = 60.

- **Relation head on single held-out sentences:**
  - PARA2: 160/160 in every seed
  - training templates: 130/130
  - PARA: move 54–55/60, take 32–34/40, drop 40/40
  - narrative with test names classified as "other": 100%
- **All PARA errors come from two templates.**
  - "Soon {n} was in the {r}" describes a state, not a motion, and is called "other".
  - "{n} lifted the {o} off the floor" is called a drop.

  We did not tune to these templates after seeing them; PARA2 exists to keep that honest.
- **The template rule drops from 1.00 to 0.00 on reworded time documents.** The ledger drops from 0.92 to 0.68–0.72. The learned part only has to notice that a sentence is an event about Mary; the exact part does not care how it was worded.

### 4.4 Where the remaining errors come from

For the plain ledger we replayed the 200 E4 chain documents with *perfect* keys, in pure Python with no model and the same read. The gold room is in the reader's context in 93% of questions where the object is still held, and in 77–83% where it was dropped. End-to-end accuracy was 0.43–0.48, so about 35–45 points were lost **after** the memory had found the right sentences. The reader was picking the wrong room among several.

With oracle roles, the bound resolver scores **1.00** on training, PARA and PARA2 documents, with exactly one room in the reader's context. The bound ledger's remaining errors are therefore relation-classification errors in the learned front end. `bound-reader` and `bound-direct` agree to within 0.005 everywhere, so once the memory has resolved the chain, the reader no longer matters.

### 4.5 Length and cost

- **Ingest:** half a forward pass per sentence, linear in document length: 3.8 s per 128k document; 17 s per 512k document (17,000 sentences, 179 records kept).
- **Read:** **0.03 ms** per question at 512k, independent of document length.
- **Reader input:** 1–4 records, where long context needs 32k tokens (2.4 s per question at 128k).
- **512k smoke (n = 4):** ledger 4/4, long context 1/4, RAG 3–4/4.
- **Full run at 512k, 1M and 10M tokens:** pending (§6).

### 4.6 Does a bigger reader make the memory unnecessary? (E7)

E7 hands the same ledger contexts (plain ledger, gated, h2m1, writer seed 17) to the 1.5B reader and to Qwen2.5-7B-Instruct (4-bit). The 7B also gets its own long-context and RAG arms. There are 100 questions per BABILong cell and 200 held-out-phrasing chain documents (`evidence/ledger-e7-full.json`, job-9bb661d65189).

| cell | 7B no memory | 7B long context | 7B RAG dense | 7B RAG timestamps | ledger → 1.5B | ledger → 7B |
|---|---|---|---|---|---|---|
| qa1 16k | 0.14 | 0.86 | **0.96** | 0.82 | 0.89 | 0.89 |
| qa1 128k | 0.14 | 0.50 | **0.95** | 0.77 | 0.92 | 0.92 |
| qa2 16k | 0.11 | 0.50 | 0.11 | 0.15 | 0.59 | **0.69** |
| qa2 128k | 0.11 | 0.28 | 0.12 | 0.12 | 0.57 | **0.66** |
| qa3 16k | 0.30 | 0.32 | 0.14 | 0.13 | **0.65** | 0.63 |
| qa3 128k | 0.30 | 0.39 | 0.11 | 0.09 | **0.59** | 0.58 |
| E4 chains, PARA | 0.16 | 0.39 | 0.195 | 0.21 | **0.46** | 0.455 |

- **Chaining still needs the memory.** A 4.7× larger reader with its own long context scores 0.28 on two-fact chains at 128k; with retrieval, 0.12. The same reader on ledger contexts scores 0.66.
- **A bigger reader barely fixes the plain ledger's choice problem.** On qa2 it gains 0.07–0.10. On qa3 and on held-out phrasing it gains nothing. Model size does not close the reader bottleneck found in §4.4; the bound read does (0.91–0.97, §4.1).
- **For single facts, retrieval plus a stronger reader is strong.** 7B RAG scores 0.95–0.96, above the plain ledger's 0.89–0.92 and on par with the bound ledger's 0.96–0.98 with the 1.5B reader. Where similarity reaches the one relevant sentence, a capable reader can pick the latest from five. The ledger's advantage is chaining, time and validity, not single-fact lookup.

### 4.7 LongMemEval-S with the reader held fixed — OPEN

> **Awaiting job-e39bfd6977e5:** oracle evidence sessions, dense RAG, dense RAG with exact day offsets, and long context (most recent 30k tokens). All use the same 4-bit Qwen2.5-7B reader and prompt, and are graded by the same rubric and graders as the ledger arm below. This section will report each memory's accuracy as a fraction of the oracle's, by question type. That removes the reader's intelligence from the comparison.

**Ledger arm (measured):**
- 500 questions, about 115k tokens of chat history each.
- The ledger here is the *plain lexical* variant: records are user turns and assistant sentences, keyed by 6-character word prefixes. The read takes the best exact key overlap, ties broken by recency, top 12 records, each annotated "N days before the question".
- Answers were graded by five independent LLM graders (Claude Sonnet) against a fixed rubric (`evidence/longmem-grading-rubric.md`).
- The author checked all 30 abstention grades (30/30 agreed, one borderline) and a random 45 of the rest (44/45 agreed).

| type | n | correct | correct + ½ partial |
|---|---|---|---|
| single-session, user facts | 64 | 0.828 | 0.844 |
| abstention | 30 | 0.800 | 0.800 |
| single-session, assistant facts | 56 | 0.732 | 0.759 |
| knowledge update | 72 | 0.681 | 0.708 |
| temporal reasoning | 127 | 0.276 | 0.280 |
| multi-session | 121 | 0.215 | 0.231 |
| single-session preference | 30 | 0.067 | 0.250 |
| **all** | **500** | **0.460** | **0.485** |

- **Strong where one exact record answers the question.** Latest-wins selection handles real knowledge updates.
- **Weak exactly where lexical keys cannot reach the evidence:**
  - preferences: the question says "phone accessories", the history says "iPhone 13 Pro"
  - cross-session counts: every relevant record is needed, and the read keeps the top 12
  - relative time: "what did I buy 10 days ago" is a time-range lookup, which the lexical read does not do although every record carries its date

These results are **not comparable** to published LongMemEval numbers, which use GPT-4o readers and GPT-4o judges.

*[Same-reader comparison table and discussion to be inserted here.]*

---

## 5. What broke, and what this does not show

### 5.1 Errors found and fixed during the work

- **Long-context truncation.**
  - The scorer cut any prompt over 32k tokens from the left as a whole, which removed the instruction and examples.
  - Fixed and re-run: cells never over the cap reproduce exactly; affected cells moved by −0.10 to +0.03 in both directions (`evidence/lc-rerun.json`).
  - All long-context numbers here are the corrected ones. No conclusion changed.
- **LLM judges.**
  - A 7B self-judge mis-graded 5 of 80 smoke verdicts; an independent Qwen3-8B judge made different errors (`evidence/longmem-smoke-rejudge.json`).
  - We therefore dropped automatic judging in the loop and used rubric-driven graders with human spot checks (§4.7).
- **Room vocabulary.**
  - The first bound-ledger run (E8) trained its place tagger on a list that included the bAbI rooms and scored 1.00 on BABILong.
  - With rooms held out (E8b) it scores 0.91–0.98. We report E8b.
- **An earlier "memory adapter" result was withdrawn:** its evaluator passed the gold fact's encoding to the model. The honest re-run of that blended memory lost to retrieval, which motivated this design.

### 5.2 Limits

1. **BABILong and E4 are bAbI worlds.** Their small grammar is known to be solvable by explicit state tracking. What is new here is not solving bAbI:
   - the state is built from a frozen LLM's own features, trained with no test entity
   - it is exact at 128k tokens inside real book text
   - it survives rewording
   - the same mechanism answers "what is current" and "has it expired", which retrieval cannot express
2. **The bound ledger covers one event schema** (move, take, drop, give). qa3 ("where was X before Y") and qa4 (spatial relations) are not implemented in it.
3. **Open conversation is not solved.** LongMemEval shows the lexical ledger's limits (§4.7). §7 lays out the design for it.
4. **One reader family (Qwen2.5), one GPU, three seeds.** Baselines are single runs.
5. **The restricted-label cloze metric** gives every arm the same closed answer set. An open-generation spot check on the earlier baseline run agreed in direction (`evidence/baselines-round1-memadapter-babilong-full.json`, `generative_check`).

---

## 6. Status of pending runs

| run | question | status |
|---|---|---|
| LongMemEval same-reader baselines (§4.7) | how much of the oracle each memory recovers | job-e39bfd6977e5, running |
| E5 (§4.5) | 512k, 1M, 10M tokens | queued |

---

## 7. Next steps: the ledger for open conversation

LongMemEval says the exact back end is sound where it gets the right key. Where it fails, the key is lexical and conversation is not. The plan below keeps the design rule (learn only where language requires it; select exactly; never blend) and moves it from bAbI events to chat.

### 7.1 Write: typed claims, not sentences

Each user turn is split into **claims**. A claim is `(subject, attribute, value, time, source)`: "I just got an iPhone 13 Pro" becomes `(user, phone, iPhone 13 Pro, t, turn-id)`.

- The front end is the frozen reader's own states, as now, plus small heads:
  - a claim detector, playing the write-gate role at clause level
  - a span tagger for subject, attribute and value
  - an **attribute normalizer** that maps the attribute phrase to a canonical slot
- **Slots are open-vocabulary but canonical.** The normalizer embeds the attribute phrase and snaps it to the nearest existing slot above a threshold, or creates a new one. That is an exact, deterministic assignment ("phone", "handset" and "my mobile" become one slot); it is never a weighted mix.
- The record keeps the **original sentence** as its payload, so the reader always sees real words.
- **Training:** synthetic claim-annotated chat, generated with training entities only. LongMemEval, LoCoMo and any test conversation stay held out.

### 7.2 Keys: binding by role, as in the bound ledger

Each claim is filed under `bind(subject, slot)`, and also under `bind(value-entity, slot)` for reverse lookups ("who gave me the scarf").

- **Knowledge updates** become latest-wins on one key: "I moved to Denver" supersedes "I live in Austin" under `user⊗home`.
- **Preferences** are claims in preference slots (`user⊗camera-brand = Sony`). A recommendation question maps to the slots its topic touches. The topic-to-slots step is learned; the read is exact.

### 7.3 Time: an exact index, not text

Every record carries an integer day number (the session date) and, when stated, an event date resolved against it ("last Tuesday" → a day number) by a small date resolver.

The read path gains **range queries**: `t ∈ [now−11, now−9]` for "10 days ago", `t < t(event)` for "before X". Orderings and day differences are computed exactly and handed to the reader as numbers, instead of being left for the reader to infer from dates in text. This targets the 127 temporal questions directly.

### 7.4 Aggregation: exact set reads

"How many X did I …" becomes: collect **every** valid record under the slot or slots, de-duplicate by value, and give the reader the list and the count.

The ledger never truncates a set read to top-k. If the set is large, it hands over the count and a sample rather than a similarity-ranked subset. This targets the 121 multi-session questions.

### 7.5 Question side

The question is parsed by the same front end into:
- **(subject, slot, operator)**, where the operator is one of latest, set/count, range, order, difference, preference
- optional time bounds

The exact read executes it. If no key matches, the memory **abstains** instead of falling back to similarity, which preserves the 0.80 abstention accuracy.

A lexical and dense fallback is kept only as an explicitly labelled secondary arm, so results report how often exact reads answer on their own.

### 7.6 Experiments, in order

1. **Claim extraction quality** on held-out synthetic chat (precision, recall, slot-assignment accuracy), with no reader involved.
2. **LongMemEval-S by type,** same 7B reader, same graders: typed ledger vs lexical ledger vs oracle vs RAG. Success means recovering most of the oracle's accuracy on knowledge update, temporal and multi-session questions.
3. **LoCoMo** as a second, differently built benchmark. It is inspected and available locally (`Percena/locomo-mc10`).
4. **Ablations:**
   - binding keys vs plain slot keys
   - exact range reads vs dates-in-text
   - set reads vs top-k
5. **Reader scaling (1.5B, 7B):** the claim to test is that the gap between readers shrinks as the memory does more of the work, as it did on BABILong (§4.4).

### 7.7 Other open items

- qa3 and qa4 in the bound schema: a "before" read and spatial relations as typed roles.
- A native spectral model whose attention *is* this select-exactly primitive, closing the loop with the SPF-native transformer work.
- PhaseLock relocation with selective recompute.

---

## 8. Reproduce

Code: `spf-wt-phaselock/domains/ml/memory-adapter-babilong/` (branch `feat/phaselock`). All runs used mrun on Beast (RTX 4080, torch 2.13.0+cu130, transformers 5.13.1).

| result | worker | job(s) | evidence file |
|---|---|---|---|
| BABILong round 1, time, expiry | `ledger_worker.py` | job-1206802b5d4f, job-cccbb7b4e2eb, job-5a62931bf4fd | `ledger-memory-full.json` |
| baselines round 1 | memory-adapter worker | job-9a2363a5481c | `baselines-round1-memadapter-babilong-full.json` |
| write gate, E4 (round 2) | `ledger_worker2.py` | job-863b673efa12 | `ledger-r2-full.json` |
| long-context re-run | `ledger_worker6.py` | job-753d8c3aaaf5 | `lc-rerun.json` |
| bound ledger E8 | `ledger_worker5.py` | job-c67300dd95dc | `ledger-e8-full.json` |
| bound ledger E8b (strict) | `ledger_worker7.py` | job-bd69b4ea4137 | `ledger-e8b-full.json` |
| 512k smoke | `ledger_worker4.py` | job-0d254d14e290 | `ledger-e5-smoke.json` |
| LongMemEval ledger arm | `longmem_worker.py --arms ledger --no-judge` | job-3cb51167bf5d | `longmem-ledger.json`, `longmem-ledger-sonnet-grades.json` |
| judge audit | `longmem_rejudge.py` | job-408dcf4bcd68 | `longmem-smoke.json`, `longmem-smoke-rejudge.json` |

Verify evidence: `cd evidence && shasum -a 256 -c SHA256SUMS`.

---

## Appendix A.1 — Answer cues

The restricted-label scorer appends a cue so that the label is the natural next token. Every arm gets the same cue:
- qa1, time, expiry: "The most recent location of X is"
- qa2: "The O is in the"
- qa3: "Before the Y the O was in the"

## Related work (from the author's knowledge; citations to be verified before submission)

- **Benchmarks:**
  - bAbI (Weston et al., 2015) and its long-context version BABILong (Kuratov et al., 2024)
  - LongMemEval (Wu et al., 2024), for chat-assistant memory
- **Neural memories:**
  - Memory Networks (Weston et al., 2014; Sukhbaatar et al., 2015)
  - EntNet (Henaff et al., 2017)
  - Neural Turing Machines (Graves et al., 2014)

  These learn soft reads over slots. The ledger's reads are exact.
- **Binding:** tensor-product representations (Smolensky, 1990) and holographic reduced representations (Plate, 1995) bind roles to fillers by superposition. The binding key here is the non-superposed limit: one address per pair.
- **Retrieval:** retrieval augmentation (Lewis et al., 2020).
- **Agent memory systems:** MemGPT (Packer et al., 2023) and temporal-knowledge-graph memories. These use an LLM to write memory. Here a frozen model's internal states and small heads write it, and time and validity are integer fields read exactly.
