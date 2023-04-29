# UFC DATA

This repository contains Python scripts to scrape fighter and event data from [UFC Stats](http://ufcstats.com/). The data can be used for various purposes, including analyzing fight outcomes using machine learning techniques.

## Modules

There are two main modules in this project:

1. `fighters.py`: Contains functions to scrape fighter data, including their name, height, weight, reach, stance, and win-loss-draw record. The `scrape_fighter_data(char)` function returns a list of fighter data for a specific character. The module also includes code to scrape data for all characters and save it to a CSV file.
2. `events.py`: Contains functions to scrape event data, including event name, date, result, fighter names, and various fight statistics (e.g., strikes, takedowns, and submissions). The `get_event_urls()` function returns a list of event URLs, and the `scrape_fight_data(event_url)` function returns fight data for a specific event URL. The module also includes code to scrape data for all events and save it to a CSV file.

## Usage

To use the modules, you will need to import them into your Python script and call the appropriate functions. For example:

```python
from fighters import scrape_fighter_data
from events import get_event_urls, scrape_fight_data

fighters = scrape_fighter_data()
event_urls = get_event_urls()
events = [scrape_fight_data(event_url) for event_url in event_urls]

To run the modules as standalone scripts and save the scraped data to CSV files, simply execute the `fighters.py` and `events.py` scripts:

python fighters.py
python events.py
