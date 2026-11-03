# When an export contains the same identity twice

Calendar Identity stops with exit code 2 when either input contains two explicit VEVENT records with the same UID and recurrence identity. It writes a fixed ambiguity error to stderr and no comparison to stdout. A later LAST-MODIFIED or higher SEQUENCE does not make this tool select a winner.

This matters when preparing an export for migration: a comparison cannot safely pair ambiguous records. Preserve the original export and investigate the duplicates in your calendar application or with an authorized administrator. This tool does not deduplicate, repair, import or upload calendars. Do not treat a successful comparison as an import-safety guarantee.

A recurring master and an explicit exception may share a UID while having different recurrence identities; that alone is not a duplicate under this tool's literal comparison. Recurrences are not expanded, and timezone representations are not normalized.

Try the fictional ambiguous example from the repository root:

```sh
.venv/bin/python calendar_identity.py calendar-identity-feedback/before.ics calendar-identity-feedback/ambiguous.ics
```

Expected exit code: 2. Expected stderr:

```json
{"error": "Duplicate UID/recurrence identity; comparison is ambiguous"}
```

Synthetic Linux/Python3.12 checks confirmed rejection of identical duplicates, duplicates with a newer LAST-MODIFIED, and duplicates with a higher SEQUENCE. A distinct recurrence-identity control passed. Inputs remained unchanged. These checks did not exercise an actual calendar provider.
