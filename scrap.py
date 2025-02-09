#USED IN CREATING DIFFERENT OUTPUT FILES

import pandas as pd
import plotly.express as px

#show results in html.  first pull complete csv then display in html
df_full = pd.read_csv('mlbfutures.csv')
df_full.to_html('index.html')

# Create a line chart using plotly
fig = px.line(df_full, x='dateandtimeran', y='odds', color='team', title='Odds Over Time by Team')

# Save the plot as an HTML file
fig.write_html('index.html')
