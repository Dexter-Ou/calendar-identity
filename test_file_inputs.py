import json, os, pathlib, subprocess, sys, tempfile, unittest
from unittest import mock
import calendar_identity as engine

class FileInputs(unittest.TestCase):
    def test_unsupported_nonblocking_fails_cleanly(self):
        with mock.patch.object(engine.os, 'O_NONBLOCK', create=True):
            del engine.os.O_NONBLOCK
            with self.assertRaises(OSError):
                engine.read_bounded('unused')

    @unittest.skipUnless(hasattr(os, 'mkfifo') and hasattr(os, 'O_NONBLOCK'), 'Unix FIFO needed')
    def test_fifo_rejected_in_both_positions(self):
        with tempfile.TemporaryDirectory() as folder:
            base = pathlib.Path(folder)
            valid = base / 'valid.ics'
            valid.write_bytes(b'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nEND:VCALENDAR\r\n')
            fifo = base / 'no-writer.ics'
            os.mkfifo(fifo)
            for before, after in [(fifo, valid), (valid, fifo)]:
                with self.subTest(before=str(before)):
                    result = subprocess.run([sys.executable, str(pathlib.Path(engine.__file__)), str(before), str(after)], capture_output=True, text=True, timeout=2)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, '')
                    self.assertEqual(json.loads(result.stderr), {'error': 'Could not read input file'})
if __name__ == '__main__':
    unittest.main()
