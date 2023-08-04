import bs4
import requests
import pandas as pd
import regex
from datetime import datetime

#create beautiful soup objects
headers = {
"Accept-Language" : "en-US,en;q=0.5",
"User-Agent": "Defined",
}

pagedata = requests.get("https://www.vegasinsider.com/mlb/odds/futures/", headers=headers)
cleanpagedata = bs4.BeautifulSoup(pagedata.text, 'html.parser')

#look for all tables
table = cleanpagedata.findAll('table')

#create dataframe from first table
df = pd.read_html(str(table))[0]

#create team column name by pulling only the first text as it also contains pitcher information from the first column
df['team']  = df[df.columns[0]].str.split().str[0]

#create odds from second column.   using the first column and time of writing this code, it points to fanduel on the vegasinsider app
df['odds'] = df[df.columns[1]].str.replace('+', '')

#only keep the two columns and drop na values
df = df[['team', 'odds']].dropna()

#convert the odds to an integer
df['odds'] = df['odds'].astype('int')

#add current date and time to the dataframe
df['dateandtimeran'] = datetime.now()

#add results to csv output file
df.to_csv('mlbfutures.csv', mode='a', index=False, header=False)

#show results in html.  first pull complete csv then display in html
df_full = pd.read_csv('mlbfutures.csv')
df_full.to_html('index.html')