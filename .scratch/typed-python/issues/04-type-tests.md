# 04 — Type the test suite

Status: ready-for-agent

Annotate the `tests/` functions and fixtures so pyright is clean over
`tests` too.

The two robustness tests in `test_parse_config.py` deliberately pass malformed
input to `parse_config` to prove the `KeyError` contract. Those specific call
sites carry a targeted `# pyright: ignore[reportArgumentType]` with a comment
explaining the intent — the malformed input is the point of the test, not a
mistake.
