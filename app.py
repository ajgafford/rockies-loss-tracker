import streamlit as st
import pandas as pd
import os
import datetime
import plotly.express as px

project_root = os.path.dirname(os.path.abspath(__file__))
processed_data_dir = os.path.join(project_root, 'Data', 'Processed')
filepath = os.path.join(processed_data_dir, 'losers.csv')

def get_last_updated(filepath):
    timestamp = os.path.getmtime(filepath)
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# MAIN APP
st.set_page_config(page_title="2025 Colorado Rockies Loss Tracker", layout="centered")

st.title("2025 Rockies Loss Tracker")
st.caption(f"Last updated: {get_last_updated(filepath)}")

df = pd.read_csv(os.path.join(processed_data_dir, 'losers.csv'))
max_games = int(df['Games Played'].max())

# calculate projected losses for a 162-game season
latest_rockies = df[df['Team'] == '2025 COL'].iloc[-1]  # get the latest game for the Rockies
rockies_losses = latest_rockies['Losses']
rockies_games_played = latest_rockies['Games Played']

# calculate the losses per game rate and project it for 162 games
losses_per_game = rockies_losses / rockies_games_played
projected_losses = losses_per_game * 162

st.subheader("Projected 162-Game Losses")
if projected_losses > 121: # they would break the record
    exceed_by = projected_losses - 121
    st.metric(
        label="Projected Losses for 2025 COL",
        value=f"{projected_losses:.0f}",
        delta=f"Breaking record by {exceed_by:.0f} games!",
        delta_color="inverse"
    )
    st.markdown(f"""
    The 2025 Rockies are on pace to break the record for most losses in a season
    (currently held by the 2024 Chicago White Sox with 121 losses) by **{exceed_by:.0f} games**.
    """)
else:
    st.metric(
        label="Projected Losses for 2025 COL",
        value=f"{projected_losses:.0f}"
    )

# SCORECARDS
st.subheader("Team Summaries")
columns = st.columns(3) 
teams = df['Team'].unique()

for i, team in enumerate(teams):
    team_df = df[df['Team'] == team]
    latest = team_df.iloc[-1]  # last row is most recent game
    with columns[i]:
        st.metric(label=f"{team} Losses", value=int(latest['Losses']))
        st.metric(label="Expected Losses", value=int(latest['Expected Losses']))

st.markdown("""
    #### How Expected Losses were calculated:
    Derived using the Pythagorean Winning Percentage formula devised by Bill James,
    which calculates the *expected* winning percentage of a team based on it's
    runs scored and runs allowed.
    """)

# SLIDER
st.subheader("Losses by Game Number")
game_limit = st.slider("Show up to game #:", 1, max_games, max_games)

filtered_df = df[df['Games Played'] <= game_limit]

# LINE CHART
color_map = {
    '2025 COL':'purple',
    '2024 CHW':'white',
    '1962 NYM':'orange'
}

fig = px.line(
    filtered_df,
    x="Games Played",
    y="Losses",
    color="Team",
    color_discrete_map=color_map,
    title="The Race to 120 Losses"
)

st.plotly_chart(fig, use_container_width=True)