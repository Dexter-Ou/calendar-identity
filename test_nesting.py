"""Synthetic regression tests for component object identity and nesting."""
import unittest
from icalendar import Calendar
from calendar_identity import compare, InvalidCalendar

EVENT = ('BEGIN:VEVENT\r\nUID:fictional@example.invalid\r\n'
         'DTSTAMP:20260101T000000Z\r\nDTSTART:20260102T090000Z\r\nEND:VEVENT\r\n')

def calendar(contents):
    return ('BEGIN:VCALENDAR\r\nVERSION:2.0\r\n'
            'PRODID:-//Fictional nesting tests//EN\r\n' + contents + 'END:VCALENDAR\r\n').encode()

def parent(child):
    return ('BEGIN:VEVENT\r\nUID:parent@example.invalid\r\n'
            'DTSTAMP:20260101T000000Z\r\nDTSTART:20260103T090000Z\r\n' + child + 'END:VEVENT\r\n')

class NestingTests(unittest.TestCase):
    def test_direct_events_supported(self):
        data = calendar(EVENT)
        self.assertEqual(compare(data, data)['shared_identities'], 1)

    def reject_both_positions(self, data):
        control = calendar(EVENT)
        for before, after in [(data, control), (control, data)]:
            with self.subTest(before_is_nested=before == data):
                with self.assertRaisesRegex(InvalidCalendar, '^Nested VEVENT unsupported$'):
                    compare(before, after)

    def test_nested_only_rejected(self):
        self.reject_both_positions(calendar(parent(EVENT)))

    def test_distinct_nested_event_rejected(self):
        self.reject_both_positions(calendar(EVENT + parent(EVENT.replace('fictional@', 'other@'))))

    def test_structurally_equal_nested_event_rejected(self):
        data = calendar(EVENT + parent(EVENT))
        parsed = Calendar.from_ical(data)
        direct, nested = parsed.subcomponents[0], parsed.subcomponents[1].subcomponents[0]
        self.assertEqual(direct, nested)
        self.assertIsNot(direct, nested)
        self.reject_both_positions(data)

if __name__ == '__main__':
    unittest.main()
