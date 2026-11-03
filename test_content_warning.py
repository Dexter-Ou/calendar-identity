"""Fictional representation-warning regression tests; no provider import tests."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from calendar_identity import compare
from test_calendar_identity import cal, event

class ContentWarningTests(unittest.TestCase):
    def assert_warning(self, before, after, expected):
        r = compare(before, after)
        self.assertEqual(r['changed_event_representations'], expected)
        self.assertEqual(r['shared_identities'], 1)
        self.assertEqual(r['added_event_positions'], [])
        self.assertEqual(r['removed_event_positions'], [])
        self.assertEqual(r['sequence_regressions'], [])
        return r

    def test_identical_and_changed_time_same_sequence(self):
        before = cal(event())
        self.assert_warning(before, before, [])
        after = before.replace(b'DTSTART:20261104T120000Z', b'DTSTART:20261104T140000Z')
        self.assert_warning(before, after, [{'before_position': 1, 'after_position': 1}])

    def test_metadata_only_change_warns(self):
        self.assert_warning(cal(event()), cal(event(sequence=1)), [{'before_position':1,'after_position':1}])

    def test_normalized_property_order_and_line_folding(self):
        before = cal(event(extra='SUMMARY:Fictional meeting\r\n'))
        after = before.replace(b'SUMMARY:Fictional meeting\r\n',b'').replace(b'UID:',b'SUMMARY:Fictional\r\n  meeting\r\nUID:')
        self.assertNotEqual(before, after)
        self.assert_warning(before, after, [])

    def test_nested_alarm_change_warns(self):
        before = cal(event(extra='BEGIN:VALARM\r\nACTION:DISPLAY\r\nTRIGGER:-PT5M\r\nDESCRIPTION:Fictional\r\nEND:VALARM\r\n'))
        self.assert_warning(before,before.replace(b'-PT5M',b'-PT10M'),[{'before_position':1,'after_position':1}])

    def test_reordered_events_use_correct_positions(self):
        r=compare(cal(event('a'),event('b')),cal(event('b',extra='SUMMARY:Changed\r\n'),event('a')))
        self.assertEqual(r['changed_event_representations'],[{'before_position':2,'after_position':1}])
        self.assertEqual(r['shared_identities'],2)

    def test_calendar_metadata_outside_warning(self):
        before=cal(event())
        after=before.replace(b'VERSION:2.0',b'VERSION:2.0\r\nX-WR-CALNAME:Fictional')
        self.assert_warning(before,after,[])

    def test_cli_privacy_and_input_preservation(self):
        before=cal(event('fictional-private-uid',extra='SUMMARY:fictional-private-title\r\nDESCRIPTION:fictional-private-description\r\nATTENDEE:mailto:fictional-private@example.invalid\r\n'))
        after=before.replace(b'120000Z',b'140000Z')
        with tempfile.TemporaryDirectory() as td:
            a=pathlib.Path(td)/'a.ics';b=pathlib.Path(td)/'b.ics'
            a.write_bytes(before);b.write_bytes(after)
            p=subprocess.run([sys.executable,'calendar_identity.py',str(a),str(b)],capture_output=True,text=True)
            self.assertEqual(p.returncode,0)
            self.assertNotIn('fictional-private',p.stdout+p.stderr)
            self.assertEqual(json.loads(p.stdout)['changed_event_representations'],[{'before_position':1,'after_position':1}])
            self.assertEqual(a.read_bytes(),before);self.assertEqual(b.read_bytes(),after)

if __name__=='__main__': unittest.main()
