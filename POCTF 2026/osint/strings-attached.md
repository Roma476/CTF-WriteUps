# Strings Attached

| | |
|---|---|
| **Section** | wave 3 |
| **Category** | osint |
| **Solves** | 292 |

## Overview

The subject is named: Michael Romaniello, illustrator and fine artist, also a comedian and YouTuber. The question is a single date — the year *I Dreamt I was a Child II* was completed.

The wording is the challenge. Completion is not publication: the year a work appears on social media is only the latest possible date it could have been finished, never the exact one. Social media alone can only bound the answer, so the job is to bound it from both sides.

## Solve

Searching the title leads to Romaniello's own Instagram: a post showing the finished painting, dated **16 May 2016**. That is the obvious answer, and it is the trap. A post is the day the photo went up, not the day the brush stopped; submitting 2016 is rejected, which confirms the question really is about completion and sends you looking for a tighter bound.

The title carries a numeral. *II* means there is a first, and scrolling the same account back finds *I Dreamt I was a Child*, published on **20 December 2014**. That is the other end of the interval: the sequel cannot belong to a period earlier than the series it continues.

The completion therefore sits between the two posts:

```
lower bound  20 December 2014   the first painting is published
upper bound  16 May 2016        the second painting is posted
```

The only year that falls entirely inside that window is 2015.

The general shape of these questions is worth remembering: for "when was this made", a social post is an upper bound, and a predecessor in a numbered series is a lower bound. Two bounds plus a one-year gap is usually the whole answer, and the work's own catalogue entry — the artist's site or an exhibition listing, where works appear as title, year, medium — is the source that would pin it directly.

The answer is **2015**.