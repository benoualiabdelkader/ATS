---
name: career-application-agent
description: Operate and extend the Career-Application-Agent engine. Triggers on keywords: "job description", "JD", "apply for role", "process JD", "tailor CV", "generate package", "job posting", "ATS score", "opportunities/", "career agent", "new opportunity", "tailor my resume", "analyze job". Operates the Python pipeline (memory, jd_parser, matcher, researcher, generator, ats_evaluator, pdf_exporter) to produce a zero-hallucination, ATS-optimized application package.
---

# Career-Application-Agent Operator

This skill governs how to work inside the `ATS/` workspace — a real Python
engine, not a manual LaTeX-filling workflow. The engine already implements
memory ingestion, JD parsing, semantic matching, company research, document
generation, ATS scoring, and PDF export. **Your job is to orchestrate and
maintain this engine, not to reimplement its logic by hand.**

## Before doing anything: read the actual code, don't assume its interface

The architecture doc describes the *shape* of the system, but exact function
signatures, CLI flags, and config keys live in the code itself. Every session,
before running or editing anything:

1. `view engine/cli.py` — find the real Typer commands and their exact flags.
   Never invent a CLI flag that isn't there; if unsure, run `python -m engine.cli --help`
   (or however the entrypoint is actually invoked per `pyproject.toml`).
2. `view engine/config.py` — confirm what env vars / API keys / model settings
   the engine expects before running anything that calls an LLM.
3. `view engine/pipeline.py` — confirm the actual stage order and function
   names before claiming a stage ran or debugging a failure in it.

Treat the Architecture doc as a map, and the code as ground truth. If they
disagree, the code wins — and flag the discrepancy to the user.

---

## Mode A — Run the pipeline for an opportunity (the common case)

Trigger: user gives a new job posting, or asks to (re)generate a package for
an opportunity already sitting in `opportunities/<Company_Role>/`.

1. **File the opportunity** if not already present: create
   `opportunities/<Company_Role>/job_description.txt` with the full posting text.
2. **Check `myself/` is current.** If the user mentions new experience,
   projects, or skills that aren't reflected in `myself/*.txt` or
   `myself/projects/`, update those files first — the whole system's
   zero-hallucination guarantee depends on `myself/` being complete and
   accurate before generation runs.
3. **Run the pipeline** via the real CLI/entrypoint found in Step 0 above,
   targeting the specific opportunity folder. Prefer running the full
   pipeline (`memory → jd_parser → matcher → researcher → generator →
   ats_evaluator → pdf_exporter`) end to end unless the user asks for a
   single stage (e.g. "just re-run the matcher" or "just regenerate the cover letter").
4. **Check the ATS score.** Read `generated_metadata.json` /
   `05_analysis_and_research/` output for the `ats_evaluator` score. If it's
   below a strong threshold (treat <80% as needing another pass), inspect
   `gap_analysis.md` and `ats_keywords.txt`, and either:
   - flag missing-but-real skills the user should confirm and add to `myself/`, or
   - re-run `generator` with better keyword coverage if the gap is phrasing, not substance.
   Never manufacture a missing skill to close the gap.
5. **Report back**: final ATS score, which documents were generated
   (list from `01_cv` through `07_portfolio_and_mapping`), and anything
   flagged as a genuine skill/experience gap the user should know about
   before applying.
6. **Learn from this run.** Before finishing, feed this opportunity's
   results into the system's cross-opportunity memory per the
   "Continuous Learning Loop" section below — this step is not optional,
   it's what makes the next opportunity's output better than this one's.

## Mode B — Develop/fix/extend the engine itself

Trigger: user asks to add a document type, fix a bug, change scoring logic,
tune a prompt, or otherwise touches `engine/*.py`, `prompts/*.txt`, or
`templates/*`.

1. Read the specific module(s) involved fully before editing — these files
   are interdependent (e.g. `generator.py` likely consumes `matcher.py`'s
   output shape and `models.py`'s schemas); check `models.py` for the
   Pydantic schemas each stage passes to the next before changing any of them.
2. Prefer editing `prompts/*.txt` over changing Python logic when the issue
   is output *quality* (hallucination, tone, missed keywords) rather than a
   *code* bug — the prompts are the tuning surface for LLM-stage behavior.
3. After any change, re-run only the affected stage(s) against a real
   opportunity folder to verify, rather than assuming the fix works.
4. If a pipeline run fails, read the actual traceback, locate the failing
   stage/function in `pipeline.py`, and fix minimally — don't rewrite
   surrounding stages that weren't implicated.

---

## Continuous Learning Loop — the system must improve with every opportunity

The engine shouldn't treat each opportunity as an isolated run. Every
`job_description.txt` processed is a data point about the job market the
user is targeting, and every `ats_evaluator` score is feedback on what
worked. Capture both, every time, so opportunity #10 is measurably better
than opportunity #1.

**Step 0 — check what already exists before building anything new.**
Look for an existing insights/memory mechanism first (e.g. inside
`memory.py`, a `learning.py`/`insights.py` module, or a persisted file the
architecture doc doesn't mention yet). If the engine already has a place
for this, use it and extend it rather than creating a parallel system.

**If nothing exists yet, maintain a lightweight persistent file:**
`ATS/myself/market_insights.md` (source-of-truth-adjacent, not
`opportunities/`-scoped, since insights should compound across all
opportunities). After every pipeline run, append/update:

- **Recurring required skills/keywords** seen across job descriptions that
  aren't yet in `myself/skills.txt` — these are real signals the user's
  profile may be under-representing something, not hallucinated additions.
  Surface these to the user as suggestions; never add them to `myself/`
  without confirmation, since that file must stay ground-truth.
- **Keyword phrasing that correlates with higher `ats_evaluator` scores**
  (e.g. "CI/CD pipelines" scored better than "automated deployment" for the
  same underlying skill) — feed this back into `prompts/cv_generator_prompt.txt`
  or `prompts/jd_parser_prompt.txt` as refined guidance, so future
  generations use the higher-scoring phrasing by default when it's honestly
  applicable.
- **Recurring gaps** (`gap_analysis.md` patterns across multiple
  opportunities in the same role family) — if the same missing
  qualification shows up across many postings for similar roles, that's
  worth flagging to the user as a real skill-development priority, not
  just a one-off gap.
- **Template/structure performance** — if certain sections or bullet
  patterns consistently produce low ATS scores regardless of content,
  that's a signal the template itself (`cv_template.tex` /
  `perfect_ats_cv_template.md`) may need a structural fix — flag it rather
  than silently patching per-opportunity.
- **Outcomes, if the user reports them** (interview received, rejected,
  no response) — if the user shares what happened with a past application,
  log it against that opportunity's keyword/matching profile. Over enough
  data points this is the strongest signal available for what's actually
  working, stronger than the ATS score alone.

**Every run, before generating documents for a new opportunity:** check
`market_insights.md` for relevant prior learnings (same role family,
overlapping keywords) and apply them — e.g. prefer previously-validated
phrasing, proactively ask the user about a recurring gap before generating
rather than after.

This loop must stay within the zero-hallucination rule: learning changes
*how existing real information is phrased and prioritized*, never *what
is claimed to be true*. Never let accumulated "insights" become a backdoor
for inflating the candidate's profile over time.

---

## Non-negotiable rules (apply in both modes)

- **Zero hallucination**: `myself/` is the only source of truth for the
  candidate's real skills, experience, projects, and achievements. Every
  document the engine produces must be traceable back to something in
  `myself/`. If `matcher.py`'s gap analysis shows a requirement the
  candidate doesn't meet, that gap gets surfaced to the user — never
  papered over by inventing a skill or number.
- **ATS structural rules still apply** to whatever `cv_template.tex` /
  `perfect_ats_cv_template.md` in `templates/` currently encodes: single
  column, no `\hfill`-based right-aligned dates (verified via `pdftotext`
  raw-order extraction to cause parser scrambling), standard section names,
  plain bullets, no icons/rating graphics, ATS-safe embeddable font. If
  `pdf_exporter.py` or the templates drift from these, flag it — don't
  silently "fix" the template's design intent without checking with the user,
  since it may have been deliberately tuned already.
- **Don't skip the `ats_evaluator` gate.** A document isn't "done" until it's
  been scored, not just generated — generation and evaluation are separate
  stages for a reason.
- **Secrets**: never print, log, or commit API keys found in `config.py` /
  `.env`. If a key is missing and a stage needs it, tell the user which
  env var is missing rather than working around it.
- **One opportunity folder per run.** Don't cross-contaminate content between
  `opportunities/<A>/` and `opportunities/<B>/` — each package must be
  independently tailored and traceable to its own `job_description.txt`.
- **Learning is additive, not inflationary.** `market_insights.md` (or
  whatever mechanism replaces it) may change phrasing and prioritization
  based on accumulated evidence, but it may never introduce a claim about
  the candidate that isn't already grounded in `myself/`. If in doubt,
  surface the insight as a question to the user rather than applying it silently.
