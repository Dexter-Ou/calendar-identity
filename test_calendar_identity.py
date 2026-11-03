import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from calendar_identity import compare, inventory, InvalidCalendar, MAX_BYTES

def event(uid='example', extra='', sequence=0):
    return f'BEGIN:VEVENT\r\nUID:{uid}\r\nDTSTAMP:20261103T000000Z\r\nDTSTART:20261104T120000Z\r\nSEQUENCE:{sequence}\r\n{extra}END:VEVENT\r\n'

def cal(*events):
    return ('BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Synthetic Test//EN\r\n'+''.join(events)+'END:VCALENDAR\r\n').encode()

class IdentityTests(unittest.TestCase):
    def test_core_journey(self):
        before = cal(event('series',sequence=4),event('series','RECURRENCE-ID:20261105T120000Z\r\n',3),event('removed'))
        after = cal(event('added'),event('series','RECURRENCE-ID:20261105T120000Z\r\nSUMMARY:Moved meeting\r\n',2).replace('DTSTART:20261104T120000Z','DTSTART:20261106T140000Z'),event('series',sequence=5))
        r=compare(before,after)
        self.assertEqual((r['before_events'],r['after_events'],r['shared_identities']),(3,3,2))
        self.assertEqual(r['added_event_positions'],[1]);self.assertEqual(r['removed_event_positions'],[3])
        self.assertEqual(r['sequence_regressions'],[{'before_position':2,'after_position':2,'before_sequence':3,'after_sequence':2}])
    def test_duplicate_rejected_across_sequence(self):
        with self.assertRaises(InvalidCalendar): inventory(cal(event(sequence=1),event(sequence=2)))
    def test_identity_not_summary_or_start(self):
        r=compare(cal(event('old','SUMMARY:Same title\r\n')),cal(event('new','SUMMARY:Same title\r\n')))
        self.assertEqual(r['shared_identities'],0)
    def test_uid_case_and_folding(self):
        self.assertEqual(compare(cal(event('ab\r\n cd')),cal(event('abcd')))['shared_identities'],1)
        self.assertEqual(compare(cal(event('a')),cal(event('A')))['shared_identities'],0)
    def test_recurrence_types_timezone_literal(self):
        for a,b in [('RECURRENCE-ID;VALUE=DATE:20261105','RECURRENCE-ID:20261105T000000Z'),('RECURRENCE-ID;TZID=Europe/London:20261105T120000','RECURRENCE-ID:20261105T120000Z')]:
            with self.subTest(a=a): self.assertEqual(compare(cal(event(extra=a+'\r\n')),cal(event(extra=b+'\r\n')))['shared_identities'],0)
    def test_default_sequence_and_empty(self):
        self.assertEqual(len(inventory(cal())),0)
        self.assertEqual(compare(cal(event().replace('SEQUENCE:0\r\n','')),cal(event()))['sequence_regressions'],[])
    def test_invalid_inputs(self):
        bad=[b'not an ICS',cal(event().replace('UID:example\r\n','')),cal(event(extra='UID:twice\r\n')),cal(event(sequence=-1)),cal(event(extra='RECURRENCE-ID:not-date\r\n')),cal(event(extra='RECURRENCE-ID;RANGE=THISANDFUTURE:20261105T120000Z\r\n')),b'x'*(MAX_BYTES+1),cal(event()).replace(b'END:VCALENDAR',b''),cal(event()).replace(b'VEVENT',b'VTODO')]
        for data in bad:
            with self.subTest(data=data[:50]),self.assertRaises(InvalidCalendar): inventory(data)
    def test_documented_parser_tolerance(self):
        for data in [cal(event().replace('DTSTART:20261104T120000Z\r\n','')),
                     cal(event()).replace(b'VERSION:2.0\r\n',b''),
                     cal(event(extra='RECURRENCE-ID;TZID=Unknown/Zone:20261105T120000\r\n')),
                     cal(event(sequence='+1'))]:
            with self.subTest(data=data[:60]): self.assertEqual(len(inventory(data)),1)
        for data in [cal(event('a'))+cal(event('b')),cal(event())+b'trailing text\r\n']:
            with self.subTest(data=data[:60]),self.assertRaises(InvalidCalendar): inventory(data)

    def test_cli_privacy_and_input_integrity(self):
        with tempfile.TemporaryDirectory() as td:
            a=pathlib.Path(td)/'a.ics';b=pathlib.Path(td)/'b.ics'
            data=cal(event('private-uid','DESCRIPTION:private-description\r\n'))
            a.write_bytes(data);b.write_bytes(data)
            r=subprocess.run([sys.executable,'calendar_identity.py',str(a),str(b)],capture_output=True,text=True)
            self.assertEqual(r.returncode,0); self.assertEqual(json.loads(r.stdout)['shared_identities'],1)
            self.assertNotIn('private-',r.stdout+r.stderr);self.assertEqual(a.read_bytes(),data);self.assertEqual(b.read_bytes(),data)
            b.write_bytes(b'broken private-content')
            r=subprocess.run([sys.executable,'calendar_identity.py',str(a),str(b)],capture_output=True,text=True)
            self.assertEqual(r.returncode,2);self.assertEqual(r.stdout,'');self.assertNotIn('private-',r.stderr)

if __name__=='__main__': unittest.main()
