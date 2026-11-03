# Verify the Calendar Identity source download

Before extracting or installing the preview, check that the ZIP matches the documented source snapshot. This uses Python 3.12's standard library and installs nothing.

Download [the pinned source ZIP](https://github.com/Dexter-Ou/calendar-identity/archive/06045639614d330526541e603b012051d0bffd5b.zip). Save it as `calendar-identity-06045639614d330526541e603b012051d0bffd5b.zip`. Open a POSIX shell in the download directory and run:

```sh
python3 - <<'PYVERIFY'
import hashlib
from pathlib import Path
archive = Path("calendar-identity-06045639614d330526541e603b012051d0bffd5b.zip")
expected = "b1f53edf1d9c407b5e80b880efa1cbe7c1bf804b540baccd2113029cbcf5904d"
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

The expected SHA256 is `b1f53edf1d9c407b5e80b880efa1cbe7c1bf804b540baccd2113029cbcf5904d`. It refers only to commit `06045639614d330526541e603b012051d0bffd5b`, not to the moving main branch or later documentation commits.

This detects byte differences against this recorded archive. It is not a publisher signature, independent authentication, a security audit, or verification of separately downloaded dependencies. The ZIP does not bundle dependency wheels. GitHub-generated archive bytes can change; if the exact commit download repeatedly differs, stop and report the commit and observed hash without sending private calendar data. Do not run the mismatching archive to diagnose it.

After a match, extract the ZIP and follow the included README. Preserve the ZIP and this checksum for source recovery; keep private calendars separately under your own backup procedure.
