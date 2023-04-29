import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape fighter data for a specific character
def scrape_fighter_data(char):
    url = f"http://ufcstats.com/statistics/fighters?char={char}&page=all"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    fighters = []
    fighter_table = soup.find('table', class_='b-statistics__table')
    rows = fighter_table.find_all('tr')[2:]  # Skipping the header and blank row

    for row in rows:
        cols = row.find_all('td')
        first_name = cols[0].text.strip()
        last_name = cols[1].text.strip()
        nickname = cols[2].text.strip()
        height = cols[3].text.strip()
        weight = cols[4].text.strip()
        reach = cols[5].text.strip()
        stance = cols[6].text.strip()
        wins = cols[7].text.strip()
        losses = cols[8].text.strip()
        draws = cols[9].text.strip()

        fighters.append([first_name, last_name, nickname, height, weight, reach, stance, wins, losses, draws])

    return fighters

# Scrape data for all characters and save to a CSV file
with open('ufc_fighters.csv', mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['First Name', 'Last Name', 'Nickname', 'Height', 'Weight', 'Reach', 'Stance', 'Wins', 'Losses', 'Draws'])

    for char in 'abcdefghijklmnopqrstuvwxyz':
        fighters = scrape_fighter_data(char)
        for fighter in fighters:
            writer.writerow(fighter)