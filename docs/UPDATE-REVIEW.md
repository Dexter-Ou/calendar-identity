# Reviewing repeated ICS exports with the same UID

Use Calendar Identity to compare explicit event identities in two local exports.
Use a separate content review to check whether a meeting's time or other fields changed.

A historical [Thunderbird 115 report about importing updates with an existing UID](https://bugzilla.mozilla.org/show_bug.cgi?id=1853250)
was closed as a duplicate. It describes an import conflict after a meeting series was updated.
It does not establish current Thunderbird behavior, and Calendar Identity does not fix or reproduce that provider conflict.

## What this comparison can tell you

These four fictional single-event cases were run with the preview on Linux/Python 3.12.15:

| After export compared with before | Shared identities | Added / removed positions | Sequence regressions |
| --- | --- | --- | --- |
| Identical bytes | 1 | none / none | none |
| Same UID; start time changes; SEQUENCE stays 3 | 1 | none / none | none |
| Same UID; start time changes; SEQUENCE increases from 3 to 4 | 1 | none / none | none |
| Different UID; same start time and SEQUENCE | 0 | `[1]` / `[1]` | none |

The first three rows have identical comparison metrics even though two inputs
contain a changed start time. The report lists sequence **regressions**, not
increases. It does not list changed event fields or say that an update was applied.
The last row shows an identity change, not proof of a duplicate meeting.

## Reproduce without a calendar account

Install the preview using the repository README. Download
[update_probe.py](../examples/updates/update_probe.py) separately; this new probe is
not included in the README's older pinned source ZIP. Save it locally and run it
with the installed product environment, replacing both absolute paths:

```sh
"/absolute/path/calendar-identity/.venv/bin/python" \
  /absolute/path/update_probe.py /absolute/path/calendar-identity
```

The probe creates temporary fictional files, invokes the actual CLI four times,
checks the expected metrics and unchanged input/engine bytes, then removes the
temporary files. It prints JSON with `pass: true` and
`first_three_metrics_identical: true` on success, and exits nonzero on a mismatch.
This is a synthetic CLI test, not a Thunderbird, Zoom or other provider import test.

## Review your own authorized exports

Keep the original exports. Compare the two individual files locally and inspect
any identity additions, removals or regressions. For shared identities, review
DTSTART, DTEND, recurrence rules and other relevant content separately in a
trusted local viewer or text tool. Such viewers may expose private calendar data.
Calendar Identity is not a complete content diff, duplicate remover, import
predictor or repair tool. Do not delete or regenerate UIDs to force an import
based on this report. Use a disposable calendar for any separate provider test;
a successful comparison does not establish that importing is safe.
