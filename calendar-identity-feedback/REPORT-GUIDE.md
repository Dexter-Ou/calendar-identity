# Read the fictional migration report

Use this guide after the [setup exercise](TASK.md). It uses only the bundled
fictional exports; no provider account, upload or calendar import is needed.
Run from the extracted repository root after installing the README requirements:

```sh
.venv/bin/python calendar_identity.py calendar-identity-feedback/before.ics calendar-identity-feedback/after.ics
```

A completed comparison exits 0 even when differences exist. Its JSON is:

```json
{
  "format": "calendar-identity-preview-1",
  "comparison": "literal UID and typed recurrence representation; no timezone equivalence or recurrence expansion",
  "before_events": 3,
  "after_events": 3,
  "added_event_positions": [
    1
  ],
  "removed_event_positions": [
    3
  ],
  "shared_identities": 2,
  "sequence_regressions": [
    {
      "before_position": 2,
      "after_position": 2,
      "before_sequence": 3,
      "after_sequence": 2
    }
  ],
  "changed_event_representations": [
    {
      "before_position": 1,
      "after_position": 3
    },
    {
      "before_position": 2,
      "after_position": 2
    }
  ],
  "limitations": [
    "Shared identity does not mean unchanged event content.",
    "Changed event representations compare parsed VEVENT serialization, including revision metadata and nested components; not semantic equivalence.",
    "No warning does not prove unchanged source bytes or content; parser normalization and external VTIMEZONE definitions are outside this check.",
    "Representation changes can appear as removal plus addition.",
    "No prediction of import, merge, notification or provider behavior.",
    "Counts cover explicit VEVENT records only, not expanded occurrences."
  ]
}
```

| Field | Meaning in this example | Review action |
| --- | --- | --- |
| `format` | Report schema marker `calendar-identity-preview-1`. | Check this marker before consuming fields in another tool. |
| `comparison` | Identity uses decoded, case-sensitive UID and literal typed RECURRENCE-ID representation, including TZID. | Do not infer equivalent timezones or expanded recurrence matches. |
| `before_events`, `after_events` | Three explicit VEVENT records in each input. | Equal totals do not establish preservation; the additions and removals differ. RRULE occurrences are not counted. |
| `added_event_positions` | After-file VEVENT position 1 has an identity absent from before. | Inspect after position 1 in your authorized local copy. This is not proof of a newly created real-world meeting. |
| `removed_event_positions` | Before-file VEVENT position 3 has an identity absent from after. | Inspect before position 3. This is not proof that a provider deleted anything. |
| `shared_identities` | Two identities occur in both files. | Inspect content separately: the fictional master changes SUMMARY and the exception changes DTSTART while retaining identity. |
| `sequence_regressions` | The shared exception at before position 2 and after position 2 falls from sequence 3 to 2. | Investigate export provenance/revisions; do not automatically select, rewrite or import a revision. |
| `changed_event_representations` | Shared before positions 1 and 2 differ from after positions 3 and 2 in parsed VEVENT serialization. | Inspect those records locally. Revision metadata and nested components count as changes; this is not semantic equivalence or a field-by-field diff. |
| `limitations` | Scope reminders attached to this report. | Keep them with any saved report; success does not certify import safety. |

Positions count VEVENT records from 1 separately in each input. They are not
line numbers, calendar indexes or permanent identifiers. A shared event can
move to a different position. Missing SEQUENCE is treated as 0; the regression
list contains only decreases for shared identities. An empty list does not mean
unchanged content or successful migration. A changed UID or recurrence
representation can appear as an addition plus a removal.

`changed_event_representations` compares parsed VEVENT serialization for shared
identities. It includes revision metadata and nested components. An empty list
does not prove unchanged source bytes or content: parser normalization and
external VTIMEZONE definitions are outside this check. It does not identify the
cause of a change or establish which revision is correct.

For this fictional migration, the next decision is to investigate the unmatched
records and the lower exception sequence before attempting any disposable
provider test. The report alone cannot decide whether to import, merge, delete
or notify attendees. It neither changes the files nor contacts a provider.

To see the separate error path, run:

```sh
.venv/bin/python calendar_identity.py calendar-identity-feedback/before.ics calendar-identity-feedback/ambiguous.ics
```

This exits 2, leaves stdout empty and writes the following JSON to stderr:

```json
{"error": "Duplicate UID/recurrence identity; comparison is ambiguous"}
```

There is no comparison report to interpret in this case. Different SEQUENCE
values do not resolve duplicate identities automatically; see the
[duplicate-export note](DUPLICATE-EXPORT-NOTE.md).

Linux/Python 3.12 is the tested platform. Each input must resolve to a regular
UTF-8 file no larger than 8 MiB. Dependencies are installed separately; reading
this guide and running an already installed CLI require no network connection.
See the root README for parser tolerance and unsupported structures. Counts
and positions can be sensitive even though reports omit UIDs, titles and
attendees. Share only fictional reproductions in public issues.
