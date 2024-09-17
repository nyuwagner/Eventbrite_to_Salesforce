import EventManager
import pandas as pd

backlog = EventManager.EventList("2024-06-01T00:00:00Z")

# Make CSV to assess Damages
events = backlog.get_events_after()
print(events.head())
events.to_csv('events.csv')

attendees = backlog.get_attenddess_after()
print(attendees.head())
attendees.to_csv('attendees.csv')