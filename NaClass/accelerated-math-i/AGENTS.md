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
