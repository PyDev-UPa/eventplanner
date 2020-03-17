import unittest
from datetime import datetime
from ep_model import Event, Activity, ActivityCollisionException


class EpModelTests(unittest.TestCase):
    def setUp(self):
        self.e = Event(
            "test",
            datetime.fromisoformat('2020-07-01'),
            datetime.fromisoformat('2020-07-05')
        )

    def test_days_count(self):
        self.assertEqual(self.e.days_count, 5)
        self.assertNotEqual(self.e.days_count, 4)
        self.assertNotEqual(self.e.days_count, 6)

    def test_get_date(self):
        self.assertEqual(
            self.e.get_date(2),
            datetime.fromisoformat('2020-07-03')
        )
        self.assertNotEqual(
            self.e.get_date(2),
            datetime.fromisoformat('2020-07-02')
        )
        self.assertNotEqual(
            self.e.get_date(2),
            datetime.fromisoformat('2020-07-04')
        )

    def test_out_of_event_collision(self):
        test_data = [
            Activity(
                "a1", "l1",
                datetime.fromisoformat('2020-06-30'),
                datetime.fromisoformat('2020-07-02'),
            ),
            Activity(
                "a1", "l1",
                datetime.fromisoformat('2020-07-01'),
                datetime.fromisoformat('2020-07-10'),
            )
        ]

        for t in test_data:
            with self.assertRaises(ActivityCollisionException):
                self.e.add_activity(t)
