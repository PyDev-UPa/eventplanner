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

    def test_get_date_activites(self):
        test_data = [
            Activity(
                "a4", "l1",
                datetime.fromisoformat('2020-07-02T09:40'),
                datetime.fromisoformat('2020-07-02T10:03'),
            ),
            Activity(
                "a1", "l1",
                datetime.fromisoformat('2020-07-02T09:00'),
                datetime.fromisoformat('2020-07-02T09:30'),
            ),
            Activity(
                "a3", "l1",
                datetime.fromisoformat('2020-07-03T09:00'),
                datetime.fromisoformat('2020-07-03T09:30'),
            ),
            Activity(
                "a2", "l1",
                datetime.fromisoformat('2020-07-02T09:30'),
                datetime.fromisoformat('2020-07-02T09:40'),
            ),
            Activity(
                "a5", "l1",
                datetime.fromisoformat('2020-07-03T09:30'),
                datetime.fromisoformat('2020-07-03T10:30'),
            )
        ]

        for t in test_data:
            self.e.add_activity(t)

        da1 = self.e.get_day_activities(0)
        da2 = self.e.get_day_activities(1)
        da3 = self.e.get_day_activities(2)

        self.assertEqual(len(da1), 0)
        self.assertEqual(len(da2), 3)
        self.assertEqual(len(da3), 2)

        self.assertIn(test_data[0], da2)
        self.assertIn(test_data[1], da2)
        self.assertNotIn(test_data[2], da2)
        self.assertIn(test_data[3], da2)

        self.assertEqual(da2[0].name, "a1")
        self.assertEqual(da2[1].name, "a2")
        self.assertEqual(da2[2].name, "a4")
