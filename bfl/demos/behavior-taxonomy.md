---
title: "Behavior Taxonomy: Counting, Typography, Lexical Gates, and Semantic Substitution"
type: experiment-report
status: native-consumer-behavioral-taxonomy
rank_in_bfl_survey: 12
model: "FLUX.2 family behavior panels"
tags: [bfl, flux, behavior, counting, typography, semantics, lexical-gating, causal-sites]
---

# Behavior Taxonomy: Counting, Typography, Lexical Gates, and Semantic Substitution

> [!summary]
> A behavior taxonomy separates several kinds of FLUX.2 capability that are often collapsed into one “understanding” score. Exact count behavior degrades sharply as requested count rises from 2 to 7, with rates 1.000, 0.875, 0.875, 0.4375, 0.1875, and 0.0625. Typography has a robust spelling-transition signal, with plain/specific admission 0.9375/0.906 and 39/48 confirmation-family passes. Lexical presence is strongly gated: “open” appears at roughly 0.94–1.0 while “exit” appears at roughly 0.00–0.06. Semantic substitutions are asymmetric: open↔closed reaches 0.8125 while push↔pull reaches 0.125. An early joint.4 counting-circuit story is demoted by strict wording 5/16 and paraphrase 0/16, despite a live-site rescue rate of 0.609.

## Research question

Image-generation behavior is multidimensional. A model can respond to word presence while failing exact numeracy, can render a spelling transition without supporting arbitrary typography, and can respond to a semantic substitution asymmetrically. This experiment builds a taxonomy with separate tests for counting, typography, lexical gating, semantic substitution, and a candidate causal site.

The scientific objective is to prevent one positive gallery or one scalar metric from standing in for a capability claim. Each family has a defined input panel, an observable endpoint, and a separate interpretation. Wilson intervals are retained for the finite panels where they are available, and discovery results are kept distinct from confirmation-family results.

## Counting behavior

The count assay requests exact counts from 2 through 7 and evaluates the rendered number of target objects against the request. The exact rates are 1.000 for 2, 0.875 for 3, 0.875 for 4, 0.4375 for 5, 0.1875 for 6, and 0.0625 for 7. The monotone degradation after four is a clear dose-of-count trend, but it should not be read as a hard capacity boundary: the assay uses a finite prompt and rendering panel, and object detection itself has a measurement boundary.

The count result is valuable because it distinguishes “the prompt contains a number” from exact cardinality control. A model can preserve the scene while producing an incorrect count, and a global image similarity score can miss that failure. The taxonomy therefore treats count correctness as its own behavioral axis.

## Typography behavior

The typography panel contains 256 minimal pairs designed to separate plain spelling changes from more specific letter-level or layout demands. The robust plain/specific admission rates are 0.9375 and 0.906. The confirmation family has 39/48 passing cases. These rates support a real spelling-transition substrate under the declared panel, while leaving room for failures in long text, unusual fonts, dense layouts, and multi-line composition.

Typography admission is scored from rendered evidence rather than prompt-token identity. A successful spelling transition requires the visible glyph sequence or the declared letter-level property to change in the intended direction. This guards against a prompt-sensitive but visually incorrect output being counted as success.

## Lexical gates and semantic substitutions

Lexical presence is strongly word-specific. The word “open” appears at approximately 0.94–1.0 under the tested prompts, while “exit” appears at approximately 0.00–0.06. That asymmetry means a word can be lexically gated into the image without implying that the model has a general concept-level substitution mechanism.

The semantic substitution panel makes that distinction explicit. Replacing open with closed reaches 0.8125 transition success, while replacing push with pull reaches only 0.125. The pair direction and semantic family matter. A single positive substitution cannot establish a general semantic operator.

## Candidate causal site and demotion

An early hypothesis proposed that a `joint.4` call 2 site was a counting circuit. The strict wording panel passes only 5/16 and the paraphrase panel passes 0/16. A wrong-site rescue rate of 0.609 shows that the site is live under some intervention, but it is not necessary or sufficient for the claimed counting computation. The correct taxonomy label is “causally live site with a demoted bottleneck interpretation,” not “counting circuit.”

This distinction is important for research. A site can carry a perturbable signal, participate in a route, or amplify an endpoint without owning the behavior. The negative wording result should not erase the live-site trend; it narrows what the instrument can support.

[Behavior taxonomy source evidence](../artifacts/behavior-taxonomy/2026-07-31-212627-what-we-know-about-the-black-forest-models-a-data-driven-report.md)

## Controls and limitations

Minimal pairs control irrelevant prompt changes. Wilson intervals preserve uncertainty in finite samples. Confirmation-family separation controls discovery-to-certification leakage. Lexical gates distinguish word presence from semantic substitution. The wrong-site rescue and strict/paraphrase split control overinterpretation of a candidate causal site.

The taxonomy remains panel-bounded. Count detection can fail because of occlusion, typography scoring can be sensitive to OCR and layout, and semantic substitution rates depend on prompt construction. The numbers establish directional behavior families, not a complete capability profile or a claim of human-like symbolic reasoning.

## Claim status

**Observation:** FLUX.2 behavior separates into count degradation, robust but bounded typography transitions, word-specific lexical gates, and asymmetric semantic substitutions.

**Convergent trend:** independent behavior families and the causal-site demotion agree that prompt responsiveness is not one homogeneous capability.

**Working inference:** several downstream image behaviors are gated by different circuits or consumer stages, with lexical presence easier to elicit than exact count or arbitrary semantic transformation.

**Terminal status:** bounded behavioral taxonomy. The report does not claim general counting competence, general typography competence, or a definitive semantic-circuit localization.

## Local proof bundle

The bundle contains the count certificates, typography certificate and discovery/confirmation records, the status notes, and the source narrative:

- [count runtime certificate](../artifacts/behavior-taxonomy/count-runtime-certificate-v3.json)
- [typography certificate](../artifacts/behavior-taxonomy/flux2-typography-behavior-certificate-v1.json)
- [confirmation report](../artifacts/behavior-taxonomy/confirmation-report-job-5bc3ca2850ed.json)
- [bundle verifier](../artifacts/behavior-taxonomy/verify.py)

Run `python ../artifacts/behavior-taxonomy/verify.py` from this directory to verify the count curve, typography rates, lexical gates, semantic asymmetry, and demoted causal-site result.
