import os
import pandas as pd

# get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_data_dir = os.path.join(project_root, 'Data', 'Raw')
processed_data_dir = os.path.join(project_root, 'Data', 'Processed')

# read in the schedules for the three teams
rockies = pd.read_csv(os.path.join(raw_data_dir, 'COL_2025_schedule.csv'))
sox = pd.read_csv(os.path.join(raw_data_dir, 'CHW_2024_schedule.csv'), usecols=['Gm#', 'W/L', 'R', 'RA'])
mets = pd.read_csv(os.path.join(raw_data_dir, 'NYM_1962_schedule.csv'), usecols=['Gm#', 'W/L', 'R', 'RA'])

# rename columns in sox and mets
for team in [sox, mets]:
    team.rename(columns={'Gm#': 'Games Played', 'W/L': 'Result'}, inplace=True)

# add in the team column
rockies['Team'] = '2025 COL'
sox['Team'] = '2024 CHW'
mets['Team'] = '1962 NYM'

# add in columns for additional features
for team in [rockies, sox, mets]:
    team['Loss?'] = team['Result'].str.startswith('L').astype('int')  # will assign 1 if started with an 'L'
    team['Losses'] = team['Loss?'].cumsum()  # add all previous values
    team['Expected Losses'] = round(
        team['Games Played'] * (1 - team['R'].cumsum() ** 2 / (team['R'].cumsum() ** 2 + team['RA'].cumsum() ** 2))
    ).astype(int)  # using the Pythag W/L Record

# join everyone together
losers = pd.concat([rockies, sox, mets], ignore_index=True)
losers.to_csv(os.path.join(processed_data_dir, 'losers.csv'), index=False)