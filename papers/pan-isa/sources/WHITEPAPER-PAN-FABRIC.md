# PAN Fabric: A Neural Control Plane For A Living Compute Fabric

Status: draft white paper  
Date: 2026-06-19

## Abstract

PAN Fabric is a proposal and implementation path for turning heterogeneous
compute into a living, measured, self-improving fabric. The target platform in
the current implementation is KRIA KV260, where the ARM processing system (PS)
and FPGA programmable logic (PL) can both execute portions of a program. The
larger goal is not to wrap accelerators with a dispatcher. The goal is for PAN
to own graph formation, value residency, placement, measurement, artifact
lifecycle, and eventually neural scheduling policy.

In the final system, a neural policy learns how to control PS and PL together.
It decides where computation should run now, which values should stay resident,
when materialization is worth the cost, and what hardware should be compiled for
future runs. `.xclbin` files and FPGA cores still exist physically, but they
become internal PAN cache artifacts. The user-facing abstraction becomes stable:
run the program, let PAN decide how the fabric should shape itself.

## Motivation

Modern heterogeneous systems expose enormous control surface area:

- CPU cores are flexible and low-latency.
- FPGA fabric can be reshaped for application-specific dataflow.
- DMA buffers and device-resident memory can avoid copies, but only when the
  runtime preserves residency correctly.
- Reconfiguration and dispatch costs can dominate small kernels.
- A kernel that is faster in isolation may be slower once transfers, app
  switching, and host synchronization are included.

This makes manual accelerator selection brittle. A static wrapper around
accelerators answers the wrong question: "Which kernel should I call?" PAN
Fabric asks a more powerful question: "Given this graph, these values, these
measurements, and this hardware state, what should the compute fabric become?"

The motivating observation from the KV260 work is simple: a PL primitive can
lose to the ARM PS when PS-side buffer synchronization and dispatch dominate.
The answer is not to abandon PL. The answer is to make residency, fusion,
measurement, and reconfiguration first-class control-plane decisions.

## Thesis

PAN Fabric should become the authority over:

- graph regions
- runtime values
- value residency
- placement decisions
- materialization
- validation
- hardware artifact selection
- bitstream lifecycle
- measurement ingestion
- neural scheduling policy

The fabric is "living" when it continuously observes execution, records what
worked, routes values to the best current execution location, and compiles
better hardware for future runs.

## Current Baseline

The current PAN Fabric implementation already has the first useful substrate:

- `FabricGraph` for typed graph regions.
- `FabricValue` and `FabricValueStore` for runtime-visible values.
- `fabric-session` execution with a long-lived daemon session.
- `pan-fabricd` graph calls and daemon-resident BO handles.
- KV260 SPF base ops through `spf32_core_pl`, including `spf32.mul`,
  `spf32.add`, `spf32.div`, `spf32.abs2`, and `spf32.fft64`.
- Foundry candidates, manifests, measurements, scheduler hints, and artifact
  cache contracts.
- A control ledger for placement decisions, health events, and quarantines.
- Fail-closed routing for known-bad or unsupported graph/core paths.

This is enough to stop treating the FPGA as a manually selected peripheral and
start treating it as a managed execution substrate.

## Architecture

PAN Fabric is organized as five cooperating planes.

### 1. Graph Plane

Program regions are lowered into typed graphs:

```text
program region -> FabricGraph -> graph ops -> typed inputs -> typed outputs
```

Graph regions may come from:

- x86 SIMD transition regions
- SPF operation chains
- repeated scalar kernels
- future neural/operator regions
- fused multi-op runtime regions

The graph is the scheduling unit. Individual kernels are implementation
details.

### 2. Value Plane

Values, not kernels, are the central runtime objects.

A fabric value tracks:

- value id
- name
- dtype
- element count or shape
- residency
- materialization state
- PS array, daemon handle, XRT BO, dma-buf descriptor, or catalog core metadata
- producer graph
- validation state
- refcount and lifetime

The scheduler should first ask where the values already live. A computation that
looks profitable in isolation can be wrong if it forces unnecessary host
materialization.

### 3. Execution Plane

Execution can occur through several routes:

- PS execution for flexible, low-overhead, or unsupported regions.
- Daemon-resident execution for graph packets whose values can stay in the
  fabric session.
- Existing catalog cores that have already been measured and promoted.
- Future fused cores produced by the foundry.

The PS remains the authority for validation, syscalls, faults, and architectural
commit. PL and daemon paths propose typed graph outputs or state deltas; PAN
validates before treating them as committed program state.

### 4. Foundry Plane

The foundry owns bitstream lifecycle:

```text
mine graph regions
generate candidates
estimate resources and payoff
queue external Vitis builds
ingest artifacts
measure on board
promote or quarantine
feed scheduler
```

The foundry does not need Vitis in the runtime process. It emits build-worker
contracts and treats `.xclbin` files as cache artifacts associated with graph
signatures, target boards, toolchain versions, and kernel strategies.

### 5. Policy Plane

The current policy is rule-based and evidence-gated. The intended endpoint is a
neural scheduler trained from real decisions and measurements.

Policy actions include:

- `run_ps_now`
- `run_daemon_resident_now`
- `run_catalog_core_now`
- `keep_resident`
- `materialize`
- `compile_better_for_next_time`
- `reject_fail_closed`

Policy inputs include:

- graph ops and size
- current value residency
- active app/core state
- daemon capabilities
- catalog artifacts
- measurement history
- transfer history
- validation risk
- quarantine state
- reconfiguration cost

## Execution Flow

The target runtime loop is:

```text
observe program region
lower to FabricGraph
bind FabricValue inputs
query scheduler
execute through selected route
preserve resident outputs when possible
materialize only for validation, output, debug, or recovery
validate result
commit typed output or architectural delta
record decision, timing, transfer, health, and value residency
queue better hardware if useful
```

In the final user-facing form:

```bash
python3 -m pan_isa_x86_runtime_spf run --program app --fabric auto
```

should be enough. PAN decides where each graph region lives now and what fabric
artifact should exist next time.

## Why This Is Not An Accelerator Wrapper

An accelerator wrapper exposes a fixed function and asks the application to
manage when it is useful.

PAN Fabric instead treats accelerators as temporary realizations of graph
regions. The stable object is the typed graph plus its values. The hardware
realization can change:

- PS today
- daemon-resident PL graph tomorrow
- measured catalog core next week
- fused foundry bitstream after enough repeated evidence
- neural-policy-controlled placement once it beats the rule scheduler

The accelerator is not the interface. The fabric control plane is the
interface.

## Neural Control Of PS/PL

The end goal is a neural controller that learns the combined PS/PL execution
space.

The controller should predict:

- placement action
- output residency
- whether materialization is needed
- compile priority
- risk/confidence
- expected latency, transfer volume, and energy

It should learn from the control ledger:

- graph signature
- value residency before and after
- active app/core
- selected action
- actual timing
- transfer buckets
- validation outcome
- health/quarantine result
- whether a compiled artifact later outperformed the old path

The neural controller should not be trusted by default. It earns authority by
beating the rule scheduler on held-out KV260 traces without validation failures.
Low-confidence or unsafe decisions fall back to rules.

## FPGA Dynamism And Bitstream Generation

The FPGA matters because its cores are dynamic. PAN Fabric should not merely
select among prebuilt kernels. It should decide what hardware should exist.

The foundry loop is the bridge:

```text
repeated graph region -> candidate fused core -> resource estimate
-> build queue -> external Vitis worker -> artifact catalog
-> on-board measurement -> promotion -> scheduler use
```

This gives PAN a learning loop over both execution and hardware generation.
When the scheduler sees that an existing app cannot preserve residency across
regions, it can queue a fused bitstream. When a measured fused artifact wins, it
becomes the preferred path. When it fails, it is quarantined.

## Validation Strategy

PAN Fabric must be validated as a control plane, not just as a benchmark.

Required validation layers:

- Correctness: outputs match PS or QEMU/SPF oracles when materialized.
- Fail-closed behavior: unsupported graph shapes, bad handles, malformed
  packets, bad status, and known-bad artifacts do not silently fall back.
- Residency: resident graph chains preserve device-resident values and report
  zero timed transfer bytes when no materialization occurs.
- Transfer accounting: setup, timed graph execution, and forced materialization
  are tracked separately.
- Scheduler evidence: every graph receives a decision record.
- Health and quarantine: failures produce structured records and block unsafe
  reuse.
- Artifact lifecycle: built artifacts are hidden until measured; promoted
  artifacts are discoverable; failed artifacts are quarantined.
- Neural gating: neural overrides are enabled only after held-out measurement
  wins and no validation regressions.

KV260 validation should include:

- PS baseline
- one-shot daemon execution
- long-lived daemon session
- fabric-session with resident values
- materialized validation run
- scheduler plus foundry catalog run
- promoted catalog-core run when available
- board restore to `k26-starter-kits`

## Expected Payoff

PAN Fabric becomes useful when it reduces:

- host materialization
- unnecessary transfers
- manual xclbin selection
- one-shot dispatch overhead
- repeated poor placement decisions
- stale accelerator assumptions

The larger payoff is qualitative: the runtime starts improving itself. It
records what happened, learns what should happen, and compiles what should
exist.

## Roadmap

1. Make normal `run --fabric auto` use the same value/session substrate as
   `fabric-exec`.
2. Move more hot-path state into `pan-fabricd`.
3. Implement true XRT BO handoff where the platform supports it.
4. Complete foundry promotion/quarantine automation.
5. Train the first neural scheduler head from real control-ledger decisions.
6. Gate neural scheduling by held-out latency, transfer, energy, and validation
   results.
7. Expand from SPF base ops to broader x86-derived graph regions.

## Conclusion

PAN Fabric is a path from accelerator dispatch to neural fabric control. The
system begins conservatively: PS-authoritative validation, explicit graph
values, measured scheduling, and fail-closed hardware use. The endpoint is more
ambitious: a neural policy that controls PS and PL as one adaptive compute
fabric, preserving correctness while learning where computation should run and
what hardware should exist next.
