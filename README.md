# Rho research

Two documents and the evidence behind them. Compiled 2026-09-11.

## The deliverables

| File | What it is | Length |
| --- | --- | --- |
| [RHO_PRODUCT_DOSSIER.md](RHO_PRODUCT_DOSSIER.md) | End to end product understanding: what Rho is, how it works, how it makes money, who it is for, and how it compares to its 2026 competitors. Written for someone with no background in business banking. Start with "The short version". | ~57,000 words |
| [RHO_API_REFERENCE.md](RHO_API_REFERENCE.md) | Practical developer reference for the Rho API: all 14 endpoints, the sandbox in depth, MCP, and 40+ places where Rho's published docs diverge from live behavior. | ~80,000 words |

Read the dossier if you are evaluating Rho. Read the API reference if you are building on it. The dossier's
section 6 is a summary of the API reference.

## The evidence

Everything in `research/` supports a claim in one of the two documents.

| Path | Contents |
| --- | --- |
| `research/VERIFIED_CLAIMS.md` | The 16 load-bearing claims that were handed to independent fact-checkers instructed to refute them, with each corrected statement and its caveats. This is the authority wherever anything else disagrees. |
| `research/QA_AUDIT.md` | The 100 defects six auditors found in the first draft of the two documents, with the prescribed fix for each. 94 were applied, 18 prescriptions were rejected on the evidence. |
| `research/findings/` | 29 research files, about 306,000 words, one per research topic. |
| `research/corpus/rho-co-pages/` | The 556 rho.co pages this was built from, as text, captured 2026-09-11. |
| `research/corpus/docs-rho-co/` and `api-reference/` | Rho's official developer documentation as of 2026-09-11. |
| `research/sandbox/` | Live API captures, the full sandbox dataset, the probe scripts, and `probe-evidence.tar.gz` (about 2,500 raw responses). |
| `research/tools/` | The crawler, the URL lists, the sitemap, and the per-section sources both documents were assembled from. |

## Rebuilding

Both documents are assembled from per-section files. Edit the sections in
`research/tools/dossier-sections/` or `research/tools/apiref-sections/`, or the headers beside them, then run:

```bash
python3 research/tools/build_docs.py
```

That regenerates both top-level documents including their tables of contents.

## How much to trust this

Two passes. An extraction pass over the corpus, then an adversarial pass where independent checkers tried to
refute the most important claims. Fifteen of sixteen came back needing correction, so the hedged wording in
the documents is deliberate. After drafting, six auditors attacked the finished text for consistency errors,
bad numbers, unfair framing, undefined jargon, misquotes and gaps.

Known limits, stated in both documents: no Rho account was opened, no sales conversation happened, and the
production API was never called with a real token, so every measured API statement is sandbox behavior.
Section 10 of the dossier lists every question this research could not settle.
