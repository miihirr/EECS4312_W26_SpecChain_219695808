# Reflection — SpecChain Project
**Author:** Mihirkumar Patel
**Student ID:** 219695808
**Application:** Headspace (com.getsomeheadspace.android)

---

## 1. Most important difference between the three pipelines

The clearest difference is in **specificity and grounding**.

The **manual pipeline** produced requirements that were tightly anchored to the
language of actual reviews. Because a human read each review individually before
coding it, every requirement could be traced to a concrete pain point that appeared
in multiple distinct reviews — for example, "background audio stops playing the
moment I switch to another app on Android 14" became the explicit, measurable FR9.
The resulting acceptance criteria were precise: they named specific time bounds,
observable state changes, and failure conditions.

The **automated pipeline** produced requirements that were broader and more
generic. The LLM inferred plausible themes from clusters of review text, but
without human grounding it sometimes merged distinct sub-problems into a single
high-level requirement. For instance, the Bluetooth, notification timing, and
landscape-tablet issues — each reported discretely by different Headspace users —
were partially collapsed into a general "Android reliability" statement. This
tendency is reflected in the lower requirement count (12 vs. 14) for the automated
pipeline.

The **hybrid pipeline** preserved the speed advantage of automation while
correcting the most significant gaps. Human review of the auto-generated groups and
personas allowed vague requirements to be split or sharpened, and the ambiguity
ratio matched the manual pipeline at 0.071 — significantly better than naive
automation would achieve without oversight.

---

## 2. Most useful pipeline

The **hybrid pipeline** was the most useful overall.

It matched the manual pipeline on requirement count (14) and test count (28),
while producing a testability rate and traceability ratio of 1.00 — the same
perfect scores as the manual pipeline. This demonstrates the core trade-off: pure
manual work is thorough but slow; pure automation is fast but imprecise; the hybrid
approach achieves near-manual quality at a fraction of the manual effort.

For a production requirements engineering workflow, the hybrid pipeline would be
the recommended choice. The automated stage handles the time-consuming first pass
of clustering 200 reviews and generating skeleton personas, and the human review
stage ensures requirements are grounded, specific, and testable. In the Headspace
context, this meant human reviewers could catch that the "nightly sleep audio"
cluster actually contained two distinct sub-groups — users bothered by timer
inaccuracy and users bothered by background audio termination — and split them
into separate, testable requirements.

---

## 3. Most surprising finding

The most surprising finding was how **grammatically correct but untestable** the
auto-generated requirements were. On the surface they read as well-formed software
requirements ("The system shall maintain reliable Bluetooth audio during sessions").
However, closer inspection revealed that they lacked measurable acceptance criteria
— no threshold, no time constraint, no observable state change. This is reflected
in the zero ambiguity ratio for the automated pipeline disguising a deeper problem:
the requirements avoided vague adjectives simply by being abstract rather than
specific.

This suggests that LLMs are very capable of pattern-matching the surface form of
requirements while missing their semantic substance. A requirement-quality checker
that verifies every requirement contains a measurable condition, a time bound, or
a verifiable observable outcome should be a standard post-processing step in any
automated RE pipeline.

---

## 4. Observed weakness in the automated pipeline

The automated pipeline's **personas contained unsupported assumptions** that were
not traceable to the review data. For example, one generated persona for the
Headspace employer-sponsored category described usage patterns and contexts that
went beyond what the review text directly supported. In the manual pipeline, every
persona attribute was grounded in quoted review evidence.

This matters for requirements quality because a persona that is partly invented
introduces requirements that satisfy an imagined user rather than a real one,
weakening the connection between market evidence and product specification. In the
Headspace project, this risk was most visible in the multilingual content persona:
the automated pipeline inferred the persona's specific language preferences from
limited evidence, while the manual pipeline carefully qualified which attributes
were directly evidenced versus inferred.

The hybrid step addressed this by reviewing each auto-generated persona against
the review evidence and revising attributes that lacked textual grounding. This
produced a more defensible persona set that directly traced each attributed goal
or pain point back to specific review IDs — an audit trail the purely automated
pipeline did not produce.
