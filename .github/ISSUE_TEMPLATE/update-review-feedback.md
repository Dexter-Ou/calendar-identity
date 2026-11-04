---
name: Fictional three-export update-review feedback
about: Describe a setup problem or unclear result using only the bundled fictional update-review exercise
title: ''
labels: ''
assignees: ''
---

This form is optional. GitHub issues are public and require an account. Use only
examples/update-review/old.ics, intended.ics and destination.ics. Do not attach real
exports or their reports, real UIDs, meeting titles, attendees, credentials or
personal file paths. Review all fields before posting; you may stop without posting.

## Setup

- Operating system and Python version:
- Source commit or downloaded ZIP commit:
- First unclear or failed step in examples/update-review/README.md:

## Fictional comparison

- Which comparison: old to intended / intended to destination / old to destination?
- Exit code (if run):
- Shared identity count (if available):
- Representation warning positions (if available):
- Sequence regression positions and numbers (if available):
- Expected result and what was unclear (fictional details only):

## Interpretation (optional)

What could you conclude about these files? What could you not conclude about an
import or provider? Describe confusing instructions in general terms.

The destination fixture deliberately equals old.ics; it is not an observed failed
import. The tool compares local files, does not expand recurrence or diagnose
provider behavior, and does not establish import safety. Do not delete events or
regenerate UIDs based on this exercise. Support is best effort.
