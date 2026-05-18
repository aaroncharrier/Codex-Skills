# Explanation Patterns

## Choose the input shape

- Treat a snippet as local behavior that needs inputs, outputs, side effects, and assumptions explained.
- Treat a whole file or module as a unit that needs purpose, public surface area, helpers, imports, and side effects explained.
- Treat a class as a unit that needs responsibilities, state, invariants, collaborators, and key methods explained.
- Treat a small multi-file example as a system that needs entrypoint, file roles, imports, and cross-file data flow explained.

## Check for missing context

- Ask clarifying questions when the explanation depends on an unknown entrypoint, omitted helper file, runtime assumption, external service, or expected behavior.
- State the assumption and continue when the gap is small and unlikely to change the main explanation.
- Delay improvement advice when the missing context is architectural rather than local.

## Follow the default explanation order

1. Give a short summary of what the code does.
2. Walk through the key code paths, structures, or interactions.
3. Call out non-obvious behavior, side effects, or assumptions.
4. Add best-practice notes only when they matter to comprehension or quality.

## Adjust the emphasis by shape

- For snippets, explain inputs, return values, mutations, exceptions, and any tricky Python syntax.
- For files or modules, explain top-level behavior, public functions, helper boundaries, and dependency flow.
- For classes, explain state ownership, constructor expectations, method groups, and mutation patterns.
- For small multi-file examples, start at the entrypoint, map each file to a role, then trace the main data flow across files.

## Clarify without drifting into rewrites

- Prefer plain-English paraphrase before proposing changes.
- Use short pseudocode or a compact flow description when it reduces confusion.
- Use a tiny rewrite example only when contrast is the clearest way to explain an important point.
