# Calendar Identity setup exercise

Use only these fictional calendars. No calendar account or import is needed.
Download the **Source with fictional exercise** ZIP linked in the repository README,
then extract it. The archive contains both the Python source and this exercise.
Python 3.12 on Linux is the tested platform. Dependencies need package-index access.
From the extracted repository's root directory, create the virtual environment and
install requirements using the README's first two setup commands. Then run:

```sh
.venv/bin/python calendar_identity.py calendar-identity-feedback/before.ics calendar-identity-feedback/after.ics
.venv/bin/python calendar_identity.py calendar-identity-feedback/before.ics calendar-identity-feedback/ambiguous.ics
```

Before opening ANSWERS.md, answer:

1. Which explicit event positions were added and removed? Which shared position regressed in sequence?
2. Does the moved exception keep its identity? Do shared identities prove unchanged content?
3. How many explicit records are counted? Is that an expanded recurrence count or proof an import is safe?
4. Does the second command produce a usable comparison? What exit code do you observe?

Optional workflow feedback (answer before reading ANSWERS.md or REPORT-GUIDE.md):
- For the fictional SEQUENCE decrease, what would you investigate next, and which before/after event positions would you inspect? What can this report alone establish about the cause?
- Are positions and SEQUENCE values enough for that next step? If not, describe the missing information without sharing real calendar data. Would you need to inspect your authorized local exports separately?
- If you already compare authorized exports, describe your current method and whether this report would change a specific decision. “No change” or “no applicable workflow” are useful answers. Do not upload exports or reports.

For setup feedback, report Python/OS version and the first confusing step or where setup stopped. No timing target or completion claim is implied.
Share only a fictional reproduction through the repository issues if you choose. Do not upload real calendars, private UIDs, titles, attendees or reports. Counts and positions may be sensitive. Support is best effort. See preview README for full parser/scope limitations.

For a structured setup or bug report, use the optional [fictional exercise issue template](../.github/ISSUE_TEMPLATE/fictional-exercise.md). GitHub issues are public and require an account; review all text before submitting.

After answering, use the [field-by-field report guide](REPORT-GUIDE.md) to connect the JSON to a fictional migration review.
