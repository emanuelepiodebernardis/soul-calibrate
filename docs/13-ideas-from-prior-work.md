# 13 — Ideas reused from the author's prior work

Author: Emanuele De Bernardis · Module: Prior work · Feeds: [[04-rolling-baseline]], [[06-personal-model]], [[08-evaluation-soul-bench]], [[17-roadmap-and-governance]]

These ideas come from the author's own research and engineering projects on intrusion detection, drift and
on-device inference. They transfer to SOUL because the underlying problems are the same: small devices,
shifting data, few labels, and claims that must be checkable.

| Idea | Where it comes from | Use in SOUL-Calibrate |
| --- | --- | --- |
| **Conformal test martingale as a label-free drift trigger**, implemented in integer arithmetic | KAN-IDS drift-adaptation study ([kan-ids-v2](https://github.com/emanuelepiodebernardis/kan-ids-v2)) | Flags when a user's signals stop looking like their baseline (new phone, new job, illness) → light re-enrollment or extra questions. In that study a simple conformal threshold trigger had inverted sensitivity and the martingale fixed it. → [[04-rolling-baseline]] |
| **Diagnose "threshold vs representation" before adapting** (compare the oracle threshold with ROC-AUC) | same study | Per user: if the ranking is right, recalibrate cheaply; if not, collect answers for a personal head. → [[06-personal-model]] |
| **Label-free alignment can make things worse** (prior, median and quantile re-alignment all degraded the model under real drift) | same study | Do not rely on unsupervised adaptation alone; a few answers are worth more. This is the argument for questions. → [[05-active-questions]] |
| **Claim–evidence map** with provenance classes and SHA-256 of each evidence file | [kan-ids-v2](https://github.com/emanuelepiodebernardis/kan-ids-v2) `docs/CLAIM_EVIDENCE_MAP.csv` | SOUL-Bench claims ledger: every number in a report points to its evidence file and says whether it was measured, regenerated or only planned. → [[17-roadmap-and-governance]] |
| **Train/serve feature parity by construction**, with a parity test | [sentineledge-core](https://github.com/emanuelepiodebernardis/sentineledge-core) | The same feature code (e.g. openSMILE eGeMAPS) runs on the phone and in training; a parity test proves it. → [[03-session-anchor]] |
| **Integer-only inference on microcontrollers** with exact additive explanations (KAN with look-up tables, a few KB of RAM) | [IDS-KAN](https://github.com/emanuelepiodebernardis/IDS-KAN), [kan-ids-v2](https://github.com/emanuelepiodebernardis/kan-ids-v2) | A personal head on the bracelet that can say exactly which signal moved the reading: "your voice was flatter than your usual; your heart rate was higher". → [[06-personal-model]] |
| **INT8 matrix multiplications with high-precision norms and a few outlier channels** | [efficient-on-device-ai](https://github.com/emanuelepiodebernardis/efficient-on-device-ai) | A recipe to quantise speech encoders for on-device use without collapse. → [[06-personal-model]] |
| **Deterministic verdict; the language model only explains** | [Assist_CLI-V2](https://github.com/emanuelepiodebernardis/Assist_CLI-V2) | The reading (which states, speak/ask/quiet) comes from calibrated statistics; the language model only phrases it and never decides it. → [[14-reading-audit]] |
| **Evidence before "done"**: a step closes only when its check has produced a saved result | the author's engineering practice | Each stage of the roadmap closes on a saved, hashed evidence file. → [[17-roadmap-and-governance]] |

## Check

Each row names its source repository, and each use links to the module where it applies.
