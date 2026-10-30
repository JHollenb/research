# Early PAN-ISA instruction execution

[Read the study](paper.md).

PAN-ISA's early result was a working, bounded execution system: neural selectors chose supplied transition semantics, architectural state remained inspectable, and subsequent instructions consumed the resulting state. Small direct-effect experiments began moving the learning boundary toward values and write masks. The work did not establish complete learned x86 execution or a speed advantage over QEMU.

The study explains the actual networks, a worked low-byte addition, stages 0–5, typed commit, SPF, PAN Fabric, measured size, and the uninterrupted 8,192-instruction comparison. It distinguishes the June 2026 reports from later runtime code inspected on October 30, 2026.

Jump to the [network mathematics](paper.md#network-architectures-and-mathematics), [worked addition](paper.md#a-worked-addition), [stage capabilities](paper.md#how-the-stages-grew), or [size and performance](paper.md#size-and-performance).

- [Evidence and source provenance](sources/README.md)
- [Verbatim snapshot manifest and SHA-256 hashes](sources/manifest.json)
- [Companion: the newer learned-ISA study](../learned-isa/README.md)

This is a source audit and research writeup. No new training or performance experiment was run.
