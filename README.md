# Calendar Identity — 0.1.0 preview

Compare two UTF-8 ICS exports locally. Output includes explicit VEVENT identity additions/removals, shared identity counts, and sequence regressions. Positions are 1-based VEVENT order in each file. No file modification or network calls by this program. Reports omit UID, titles, descriptions and attendees; counts and positions can still be sensitive.

## Start here: install the CLI

Install the pinned preview in a virtual environment, then replace the two absolute file paths below with your authorized local ICS exports. Use an empty working directory and a POSIX shell. Python 3.11+ is required; Linux/Python 3.12.15 is tested. Installation downloads build tools and dependencies; the comparison command makes no network calls.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install "https://codeload.github.com/Dexter-Ou/calendar-identity/zip/eec1ad9324bacaa0112130b7c30a811d799f0755#sha256=6c28820a96ace1c25fc0875c7314aea9b37f641666aca145f5994c6fff508504"
.venv/bin/calendar-identity --help
.venv/bin/calendar-identity /absolute/path/before.ics /absolute/path/after.ics
```

This installs `0.1.0a1` from source revision `eec1ad9324bacaa0112130b7c30a811d799f0755` with an archive checksum, rather than from a PyPI package-name listing. Invoke the CLI by its virtual-environment path from other directories. To remove it, run `.venv/bin/python -m pip uninstall calendar-identity`.

## Try fictional calendars instead

The installed package contains the CLI and license; fictional inputs, guides and tests require the separate complete source ZIP below. You do not need both setups to compare your own files. The source example uses Python 3.12 on Linux; other configurations remain untested.

[Source with fictional exercise — download the complete pinned ZIP](https://github.com/Dexter-Ou/calendar-identity/archive/3c7ebbd62b43b0f0fb20b7a91b7310bc2d30acc1.zip). It contains the CLI source, automated tests, fictional calendars, migration checklist, timezone and newline review guides, Unicode and file-layout probes, duplicate-export guidance and optional issue template. Extract it and open the `calendar-identity-3c7ebbd62b43b0f0fb20b7a91b7310bc2d30acc1` directory.

[Verify the source ZIP before extracting or installing](docs/DOWNLOAD-INTEGRITY.md). The current online guide records the checksum for this exact snapshot. The ZIP includes the corrected fictional report guide and exercise instructions. Its embedded README and integrity guide point to a preceding exercise snapshot; use the checksum in the current online guide for this ZIP. After verifying this ZIP using the current online guide, continue with the setup commands below (or the identical setup commands inside the ZIP); you do not need to download the older snapshot.

Free, MIT-licensed preview from Gong LLC. Use Python 3.12 (tested on Linux only). In the extracted source directory, run these POSIX shell commands:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python synthetic_journey.py
```

The disposable synthetic example should report 3 events in each file, one addition, one removal, two shared identities and one sequence regression, with `inputs_unchanged: true`. It creates its own temporary fictional calendars and removes them when finished. For your own authorized local exports and the automated tests, run:

```
.venv/bin/python calendar_identity.py before.ics after.ics
.venv/bin/python -m unittest -v
```

To run from another directory after completing setup, set `PROJECT` to the absolute path of your extracted source directory. Keep the quotes, including when paths contain spaces. This example compares only the included fictional calendars:

```sh
PROJECT="/absolute/path/calendar-identity"
"$PROJECT/.venv/bin/python" "$PROJECT/calendar_identity.py" \
  "$PROJECT/calendar-identity-feedback/before.ics" \
  "$PROJECT/calendar-identity-feedback/after.ics"
```

Expected: 3 events per file, added position `[1]`, removed position `[3]`, 2 shared identities and one sequence regression (before position 2, sequence 3; after position 2, sequence 2). Exit status is 0. The command reads both inputs without changing them; it does not import events.

Exit 0 means comparison completed, including when differences exist. Exit 2 means rejected/unreadable input. Duplicate UID plus recurrence identity is ambiguous, including different revisions in one file, and stops comparison. Missing SEQUENCE is treated as 0. Inputs are limited to 8 MiB each. Nested VEVENT records are rejected, including records structurally equal to a top-level event. Multiple calendars and non-event top-level components other than VTIMEZONE are unsupported. RECURRENCE-ID RANGE and extension parameters are unsupported. The parser is an established third-party component; this program is not a comprehensive RFC validator or a hostile-file security audit.

Identity is case-sensitive decoded UID plus literal typed recurrence representation including TZID. Equivalent timezone representations are not normalized. VTIMEZONE definitions are not compared: the same TZID and recurrence text can retain identity despite a changed UTC offset. [Review timezone definitions separately](docs/TIMEZONE-REVIEW.md), including three runnable synthetic examples. A changed UID can appear as an addition and removal; this does not prove it is a duplicate. Shared identity does not mean unchanged content. No recurrence expansion, provider API, live calendar check, import prediction or repair. Test first on disposable copies; never infer it is safe to import from this report.

UID comparison does not normalize Unicode spelling. For example, fictional `caf\u00e9@example.invalid` (precomposed é) and `cafe\u0301@example.invalid` (e followed by a combining accent) can look the same but report one removal and one addition, with zero shared identities. The `\u` notation here names Unicode code points, not literal backslashes in the UID. Identical accented UIDs, including the tested folded/unfolded representation, share identity. Do not rewrite UIDs from appearance alone; retain the original exports for review.

To reproduce these three synthetic cases after setup, save [unicode_probe.py](examples/unicode/unicode_probe.py) locally and run `"/absolute/path/calendar-identity/.venv/bin/python" /absolute/path/unicode_probe.py /absolute/path/calendar-identity`. The probe prints JSON and exits nonzero if expected identities or unchanged input/engine bytes do not match. It creates temporary fictional calendars and removes them afterward. Tested on Linux/Python 3.12.15; this is not a provider import/export test. This probe is included in the pinned source ZIP.


Source recovery: retain/extract the source ZIP and reinstall pinned dependencies in an isolated environment. Inputs are never rewritten. Dependency installation requires access to the package index or separately prepared packages. The ZIP does not bundle dependency wheels. 


## Choose your review task

| Your task | Start here | What this tool can establish |
| --- | --- | --- |
| Compare identities in two calendar export files | [Migration review checklist](docs/MIGRATION-CHECKLIST.md) | Added, removed and shared literal event identities, plus sequence regressions. |
| Investigate repeated imports or changed meeting times | [Repeated-export review](docs/UPDATE-REVIEW.md) | Identity overlap only; matching metrics do not confirm unchanged content or a successful update. |
| Understand a report before using your own exports | [Fictional report guide](calendar-identity-feedback/REPORT-GUIDE.md) | Field meanings and the ambiguous-identity error path, using included fictional inputs. |

Use two individual regular ICS files. Collection directories, import repair and provider synchronization are outside this tool's scope. Keep original exports unchanged and perform any import test separately on disposable calendars. The setup and pinned download above remain the starting point for running the CLI.


## Parser tolerance and supported scope

This checks identity/revision properties rather than complete event validity. The parser can accept events missing DTSTART and calendars missing VERSION. Unknown TZID names are retained literally, without proving the timezone exists. The library normalizes integer spellings such as SEQUENCE:+1 before comparison. Invalid parsed dates, multiple calendars and trailing non-calendar text are rejected in the tested fixtures; this is not exhaustive malformed-input coverage. An empty calendar reports zero explicit events. Successful comparison is not a validation certificate. Raw newline behavior can depend on the following text: [see the synthetic DESCRIPTION examples and probe](docs/NEWLINE-REVIEW.md).

## Feedback and support

Report setup problems or reproducible bugs through this repository's issues. Include a minimal fictional example, Python version and expected result. Do not upload real calendars, UIDs, titles, attendees or private reports. Support is best effort; no response-time commitment. Dependencies retain their own licenses and are installed separately.

## Fictional setup exercise

The complete ZIP above includes three fictional calendars. After setup, follow [the exercise instructions](calendar-identity-feedback/TASK.md) to compare a moved recurrence exception and an ambiguous duplicate identity without using private calendars. [Expected answers](calendar-identity-feedback/ANSWERS.md) are separate so you can inspect the results first. An optional [fictional exercise issue template](.github/ISSUE_TEMPLATE/fictional-exercise.md) helps describe setup problems; GitHub issues are public and require an account.

## Duplicate exports

[Duplicate-export guidance](calendar-identity-feedback/DUPLICATE-EXPORT-NOTE.md) explains why revision metadata does not resolve ambiguous identities and how to investigate without modifying the export. The guide is included in the complete ZIP above.

## Equal-count snapshots

[Compare fictional snapshots with equal event totals](examples/equal-count/README.md) to see why equal counts can hide an identity change and how to interpret the result. The complete ZIP above includes both fictional inputs and the guide.

## Regular-file inputs

Compare two individual ICS files, not collection directories. For a calendar stored as item files, select the corresponding item file from each snapshot. Filenames are not identity: renaming an otherwise identical item still reports shared identity. A single item containing a master event and one recurrence exception reports two explicit identities. This tool does not traverse directories, match item files across a collection or compare a whole collection automatically. Do not concatenate item files as a workaround; multiple VCALENDAR containers are unsupported.

To check this boundary after setup, save [file_layout_probe.py](examples/file-layout/file_layout_probe.py) locally and run `"/absolute/path/calendar-identity/.venv/bin/python" /absolute/path/file_layout_probe.py /absolute/path/calendar-identity`. It creates and removes temporary fictional calendars, checks renamed items and a master/exception item, and verifies directory rejection. It prints JSON and exits nonzero on a mismatch or changed input/engine bytes. Tested on Linux/Python 3.12.15; no Vdirsyncer execution or provider interoperability test is implied. This probe is included in the pinned source ZIP.

Linux/Python 3.12 is the tested platform. Inputs must resolve to regular files; symlinks to regular files remain supported. FIFOs and directories are rejected. Platforms without os.O_NONBLOCK are unsupported and return the usual input error. Windows and other Unix systems have not been tested. This guard prevents the observed no-writer FIFO open hang; it does not impose a deadline on regular-file reads or guarantee arbitrary device/network-filesystem behavior.

## Fictional CLI preview

[Download the self-contained HTML preview](https://raw.githubusercontent.com/Dexter-Ou/calendar-identity/main/docs/CLI-PREVIEW.html), save it as `CLI-PREVIEW.html`, and open it locally in a browser. It shows a styled rendering of actual CLI output from the bundled fictional before/after calendars on Linux/Python 3.12; it is not an interactive terminal. The preview needs no external page resources. It is also included as `docs/CLI-PREVIEW.html` in the pinned source ZIP above. For field meanings and the error path, see the [report guide](calendar-identity-feedback/REPORT-GUIDE.md).

## Migration review checklist

[Use the calendar export comparison checklist](docs/MIGRATION-CHECKLIST.md) to investigate export scope, identity differences, sequence regressions and ambiguous duplicates before a separate provider import test. The checklist is included in the pinned source ZIP above.

## Repeated exports with the same UID

[Review repeated exports and changed meeting times](docs/UPDATE-REVIEW.md) to see why identical comparison metrics do not establish unchanged content or a successful import update. The guide includes a separately downloadable four-case fictional probe; the probe and guide are included in the pinned ZIP above.

## Content-change warning

The pinned download includes `changed_event_representations`: before/after position pairs for shared identities whose parsed VEVENT serialization differs. It includes event properties, revision metadata and nested components such as alarms. A moved DTSTART with unchanged UID and SEQUENCE therefore produces a warning. No titles, UIDs, property values or fingerprints are included. Existing identity and sequence fields retain their meanings.

This is a conservative representation check, not a semantic diff. Property ordering normalized by the parser may compare equal; metadata-only changes may warn. An empty warning list does not establish unchanged source bytes or meaning. External VTIMEZONE definitions remain outside the check. Do not infer importer behavior or safety from either result. This warning is included in the pinned ZIP above. After setup, run the CLI or `.venv/bin/python -m unittest -v` to exercise the automated synthetic cases.
