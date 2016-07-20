"""A module for creating greeting strings based on a user's timezone
offset and user's level."""
from datetime import datetime
import time
import calendar


def time_greeting(user):
    def get_part_of_day(user_tz_offset, time_now):
        """Return part of day depending on time_now and the user's timzone
        offset value.

        user_tz_offset - integer of user's time zone offset in hours
        time_now - UTC time in seconds

        From  -  To  => part of day
        ---------------------------
        00:00 - 04:59 => midnight
        05:00 - 06:59 => dawn
        07:00 - 10:59 => morning
        11:00 - 12:59 => noon
        13:00 - 16:59 => afternoon
        17:00 - 18:59 => dusk
        19:00 - 20:59 => evening
        21:00 - 23:59 => night
        """
        user_time = time_now + (user_tz_offset*60*60)
        # gmtime[3] is tm_hour
        user_hour = time.gmtime(user_time)[3]

        if 0 <= user_hour < 5:
            return 'midnight'
        elif 5 <= user_hour < 7:
            return 'dawn'
        elif 7 <= user_hour < 11:
            return 'morning'
        elif 11 <= user_hour < 13:
            return 'noon'
        elif 13 <= user_hour < 17:
            return 'afternoon'
        elif 17 <= user_hour < 19:
            return 'dusk'
        elif 19 <= user_hour < 21:
            return 'evening'
        else:
            return 'night'

    def choose_greeting(username, part_of_day):
        """Return greeting string based on user's level and part of day.

        username - username string
        part_of_day - string from function `get_part_of_day`
        """

        greetings = {
                'dawn': 'Good early morning',
                'morning': 'Good morning',
                'afternoon': 'Good afternoon',
                'dusk': 'Good afternoon',
                'evening': 'Good evening',
                }

        # Use generic 'Hi' when specific greeting is not implemented
        greeting = greetings.get(part_of_day, 'Good day')
        return '%s, %s!' % (greeting, username)

    current_part_of_day = get_part_of_day(1, calendar.timegm(time.gmtime()))
    return choose_greeting(user.username, current_part_of_day)