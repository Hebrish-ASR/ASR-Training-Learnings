---
title: Brands that are also ordinary words (Parakeet, Fritter) lose their capital
date: 2026-11-18
models: [nvidia/parakeet-tdt-0.6b-v2]
lines: [Sabich, Fritter]
topic: tokenizer
status: observed in use; cause inferred
---

## What we saw

"Parakeet" is often written lowercase in dictation, although in this project it almost always means the AI model,
not the bird. The same risk applies to model and product names such as Fritter, Blender, Fedora, Rhino and Svelte.

## Why (inferred)

The model has heard the ordinary word, lowercase mid-sentence, far more often than the brand. Unlike Deepgram, the
pieces are not the problem (`▁P ar ake et` either way, apart from the first letter); the prior for the common word is.

## What changed in our training

A one-word capitalised term whose lowercase form is an ordinary English word gets a `homonym` difficulty point, so it
needs more takes (Parakeet 20 -> 25, Fritter 15 -> 19). Multi-word title-case phrases made of ordinary words
("Feedback Panel") do not: their case is genuinely ambiguous. See
[Case is decided on the first piece](2026-11-18-case-is-decided-on-the-first-piece.md).
