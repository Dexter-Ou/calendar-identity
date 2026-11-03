# Compare calendar exports before investigating a migration

For technical migration operators. Calendar Identity compares two local UTF-8 ICS files; it does not migrate events or certify an import.

1. Keep original exports intact and use authorized disposable copies. Use the [README setup instructions](../README.md) on the tested Linux/Python 3.12 platform. Start with the included fictional exercise before processing private exports.
2. Check that each export represents the intended source, destination and time of capture. This tool cannot establish those facts or query the live provider. Different export scopes can explain differences.
3. Run the comparison. Exit 0 means comparison completed, including when differences exist. Exit 2 means input was rejected or unreadable; do not interpret that as a completed comparison. Review unsupported formats and ambiguity guidance before proceeding.
4. Inspect additions/removals even when both files contain equal event totals. Positions are 1-based VEVENT order separately in each input, not shared row numbers. Preserve the original file when locating an event privately by position.
5. Treat an added/removed pair as an investigation lead. A UID change can cause that result; literal recurrence representations and TZID are not normalized. A moved occurrence can retain the same recurrence identity. No recurrence expansion is performed.
6. Investigate sequence regressions using the source system's history. Missing SEQUENCE is treated as 0. Shared identity does not establish equal titles, times, attendees or content. The report does not compare all content.
7. If duplicate identity causes rejection, do not delete records or select the highest revision solely to make this tool accept the file. Follow the [duplicate-export guidance](../calendar-identity-feedback/DUPLICATE-EXPORT-NOTE.md) and investigate the source privately.
8. Validate any proposed import separately through the calendar provider's documented process on disposable test data. A successful comparison is neither a validation certificate nor evidence that an import is safe.

Keep real calendars and reports private: counts and positions may be sensitive even when UID, titles, descriptions and attendees are omitted. Report setup problems using a minimal fictional example, Python version and expected result; do not upload private calendars to public issues.

Tested examples: four synthetic CLI cases on Linux/Python 3.12 checked equal-count identity changes, ambiguous duplicate rejection, sequence regression and changed-time limitations against source revision `06045639614d330526541e603b012051d0bffd5b`. These checks used an existing dependency environment; they did not test a provider import.
