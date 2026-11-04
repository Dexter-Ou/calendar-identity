"""Subprocess contract tests using fictional calendars only."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from test_calendar_identity import cal, event

class ExitCodeTests(unittest.TestCase):
    def test_status_matrix_and_integrity(self):
        base=cal(event('fictional', 'SUMMARY:Private fictional title\r\n', 3))
        cases=[('same',base,base,0),
               ('addition',base,cal(event('fictional','SUMMARY:Private fictional title\r\n',3),event('added')),1),
               ('removal',base,cal(),1),
               ('content',base,base.replace(b'Private fictional title',b'Changed fictional title'),1),
               ('sequence_down',base,base.replace(b'SEQUENCE:3',b'SEQUENCE:2'),1),
               ('sequence_up',base,base.replace(b'SEQUENCE:3',b'SEQUENCE:4'),1),
               ('empty',cal(),cal(),0),
               ('order',cal(event('a'),event('b')),cal(event('b'),event('a')),0)]
        with tempfile.TemporaryDirectory() as td:
            a=pathlib.Path(td)/'before.ics';b=pathlib.Path(td)/'after.ics'
            for name,before,after,expected in cases:
                with self.subTest(name=name):
                    a.write_bytes(before);b.write_bytes(after)
                    command=[sys.executable,'calendar_identity.py',str(a),str(b)]
                    plain=subprocess.run(command,capture_output=True,text=True)
                    flagged=subprocess.run(command+['--exit-code'],capture_output=True,text=True)
                    self.assertEqual(plain.returncode,0)
                    self.assertEqual(flagged.returncode,expected)
                    self.assertEqual(plain.stdout,flagged.stdout)
                    self.assertEqual(flagged.stderr,'')
                    json.loads(flagged.stdout)
                    self.assertNotIn('Private fictional title',flagged.stdout)
                    self.assertNotIn('fictional',flagged.stdout)
                    self.assertEqual(a.read_bytes(),before);self.assertEqual(b.read_bytes(),after)
            for data in [b'broken fictional private input',None]:
                if data is None:b.unlink()
                else:b.write_bytes(data)
                r=subprocess.run(command+['--exit-code'],capture_output=True,text=True)
                self.assertEqual(r.returncode,2);self.assertEqual(r.stdout,'')
                self.assertNotIn('fictional',r.stderr)
            r=subprocess.run([sys.executable,'calendar_identity.py','--exit-code'],capture_output=True,text=True)
            self.assertEqual(r.returncode,2)
