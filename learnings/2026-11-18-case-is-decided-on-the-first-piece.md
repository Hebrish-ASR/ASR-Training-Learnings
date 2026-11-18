---
title: Case is decided on the first piece, so Deepgram comes out as "deepgram"
date: 2026-11-18
models: [nvidia/parakeet-tdt-0.6b-v2]
lines: [Sabich, Jachnun, Fritter, Falafel]
topic: tokenizer
status: segmentation measured; cause inferred
---

## What we saw

The fine-tuned Sabich wrote "deepgram" and once "Degram" for the brand Deepgram, even when it was said slowly and
clearly. Every training transcript wrote it as `Deepgram`, so the labels were not the problem.

## Why (as far as we can tell)

Parakeet TDT 0.6B v2 has a 1,024-piece SentencePiece vocabulary. It has no `Deep` piece, so the two spellings start
differently:

| Word | Cased pieces | Lowercase pieces |
|---|---|---|
| Deepgram | `▁D e ep gr am` (5) | `▁de ep gr am` (4) |
| DeepSeek | `▁D e ep S e e k` (7) | `▁de ep se e k` (5) |
| GitHub | `▁G it H ub` (4) | `▁g ith ub` (3) |
| Docker | `▁D ock er` | `▁do ck er` |

The capital has to be chosen on the very first piece, as a bare `▁D`, against `▁de`, one of the commonest word starts
in English (delete, deploy, decide). The decoder's general English habits favour the lowercase path, and a handful of
examples does not outweigh them. "Degram" is the same path with the `ep` piece dropped.

How few examples: the word had 21 recorded takes, but only 11 were in the training split (see
[Test takes don't teach](2026-11-18-test-takes-do-not-teach.md)).

## What changed in our training

Take targets now scale with how hard a word is for this tokenizer, not only with how important it is. A term earns a
difficulty point for each of: a bare-capital first piece where the lowercase form starts with a longer piece (`case`),
a capital inside the word (`camel`), five or more pieces or three or more single letters (`frag`), and being a brand
that is also an ordinary word (`homonym`, [Parakeet](2026-11-18-brands-that-are-common-words.md)). Ordinary English words score nothing.
Target = importance target x (1 + 0.25 x points): Deepgram went from 20 takes to 30.
