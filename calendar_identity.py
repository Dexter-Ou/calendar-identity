#!/usr/bin/env python3
"""Read-only, literal VEVENT identity comparison; not an import predictor."""
import argparse
import os
import stat
import datetime
import json
import re
import sys
from pathlib import Path
from icalendar import Calendar

MAX_BYTES = 8 * 1024 * 1024

class InvalidCalendar(ValueError):
    pass

def one(event, name, required=False):
    value = event.get(name)
    if isinstance(value, list) or (required and value is None):
        raise InvalidCalendar('Missing or repeated identity/revision property')
    return value

def inventory(data):
    if len(data) > MAX_BYTES:
        raise InvalidCalendar('Input exceeds 8 MiB limit')
    try:
        data.decode('utf-8-sig')
        cal = Calendar.from_ical(data)
        if cal.name != 'VCALENDAR':
            raise InvalidCalendar('Expected one VCALENDAR')
        for component in cal.walk():
            if component.errors:
                raise InvalidCalendar('Parser reported invalid properties')
        if any(c.name not in ('VEVENT', 'VTIMEZONE') for c in cal.subcomponents):
            raise InvalidCalendar('Only VEVENT and VTIMEZONE components supported')
        top_level_ids = {id(c) for c in cal.subcomponents}
        if any(c.name == 'VEVENT' for c in cal.walk()[1:] if id(c) not in top_level_ids):
            raise InvalidCalendar('Nested VEVENT unsupported')
        result = {}
        for index, event in enumerate((c for c in cal.subcomponents if c.name == 'VEVENT'), 1):
            uid = one(event, 'UID', True)
            if not isinstance(uid, str) or not str(uid).strip():
                raise InvalidCalendar('Empty or invalid UID')
            # UID is case-sensitive TEXT; library decodes text escaping and folds.
            rid = one(event, 'RECURRENCE-ID')
            recurrence = None
            if rid is not None:
                if 'RANGE' in rid.params:
                    raise InvalidCalendar('RECURRENCE-ID RANGE unsupported')
                if set(rid.params) - {'VALUE', 'TZID'}:
                    raise InvalidCalendar('Unsupported recurrence identity parameter')
                value_type = str(rid.params.get('VALUE', 'DATE-TIME')).upper()
                if value_type not in ('DATE', 'DATE-TIME'):
                    raise InvalidCalendar('Unsupported recurrence identity value type')
                value = rid.dt
                if value_type == 'DATE' and (not isinstance(value, datetime.date) or isinstance(value, datetime.datetime)):
                    raise InvalidCalendar('Invalid DATE recurrence identity')
                if value_type == 'DATE-TIME' and not isinstance(value, datetime.datetime):
                    raise InvalidCalendar('Invalid DATE-TIME recurrence identity')
                tzid = str(rid.params.get('TZID', ''))
                if tzid and (value_type == 'DATE' or rid.to_ical().endswith(b'Z')):
                    raise InvalidCalendar('Invalid TZID recurrence identity')
                recurrence = (value_type, tzid, rid.to_ical().decode('ascii'))
            sequence = one(event, 'SEQUENCE')
            if sequence is None:
                revision = 0
            else:
                raw = sequence.to_ical().decode('ascii')
                if not re.fullmatch(r'\d+', raw) or int(raw) > 2147483647:
                    raise InvalidCalendar('Invalid SEQUENCE')
                revision = int(raw)
            key = (str(uid), recurrence)
            if key in result:
                raise InvalidCalendar('Duplicate UID/recurrence identity; comparison is ambiguous')
            # Keep parsed serialization private; reports expose positions only.
            # This is deliberately a representation check, not semantic equality.
            result[key] = (index, revision, event.to_ical())
        return result
    except InvalidCalendar:
        raise
    except Exception:
        # Library errors may include calendar contents. Never echo them.
        raise InvalidCalendar('Calendar could not be parsed within supported scope') from None

def compare(before, after):
    a, b = inventory(before), inventory(after)
    shared = a.keys() & b.keys()
    return {
        'format': 'calendar-identity-preview-1',
        'comparison': 'literal UID and typed recurrence representation; no timezone equivalence or recurrence expansion',
        'before_events': len(a), 'after_events': len(b),
        'added_event_positions': sorted(b[k][0] for k in b.keys() - a.keys()),
        'removed_event_positions': sorted(a[k][0] for k in a.keys() - b.keys()),
        'shared_identities': len(shared),
        'sequence_regressions': sorted([
            {'before_position': a[k][0], 'after_position': b[k][0],
             'before_sequence': a[k][1], 'after_sequence': b[k][1]}
            for k in shared if b[k][1] < a[k][1]
        ], key=lambda row: row['before_position']),
        'changed_event_representations': sorted([
            {'before_position': a[k][0], 'after_position': b[k][0]}
            for k in shared if a[k][2] != b[k][2]
        ], key=lambda row: row['before_position']),
        'limitations': ['Shared identity does not mean unchanged event content.',
                        'Changed event representations compare parsed VEVENT serialization, including revision metadata and nested components; not semantic equivalence.',
                        'No warning does not prove unchanged source bytes or content; parser normalization and external VTIMEZONE definitions are outside this check.',
                        'Representation changes can appear as removal plus addition.',
                        'No prediction of import, merge, notification or provider behavior.',
                        'Counts cover explicit VEVENT records only, not expanded occurrences.']
    }

def read_bounded(path):
    if not hasattr(os, 'O_NONBLOCK'):
        raise OSError('Nonblocking regular-file reads unsupported')
    fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise OSError('Input must be a regular file')
        with os.fdopen(fd, 'rb', closefd=False) as stream:
            return stream.read(MAX_BYTES + 1)
    finally:
        os.close(fd)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exit-code', action='store_true',
                        help='exit 1 for reported export differences, 0 for none; errors exit 2')
    parser.add_argument('before')
    parser.add_argument('after')
    args = parser.parse_args()
    try:
        report = compare(read_bounded(args.before), read_bounded(args.after))
    except (OSError, InvalidCalendar) as error:
        message = str(error) if isinstance(error, InvalidCalendar) else 'Could not read input file'
        print(json.dumps({'error': message}), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    if args.exit_code and any(report[field] for field in (
            'added_event_positions', 'removed_event_positions',
            'sequence_regressions', 'changed_event_representations')):
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
