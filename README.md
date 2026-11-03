# Calendar Identity — 0.1.0 preview

Compare two UTF-8 ICS exports locally. Output includes explicit VEVENT identity additions/removals, shared identity counts, and sequence regressions. Positions are 1-based VEVENT order in each file. No file modification or network calls by this program. Reports omit UID, titles, descriptions and attendees; counts and positions can still be sensitive.

[Source with fictional exercise — download the complete pinned ZIP](https://github.com/Dexter-Ou/calendar-identity/archive/ef8879b9fbe76c6f4ad830157d158f8a869b2e3d.zip). It contains the CLI source, automated tests, fictional calendars, duplicate-export guidance and optional issue template. Extract it and open the `calendar-identity-ef8879b9fbe76c6f4ad830157d158f8a869b2e3d` directory.

Free, MIT-licensed preview from Gong LLC. Use Python 3.12 (tested on Linux only). In the extracted source directory, run these POSIX shell commands:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python synthetic_journey.py
```

The disposable synthetic example should report 3 events in each file, one addition, one removal, two shared identities and one sequence regression, with `inputs_unchanged: true`. It creates its own temporary fictional calendars and removes them when finished. For your own authorized local exports and the automated tests, run:

```
.venv/bin/python calendar_identity.py before.ics after.ics
.venv/bin/python -m unittest -v
```

Exit 0 means comparison completed, including when differences exist. Exit 2 means rejected/unreadable input. Duplicate UID plus recurrence identity is ambiguous, including different revisions in one file, and stops comparison. Missing SEQUENCE is treated as 0. Inputs are limited to 8 MiB each. Multiple calendars and non-event top-level components other than VTIMEZONE are unsupported. RECURRENCE-ID RANGE and extension parameters are unsupported. The parser is an established third-party component; this program is not a comprehensive RFC validator or a hostile-file security audit.

Identity is case-sensitive decoded UID plus literal typed recurrence representation including TZID. Equivalent timezone representations are not normalized. A changed UID can appear as an addition and removal; this does not prove it is a duplicate. Shared identity does not mean unchanged content. No recurrence expansion, provider API, live calendar check, import prediction or repair. Test first on disposable copies; never infer it is safe to import from this report.

Source recovery: retain/extract the source ZIP and reinstall pinned dependencies in an isolated environment. Inputs are never rewritten. Dependency installation requires access to the package index or separately prepared packages. The ZIP does not bundle dependency wheels. 


## Parser tolerance and supported scope

This checks identity/revision properties rather than complete event validity. The parser can accept events missing DTSTART and calendars missing VERSION. Unknown TZID names are retained literally, without proving the timezone exists. The library normalizes integer spellings such as SEQUENCE:+1 before comparison. Invalid parsed dates, multiple calendars and trailing non-calendar text are rejected in the tested fixtures; this is not exhaustive malformed-input coverage. An empty calendar reports zero explicit events. Successful comparison is not a validation certificate.

## Feedback and support

Report setup problems or reproducible bugs through this repository's issues. Include a minimal fictional example, Python version and expected result. Do not upload real calendars, UIDs, titles, attendees or private reports. Support is best effort; no response-time commitment. Dependencies retain their own licenses and are installed separately.

## Fictional setup exercise

The complete ZIP above includes three fictional calendars. After setup, follow [the exercise instructions](calendar-identity-feedback/TASK.md) to compare a moved recurrence exception and an ambiguous duplicate identity without using private calendars. [Expected answers](calendar-identity-feedback/ANSWERS.md) are separate so you can inspect the results first. An optional [fictional exercise issue template](.github/ISSUE_TEMPLATE/fictional-exercise.md) helps describe setup problems; GitHub issues are public and require an account.

## Duplicate exports

[Duplicate-export guidance](calendar-identity-feedback/DUPLICATE-EXPORT-NOTE.md) explains why revision metadata does not resolve ambiguous identities and how to investigate without modifying the export. The guide is included in the complete ZIP above.
