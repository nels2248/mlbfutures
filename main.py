import bs4
import requests
import pandas as pd
import regex as re
import json
import plotly.express as px
from datetime import datetime

# Create headers for web request
headers = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Defined",
}

# Dictionary of MLB teams and primary colors
team_colors = {
    "Arizona Diamondbacks": "#A71930",
    "Atlanta Braves": "#CE1141",
    "Baltimore Orioles": "#DF4601",
    "Boston Red Sox": "#BD3039",
    "Chicago Cubs": "#0E3386",
    "Chicago White Sox": "#27251F",
    "Cincinnati Reds": "#C6011F",
    "Cleveland Guardians": "#0C2340",
    "Colorado Rockies": "#33006F",
    "Detroit Tigers": "#FA4616",
    "Houston Astros": "#002D62",
    "Kansas City Royals": "#004687",
    "Los Angeles Angels": "#BA0021",
    "Los Angeles Dodgers": "#005A9C",
    "Miami Marlins": "#00A3E0",
    "Milwaukee Brewers": "#FFC52F",
    "Minnesota Twins": "#002B5C",
    "New York Mets": "#FF5910",
    "New York Yankees": "#003087",
    "Oakland Athletics": "#003831",
    "Philadelphia Phillies": "#E81828",
    "Pittsburgh Pirates": "#FDB827",
    "San Diego Padres": "#2F241D",
    "San Francisco Giants": "#FD5A1E",
    "Seattle Mariners": "#0C2C56",
    "St. Louis Cardinals": "#C41E3A",
    "Tampa Bay Rays": "#092C5C",
    "Texas Rangers": "#C0111F",
    "Toronto Blue Jays": "#134A8E",
    "Washington Nationals": "#AB0003",
}

# Function to extract team name from the JSON string
def extract_team_name(json_string):
    if isinstance(json_string, str):  # Check if it's a string
        json_match = re.match(r'({.*?})', json_string)
        if json_match:
            json_part = json_match.group(1)
            try:
                json_data = json.loads(json_part)
                return json_data.get('description', None)
            except json.JSONDecodeError:
                return None
    return None

# Fetch and parse webpage
pagedata = requests.get("https://www.vegasinsider.com/mlb/odds/futures/", headers=headers)
cleanpagedata = bs4.BeautifulSoup(pagedata.text, 'html.parser')

# Extract table
table = cleanpagedata.findAll('table')
df = pd.read_html(str(table))[0].drop(index=0)

# Extract team names and odds
df['team'] = df.iloc[:, 0].apply(extract_team_name)
df['odds'] = df[df.columns[1]].str.replace(r'\+', '', regex=True)  # Fixing the regex issue
df = df[['team', 'odds']].dropna()
df['odds'] = df['odds'].astype(int)
df['dateandtimeran'] = datetime.now().date()

# Save data
df.to_csv('mlbfutures.csv', mode='a', index=False, header=False)

# Read full dataset
df_full = pd.read_csv('mlbfutures.csv')
df_full['dateandtimeran'] = pd.to_datetime(df_full['dateandtimeran'], format='mixed').dt.date.astype(str)
df_full['team'] = pd.Categorical(df_full['team'], categories=sorted(df_full['team'].unique()), ordered=True)
df_full = df_full.sort_values(by=['team', 'dateandtimeran']).reset_index(drop=True)

# Assign team colors
df_full['color'] = df_full['team'].map(team_colors)

# Create the line chart with team colors
fig = px.line(
    df_full,
    x='dateandtimeran',
    y='odds',
    color='team',
    title='Odds Over Time by Team',
    markers=True,
    color_discrete_map=team_colors  # Applying team colors to the lines
)

# Save as interactive HTML
fig.write_html('index.html')
