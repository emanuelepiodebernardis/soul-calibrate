# 09 — Privacy and regulation

Author: Emanuele De Bernardis · Module: Privacy and regulation · Constrains: [[01-architecture]], [[02-enrollment]], [[03-session-anchor]]

This page is an engineering summary, not legal advice.

## Design principles

- Features computed on the device, raw audio deleted immediately (Koch et al., 2026 protocol).
- Baseline and personal head stay on the phone.
- The shared model improves only with explicit consent, kept separate from "never used for training" users. → [[15-labels-and-consent]]
- Future option: federated learning with differential privacy, as in Google's Gboard (more than 30 on-device
  language models in production with formal privacy guarantees and user controls). → [[11-analogous-systems]]

## EU rules

- **AI Act, Article 5(1)(f):** since 2 February 2025, inferring emotions from biometric data in the workplace
  and in education is prohibited (except for medical or safety reasons) → no "corporate wellbeing" version without legal review.
- **Outside work and education:** emotion recognition is a high-risk use under Annex III (Future of Privacy
  Forum reading); with the Digital Omnibus those obligations apply from **2 December 2027**.
- **GDPR:** voice is personal data; inferring emotions or health brings a strict regime (Spanish DPA, AEPD, April 2026 guidance).
- **Face via camera:** biometric data, the most sensitive part → optional, kept only if it proves useful. → [[07-fusion]]

## Why calibration helps compliance

- Per-person records of when and how often the model is wrong (conformal coverage) are the kind of evidence a
  high-risk risk assessment asks for.
- The user remains "the best source" (from Nightlet's disclaimer): transparency and control.
- The decision is deterministic and auditable; the language model only phrases it. → [[13-ideas-from-prior-work]]

## The line not to cross

Stay in wellbeing: no diagnosis. Kintsugi (voice → depression screening) closed its commercial operations in
2026 after years of waiting for FDA clearance and released its models publicly.
