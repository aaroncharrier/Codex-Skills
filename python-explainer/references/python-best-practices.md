# Python Best Practices

## Apply guidance selectively

- Add best-practice guidance only when it improves understanding or highlights a real quality issue.
- Prefer concrete correctness, maintainability, readability, or safety concerns over stylistic nitpicks.
- Keep the focus on explanation first and recommendations second.

## Categorize issues

### Likely bugs

- Call out mutable default arguments, accidental shared state, or incorrect `None` handling.
- Flag swallowed exceptions, overly broad `except` blocks, or missing cleanup for owned resources.
- Flag async mistakes such as missing `await`, blocking calls in async paths, or confused coroutine lifecycles.
- Flag initialization or import-order behavior that can fail depending on execution path.

### Maintainability issues

- Call out unclear names, mixed responsibilities, or oversized functions and classes.
- Call out hidden import-time side effects, brittle implicit contracts, or repeated validation and parsing logic.
- Recommend type hints when they materially clarify a public interface or complex data flow.
- Recommend `dataclass` or other focused data structures when state is manual and hard to reason about.

### Optional improvements

- Suggest context managers, `pathlib`, or clear standard-library helpers when they improve readability.
- Suggest docstrings for public or non-obvious behavior when they would help future readers.
- Suggest small control-flow simplifications when they improve clarity.
- Mention tests only when behavior is subtle or regression-prone.

## Use modern Python 3.11+ guidance

- Prefer precise exceptions over catch-all handlers.
- Use context managers for files, locks, subprocesses, and other owned resources.
- Separate pure logic from I/O when that makes the code easier to explain and test.
- Prefer immutable or well-scoped state for configuration-like data when practical.
- Keep module imports light on side effects.
- Mention performance only for concrete hotspots such as repeated quadratic work, unnecessary copying, or blocking I/O in sensitive paths.
