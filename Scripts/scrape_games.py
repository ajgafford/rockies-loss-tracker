import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

os.makedirs('../Data/Raw', exist_ok=True)

def fetch_game_data():
    url = 'https://www.baseball-reference.com/teams/COL/2025-schedule-scores.shtml'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f'Failed to retrieve data. Status code: {response.status_code}')
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'sortable stats_table'})

    games_data = []
    gp = 1 # having trouble extracting the Gm# column, so manually tracking games played

    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')

        # ensure there are enough columns
        if len(columns) > 8:
            result = columns[5].get_text(strip=True)
            runs_scored = columns[6].get_text(strip=True)
            runs_allowed = columns[7].get_text(strip=True)
            
            # skip non-numeric R or RA
            if not (runs_scored.isdigit() and runs_allowed.isdigit()):
                print(f'Skipping row. Non-numeric R or RA. {row.get_text(strip=True)}')
                continue

            games_data.append({
                'Games Played': gp,
                'Result': result,
                'R': runs_scored,
                'RA': runs_allowed
            })

            gp += 1

    return games_data

def save_to_csv(games_data):
    df = pd.DataFrame(games_data)
    filename = '../Data/Raw/COL_2025_schedule.csv'
    df.to_csv(filename, index=False)
    print(f'Data saved to {filename}!')

if __name__ == "__main__":
    game_data = fetch_game_data()
    if game_data:
        save_to_csv(game_data)
    else:
        print('No data retrieved.')
