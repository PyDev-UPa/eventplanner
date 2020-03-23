"""Eventplanner csv importer - just a helper module for separation of import
logic from other logic"""

import csv
import ep_model as epm
from datetime import datetime
from pathlib import Path


def import_staff(file, context):
    with open(file) as f:
        reader = csv.reader(f)
        for r in reader:
            p = epm.Person(r[0])
            context.add_person(p)


def import_locations(file, context):
    with open(file) as f:
        reader = csv.reader(f)
        for r in reader:
            loc = epm.Location(r[0], "")
            context.add_location(loc)


def import_events(file, context):
    with open(file) as f:
        reader = csv.reader(f)
        for r in reader:
            event_name = r[0]
            event_start = datetime.strptime(r[1], "%d.%m.%Y %H:%M")
            event_end = datetime.strptime(r[2], "%d.%m.%Y %H:%M")

            event = epm.Event(event_name, event_start, event_end)
            context.add_event(event)


def import_activities(file, context):
    with open(file) as f:
        reader = csv.reader(f)
        for r in reader:
            act_event = r[0]
            assert act_event in context.events.keys(), \
                "{} not in defined events".format(act_event)
            act_event = context.events[act_event]

            act_name = r[1]

            act_start = datetime.strptime(r[3], "%d.%m.%Y %H:%M")
            act_end = datetime.strptime(r[4], "%d.%m.%Y %H:%M")

            act_loc = r[5]
            assert act_loc in context.locations.keys(), \
                "{} not in defined events".format(act_loc)
            act_loc = context.locations[act_loc]

            new_activity = epm.Activity(
                act_name, act_loc, act_start, act_end
            )

            act_staff = r[2].split("|")
            for s in act_staff:
                assert s in context.staff.keys(), \
                    "{} not in defined staff".format(s)
                person = context.staff[s]
                new_activity.add_person(person)

            act_event.add_activity(new_activity)


def import_default_files(folder, context):
    directory = Path(folder)
    files = [
        ("staff.csv", import_staff),
        ("locations.csv", import_locations),
        ("events.csv", import_events),
        ("activities.csv", import_activities)
    ]

    for f in files:
        data_file = directory / f[0]
        f[1](data_file, context)


if __name__ == "__main__":
    context = epm.EPContext()
    import_default_files("test_data", context)
    ...
