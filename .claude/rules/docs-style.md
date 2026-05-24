---
paths:
  - "documents/**/*.md"
---

# Framework Docs — Writing Style

When editing files under `documents/`:

- **No emojis.** None.
- **Prose first, lists second.** The framework docs argue from first principles. Use full sentences for argument; reserve lists for enumerations.
- **Define before use.** When introducing a term, define it the same paragraph. Cross-reference the part number for the formal definition.
- **One claim per paragraph.** If a paragraph holds two claims, split it.
- **Concede openly.** When a counterargument exists, name it and address it. The "Anticipated objections" section (3.4) is the template.
- **No hype.** Avoid words like "revolutionary," "game-changing," "unprecedented." The framework's value is structural, not rhetorical.
- **Specificity in falsifiers.** Falsification conditions must be specific enough to operationalize. Vague falsifiers are unfalsifiable.
- **Cross-doc consistency.** Terminology, section numbering, and pyramid labels must stay aligned across all four docs. Before changing a term, grep for it in the other three.
- **Footnotes belong in prose.** No actual footnote syntax. If something deserves a caveat, write it as a paragraph that begins "One caveat..." or "A related concern..."
- **HTML comments for human notes.** `<!-- ... -->` blocks are stripped before context injection. Use them for maintainer notes you don't want spending tokens.
