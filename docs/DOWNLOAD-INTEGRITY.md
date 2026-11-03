# Verify the Calendar Identity source download

Before extracting or installing the preview, check that the ZIP matches the documented source snapshot. This uses Python 3.12's standard library and installs nothing.

Download [the pinned source ZIP](https://github.com/Dexter-Ou/calendar-identity/archive/f9f28a77bcbbb2ab891f301e8b11dc8ea1ea80b7.zip). Save it as `calendar-identity-f9f28a77bcbbb2ab891f301e8b11dc8ea1ea80b7.zip`. Open a POSIX shell in the download directory and run:

```sh
python3 - <<'PYVERIFY'
import hashlib
from pathlib import Path
archive = Path("calendar-identity-f9f28a77bcbbb2ab891f301e8b11dc8ea1ea80b7.zip")
expected = "7bf70ce0392b9eeca6b3e05877872ec9905caae702275568c4c67212dd3e1a46"
try:
    with archive.open("rb") as source:
        actual = hashlib.file_digest(source, "sha256").hexdigest()
except OSError:
    raise SystemExit("Archive unreadable; check the filename and download location.")
if actual != expected:
    raise SystemExit("SHA256 mismatch; stop before extracting or installing.")
print("SHA256 matches the pinned archive.")
PYVERIFY
```

Continue with README setup only after the matching message and exit status 0. A mismatch exits nonzero: stop, confirm the exact commit URL and filename, and retrieve a fresh copy from that URL. Do not change the expected hash just to silence a mismatch. An unreadable-file message means the file could not be opened; check your working directory, filename and permissions.

The expected SHA256 is `7bf70ce0392b9eeca6b3e05877872ec9905caae702275568c4c67212dd3e1a46`. It refers only to commit `f9f28a77bcbbb2ab891f301e8b11dc8ea1ea80b7`, not to the moving main branch or later documentation commits.

This detects byte differences against this recorded archive. It is not a publisher signature, independent authentication, a security audit, or verification of separately downloaded dependencies. The ZIP does not bundle dependency wheels. GitHub-generated archive bytes can change; if the exact commit download repeatedly differs, stop and report the commit and observed hash without sending private calendar data. Do not run the mismatching archive to diagnose it.

After a match, extract the ZIP and open `calendar-identity-f9f28a77bcbbb2ab891f301e8b11dc8ea1ea80b7`. This snapshot includes the migration checklist, timezone and newline review guides with their probes, plus Unicode and file-layout probes. Its embedded README and integrity guide still reference the preceding source snapshot; do not redownload that older snapshot or apply its checksum to this ZIP. Continue with the Python 3.12 setup commands in the included README, which are unchanged, or the current online README. Preserve the ZIP and this checksum for source recovery; keep private calendars separately under your own backup procedure.
