"""
Created on Sun Mar 16 00:28 2025

@author: Omar Nassar
"""

import json
from trivia import get_trivia_day

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
    
    if day < 0 or day > 30:
        day = 30
    
    return round(entries/day)

def getData(file: str):
    try:
        if file == "winners":
            with open('../resources/trivia_winners.json', "r") as data:
                return json.load(data)

        elif file == "all":
            with open('../resources/trivia_all_answers.json', "r") as data:
                return json.load(data)
        
        elif file == "both":
            with open('../resources/trivia_winners.json', "r") as data:
                data1 = json.load(data)
            with open('../resources/trivia_all_answers.json', "r") as data:
                data2 = json.load(data)
            return data1,data2

    except FileNotFoundError:
        print("Files not found. Exiting...")
        exit(1)

def printAllStats():
    print(f"Total Entries: {totalEntries()} ({uniqueEntries()} Unique)")
    print(f"Total Winners: {totalWinners()} ({uniqueWinners()} Unique)")
    print(f"Average Entries Per Day: {averageDailyEntries()}")
    print(f"Total Amount Gifted: ${totalMoney()}")

def main():
    printAllStats()

if __name__ == '__main__':
    main()
