# ASR Training Learnings

A public notebook of the non-obvious things learned while fine-tuning speech recognition models for
[Hebrish](https://hebrish.app): English dictation with romanized Hebrew, tech vocabulary and voice commands, mostly on
[`nvidia/parakeet-tdt-0.6b-v2`](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v2).

Each entry is **specific to the model it names and dated** the day it was found. It records what was seen, why (marked
as measured or inferred), and **what it changed in the training strategy**: data rules, take targets, which ideas were
dropped. A finding about one tokenizer may not hold for another; check the `models` field before applying it.

Also published at <https://hebrish.app/learnings>.

## Learnings

<!-- index:begin -->
| Date | Learning | Models | Topic | Status |
|---|---|---|---|---|
| 2026-11-18 | [Test takes don't teach, so count only training takes toward a word's target](learnings/2026-11-18-test-takes-do-not-teach.md) | nvidia/parakeet-tdt-0.6b-v2 | data | counts measured; split mechanism inferred |
| 2026-11-18 | [Case is decided on the first piece, so Deepgram comes out as "deepgram"](learnings/2026-11-18-case-is-decided-on-the-first-piece.md) | nvidia/parakeet-tdt-0.6b-v2 | tokenizer | segmentation measured; cause inferred |
| 2026-11-18 | [Brands that are also ordinary words (Parakeet, Fritter) lose their capital](learnings/2026-11-18-brands-that-are-common-words.md) | nvidia/parakeet-tdt-0.6b-v2 | tokenizer | observed in use; cause inferred |
| 2026-11-17 | [Adding symbols to v2's tokenizer by surgery broke the model](learnings/2026-11-17-tokenizer-surgery-broke-the-model.md) | nvidia/parakeet-tdt-0.6b-v2 | tokenizer | confirmed (outcome); cause not investigated |
| 2026-11-13 | [Parakeet v3's bigger tokenizer has the same missing symbols as v2](learnings/2026-11-13-parakeet-v3-tokenizer-same-gaps.md) | nvidia/parakeet-tdt-0.6b-v2, nvidia/parakeet-tdt-0.6b-v3 | tokenizer | confirmed |
| 2026-10-25 | [A character the tokenizer lacks becomes <unk>, and the model learns to write it](learnings/2026-10-25-missing-characters-become-unk.md) | nvidia/parakeet-tdt-0.6b-v2, nvidia/nemotron-speech-streaming-en-0.6b | tokenizer | confirmed |
<!-- index:end -->

## Format

`learnings/YYYY-MM-DD-<slug>.md`, with front matter:

```yaml
---
title: One line, the finding itself
date: 2026-11-18
models: [nvidia/parakeet-tdt-0.6b-v2]        # base models it was measured on
lines: [Sabich, Fritter]                       # fine-tune lines it affects
topic: tokenizer | data | training | decoding | export
status: confirmed | measured; cause inferred | observed in use | inferred
---
```

Then three sections: what was seen (or the question), why (or the finding), and `## What changed in the training`.
`python3 scripts/build_index.py` rebuilds the table above and `learnings.json` (read by the hebrish.app page). A newer
finding on the same question is a new dated entry; old entries are not rewritten.

Model lines: **Sabich** (everything, the app default), **Jachnun** (code-switching only), **Fritter** (no Hebrew; its
own project), **Shakshuka** (streaming), **Falafel** (voice commands). Details: <https://hebrish.app/models>.

## Licence

Text CC-BY-4.0. Written by Claude (Anthropic) from Daniel Rosehill's training notes.
