import bs4
import requests
import pandas as pd
import regex as re
from datetime import datetime
import json
import plotly.express as px

#create beautiful soup objects
headers = {
"Accept-Language" : "en-US,en;q=0.5",
"User-Agent": "Defined",
}

#Function to extract team name from the JSON string
def extract_team_name(json_string):
    if isinstance(json_string, str):  # Check if it's a string
        # Use a regular expression to extract valid JSON part (everything up to the first occurrence of '}')
        json_match = re.match(r'({.*?})', json_string)
        
        if json_match:
            json_part = json_match.group(1)  # Get the valid JSON part
            
            try:
                # Parse the JSON
                json_data = json.loads(json_part)
                
                # Extract the description which contains name of team and city/state
                team_name = json_data.get('description', None) 
                
                return team_name
            except json.JSONDecodeError:
                return None  # If JSON is still invalid, return None
        else:
            return None  # If no valid JSON found, return None
    else:
        return None  # Handle non-string values by returning None


pagedata = requests.get("https://www.vegasinsider.com/mlb/odds/futures/", headers=headers)
cleanpagedata = bs4.BeautifulSoup(pagedata.text, 'html.parser')

#look for all tables
table = cleanpagedata.findAll('table')

#create dataframe from first table
df = pd.read_html(str(table))[0]

#drop the first row as it's empty
df = df.drop(index=0)


#use function to get values
df['team'] = df.iloc[:,0].apply(extract_team_name) 

#create odds from second column.   using the first column and time of writing this code, it points to fanduel on the vegasinsider app
df['odds'] = df[df.columns[1]].str.replace('+', '')

#only keep the two columns and drop na values
df = df[['team',  'odds']].dropna()

#convert the odds to an integer
df['odds'] = df['odds'].astype('int')

#add current date and time to the dataframe
df['dateandtimeran'] = datetime.now().date()
 


#add results to csv output file
df.to_csv('mlbfutures.csv', mode='a', index=False, header=False)

# Read the complete CSV
df_full = pd.read_csv('mlbfutures.csv')

# Ensure 'dateandtimeran' is treated properly
df_full['dateandtimeran'] = pd.to_datetime(df_full['dateandtimeran'], format='mixed').dt.date.astype(str)

# Sort teams alphabetically and set categorical order
unique_teams = sorted(df_full['team'].unique())
df_full['team'] = pd.Categorical(df_full['team'], categories=unique_teams, ordered=True)

# Sort DataFrame by team (ensures legend order)
df_full = df_full.sort_values(by=['team', 'dateandtimeran']).reset_index(drop=True)

# Create the line chart
fig = px.line(df_full, x='dateandtimeran', y='odds', color='team', title='Odds Over Time by Team', markers=True)

# Save the plot as an HTML file
fig.write_html('index.html')
