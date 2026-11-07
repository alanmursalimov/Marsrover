# Marsrover – Claude context

Class Mars rover build at Kantonsschule Kreuzlingen (KSK), Switzerland. Owner: Alan
(GitHub: alanmursalimov). 3D-printed parts come from Alan's Voron printer.
This repo holds the rover code that runs on the school Raspberry Pi (hostname `kskpi1`).

## How to work with Alan
- Reply in the language he writes in (English or German). Code comments/user guides in this repo are German.
- Honest, critical feedback without softening.
- Code: targeted minimal fixes, not structural rewrites.
- Say clearly what is a **calculation**, an **estimate**, or something he should **measure** himself.
- Ask before assuming dimensions or parts he hasn't confirmed.
- He'll say when he wants hints instead of direct answers; otherwise just answer.
- Math/physics formulas: properly typeset (LaTeX), never plain text like `x^2`.

## Keep these files up to date (every session)
At the end of every session in which anything about the rover changed (design decision,
measurement, new part, test result, code change, question resolved or added):
1. Update the matching file in `docs/claude/` (and this file if the rules change).
2. Move resolved items out of `open-questions.md`; put dropped ideas in `history.md` with the reason.
3. Newer info replaces older info – don't keep two conflicting values as "current".
4. Only record what Alan said, decided or measured, or what is in the code. Mark
   estimates as estimates. Don't add guesses as facts.
5. Commit with a short message (e.g. `docs: update rover context`) – only if Alan agrees to commit/push.
Note: the repo is **public**, so nothing private goes in these files.

## Context files (auto-loaded)
@docs/claude/design.md
@docs/claude/electronics-power.md
@docs/claude/software-pi.md
@docs/claude/open-questions.md
@docs/claude/history.md
