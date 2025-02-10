import bs4
import requests
import pandas as pd
import regex as re
from datetime import datetime
import json
import plotly.express as px


#show results in html.  first pull complete csv then display in html
df_full = pd.read_csv('mlbfutures.csv')
# Create a line chart using plotly
fig = px.line(df_full, x='dateandtimeran', y='odds', color='team', title='Odds Over Time by Team', markers=True)

# Save the plot as an HTML file
fig.write_html('indextest.html')
