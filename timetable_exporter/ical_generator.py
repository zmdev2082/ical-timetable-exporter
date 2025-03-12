import json
from datetime import datetime, timedelta
from icalendar import Calendar, Event
import uuid

class IcalGenerator:
    REQUIRED_FIELDS = ['summary', 'location']
    ics_mapping = {
        'summary': 'summary',
        'location': 'location',
        'description': 'description', 
        'time_start': 'dtstart',
        'duration': 'duration',
        'start': 'dtstart',
        'end': 'dtend',
        'attendees': 'attendee',
        'categories': 'categories'
    }
    def __init__(self, file_name, config_file, timezone='Australia/Sydney'):
        # Ensure the file name ends with .ics
        if not file_name.endswith('.ics'):
            raise ValueError("Output file must have a .ics extension")
        
        self.file_name = file_name
        with open(config_file, 'r') as f:
            config = json.load(f)
            self.columns = config["columns"]
            self.additional_parsing = config["additional_parsing"]

        # Check if all required fields are present in the config
        for field in self.REQUIRED_FIELDS:
            if field not in self.columns:
                raise ValueError(f"Missing required field in config: {field}")

        # check if start and end or date_start, time_start and duration are present
        if not (('start' in self.columns and 'end' in self.columns) or
                ('date_start' in self.columns and 'time_start' in self.columns and 'duration' in self.columns)):
            raise ValueError("Event time fields need to be configured as: (start & end) or (date_start & time_start & (date_end & time_end | duration)")
        self.timezone  = timezone

    def add_event_property(self, event, key, value, entry):

        if key in self.additional_parsing:
            parse = self.additional_parsing[key]
            value = getattr(value,parse["func"])(*parse["args"], **parse["kwargs"])

        if key in ['start','end']:
            if isinstance(value, str):
                value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                value = self.timezone.localize(value)

        elif key == 'time_start':
            date = entry.get(self.columns['date_' + key.split('_')[1]])
            value = date.replace(hour=value.hour, minute=value.minute, second=value.second)
            value.tz_localize(self.timezone)
        
        elif key == 'duration':
            value = timedelta(hours=value)
        elif key not in self.ics_mapping:
            return



        event.add(self.ics_mapping[key], value)

    def generate_ical(self, timetable_data: list[dict[str, str]]) -> None:
        cal = Calendar()
        cal.add('prodid', '-//TSSAMME//timetable-exporter//EN')
        cal.add('version', '2.0')

        for entry in timetable_data:
            event = Event()
            event.add('UID', str(uuid.uuid4()))  # Add a unique identifier for each event
            event.add('DTSTAMP', datetime.now())
            for key, column in self.columns.items():
                value = entry.get(column)
                self.add_event_property(event, key, value, entry)
            cal.add_component(event)

        with open(self.file_name, 'wb') as f:
            f.write(cal.to_ical())