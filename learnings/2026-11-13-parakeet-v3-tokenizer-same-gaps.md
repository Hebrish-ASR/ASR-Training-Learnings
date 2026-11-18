---
title: Parakeet v3's bigger tokenizer has the same missing symbols as v2
date: 2026-11-13
models: [nvidia/parakeet-tdt-0.6b-v2, nvidia/parakeet-tdt-0.6b-v3]
lines: [Sabich, Fritter]
topic: tokenizer
status: confirmed
---

## Question

v3 is multilingual with an 8,192-piece vocabulary. Would moving to it let the model write `+` (for `+972`), `*` or
brackets?

## Finding

No. Measured on both tokenizers (each `tokenizer.model` read out of the `.nemo` by HTTP range requests; a character
counts as writable if `a<c>b` encodes without `<unk>` and decodes back unchanged):

| | Parakeet TDT 0.6B v2 | Parakeet TDT 0.6B v3 |
|---|---|---|
| Pieces | 1,024 | 8,192 |
| Writable of 699 candidates | 205 | 327 |
| ASCII symbols | `` !$%',-./:?^`` | `` !$%',-./:?`` (loses `^`) |

The extra pieces are European letters, not symbols.

## What changed in the training

Nothing: v2 stays the base for the dictation lines (chosen over v3 earlier from real-use results). Symbols are
handled by spoken-form targets plus formatting after decoding (see
[Missing characters become <unk>](2026-10-25-missing-characters-become-unk.md)).
