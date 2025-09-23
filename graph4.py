import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from pathlib import Path

# Load data
df = pd.read_csv("team_data_pop.csv")
df['TV_Homes'] = df['TV_Homes'].astype(float)
df['Population'] = df['Population'].astype(float)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['TV_Homes'],
    y=df['Chmp'],
    mode='markers',
    marker=dict(size=0.5),  # hide points
    hovertext=df['Tm'],
    hoverinfo='text'
))

logo_path = Path("NFL_Logos") 
max_size = 0.6  

# Parameters
min_logo = 0.03  # min logo size in axis units
max_logo = 0.4  # max logo size in axis units

pop_min = df['Population'].min()
pop_max = df['Population'].max()

for idx, row in df.iterrows():
    png_file = logo_path / f"{row['Tm'].lower().replace(' ', '')}.png"  
    if png_file.exists():
            scale = min_logo + (row['Population'] - pop_min) / (pop_max - pop_min) * (max_logo - min_logo)        
            fig.add_layout_image(
                x=row['TV_Homes'],
                y=row['Chmp'],
                source=Image.open(png_file),
                xref="x",
                yref="y",
                sizex=scale * df['TV_Homes'].max(),
                sizey=scale * df['Chmp'].max(),
                xanchor="center",
                yanchor="middle",
            )

fig.update_layout(
    title="NFL Teams: TV Homes vs Championships",
    xaxis_title="TV Homes",
    yaxis_title="Championships",
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True),
    width=1200,
    height=800
)

fig.write_html("NFL_Teams_Chart.html")
