# Review timezone definitions separately

Calendar Identity compares literal UID and typed RECURRENCE-ID representations. A shared identity is not evidence that two calendar exports put an occurrence at the same instant.

Two fictional exports with UID `fictional-series`, RECURRENCE-ID `20261104T120000` and TZID `Experiment/Fixed` retain a shared identity when the accompanying VTIMEZONE fixed offset changes from +0100 to +0200. Those definitions put local noon at different UTC instants. The tool does not compare timezone definitions. Conversely, local noon at +0100 and 11:00Z can describe the same instant but produce a removal and addition when their recurrence representations differ.

Keep both exports and review timezone definitions and displayed occurrence times separately before drawing a migration conclusion. Do not infer unchanged times from shared identity or infer actual event deletion from a representation-only change. This tool does not expand recurrence rules or predict provider imports.

Review basis: three synthetic CLI cases passed on Linux/Python 3.12.15 with pinned engine SHA256 e3313cf399843c9cb888ac225005b75421e8d0e8961ba78f6914ad444441a0a9. These cases cover two fixed-offset examples and an identical control, not DST transition correctness, real provider exports, customer migration or import behavior.

## Run the synthetic probe

After completing the [README setup](../README.md), save [timezone_probe.py](../examples/timezone/timezone_probe.py) locally. It is a separate example added after the pinned source ZIP. With the ZIP extracted and dependencies installed, use its virtual environment to run:

```sh
PROJECT="/absolute/path/calendar-identity"
"$PROJECT/.venv/bin/python" /absolute/path/timezone_probe.py "$PROJECT/calendar_identity.py"
```

The probe creates and removes temporary fictional inputs. It asserts one shared identity for the changed-definition and identical-control cases, and one addition/removal with zero shared identities for the equivalent-instant representation change. Success exits 0 and prints JSON for all three cases; a failed assertion exits nonzero. It checks that input and engine bytes are unchanged. Run normally without Python's `-O` option, which disables assertions. These fixed-offset cases do not validate DST behavior.
