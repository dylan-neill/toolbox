# 05: Window geometry & last-toolset persistence

**What to build:** Toolbox remembers its window size/position and the
last-selected toolset between runs, with no visible settings for them. On launch
it restores the saved geometry and toolset; on close it saves the geometry;
changing the toolset saves it. These are silently persisted settings — no dialog
row.

See `../spec.md` §5 (persistence lifecycle).

**Blocked by:** 01 (the store), 03 (the reload/top-bar combo logic the guarded
on-change save must coexist with)

**Status:** ready-for-agent

- [ ] On launch, saved window geometry and `last_toolset` are restored — falling
  back to the centered default size and the first toolset when absent — replacing
  the hardcoded geometry and `setCurrentIndex(0)`.
- [ ] Window geometry is saved on window close (base64 of `saveGeometry()`);
  `last_toolset` is saved when the user changes the toolset.
- [ ] The on-change save is guarded (signal-block / re-entrancy flag) so
  programmatic combo updates (reload, launch restore) do not persist spurious
  values — only genuine user changes write.
- [ ] Both saves use load-modify-write so `config_path`/`terminal` settings are
  never clobbered.
