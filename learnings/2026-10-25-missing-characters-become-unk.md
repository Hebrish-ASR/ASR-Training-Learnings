---
title: A character the tokenizer lacks becomes <unk>, and the model learns to write it
date: 2026-10-25
models: [nvidia/parakeet-tdt-0.6b-v2, nvidia/nemotron-speech-streaming-en-0.6b]
lines: [Sabich, Jachnun, Fritter, Shakshuka, Falafel]
topic: tokenizer
status: confirmed
---

## What was seen

An early Sabich wrote `<unk>` at clause breaks in real dictation. The training data held 22 semicolons.

## Why

A character missing from the model's vocabulary tokenizes to `<unk>`, and fine-tuning teaches the model to emit it.
Parakeet v2 cannot write `; " “ ” ’ — – ( ) & + @ _` or some accented capitals; the Nemotron streaming base cannot
write any accented letter. Measured on the tokenizers themselves: of 699 candidate characters, v2 can write 205.

## What changed in the training

Every training transcript uses only ASCII letters, digits, spaces, `. , ? ! ' : - / % $`, `£` and `€`. Anything else
is mapped before training: `;` and dashes to a comma, `&` to "and", `+` to "plus", curly apostrophes to `'`, quotes
and brackets dropped, accents folded. 211 already-published rows were rewritten to match. Where the real form matters
(email addresses, filenames with `_`), a row keeps a spoken-form target for v2 ("dana underscore levi at tidewell.io")
and the real form separately for bases that can write it, and a formatting step after decoding turns one into the
other.
