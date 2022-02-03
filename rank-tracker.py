import time
import datetime
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

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
def data_fetch(val):
    rank = browser.find_element(By.ID, "user-rank").text
    percentile = browser.find_element(By.ID, "profile-rank-badge").text
    if(val == "rank"):
        return rank
    else:
        return percentile

# Reading score before writing (to prevent duplicates)
def last_score_stored():
    with open("pandas_data.csv", "r") as file:
        lines = file.read().splitlines()
        rank_saved = int(list(lines[-1].split(" "))[0])
        file.close()
    return int(rank_saved)

# Writing data to a file in a while loop:
while flag:
    # Calling data_fetch() func to periodically update rank & percentile
    rank = data_fetch("rank")
    
    # Comparing updated score to lastest saved score in rank-data.txt
    # If the value is different it will append it to file, avoiding duplicate data
    if(last_score_stored() != int(rank)):
        with open("pandas_data.csv", "a") as file:
            
            # Calc difference in rank postition
            pos_dif = last_score_stored() - int(rank) 
            
            # Appending latest posititonal rank to file
            file.write(rank + " " + str(datetime.date.today()))
            file.write("\n")

            # Close file to avoid erroring out
            file.close()
            
            # Update last_score_stored
            last_score_stored()

            print("Score updated! Position changed by: " + str(pos_dif))    
    else:
        print("Score hasn't changed, sleeping for 180s...")
        time.sleep(180)
