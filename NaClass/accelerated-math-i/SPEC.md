# SPEC — Accelerated Math I Tutoring Project

**Agent: when you read this spec, your job is to scaffold the project described below in the current working directory and seed it with the content provided in §6. After scaffold is done, you operate per the workflows in §7.**

---

## 1. Purpose

A local project folder that helps a teacher prepare and run a year-long 1-on-1 tutoring track for his niece, covering **Accelerated Mathematics I** (US 6th-grade math + first half of 7th-grade math), aligned to Khan Academy. The project is the source of truth for sessions, homework, and progress.

## 2. Background

- **Student:** niece, living in **Connecticut, USA**, in/entering the district's "Accelerated Mathematics I" course (district-named; standard meaning = year 1 of a compacted middle-school sequence ending at Algebra 1 in grade 8).
- **Teacher:** her uncle. Native Vietnamese speaker, fluent enough in English to teach. Not a professional math teacher — needs ready-to-use, plain-language plans.
- **Platform:** Khan Academy (free).
  - 6th grade: `https://www.khanacademy.org/math/cc-sixth-grade-math`
  - 7th grade: `https://www.khanacademy.org/math/cc-seventh-grade-math`
- **Cadence:** ~30 min/day, 5 study days + 1 review day + 1 rest day per week. ~32 weeks total.
- **Language of delivery:** English for the niece. Teacher's private notes may include Vietnamese; the glossary is bilingual.

## 3. Scope of this kickoff

In scope:
1. Create the folder structure in §4.
2. Write the file templates in §5.
3. Drop seed content from §6 into `curriculum/roadmap.md`, `sessions/week-01/session-01-ratios.md`, `homework/week-01/hw-01-ratios.md`, `resources/khan-academy-map.md`, `resources/glossary.md`.
4. Create the project's own `README.md` and `AGENTS.md` (templates in §5).
5. Create empty placeholder folders for `sessions/week-02/` through `sessions/week-32/` (and matching `homework/`).

Out of scope:
- Building an app or website.
- Pre-generating all 32 weeks of session/homework files. Do them **just-in-time, one week ahead.**
- Khan Academy API integration.

## 4. Folder structure to create

```
accelerated-math-i/
├── README.md
├── AGENTS.md
├── SPEC.md                        # this file (copy in)
├── curriculum/
│   └── roadmap.md
├── sessions/
│   ├── _template.md
│   ├── week-01/
│   │   └── session-01-ratios.md
│   ├── week-02/ ... week-32/      # empty placeholders
├── homework/
│   ├── _template.md
│   ├── week-01/
│   │   └── hw-01-ratios.md
│   └── week-02/ ... week-32/      # empty placeholders
├── progress/
│   ├── tracker.md
│   └── notes.md
└── resources/
    ├── khan-academy-map.md
    └── glossary.md
```

## 5. File templates

### 5.1 `README.md`

```markdown
# Accelerated Math I — Tutoring Project
1-on-1 prep for [niece's name] (Connecticut, USA).
Course: Accelerated Mathematics I (grade 6 + first half of grade 7).
Cadence: ~30 min/day, 5 days + 1 review + 1 rest per week. ~32 weeks.
## Use it
- Start of week → check `curriculum/roadmap.md` for the topic.
- Each session → use the matching file in `sessions/week-NN/`.
- Each homework → use the matching file in `homework/week-NN/`.
- After each session → log to `progress/tracker.md`, add color in `progress/notes.md`.
## Working with the AI agent
See `AGENTS.md`. Common commands:
- "Prep Session N for tomorrow"
- "Generate homework for Session N"
- "Log: she got X/10 on HW N"
- "Make 5 extra practice problems on [topic]"
```

### 5.2 `AGENTS.md`

```markdown
# Notes for AI Agents
## Context
1-on-1 math tutoring project. Teacher = uncle. Student = niece in Connecticut, USA, taking Accelerated Mathematics I (US grade 6 + first half of grade 7). Khan Academy is the primary content source.
## When asked to "prep Session N"
1. Read `curriculum/roadmap.md` to find Session N's topic.
2. Read `sessions/_template.md`.
3. Read `resources/khan-academy-map.md` for the matching KA unit/lesson names.
4. Write a new file at `sessions/week-{WW}/session-{NN}-{topic-slug}.md` using the template.
5. Language: plain English. Examples: real-world objects a kid can see around her.
## When asked to "make homework for Session N"
1. Read the matching session file for scope.
2. Generate exactly **10 problems**, progressive difficulty (basic → mixed → 1 stretch).
3. Save to `homework/week-{WW}/hw-{NN}-{topic-slug}.md` using the homework template.
4. Always include the answer key in the same file under "Answer key (for teacher)".
## When asked to "log: ..."
- Append a row to `progress/tracker.md`.
- If the user added narrative ("she struggled with X"), append a dated entry to `progress/notes.md`.
## When asked "what's coming this week?"
- Read `curriculum/roadmap.md` and summarize the current and next week's topics in 3-5 lines.
## Conventions (don't violate)
- **Order matters in math notation.** Preserve the order stated in any problem (e.g. "cats : dogs" = cats first).
- **Don't rush mastery.** Accelerated ≠ skipping. If she's not at mastery, don't advance.
- **Use concrete examples.** Fruit, pens, marbles, pets — things a kid can see.
- **Don't introduce a concept earlier than the roadmap.** If she finishes fast, note it in `progress/notes.md` and let the teacher decide.
- **Glossary extends as terms appear.** Whenever a new math term is introduced in a session, add it to `resources/glossary.md` (English | Vietnamese | plain definition).
```

### 5.3 `sessions/_template.md`

```markdown
# Session {N} — {Topic} · ~30 min
**Date:** YYYY-MM-DD
**Week:** {WW}
**Khan Academy:** {course} → {unit} → {lesson(s)}
**Goal:** {one-sentence learning objective}
## 1. Warm-up — 3 min
{Real-world hook using objects she can see.}
## 2. Teach the concept — 7 min
{Plain-language explanation. Include the key idea and one common pitfall.}
## 3. Khan Academy — 8 min
Watch together: {video titles}. Pause and explain as needed.
## 4. Practice — 8 min
Do the {KA exercise name}, or these problems:
1. ...
2. ...
**Answers (for teacher):** ...
## 5. Check understanding + close — 4 min
Ask: "{one final question}".
If correct → mastered. Preview tomorrow: "{next concept}".
## Common mistake to watch for
{The single most likely error.}
## Stretch (if she finishes fast)
{Optional bridge to tomorrow.}
```

### 5.4 `homework/_template.md`

```markdown
# Homework {N} — {Topic}
*~15–20 min. {one-line instruction}.*
1. ...
2. ...
...
10. ...
---
## Answer key (for teacher)
1. ...
...
**Note on common variations:** {e.g., reduced vs unreduced answers}
**Scoring guide:** 9–10 → move on. 6–8 → review wrong ones before next session. ≤5 → re-watch the relevant Khan video and redo this homework.
```

### 5.5 `progress/tracker.md`

```markdown
# Progress Tracker
| Week | Session | Topic | Date | HW score | Quiz score | Notes |
|------|---------|-------|------|----------|------------|-------|
| 1 | 1 | Ratios — intro | | | | |
| 1 | 2 | Equivalent ratios | | | | |
| ... | | | | | | |
```

### 5.6 `progress/notes.md`

```markdown
# Teacher's Notes
Free-form. Date entries. Capture what worked, what didn't, what to revisit.
## YYYY-MM-DD
- ...
```

## 6. Seed content (paste verbatim)

### 6.1 `curriculum/roadmap.md`

See the written file — 32-week roadmap covering Grade 6 (Units 1–7) and first half of Grade 7 (Units 8–10).

### 6.2 `sessions/week-01/session-01-ratios.md`

See the written file — Session 1: What Is a Ratio?

### 6.3 `homework/week-01/hw-01-ratios.md`

See the written file — Homework 1: Ratios (10 problems + answer key).

### 6.4 `resources/khan-academy-map.md`

See the written file — KA course URLs and unit listing for 6th and 7th grade.

### 6.5 `resources/glossary.md`

See the written file — Bilingual EN ↔ VI glossary, starting with ratio, equivalent ratios, unit rate, percent, variable.

## 7. Workflow after kickoff

Day-to-day commands the teacher will give:

| Teacher says | Agent does |
|--------------|-----------|
| "Prep Session 2 for tomorrow" | Generates `sessions/week-01/session-02-equivalent-ratios.md` from template + roadmap. |
| "Make homework for Session 2" | Generates `homework/week-01/hw-02-equivalent-ratios.md` with 10 problems + answer key. |
| "Log: she got 9/10 on HW 1" | Appends row to `progress/tracker.md`. |
| "She struggled with order in ratios" | Appends dated entry to `progress/notes.md`. |
| "Make 5 extra practice problems on equivalent ratios" | Creates `homework/week-01/extra-equivalent-ratios.md`. |
| "What's coming this week?" | Reads roadmap, summarizes current + next week in 3-5 lines. |

## 8. Definition of done

Kickoff is complete when:
- All folders in §4 exist.
- Every file in §5 (templates + README + AGENTS.md) is populated.
- All seed files in §6 contain the exact content above.
- Empty placeholder folders for `sessions/week-02..32/` and `homework/week-02..32/` exist.
- Teacher can immediately run **"Prep Session 2 for tomorrow"** and the agent has enough context to do it without re-asking the basics.

## 9. Stretch goals (later, not now)

- `make-worksheet hw-NN` — markdown-to-printable-PDF generator.
- Local progress dashboard (single HTML reading `progress/tracker.md`).
- iOS Shortcut to log scores into `progress/tracker.md` from the phone.
- Auto-import Khan Academy mastery via parent-account export (if API permits).

---

**End of spec.**
