import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm
import re

# Function to scrape event URLs from the completed events page
def get_event_urls():
    url = "http://ufcstats.com/statistics/events/completed?page=all"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    event_links = [a['href'] for a in soup.select('td.b-statistics__table-col a')]
    return event_links[1:] # skipping first one because its in the future



def scrape_fight_data(event_url):
    response = requests.get(event_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    fights = []

    event_name = soup.find('h2', class_='b-content__title').text.strip()
    event_date = soup.find('li', class_='b-list__box-list-item').text.strip().split('\n')[-1].strip()

    fight_table = soup.find('table', class_='b-fight-details__table')
    rows = fight_table.find_all('tr', class_='b-fight-details__table-row')[1:]  # Skipping the header row

    for row in rows:
        cols = row.find_all('td', recursive=False)
        result = cols[0].find('i', class_='b-flag__inner').text.strip()
        result = ' '.join(result.split()) 
        fighters = cols[1].find_all('a')
        fighter1 = fighters[0].text.strip()
        fighter2 = fighters[1].text.strip()
        fighters_combined = f"{fighter1} vs {fighter2}"
        kd = cols[2].text.strip().replace('\n', '')
        kd = re.sub(r'\s+', '-', kd)
        str_stats = cols[3].text.strip().replace('\n', '')
        str_stats = re.sub(r'\s+', '-', str_stats)
        td = cols[4].text.strip().replace('\n', '')
        td = re.sub(r'\s+', '-', td)
        sub = cols[5].text.strip().replace('\n', '')
        sub = re.sub(r'\s+', '-', sub)
        weight_class = cols[6].text.strip()
        method = cols[7].text.strip().replace('\n', '')
        method = re.sub(r'\s+', '-', method)
        round_ = cols[8].text.strip()
        time = cols[9].text.strip()

        # Identify winner or draw
        if result == "win":
            winner = fighter1
        elif result == "draw":
            winner = "Draw"
        else:
            winner = "Unknown"

        fights.append([event_name, event_date, winner, fighter1, fighter2, kd, str_stats, td, sub, weight_class, method, round_, time])

    return fights



# Scrape event data and save to a CSV file
event_urls = get_event_urls()
with open('ufc_event_data.csv', mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Event Name', 'Event Date', 'Result', 'Fighter1','Fighter2', 'KD', 'Strikes', 'TD', 'Sub', 'Weight Class', 'Method', 'Round', 'Time'])

    # Wrap the event_urls in tqdm for progress bar display
    for event_url in tqdm(event_urls, desc="Loading data:"):
        fights = scrape_fight_data(event_url)
        for fight in fights:
            writer.writerow(fight)