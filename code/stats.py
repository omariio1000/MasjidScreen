"""
Created on Sun Mar 16 00:28 2025

@author: Omar Nassar
"""

import json
import os
from trivia import get_trivia_day

# Base directory and resource paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, '..', 'resources')
TRIVIA_WINNERS_FILE = os.path.join(RESOURCES_DIR, 'trivia_winners.json')
TRIVIA_ALL_ANSWERS_FILE = os.path.join(RESOURCES_DIR, 'trivia_all_answers.json')

def totalEntries() -> int:
    data = getData("all")
    total = 0

    for day in data:
        total += len(data[day])

    return total


def uniqueEntries() -> int:
    data = getData("all")
    entries = set()
    for answer_list in data.values():
        for entry in answer_list:
            entries.add(entry["First Name"] + " " + entry["Last Name"])
    return len(entries)

def uniqueWinners() -> int:
    data = getData("winners")
    winners = set()
    for winners_list in data.values():
        for winner in winners_list:
            winners.add(winner[0])
    return len(winners)

def totalWinners() -> int:
    data = getData("winners")
    total = 0

    for day in data:
        total += len(data[day])

    return total

def totalMoney(prizeAmount: int = 5) -> int:
    return totalWinners() * prizeAmount

def averageDailyEntries() -> int:
    entries = totalEntries()
    day = get_trivia_day()
    
    if day <= 0 or day > 30:
        day = 30
    
    return round(entries/day)

def getData(file: str):
    try:
        if file == "winners":
            with open(TRIVIA_WINNERS_FILE, "r") as data:
                return json.load(data)

        elif file == "all":
            with open(TRIVIA_ALL_ANSWERS_FILE, "r") as data:
                return json.load(data)
        
        elif file == "both":
            with open(TRIVIA_WINNERS_FILE, "r") as data:
                data1 = json.load(data)
            with open(TRIVIA_ALL_ANSWERS_FILE, "r") as data:
                data2 = json.load(data)
            return data1, data2

    except (FileNotFoundError, json.JSONDecodeError):
        print("Warning: Stats data files not found or invalid, returning empty data")
        if file == "both":
            return {}, {}
        return {}

def printAllStats():
    print(f"Total Entries: {totalEntries()} ({uniqueEntries()} Unique)")
    print(f"Total Winners: {totalWinners()} ({uniqueWinners()} Unique)")
    print(f"Average Entries Per Day: {averageDailyEntries()}")
    print(f"Total Amount Gifted: ${totalMoney()}")

def main():
    printAllStats()

if __name__ == '__main__':
    main()
