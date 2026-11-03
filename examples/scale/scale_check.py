#!/usr/bin/env python3
"""Check an installed Calendar Identity CLI using disposable fictional inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time


def calendar(regression):
    rows = ['BEGIN:VCALENDAR', 'VERSION:2.0',
            'PRODID:-//Calendar Identity Fictional Scale Check//EN']
    for position in range(1, 5001):
        rows.extend(['BEGIN:VEVENT',
                     f'UID:fictional-scale-{position}@example.invalid',
                     'DTSTAMP:20261103T000000Z', 'DTSTART:20261104T120000Z',
                     f'SEQUENCE:{6 if regression and position == 5000 else 7}',
                     'END:VEVENT'])
    return ('\r\n'.join(rows + ['END:VCALENDAR']) + '\r\n').encode('utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cli', help='Path to the installed calendar-identity executable')
    args = parser.parse_args()
    cli = Path(args.cli).expanduser().resolve()
    if not cli.is_file():
        parser.error('CLI executable does not exist')
    try:
        with tempfile.TemporaryDirectory(prefix='calendar-identity-scale-') as folder:
            root = Path(folder)
            before, after = root / 'before.ics', root / 'after.ics'
            before.write_bytes(calendar(False))
            after.write_bytes(calendar(True))
            hashes = [digest(before), digest(after)]
            started = time.monotonic()
            result = subprocess.run([str(cli), str(before), str(after)],
                                    capture_output=True, text=True, timeout=30)
            elapsed = time.monotonic() - started
            report = json.loads(result.stdout)
            if not isinstance(report, dict):
                raise ValueError('Expected JSON object')
            checks = {
                'exit0': result.returncode == 0,
                'empty_stderr': result.stderr == '',
                'under_30_seconds': elapsed < 30,
                'exact_counts': [report.get(k) for k in
                                 ('before_events', 'after_events', 'shared_identities')]
                                == [5000, 5000, 5000],
                'no_additions': report.get('added_event_positions') == [],
                'no_removals': report.get('removed_event_positions') == [],
                'final_regression': report.get('sequence_regressions') == [
                    {'before_position': 5000, 'after_position': 5000,
                     'before_sequence': 7, 'after_sequence': 6}],
                'final_change': report.get('changed_event_representations') == [
                    {'before_position': 5000, 'after_position': 5000}],
                'inputs_unchanged': [digest(before), digest(after)] == hashes,
                'no_fixture_uids_in_output': 'fictional-scale-' not in
                                            result.stdout + result.stderr,
            }
            print(json.dumps({'synthetic_only': True, 'events_per_file': 5000,
                              'elapsed_seconds': elapsed, 'timeout_seconds': 30,
                              'checks': checks, 'passed': all(checks.values())}, indent=2))
            return 0 if all(checks.values()) else 1
    except subprocess.TimeoutExpired:
        print('Scale check failed: CLI exceeded the 30-second timeout.', file=__import__('sys').stderr)
    except (OSError, ValueError):
        print('Scale check failed: CLI execution or JSON report was invalid.', file=__import__('sys').stderr)
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
