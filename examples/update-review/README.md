# A fictional three-export update review

This exercise uses three original fictional single-event files. It needs no calendar account or network access during comparison. Nothing is imported or repaired.

- `old.ics`: meeting at 09:00 UTC, SEQUENCE 3.
- `intended.ics`: same UID, meeting at 11:00 UTC, SEQUENCE 4.
- `destination.ics`: deliberately constructed with exactly the old file bytes.

The destination is a teaching fixture, not an observed provider export or a reproduction of an import failure. All files describe 5 January 2027.

## Run locally

Install Calendar Identity using its repository README. These commands require the content-warning version of `calendar_identity.py` from source revision `3c7ebbd62b43b0f0fb20b7a91b7310bc2d30acc1` (or a reviewed compatible revision). This exercise is distributed separately; older pinned source archives do not contain it.

Unzip this exercise into a new directory. Open a terminal in that directory containing the three ICS files. Set these two variables to your actual absolute source and virtual-environment Python paths, using quotes if needed:

```sh
export CALENDAR_SOURCE="/absolute/path/calendar-identity"
export CALENDAR_PYTHON="$CALENDAR_SOURCE/.venv/bin/python"
```

Run the three comparisons. The JSON report filenames below are overwritten; use a new exercise directory to retain earlier reports.

```sh
"$CALENDAR_PYTHON" "$CALENDAR_SOURCE/calendar_identity.py" old.ics intended.ics > old-to-intended.json
"$CALENDAR_PYTHON" "$CALENDAR_SOURCE/calendar_identity.py" intended.ics destination.ics > intended-to-destination.json
"$CALENDAR_PYTHON" "$CALENDAR_SOURCE/calendar_identity.py" old.ics destination.ics > old-to-destination.json
```

## Interpret the three reports

| Report | Shared identities | Representation warning | Sequence regressions |
| --- | --- | --- | --- |
| old-to-intended.json | 1 | before 1 / after 1 | none |
| intended-to-destination.json | 1 | before 1 / after 1 | 4 to 3 at position 1 |
| old-to-destination.json | 1 | none | none |

All three reports have no identity additions or removals. A representation warning means parsed VEVENT serialization differs; it does not identify the changed field or prove a meaningful scheduling difference. This fixture changes both times and SEQUENCE. Sequence increases are not separately listed.

For this constructed data, the intended and destination representations differ, while old and destination bytes match by construction. That demonstrates a local evidence gap between intended content and destination content. It does not establish whether an import happened, why content differs, which file is authoritative, or what a live service will do. No warning is not a general proof of byte equality: normalization and external timezone definitions can hide differences.

With your own authorized exports, preserve originals and use a trusted local viewer to inspect relevant fields. Reports omit event titles and UIDs but positions/counts still reveal structural information. Do not post private exports or reports without reviewing them. This tool does not expand recurrence, predict notifications, merge calendars, or recommend deletion/UID regeneration. Any provider experiment requires a separately authorized disposable calendar.

License: the repository MIT license applies to these original files.
