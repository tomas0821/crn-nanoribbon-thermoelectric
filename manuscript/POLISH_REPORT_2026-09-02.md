---
type: polish-report
draft: manuscript/manuscript.tex
output: manuscript/manuscript_polished.tex
date: 2026-09-02
language-variant: US
meaning-check: PASS-with-queries
---

# Polish report — CrN nanoribbon thermoelectric (Physica E)

Language-only pass. The polished text was written to `manuscript_polished.tex` (builds clean:
27 pp, 0 undefined refs/cites, one pre-existing 5.8 pt overfull in the Eq. (1) matrix).
**Addendum, same day:** on the author's instruction the polished text was adopted in place
(`manuscript.tex.bak` holds the pre-polish original) and Queries 1–3 plus the §3.9/§1 items
of the succinctness list were then applied as content edits — see `00_Master_Notebook.md`.

## Verification
- Numbers preserved: ✅ multiset of every numeric token identical (original vs polished)
- Citation keys & labels preserved: ✅ `\cite`/`\ref`/`\label` multiset identical
- Inline math preserved: ✅ every `$...$` span identical; displayed equations, Eq. (1)
  matrix, both `tabular` bodies, every `\includegraphics` and every heading byte-identical
- LaTeX environments balanced: ✅ 25 `\begin` / 25 `\end` (same as original); PDF builds
- Semantic drift check: 52 paragraphs/captions/claims checked by five fresh agents that had
  not seen the edit, instructed to default to "drift" — **2 drifts found, both reverted**
  (see below)
- Word count: body 6878 → 6910 (+0.5 %); abstract 217 → 222 (limit 250, no citations, no
  undefined acronyms). Physica E has no body word limit.
- Style counters: prose em-dashes 70 → 0; `\emph` 28 → 6; "honest" 4 → 0; UK spellings
  13 → 0; trailing present participles 9 → 0; straight double quotes in prose 2 → 0.

**On succinctness.** The brief targeted a 10–20 % cut; the polished text is 0.5 % longer.
Every section agent reported the same reason independently: the paper is number-, caveat-
and condition-dense (three referee rounds added caveats), and the contract forbids
dropping any number, citation, hedge or stated condition. Converting ~70 dashed asides into
clauses costs connectives. What the pass did achieve is sentence-level compactness: shorter
sentences (the 90-word Conclusions claim (iii) is now three sentences), no parenthetical
chains, no rhetorical italics, no voice tics. Real word-count reduction now requires
*content* decisions, which are yours — candidates are listed at the end under
"Succinctness: content-level suggestions".

## Structural changes
- None to headings (all `\section`/`\subsection` identical). Paragraph splits only, within
  a subsection: §3.5 observations (i)/(ii)/(iii) set as separate paragraphs; Conclusions
  split into two paragraphs (opening + claims i–ii | claims iii–iv + closing).
- Not done, proposed as queries: merging the two one-paragraph subsections (§3.2, §3.6) —
  see Queries 1–2.

## Language changes by category
| Category | Count | Examples (before → after) |
|---|---|---|
| Em-dash asides → commas / parentheses / colon / new sentence | 70 | "adjusted by hand---there is no automated objective function for them---to reproduce" → "adjusted by hand (there is no automated objective function for them) to reproduce"; "$T_{\rm AP}\simeq0.6$---an ON/OFF ratio of order ten---half transparency" → "$T_{\rm AP}\simeq0.6$ (an ON/OFF ratio of order ten), half transparency"; "outstanding---the minority channel is gapped over nearly $4$~eV---though" → "outstanding: the minority channel is gapped over nearly $4$~eV. The half-metallicity itself, however," |
| UK → US spelling | 13 | analysed → analyzed (×3); quantised → quantized (×2); two-centre → two-center; second-/third-neighbour → -neighbor; neighbours → neighbors; modelling → modeling; emphasise(d) → emphasize(d) (×2); maximises → maximizes; grey → gray |
| "honest" voice tic removed | 4 | "to an honest $0.04$" → "to $0.04$"; "the honest optima" → "the corrected optima"; "the honest single-number uncertainty" → "the single-number uncertainty"; "These are honest but modest values" → "These values are modest" |
| Trailing participle → clause | 9 | "gate-robust spin filters, confirming in the phase-coherent limit…" → ". This confirms, in the phase-coherent limit, …"; "identical for $N=14$ and $N=20$), confirming it as a genuine edge effect" → "…, which confirms it as a genuine edge effect"; "($W=10$--$32$~\AA), growing with width" → "…, which grows with width" |
| Rhetorical italics removed (words kept) | 22 | `\emph{not sufficient}`, `\emph{required}`, `\emph{global}`, `\emph{ends}`, `\emph{edges}` … ; kept: `\emph{exact}` (×2, the OFF-state contrast), `\emph{continuous}`, `\emph{inside}` (×2, DFT-peak and in-window contrasts), `\emph{$\pi^*$-pinned}` (defined term) |
| Long sentence split | 12 | Conclusions (iii) 90 words → 3 sentences; §2.1 digitization/fit sentence → 2; §3.5 (i) → 3; §3.8 J1/J2 run-on → 3 |
| Redundancy / intensifier cut | 33 | "which is what makes" → "which makes"; "stated openly" → "stated"; "a dedicated π*-pinned variant" → "a π*-pinned variant"; "Going further, …" / "Interestingly, …" / "For context, …" dropped; "sized to contain the wall (see there)" → "sized to contain the wall"; "The limitations are stated transparently." → "The limitations are as follows." |
| Nominalization → verb | 2 | "A parameter-sensitivity analysis … varying every retained parameter … leaves" → "Varying every retained parameter … leaves"; "The consequences … are quantified in Sec." → "Section … quantifies the consequences" |
| Term unified | 3 | "conductance-polarization" → "conductance polarization"; bare "the systematic" → "the systematic misfit" (matches its definition); "the operating window" (2nd use) → "that window" |
| Grammar / typography | 5 | "the larger of [three items]" → "the largest of"; `"exact"` and `"global optimum"` straight quotes → ``…''; "Figs.~\ref{fig:designrules}" (single ref) → "Fig."; comma splice in Fig. 7 caption → semicolon |
| List count corrected | 1 | §3.7 "Two practical remarks, both anchored to…" followed by First / Second / Finally → "Three practical remarks follow, all anchored to…" (the "Finally" item — the λ_int estimate — is also anchored to first-principles numbers; if you meant it as a separate point, revert to "Two … both" and change "Finally" to "Separately") |
| Caption prose tightened | 8 | Fig. 1 row-counting sentence; Fig. 2/5/wall dashes; Fig. 6(d) parenthetical shortened |
| Revision-history artifact removed | 1 | "[now plotted in Fig.~\ref{fig:spin}(b)]" → "[plotted in …]" |

## Reverted by the drift check
- §1 ¶1 — polish had "which enable spin-caloritronic functionality"; original "which open
  the door to spin-caloritronic functionality" restored ("enable" hardens the causal link
  from possibility to capability).
- §3.4 — polish had "…framework~\cite{OuyangGuo2009}, where an order-of-magnitude
  enhancement was achieved…"; original "…framework~\cite{OuyangGuo2009}; there, an
  order-of-magnitude enhancement…" restored (the relative "where" attached the Sevinçli
  result to the Ouyang–Guo framework rather than to graphene nanoribbons).
- §1 ¶2 — "Besides its bulk antiferromagnetic…" restored to "In addition to its bulk…":
  not drift, but the shorter opener produced a 21 pt overfull line; the original wording
  sets cleanly.

## Queries for the author — NOT changed
1. **§3.2 "Ribbon transmission: robust spin filtering" is one paragraph + one figure.** The
   skill's rule is that a one-paragraph section is not a section. Options: fold it into the
   end of §3.1 (it is the ribbon counterpart of the monolayer result) or leave it because it
   carries Fig. 3. Not merged: it would renumber §3.3–§3.9, which the referee reports and
   the Fig. 3 caption's `Sec.~\ref{sec:polar}` depend on. **Your call.**
2. **§3.6 "Spin caloritronics" is one paragraph.** Same rule. It reads naturally as the
   closing paragraph of §3.4 (the S/ZT-vs-polarization trade-off) or the opening of §3.7.
   Moving it is a content move, so it was left. **Your call.**
3. **Abstract, "Sec.~3.5"** — hard-coded section number in an Elsevier abstract (`\ref` is
   not allowed there). Fine if numbering is final; it goes stale silently if §3 is
   renumbered (see Queries 1–2). Consider dropping the pointer.
4. **Fig. 6(d) caption, "Sec.~2.3"** — hard-coded; a `\ref` would need a new label on the
   Landauer-transport subsection (adding a label is outside a language pass).
5. **Terminology: "minimal orbital manifold" (abstract, §1, §3.3 heading) vs "reduced
   manifold" (§2.2, §3.3 body, §3.8).** Both name the same object. They read as
   concept-vs-model variant, which is defensible; if not intended, unify.
6. **Abstract, "the corrected optima are ZT≃0.04–0.15"** — "corrected" replaced "honest".
   It asserts only what the previous clause states (values after restoring the pocket).
   If you prefer no adjective, "the optima are" also reads fine.
7. **§2.1 vs §2.2 uncertainty phrasing** — §2.1 gives "±0.1 eV in the transport window,
   ±0.3 eV near Γ" and "~0.2 eV" single-number; §2.2 says "the stated ~0.1–0.2 eV
   digitization accuracy". Compatible but phrased three ways.
8. **§2.2 "we target the conduction edge (+0.9 eV) … at the stated accuracy"** — the model
   places it at +1.0 eV, i.e. 0.1 eV off; the sentence can be read as hitting +0.9 exactly.
   "…and reproduce it to within the stated accuracy" would be explicit. Sharpens a claim,
   so left alone.
9. **§2.3 "converged to better than 1 %"** — true for 5 → 2.5 meV (0.75 %); the 10 → 5 meV
   step is 2.3 %. A referee could read "converged" as a statement about the whole sequence.
10. **§2.5 optical-branch tuples "(13.7, 13.2, 16.85)" / "(7.2, 10.8, 15.1)"** — not
    monotone; fine if branch-ordered, but a reader expecting ascending order may suspect a
    typo. A parenthetical "(ZO, TO, LO)" would settle it — that is content, so not added.
11. **§3.5 "drop by factors of 1.2–4 (zigzag N=8: 0.062→0.028; armchair N=20:
    0.104→0.027)"** — the two examples are ~2.2× and ~3.9×; the 1.2 end is not illustrated.
12. **§3.5 two "the one optimum" statements** — (i) says armchair N=8 is "the one optimum
    immune to" the CB2 caveat; the next paragraph says it is the one "essentially
    untouched" by the π* systematic. Different caveats; a reader may conflate them.
13. **§3.7 "the classic spin-mistracking physics of domain-wall resistance"** —
    "mechanism" would read more naturally than "physics"; word choice, yours.
14. **§3.8 exchange convention** — LKAG values in "unit-vector convention" are compared
    directly with DMRG "meV/Cr" values ("overestimates J1 by a factor of ~5"). If the DMRG
    spin normalization differs, the factor changes. Not language; a referee might ask.
15. **§3.9 First vs Fig. 7 caption** — prose says peak heights "not converged beyond a
    factor of ~2"; caption says "semi-quantitative" with no factor. Consistent in spirit.
16. **Conclusions (iv)** — the original dash chain let "a concrete caution…" attach either
    to the whole finding or to "invisible to parameter-sensitivity analysis"; the polished
    version attaches it to the latter. If the wider referent was intended: "The artifact is
    moreover invisible to parameter-sensitivity analysis, a concrete caution…".
17. **§2.1 "a short list of explicit targets" → "explicit targets"** — the list is
    enumerated in the same sentence; flagged by the drift checker as the only deleted
    characterizing phrase. Restore if you want the "short" emphasis.

## Succinctness: content-level suggestions (author's call; nothing done)
These are where 10–20 % would actually come from. Each is a content decision.
- **§3.9 Scope and limitations (≈420 words)** restates caveats already made in place
  (digitization ±0.1–0.3 eV in §2.1; CB2 unresolved in §2.1 and §3.5(i); π* misfit in §3.1;
  κ_ph bracket in §2.5). Items First–Third could become one-line pointers to those
  sections, keeping Fourth–Finally (uniform exchange, T_C, dephasing, rigid band) in full.
  Potential saving ≈150 words.
- **§3.4 last four sentences (≈95 words)** on why disorder-enhancement is not computed
  duplicate the Third caveat of §3.9 almost verbatim; keep one.
- **§3.7 "Experiment supports the picture…" paragraph opener** and the two literature
  sentences (Coey, Mathur) could compress to one sentence with both citations.
- **§1 ¶2 (≈150 words)** lists five prior-work items in one paragraph; the Xiang2023 1D
  item and the thin-film thermoelectric sentence could go to a single clause each.
- **Merging §3.2 into §3.1 and §3.6 into §3.4** (Queries 1–2) saves no words but removes
  two headings and makes §3 read as seven results instead of nine.

## Process notes
- Five section agents (A: abstract+intro; B: methods; C: results 3.1–3.6; D: results
  3.7–3.9; E: conclusions) each returned polished text plus a change log; the change logs
  are archived in this session's scratchpad. Five independent drift-check agents then
  compared original and polished text paragraph by paragraph.
- Mechanical verification (numbers, keys, math, environments, headings, graphics,
  tabulars) was run before and after the two drift reverts and the seven manual fixes.
