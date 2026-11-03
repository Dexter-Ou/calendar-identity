# Fictional 5,000-event scale check

After installing the pinned CLI using the root README, save `scale_check.py` and run:

```sh
python3 scale_check.py /absolute/path/to/.venv/bin/calendar-identity
```

The script uses only Python's standard library. It creates two temporary fictional calendars with 5,000 events each and changes SEQUENCE from 7 to 6 at the final event. It checks exact identity counts, the sole changed position and regression, unchanged input bytes, and omitted fixture UIDs. Temporary calendars are removed when the script exits normally, including handled errors. The script makes no network requests; it invokes the CLI you select. Run only a trusted executable.

Expected: JSON with `synthetic_only: true`, ten true checks, `passed: true` and exit 0. A failed check or execution error exits nonzero. The CLI has a fixed 30-second timeout; slow systems may fail this check. Measured elapsed time describes one synthetic run on your system, not a general performance guarantee. No real calendar exports are needed or read by this script.

Tested on Linux with Python 3.12; other platforms are untested. This checks explicit VEVENT identities, not recurrence expansion, provider import behavior or repair. It does not install dependencies or modify the installed CLI.
