# Equal totals can hide an identity change

This fictional exercise compares two destination snapshots with three explicit VEVENT records each. At event position 2, the UID differs. Counting alone reports a zero delta; Calendar Identity reports one removed identity, one added identity and two shared identities. Positions are one-based within each input file.

From the extracted source directory, after following the root README setup:

```sh
.venv/bin/python calendar_identity.py examples/equal-count/before.ics examples/equal-count/after.ics
.venv/bin/python calendar_identity.py examples/equal-count/before.ics examples/equal-count/before.ics
```

The first command reports `before_events: 3`, `after_events: 3`, `added_event_positions: [2]`, `removed_event_positions: [2]`, `shared_identities: 2` and no sequence regressions. The unchanged-file control reports three shared identities and empty addition/removal lists. These are synthetic examples; no provider import or real calendar was used.

For an authorized local comparison, preserve original exports and use the same destination scope before and after a change. The report observes literal explicit identities in those files. It does not explain why an identity changed, prove an import succeeded, establish deletion in the live service, or show that a removed and added identity represent the same appointment. Export scope and representation differences affect interpretation.

Shared identity does not establish unchanged event content. Recurrences are not expanded: explicit VEVENT counts are not occurrence counts. This tool does not repair calendars or predict provider behavior. Reports omit UID and event text, but counts and positions can still be sensitive. Never upload real calendars or private reports to public issues.
