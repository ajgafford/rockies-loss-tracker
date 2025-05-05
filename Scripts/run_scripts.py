import subprocess
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

scrape_games_path = os.path.join(base_dir, 'Scripts', 'scrape_games.py')
merge_schedules_path = os.path.join(base_dir, 'Scripts', 'merge_schedules.py')
app_path = os.path.join(base_dir, 'app.py')

subprocess.run(['/usr/bin/python3', scrape_games_path])
subprocess.run(['/usr/bin/python3', merge_schedules_path])
subprocess.run(['/usr/bin/python3', app_path])