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

        activity.event = self
        self.activities.append(activity)

    def get_date(self, ord):
        """Returns date of desired day of the event"""
        if 0 <= ord < self.days_count:
            return self.start + timedelta(days=ord)
        else:
            raise IndexError()

    def get_day_activities(self, ord):
        """Returns sorted activities of desired day of the event"""
        da = [a for a in self.activities
              if a.start.date() == self.get_date(ord).date()]
        da.sort(key=lambda x: x.start)
        return da


class Activity():
    def __init__(self, name, location, start, end, event=None):
        self.name = name
        self.location = location
        self.start = start
        self.end = end
        self.event = event
        self.staff = []

    def add_person(self, person):
        if person not in self.staff:
            self.staff.append(person)
            person.add_activity(self)


class Location():
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Person():
    def __init__(self, name):
        self.name = name
        self.activities = []

    def add_activity(self, activity):
        if activity not in self.activities:
            self.activities.append(activity)


class EPContext():
    def __init__(self):
        self.events = {}
        self.locations = {}
        self.staff = {}

    def add_event(self, event):
        if event.name not in self.events.keys():
            self.events[event.name] = event
        else:
            existing = self.events[event.name]
            existing.start = event.start
            existing.end = event.end

    def add_location(self, loc):
        if loc.name not in self.locations.keys():
            self.locations[loc.name] = loc
        else:
            self.locations[loc.name].description = loc.description

    def add_person(self, p):
        if p.name not in self.staff.keys():
            self.staff[p.name] = p


if __name__ == "__main__":
    ...
