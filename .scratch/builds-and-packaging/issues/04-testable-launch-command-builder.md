# 04: Testable launch-command builder

**What to build:** The core behaviour of the launcher — turning a Tool's `rez_wants` and `command` into the `rez-env <rez_wants> -- <command>` invocation — is a pure function that can be unit-tested in isolation, instead of being tangled inside the UI. Launching a Tool behaves exactly as before; the logic is simply now guarded by tests.

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] Seam A: launch-command construction is a pure function taking the Rez command, a Tool's `rez_wants`, and the Tool's `command`, returning the full invocation string
- [ ] The UI calls this function; launching a Tool produces the same command it did before
- [ ] Unit tests cover the produced string, including multiple `rez_wants` and an empty `rez_wants`
- [ ] Tests assert external behaviour (the output string), not internal call sequences
