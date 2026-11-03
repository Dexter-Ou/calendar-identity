"""Synthetic CLI output checks; finite fixtures, not a security audit.

Run with: python -m unittest -v test_cli_privacy
Only stdout/stderr and input bytes are checked. Filenames, argument errors,
process metadata, memory and other parser behavior are outside this test.
"""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


SENTINELS = (
    'FICTIONAL_UID_PRIVACY',
    'FICTIONAL_TITLE_PRIVACY',
    'FICTIONAL_DESCRIPTION_PRIVACY',
    'fictional_attendee_privacy@example.invalid',
    'FICTIONAL_RECURRENCE_PRIVACY',
)


def fixtures():
    def wrap(body):
        return ('BEGIN:VCALENDAR\r\nVERSION:2.0\r\n'
                'PRODID:-//Fictional privacy regression//EN\r\n'
                + body + 'END:VCALENDAR\r\n').encode('utf-8')

    event = ('BEGIN:VEVENT\r\nUID:' + SENTINELS[0]
             + '\r\nSUMMARY:' + SENTINELS[1]
             + '\r\nDESCRIPTION:' + SENTINELS[2]
             + '\r\nATTENDEE:mailto:' + SENTINELS[3]
             + '\r\nSEQUENCE:2\r\nEND:VEVENT\r\n')
    return {
        'valid': wrap(event),
        'changed': wrap(event.replace('SEQUENCE:2', 'SEQUENCE:1')),
        'duplicate': wrap(event + event),
        'missing_uid': wrap(event.replace('UID:' + SENTINELS[0] + '\r\n', '')),
        'bad_sequence': wrap(event.replace('SEQUENCE:2', 'SEQUENCE:' + SENTINELS[2])),
        'bad_recurrence': wrap(event.replace('SEQUENCE:2', 'RECURRENCE-ID:' + SENTINELS[4])),
        'unclosed': wrap(event).replace(b'END:VEVENT\r\n', b''),
        'bad_utf8': wrap(event) + b'\xff',
        'unsupported_component': wrap(event + 'BEGIN:VTODO\r\nUID:' + SENTINELS[0] + '\r\nEND:VTODO\r\n'),
    }


class CLIPrivacyTests(unittest.TestCase):
    def test_fictional_content_suppressed_and_inputs_unchanged(self):
        data = fixtures()
        cases = [('accepted_same', 'valid', 'valid', 0),
                 ('accepted_regression', 'valid', 'changed', 0)]
        for name in data:
            if name not in ('valid', 'changed'):
                cases.extend([(name + '_before', name, 'valid', 2),
                              (name + '_after', 'valid', name, 2)])
        self.assertEqual(len(cases), 16)
        engine = pathlib.Path(__file__).resolve().with_name('calendar_identity.py')
        with tempfile.TemporaryDirectory() as folder:
            base = pathlib.Path(folder)
            for name, content in data.items():
                (base / (name + '.ics')).write_bytes(content)
            for name, before, after, expected in cases:
                with self.subTest(case=name):
                    result = subprocess.run(
                        [sys.executable, str(engine), str(base / (before + '.ics')),
                         str(base / (after + '.ics'))],
                        capture_output=True, text=True, timeout=10, cwd=base)
                    self.assertEqual(result.returncode, expected)
                    for sentinel in SENTINELS:
                        self.assertNotIn(sentinel, result.stdout + result.stderr)
                    if expected == 0:
                        self.assertEqual(result.stderr, '')
                        report = json.loads(result.stdout)
                        self.assertEqual(report['shared_identities'], 1)
                        expected_regressions = [] if name == 'accepted_same' else [{
                            'before_position': 1, 'after_position': 1,
                            'before_sequence': 2, 'after_sequence': 1}]
                        self.assertEqual(report['sequence_regressions'], expected_regressions)
                    else:
                        self.assertEqual(result.stdout, '')
                        error = json.loads(result.stderr)
                        self.assertEqual(set(error), {'error'})
                        self.assertIsInstance(error['error'], str)
                        self.assertTrue(error['error'])
                    for fixture, content in data.items():
                        self.assertEqual((base / (fixture + '.ics')).read_bytes(), content)


if __name__ == '__main__':
    unittest.main()
