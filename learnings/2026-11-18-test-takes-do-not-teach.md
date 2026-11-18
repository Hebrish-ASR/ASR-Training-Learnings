---
title: Test takes don't teach, so count only training takes toward a word's target
date: 2026-11-18
models: [nvidia/parakeet-tdt-0.6b-v2]
lines: [Sabich, Jachnun, Fritter, Falafel]
topic: data
status: counts measured; split mechanism inferred
---

## What we saw

Of 21 takes of "Deepgram", 10 were in the test split, which is never trained on. The recording app counted all 21
toward the word's target of 20, so it stopped serving the word as done while the model had seen it only 11 times.

## Why

The sentence bank's split is term-disjoint: a term picked for evaluation sends every sentence containing it to test.
Two things moved takes into test that should have trained:

- A take keeps the split its sentence had when it was recorded. Words later exempted from the hold-out (we exempt
  words the model is known to get wrong) kept their earlier test takes.
- Compound terms held out for evaluation ("Deepgram Nova", "Deepgram Aura") take the shorter word with them.

Across all tracked terms, 15,910 takes of target words sat in test on 2026-11-18.

## What changed in our training

Each word's target is now its training target plus its current test takes, so the app keeps serving it until the
training split alone has enough. The audit is rerun before every training run, because new test takes keep arriving.
Measured shortfall after the change: about 60,000 training takes across 13,000 terms, against 42,000 under the old
count.
