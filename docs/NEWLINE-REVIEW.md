# Comparison success does not validate description text

Calendar Identity compares event identities and SEQUENCE values. Exit 0 does not establish that descriptions were preserved as intended or that another calendar application will import the file correctly.

Consider three fictional DESCRIPTION byte sequences (the rest of each calendar is identical):

| DESCRIPTION bytes shown with Python bytes-literal escapes | Observed comparison |
| --- | --- |
| `b'DESCRIPTION:Fictional first\\nFictional second'` | Exit 0; one shared identity |
| `b'DESCRIPTION:Fictional first\nFictional second'` | Exit 2; parser reported invalid properties |
| `b'DESCRIPTION:Fictional first\nX-FICTIONAL:second'` | Exit 0; one shared identity |

In this notation, `\\n` is a literal backslash followed by n; `\n` is an actual LF byte. The second and third fixtures deliberately insert a raw LF where their fictional author intended description text. The property-shaped line in the third fixture may instead be parsed as a separate extension property. A successful identity comparison cannot determine that author's intent. These examples do not classify every raw newline as invalid.

Keep the original exports and inspect suspicious description content with an appropriate calendar editor or validator. Do not automatically replace newlines or rewrite calendar files from these results. Calendar Identity does not repair input or predict provider imports.

## Run the synthetic probe

Complete the [README setup](../README.md), then save [newline_probe.py](../examples/newline/newline_probe.py) locally. This example is separate from the pinned source ZIP and was added after it. Use the installed environment with an explicit engine path:

```sh
PROJECT="/absolute/path/calendar-identity"
"$PROJECT/.venv/bin/python" /absolute/path/newline_probe.py "$PROJECT/calendar_identity.py"
```

The probe creates and removes temporary fictional inputs, runs three CLI comparisons, checks the expected exit codes and identity counts or diagnostic, and checks that input and engine bytes remain unchanged. It prints JSON and exits 0 when those checks pass; otherwise it exits nonzero. The raw-text fixture's expected CLI exit 2 is a passing probe result.

These synthetic cases were tested on Linux/Python 3.12.15 with engine SHA256 `e3313cf399843c9cb888ac225005b75421e8d0e8961ba78f6914ad444441a0a9`. They are not Thunderbird export/import tests or comprehensive RFC validation. Results may differ with other parser versions.
