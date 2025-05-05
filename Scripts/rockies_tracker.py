import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('../Data/Processed/losers.csv')

sns.set_style('darkgrid')

# Colors for the different teams
team_colors = {
    '2025 COL':'#333366',
    '2024 CHW':'#C4CED4',
    '1962 NYM':'#FF5910'
}

# Team selector
teams = df['Team'].unique()
selected_teams = st.sidebar.multiselect("Select teams", teams, default=teams)

# Filtered data
filtered_df = df[df['Team'].isin(selected_teams)]

# Plotting
st.title('The Race to 120 Losses')
fig, ax = plt.subplots(figsize=(10,8))
plt.axhline(y=120, color='red', linestyle='dashed', alpha=0.5)
plt.text(10, 122, 'The 120 Loss Threshold')
for team in selected_teams:
    team_data = filtered_df[filtered_df['Team'] == team]
    ax.plot(team_data['Games Played'], team_data['Losses'], label=team + ' Actual Losses', color=team_colors[team])
    ax.plot(team_data['Games Played'], team_data['Expected Losses'], label=team + ' Expected Losses', color=team_colors[team], linestyle='dashed', alpha=0.5)
ax.set_xlabel('Games Played')
ax.set_ylabel('Losses')
ax.legend()
st.pyplot(fig)