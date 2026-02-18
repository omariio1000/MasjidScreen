"""
Ramadan Prayer Times Generator
Fetches Isha Adhan times for each day of Ramadan from the prayer times API.

@author: Omar Nassar
"""

import requests
import json
from datetime import datetime, timedelta
import os

# ICCH coordinates
LATITUDE = 45.5408
LONGITUDE = -122.8644

# API endpoint
API_URL = "https://us-west1-pdx-msa.cloudfunctions.net/prayertimes"

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAMADAN_TIMES_FILE = os.path.join(BASE_DIR, '..', 'resources', 'ramadan_isha_times.json')
RAMADAN_FIRST_DAY_FILE = os.path.join(BASE_DIR, '..', 'resources', 'ramadan_first_day.txt')


def get_prayer_times(date: datetime) -> dict:
    """Fetch prayer times for a specific date"""
    # Format date as yyyy-MM-dd for API (ISO format)
    date_str = date.strftime("%Y-%m-%d")
    
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "date": date_str
    }
    
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") == 200:
            return data.get("data", {})
        else:
            print(f"API error for {date_str}: {data}")
            return None
    except Exception as e:
        print(f"Error fetching times for {date_str}: {e}")
        return None


def get_ramadan_times_range(start_date: datetime, num_days: int = 30) -> list:
    """Fetch prayer times for a range of days using the API's range feature"""
    start_str = start_date.strftime("%Y-%m-%d")
    
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start": start_str,
        "days": num_days
    }
    
    try:
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get("ok"):
            return data.get("data", [])
        else:
            print(f"API error: {data}")
            return []
    except Exception as e:
        print(f"Error fetching range: {e}")
        return []


def get_ramadan_first_day() -> datetime:
    """Get the first day of Ramadan from the config file"""
    try:
        with open(RAMADAN_FIRST_DAY_FILE, 'r') as f:
            first_day_str = f.readline().strip()
    except FileNotFoundError:
        print(f"Warning: {RAMADAN_FIRST_DAY_FILE} not found")
        # Create file with a default date so it doesn't crash again
        os.makedirs(os.path.dirname(RAMADAN_FIRST_DAY_FILE), exist_ok=True)
        default_date = datetime.now().strftime("%Y-%m-%d")
        with open(RAMADAN_FIRST_DAY_FILE, 'w') as f:
            f.write(default_date)
        print(f"Created {RAMADAN_FIRST_DAY_FILE} with default date {default_date}")
        first_day_str = default_date
    
    return datetime.strptime(first_day_str, "%Y-%m-%d")


def generate_ramadan_isha_times(num_days: int = 30) -> dict:
    """Generate Isha times for all days of Ramadan using range API"""
    first_day = get_ramadan_first_day()
    
    ramadan_times = {
        "ramadan_start": first_day.strftime("%Y-%m-%d"),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "location": {
            "name": "ICCH - Islamic Center of Cedar Hills",
            "address": "7270 NW Helvetia Rd, Hillsboro, OR 97124",
            "latitude": LATITUDE,
            "longitude": LONGITUDE
        },
        "days": {}
    }
    
    print(f"Fetching Isha times for Ramadan {first_day.year}...")
    print(f"Ramadan starts: {first_day.strftime('%Y-%m-%d')}")
    print("-" * 50)
    
    # Use range API to fetch all days at once
    range_data = get_ramadan_times_range(first_day, num_days)
    
    if range_data:
        for day_num, day_entry in enumerate(range_data, start=1):
            prayer_data = day_entry.get("data", {})
            date_str = day_entry.get("date", "")
            
            timings = prayer_data.get("timings", {})
            isha_time = timings.get("Isha", "")
            hijri_date = prayer_data.get("date", {}).get("hijri", {})
            gregorian = prayer_data.get("date", {}).get("gregorian", {})
            
            ramadan_times["days"][str(day_num)] = {
                "date": date_str,
                "isha_adhan": isha_time,
                "hijri": hijri_date.get("date", ""),
                "weekday": gregorian.get("weekday", {}).get("en", "")
            }
            
            print(f"Day {day_num:2d} ({date_str}): Isha at {isha_time}")
    else:
        # Fallback to individual requests
        print("Range request failed, trying individual requests...")
        for day_num in range(1, num_days + 1):
            current_date = first_day + timedelta(days=day_num - 1)
            
            prayer_data = get_prayer_times(current_date)
            
            if prayer_data:
                timings = prayer_data.get("timings", {})
                isha_time = timings.get("Isha", "")
                hijri_date = prayer_data.get("date", {}).get("hijri", {})
                
                ramadan_times["days"][str(day_num)] = {
                    "date": current_date.strftime("%Y-%m-%d"),
                    "isha_adhan": isha_time,
                    "hijri": hijri_date.get("date", ""),
                    "weekday": prayer_data.get("date", {}).get("gregorian", {}).get("weekday", {}).get("en", "")
                }
                
                print(f"Day {day_num:2d} ({current_date.strftime('%Y-%m-%d')}): Isha at {isha_time}")
            else:
                print(f"Day {day_num:2d} ({current_date.strftime('%Y-%m-%d')}): FAILED to fetch")
    
    return ramadan_times


def save_ramadan_times(times: dict):
    """Save Ramadan times to JSON file"""
    with open(RAMADAN_TIMES_FILE, 'w') as f:
        json.dump(times, f, indent=4)
    print(f"\n✅ Saved to: {RAMADAN_TIMES_FILE}")


def load_ramadan_times() -> dict:
    """Load Ramadan times from JSON file"""
    try:
        with open(RAMADAN_TIMES_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Warning: Ramadan times file not found or invalid at {RAMADAN_TIMES_FILE}")
        print("Run 'python ramadan_times.py' to generate Isha times.")
        # Create empty structure so it doesn't crash
        empty_times = {"days": {}}
        os.makedirs(os.path.dirname(RAMADAN_TIMES_FILE), exist_ok=True)
        with open(RAMADAN_TIMES_FILE, 'w') as f:
            json.dump(empty_times, f, indent=4)
        return empty_times


def get_isha_time_for_day(day: int) -> str:
    """Get the Isha adhan time for a specific day of Ramadan"""
    times = load_ramadan_times()
    day_data = times.get("days", {}).get(str(day), {})
    return day_data.get("isha_adhan", "")


def is_past_isha(day: int) -> bool:
    """Check if current time is past Isha for the given Ramadan day"""
    isha_time_str = get_isha_time_for_day(day)
    if not isha_time_str:
        return False
    
    # Parse Isha time (format: "HH:MM")
    try:
        isha_hour, isha_min = map(int, isha_time_str.split(":"))
        now = datetime.now()
        isha_datetime = now.replace(hour=isha_hour, minute=isha_min, second=0, microsecond=0)
        return now >= isha_datetime
    except:
        return False


def main():
    """Generate and save Ramadan Isha times"""
    print("=" * 50)
    print("RAMADAN ISHA TIMES GENERATOR")
    print("=" * 50)
    
    times = generate_ramadan_isha_times(30)
    save_ramadan_times(times)
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total days: {len(times['days'])}")
    print(f"First day: {times['ramadan_start']}")
    
    # Show first and last Isha times
    if times['days']:
        first_isha = times['days'].get('1', {}).get('isha_adhan', 'N/A')
        last_isha = times['days'].get('30', {}).get('isha_adhan', 'N/A')
        print(f"First Isha (Day 1): {first_isha}")
        print(f"Last Isha (Day 30): {last_isha}")


if __name__ == '__main__':
    main()
