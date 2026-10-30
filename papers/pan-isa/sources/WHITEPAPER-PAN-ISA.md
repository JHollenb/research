# PAN ISA: A Learned Transition Architecture For Universal Efficient Execution

Status: draft white paper  
Date: 2026-06-19

## Abstract

PAN ISA is a research path toward an instruction execution system where neural
models learn typed architectural transition semantics and use those semantics to
run programs efficiently across a heterogeneous compute fabric. The current
implementation focuses on x86 as a demanding source ISA: many encodings, many
operand forms, complex flags, memory effects, SIMD/x87 behavior, exceptions,
and system boundaries.

The end goal is stronger than decode classification and stronger than wrapping
an emulator. PAN ISA should learn executable transition effects, validate them
against independent oracles, commit them through a typed fail-closed runtime,
and expose graph regions to PAN Fabric so a neural controller can decide how
best to run them on PS, PL, catalog cores, or newly compiled FPGA fabric.

The long-term thesis is that an ISA can be represented as a learned, typed,
validated transition manifold rather than as a hand-coded interpreter. The
runtime should then efficiently run anything by combining learned semantics,
exact validation gates, and a fabric policy that maps computation to the best
available execution substrate.

## Motivation

General-purpose ISAs are enormous contracts. x86 in particular includes:

- dense variable-length encodings
- mode-dependent operand behavior
- flags with defined, undefined, and advisory state
- partial register aliases
- memory events and exceptions
- SIMD, x87, scalar, system, and privileged forms
- vendor and CPUID variation

Traditional execution handles this with hand-written decoders,
microarchitectural machinery, emulators, or JIT translators. PAN ISA explores a
different direction: can a neural system learn the typed transition relation of
an ISA, then use that learned relation to execute and optimize programs?

The answer must be conservative. A model that predicts labels has not learned
an ISA. A model that selects a handwritten semantic candidate has not fully
learned an ISA. A model that only matches final state for one-instruction
programs has not learned an ISA. The target is exact typed transition behavior
under held-out byte streams, held-out operand structures, independent emulator
oracles, negative controls, and free-run execution.

## Thesis

PAN ISA should represent instruction execution as:

```text
(instruction_bytes, architectural_state_t, profile)
  -> typed_transition_effects
  -> architectural_state_t+1
```

The transition effects include:

- register write masks and values
- flag write masks, values, and definedness
- memory read/write events
- RIP/RSP/control-flow updates
- exception class and priority
- preserved-state certificates
- profile and provenance metadata

The runtime commits only validated typed proposals. Unsupported or low-confidence
behavior fails closed. QEMU, Bochs, Unicorn, and other oracles are used for
training and validation, not as hidden runtime fallbacks.

## Current Baseline

The current PAN-ISA repository already contains several layers of evidence:

- Staged x86 learned/structured runners in `pan_x86_stages/`.
- Static ELF loading, sparse memory, GDB support, oracle tooling, and full-ISA
  classification support in `pan_x86_isa/`.
- An SPF-primary runtime in `pan_isa_x86_runtime_spf/` that commits typed
  transition proposals into architectural state.
- Stage 0-4 scoped learned selector/effect modes for low-byte ALU,
  memory/addressing, control/stack, complex scalar, SIMD, and x87 slices.
- Runtime proposal validation for profile, confidence, RIP, register masks,
  flag masks, memory writes, stage/effect metadata, and provenance.
- A learned runtime model loader with fail-closed `--model --learned-only`
  behavior.
- Stage 4 runtime heads for MOVDQA/MOVDQU, PXOR/PADDQ, aligned MOVDQA fault
  behavior, and x87 FNOP/FLD1/FLDZ/FSTP ST(i).
- PAN Fabric hooks that can turn eligible runtime regions into graph work and
  route them through PS, daemon, PL simulation, XRT, or catalog/foundry paths.

This baseline is not full x86. It is a staged, evidence-producing path toward a
learned executable ISA.

## Architectural Model

PAN ISA separates execution into five contracts.

### 1. Decode And Profile Contract

Every instruction is interpreted relative to a profile:

- mode
- ring
- CPUID feature set
- operand size
- address size
- vendor policy
- memory and syscall environment

Decode is not enough, but it is required. The runtime must know which iform,
operands, prefixes, widths, and profile assumptions are in scope before a
transition head can safely run.

### 2. Typed State Contract

Architectural state is represented as typed channels:

- GPRs and partial-register aliases
- RIP and RSP
- RFLAGS values and definedness
- sparse memory windows and events
- XMM/SIMD lanes
- x87 stack state
- exception outcome channel

The state contract makes preservation checkable. Untouched state must remain
untouched, not merely absent from the loss function.

### 3. Transition Proposal Contract

A learned or deterministic head emits a transition proposal:

```text
decoded instruction
selected before-state
model/profile metadata
write masks
value outputs
memory events
exception outcome
next RIP/RSP
confidence/provenance
```

The proposal is not state mutation. It is a typed claim that the runtime
validates before commit.

### 4. Commit Contract

The runtime validates:

- compatible profile and iform
- confidence threshold
- next RIP correctness
- legal register and flag write masks
- flag definedness
- valid memory events and write windows
- preserved-state constraints
- exception/fault outcome
- model and source provenance

Only then does it mutate architectural state.

### 5. Fabric Contract

Some transition regions can also be graph regions. PAN ISA should emit graph
work to PAN Fabric when that is the best execution strategy.

The ISA runtime remains PS-authoritative for architectural commit. The fabric
executes graph regions and returns typed outputs or deltas. This keeps
heterogeneous execution compatible with exact ISA semantics.

## Learning Strategy

PAN ISA should not jump directly to a monolithic black-box model. It should
learn one executable axis at a time.

The staged strategy is:

1. Learn compact selectors over well-defined transition families.
2. Replace selector axes with learned effect heads.
3. Learn typed register/flag values and masks.
4. Learn memory events and preservation.
5. Learn control-flow targets and stack effects.
6. Learn exception class and priority.
7. Learn SIMD/XMM lane updates.
8. Compose promoted iform/profile rows into free-running programs.
9. Integrate graph-region emission so the fabric can optimize execution.

This produces a sequence of scoped claims rather than one broad claim that
"x86 is learned."

## Runtime Shape

The runtime loop is:

```text
fetch bytes
decode under profile
select relevant typed state
ask learned head for transition proposal
validate proposal
commit exact state
emit trace and training record
optionally emit fabric graph region
```

For unsupported behavior:

```text
unsupported form -> explicit stop or policy-controlled PS fallback
```

For promoted learned behavior:

```text
learned proposal -> validation -> commit
```

For accelerable regions:

```text
transition region -> FabricGraph -> FabricValue inputs -> fabric scheduler
-> typed output/delta -> runtime validation -> architectural commit
```

## Integration With PAN Fabric

PAN ISA learns what an instruction or region means. PAN Fabric learns where and
how to run it.

The combined system should work like this:

1. PAN ISA observes executable instruction streams.
2. It forms typed transition proposals and graph regions.
3. PAN Fabric tracks values and residency.
4. A scheduler chooses PS, daemon, catalog core, or future generated PL fabric.
5. The result is validated against the architectural contract.
6. Measurements train the fabric policy.
7. Transition traces train the ISA policy.

The neural end state has two cooperating learned systems:

- a learned ISA transition model that knows semantics
- a learned fabric controller that knows placement, residency, and compilation

Together they should efficiently run anything that is in the promoted ISA and
fabric coverage ledger.

## "Run Anything" Without Overclaiming

The phrase "run anything" must be earned through coverage.

PAN ISA can claim broad execution only when:

- the iform/profile coverage ledger has closure
- unsupported rows are explicit
- each promoted row has exact teacher-forced and free-run validation
- independent oracles agree or divergences are retained
- memory, flags, exceptions, and preserved state are exact
- negative controls degrade
- runtime execution does not call hidden oracles
- fabric acceleration preserves architectural correctness

Until then, claims should be scoped:

```text
PAN has learned this iform/profile/operand scope under these validation gates.
```

The system becomes universal by increasing the promoted ledger, not by making a
blanket claim.

## Efficient Execution

Efficiency comes from more than faster kernels.

PAN ISA contributes:

- typed semantics
- graph-region identification
- exact touched-state information
- preservation masks
- exception boundaries
- profile-scoped behavior

PAN Fabric contributes:

- placement decisions
- value residency
- transfer avoidance
- daemon-resident execution
- catalog core selection
- fused bitstream generation
- neural scheduling policy

The combination lets PAN choose between:

- PS scalar execution for flexible low-overhead regions
- PL execution for repeated or data-parallel regions
- resident daemon graph execution when values can stay on device
- catalog cores when measured faster
- generated fused cores when existing paths materialize too much

The goal is not "always use PL." The goal is "always choose the best verified
execution path."

## Validation Strategy

PAN ISA validation is row/profile scoped.

Required gates:

- source and profile freeze
- trace integrity
- split hygiene
- teacher-forced exactness
- free-run exactness
- oracle parity
- negative controls
- runtime isolation
- operator probes
- promotion records

Promotion records must include:

- iform and iclass
- profile and CPUID feature set
- operand scope
- artifact root
- model artifact hash
- source hashes
- split manifest
- exactness metrics
- oracle reports
- negative-control results
- unsupported cases
- retained divergences
- reviewer decision

Fabric-integrated validation also requires:

- PAN/QEMU or PAN/SPF output match
- no hidden oracle fallback
- typed output/delta validation before commit
- route trace and control-ledger evidence
- materialization and transfer accounting
- fail-closed behavior for unsupported graph regions

## Neural ISA Model Requirements

A useful neural ISA model should provide:

- calibrated confidence
- typed outputs, not unstructured blobs
- explicit masks for touched state
- preserved-state certificates
- exception outcomes
- profile compatibility metadata
- source and model hashes
- fallback refusal when out of scope

The model should be trainable from traces but executable without calling the
trace generator or oracle at runtime.

## Research Risks

PAN ISA must address several hard problems:

- undefined flags and later flag consumption
- partial-register aliasing
- memory aliasing and overlapping writes
- exception priority
- vendor divergence
- broad SIMD and floating-point corner cases
- system calls, signals, threads, and privileged behavior
- hidden leakage from semantic candidates or trace fixtures
- neural confidence calibration
- fabric acceleration that preserves exact architectural semantics

These risks are manageable only if the project stays evidence-led and
fail-closed.

## Roadmap

1. Finish typed effect-head schemas shared by stages and runtime.
2. Promote small learned effect scopes with exact oracle validation.
3. Replace selector heads with direct typed value heads one family at a time.
4. Expand Stage 4 SIMD/x87 and then broader AVX/YMM/ZMM only after profile and
   oracle paths are ready.
5. Integrate `run --fabric auto` so learned transition regions can become
   fabric graph regions.
6. Train the first neural fabric controller from placement and residency
   records.
7. Let the foundry compile better hardware for repeated learned graph regions.
8. Grow the promoted iform/profile ledger until broad user-mode execution is
   covered.

## Conclusion

PAN ISA is the semantic half of the larger PAN vision. It learns what programs
mean as typed architectural transitions. PAN Fabric learns where those
transitions and graph regions should run. The combined endpoint is a neural
system that can execute programs correctly while controlling PS and PL in the
best measured way possible.

The practical path is conservative: staged coverage, exact validation,
fail-closed runtime commits, measured scheduling, and gated neural authority.
The ambition is large: an ISA that can efficiently run anything by learning
semantics, preserving correctness, and shaping the compute fabric around the
program.
