from datetime import datetime
from eventplanner_csv import *

if __name__ == "__main__":
    org_staff = import_staff("test_data/staff.csv")
    locs = import_locations("test_data/locations.csv")
    evs = import_events("test_data/events.csv")

    activities = import_activities(
        "test_data/activities.csv",
        staff=org_staff,
        locations=locs,
        events=evs
    )

    print(activities)
