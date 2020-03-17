from datetime import datetime, timedelta


class ActivityCollisionException(Exception):
    ...


class Event():
    def __init__(self, name, start, end):
        self.name = name
        self.start = min(start, end)
        self.end = max(start, end)
        self.activities = []

    @property
    def days_count(self):
        d = self.end - self.start
        d = d.days + 1
        return d

    def add_activity(self, activity):
        """Adds activity to the activities of the events
        and checks some collision with existing activities"""
        if (activity.start < self.start) or (activity.end > self.end):
            raise ActivityCollisionException(
                "Activity cannot start before event start or end",
                "after event end."
            )
        self.activities.append(activity)

    def get_date(self, ord):
        """Returns date of desired day of the event"""
        if 0 <= ord < self.days_count:
            return self.start + timedelta(days=ord)
        else:
            raise IndexError()

    def get_day_activities(self, ord):
        """Returns activities of desired day of the event"""
        ...


class Activity():
    def __init__(self, name, location, start, end, event=None):
        self.name = name
        self.location = location
        self.start = start
        self.end = end
        self.event = event
