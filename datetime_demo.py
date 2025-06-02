#!/usr/bin/env python3
"""
Datetime Module Demonstration
This script demonstrates various features of the datetime module.
"""

import datetime

def main():
    print("===== Datetime Module Demonstration =====\n")
    
    # 1. Current date and time
    now = datetime.datetime.now()
    print(f"1. Current date and time: {now}")
    
    # 2. Current date
    today = datetime.date.today()
    print(f"2. Current date: {today}")
    
    # 3. Creating a specific date
    specific_date = datetime.date(2025, 12, 31)
    print(f"3. Specific date: {specific_date}")
    
    # 4. Creating a specific datetime
    specific_datetime = datetime.datetime(2025, 12, 31, 23, 59, 59)
    print(f"4. Specific datetime: {specific_datetime}")
    
    # 5. Formatting dates
    print(f"5. Formatted date (YYYY-MM-DD): {today.strftime('%Y-%m-%d')}")
    print(f"   Formatted date (DD/MM/YYYY): {today.strftime('%d/%m/%Y')}")
    print(f"   Formatted date (Month Day, Year): {today.strftime('%B %d, %Y')}")
    
    # 6. Parsing string to datetime
    date_string = "2025-01-15 14:30:00"
    parsed_date = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    print(f"6. Parsed date from string '{date_string}': {parsed_date}")
    
    # 7. Date arithmetic
    tomorrow = today + datetime.timedelta(days=1)
    print(f"7. Tomorrow: {tomorrow}")
    
    next_week = today + datetime.timedelta(weeks=1)
    print(f"   Next week: {next_week}")
    
    two_hours_later = now + datetime.timedelta(hours=2)
    print(f"   Two hours later: {two_hours_later}")
    
    # 8. Difference between dates
    future_date = datetime.date(2026, 1, 1)
    days_until = (future_date - today).days
    print(f"8. Days until January 1, 2026: {days_until}")
    
    # 9. Day of week
    day_of_week = today.strftime("%A")
    print(f"9. Today is a {day_of_week}")
    
    # 10. ISO calendar
    year, week, weekday = today.isocalendar()
    print(f"10. ISO Calendar: Year {year}, Week {week}, Weekday {weekday}")
    
    # 11. Timezone aware datetime (requires tzinfo)
    try:
        from datetime import timezone
        utc_now = datetime.datetime.now(timezone.utc)
        print(f"11. Current UTC time: {utc_now}")
        
        # UTC offset
        offset = datetime.timezone(datetime.timedelta(hours=9))  # JST (Japan Standard Time)
        jst_now = datetime.datetime.now(offset)
        print(f"    Current time in JST (UTC+9): {jst_now}")
    except ImportError:
        print("11. Timezone functionality not available")
    
    # 12. Getting components of a date
    print(f"12. Year: {today.year}, Month: {today.month}, Day: {today.day}")
    
    # 13. Getting components of a datetime
    print(f"13. Hour: {now.hour}, Minute: {now.minute}, Second: {now.second}, Microsecond: {now.microsecond}")

if __name__ == "__main__":
    main()