import time
import datetime
# Selenium related imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

"""
This Project was created by Kirwin Webb, 01/02/2022

This is a global ranking tracker for tryhackme.com,
Logs any changes in global rank and saves the collected data 
so I can later use it for some data science

I typically run this script as I'm studying on tryhackme,
as it allows me to see the change in rank as I progress and complete
tasks and questions, it's a helpful way to motivate me.

It also shows if how much I've gone down in rank from inactivity.

"""

# Disables web browser display
options = Options()
options.headless = True

# Url to visit 
url = "https://tryhackme.com/p/Blackwolf"
service = Service("/home/blackwolf/scripts/python/webdrivers/geckodriver/geckodriver")

browser = webdriver.Firefox(options=options, service=service)
browser.get(url)
flag = True

# Fetching appropriate data for logging
def data_fetch():
    rank = browser.find_element(By.ID, "user-rank").text

    # Not used for now but may be implemented later
    # percentile = browser.find_element(By.ID, "profile-rank-badge").text
    return rank

# Reading score before writing (to prevent duplicates)
def last_score_stored():
    with open("/home/blackwolf/scripts/github/StatTracker/pandas_data.csv", "r") as file:
        lines = file.read().splitlines()
        rank_saved = int(list(lines[-1].split(" "))[0])
    return int(rank_saved) 


# This function is for a daily score increase tracker, monitor how much your score
# Has increased by in todays period of work.
def daily_ladder():
    # Initialising variables
    daily_increase = 0
    todays_score = 0
    
    # Reading log file
    with open("/home/blackwolf/scripts/github/StatTracker/pandas_data.csv", "r") as file:
        lines = file.read().splitlines()
        
        # Looping over every line in log file
        for line in lines:

            # Updating date and score value every new line
            dateVal = line.split(" ")[1]
            scoreVal = line.split(" ")[0]
            
            # Checking for first appearance of current date, sets starting score val 
            if dateVal == str(datetime.date.today()) and todays_score == 0:
                todays_score = int(scoreVal)
                found_latest = True
                print("Todays Starting Score:", todays_score)
            
            # Records difference in rank for todays date occurences
            elif dateVal == str(datetime.date.today()):
                daily_increase += todays_score - int(scoreVal)

    # Returning difference in score from first val of todays work
    return daily_increase
    
# Writing data to a file in a while loop:
while flag:
    # Calling data_fetch() func to periodically update rank & percentile
    browser.refresh()
    rank = data_fetch()
    
    # Comparing updated score to lastest saved score in rank-data.txt
    # If the value is different it will append it to file, avoiding duplicate data
    if(last_score_stored() != int(rank)):
        with open("/home/blackwolf/scripts/github/StatTracker/pandas_data.csv", "a") as file:
            
            # Calc difference in rank postition
            pos_dif = last_score_stored() - int(rank) 
            
            # Appending latest posititonal rank to file
            file.write(rank + " " + str(datetime.date.today()))
            file.write("\n")

            # Close file to avoid erroring out
            file.close()
            print("Score updated! Position changed by: ", str(pos_dif), "           Daily Ladder:", daily_ladder())
    else:
        print("Score hasn't changed, sleeping for 180s...           Daily Ladder:", daily_ladder() )
        time.sleep(180)
