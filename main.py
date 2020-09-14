from datetime import date, timedelta
from dateutil import relativedelta
from ics import Calendar, Event, alarm


YEARS = 20


def make_calendar_event(dates_in_isoformat):
  c = Calendar()
  for d in dates_in_isoformat:
    e = Event()
    e.name = 'Friday the 13th'
    e.begin = d
    e.make_all_day()
    notification = alarm.DisplayAlarm(timedelta(seconds=-60*60*12))
    e.alarms.append(notification)
    c.events.add(e)

  fname = 'f13.ics'
  with open(fname, 'w') as my_file:
    my_file.writelines(c)
  print(f'Wrote to: {fname}')


def is_friday_the_13th(d):
  # date.weekday == 4 when day is Friday
  return d.weekday() == 4 and d.day == 13


def iterate_dates(num_years, verbose=False):
  """Checks num_years from the closest 13th."""
  found_dates = []
  today = date.today()
  if today.day > 13:
    today = today + relativedelta.relativedelta(months=1)
  first_day = today.replace(day=13)
  for y in range(num_years):
    for m in range(12):
      candidate = first_day + relativedelta.relativedelta(months=m, years=y)
      found = is_friday_the_13th(candidate)
      if found:
        found_dates.append(candidate.isoformat())
        if verbose:
          print(candidate)
  print(f'After searching over {num_years}, found {len(found_dates)} F13\'s')
  return found_dates

found_dates = iterate_dates(YEARS)
make_calendar_event(found_dates)
