---
name: python-explainer
description: Explain Python snippets, files, classes, modules, and small multi-file examples, and review them for modern Python 3.11+ best practices or targeted improvement guidance. Use when requests ask what Python code does, whether Python code follows best practices, or how to improve a Python module without defaulting to a full rewrite.
---

# Python Explainer

Explain Python code before recommending changes. Assume general-purpose Python 3.11+ unless the code or user indicates otherwise.

## Workflow

1. Identify the input shape: snippet, whole file, class, or small multi-file example.
2. Check for missing context such as entrypoint, expected behavior, surrounding files, or runtime constraints.
3. Ask clarifying questions first when missing context would materially change the explanation or guidance.
4. Explain the code in this order:
   - short summary
   - key code paths, data flow, or important moving parts
   - best-practice notes only when clearly warranted
5. Group issues, when present, into:
   - likely bugs
   - maintainability issues
   - optional improvements
6. Mention performance only when there is a concrete issue.
7. Offer a tiny local rewrite example only when it materially improves understanding.

## References

- Read `references/explanation-patterns.md` to choose an explanation shape for the current input.
- Read `references/python-best-practices.md` when the user asks about quality, best practices, or improvements, or when strong issues are visible.

## Response Style

- Optimize for comprehension first, not rewriting.
- Keep explanations approachable and precise.
- Avoid assuming framework behavior unless the code clearly depends on it.
- Suggest code changes only when strong best-practice issues are present.
- Keep rewrite examples small and local.

## Examples

- "Explain what this Python function does."
- "Does this Python module follow best practices, and how should I improve it?"
