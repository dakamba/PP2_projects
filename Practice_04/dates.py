#1. Subtract five days from current date
from datetime import datetime, timedelta

current_date = datetime.now()
new_date = current_date - timedelta(days=5)
print(f"Current date: {current_date}")
print(f"Date after subtracting 5 days: {new_date}")

# Example Output:
# Current date: 2026-02-26 15:34:21.123456
# Date after subtracting 5 days: 2026-02-21 15:34:21.123456

#2. Print yesterday, today, tomorrow
from datetime import datetime, timedelta

today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print(f"Yesterday: {yesterday}")
print(f"Today: {today}")
print(f"Tomorrow: {tomorrow}")

# Example Output:
# Yesterday: 2026-02-25 15:34:21.123456
# Today: 2026-02-26 15:34:21.123456
# Tomorrow: 2026-02-27 15:34:21.123456

#3. Drop microseconds from datetime
from datetime import datetime

now = datetime.now()
no_microseconds = now.replace(microsecond=0)
print(f"Original datetime: {now}")
print(f"Datetime without microseconds: {no_microseconds}")

# Example Output:
# Original datetime: 2026-02-26 15:34:21.123456
# Datetime without microseconds: 2026-02-26 15:34:21

#4. Calculate difference between two dates in seconds
from datetime import datetime

# Input two dates
date_str1 = input("Enter first date (YYYY-MM-DD HH:MM:SS): ")
date_str2 = input("Enter second date (YYYY-MM-DD HH:MM:SS): ")

date1 = datetime.strptime(date_str1, "%Y-%m-%d %H:%M:%S")
date2 = datetime.strptime(date_str2, "%Y-%m-%d %H:%M:%S")

diff_seconds = abs((date2 - date1).total_seconds())
print(f"Difference in seconds: {diff_seconds}")

# Example Input:
# Enter first date: 2026-02-26 12:00:00
# Enter second date: 2026-02-26 15:00:00
# Output: Difference in seconds: 10800.0