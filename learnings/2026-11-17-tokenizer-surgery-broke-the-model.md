---
title: Adding symbols to v2's tokenizer by surgery broke the model
date: 2026-11-17
models: [nvidia/parakeet-tdt-0.6b-v2]
lines: [Sabich]
topic: tokenizer
status: confirmed (outcome); cause not investigated
---

## What we tried

Eight symbol pieces (`@ & + # ( ) _ =`) were appended to the v2 vocabulary after the existing 1,024, with the blank
token moved after them and the new output rows trained in one rolling fine-tune, so the model could write email
addresses and code symbols directly.

## What happened

The resulting release (Sabich v4.8) produced "no speech" or invented sentences in real dictation. Its export metadata
was consistent, so the fault is in the weights or the decoding, not the packaging. It was withdrawn the same evening
and the previous release restored.

## What changed in our training

Tokenizer surgery is not to be retried on these lines. Symbols stay out of the v2 targets: rows carry the spoken form
("at", "underscore", "plus") and a separate full-form target for bases whose tokenizer already has the symbol; a
formatting step after decoding writes the symbol. See
[Parakeet v3 has the same gaps](2026-11-13-parakeet-v3-tokenizer-same-gaps.md).
