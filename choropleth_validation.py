import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import code

# Load the datasets
df_sample = pd.read_csv('minoritymajority.csv')
df_sample_r = df_sample[df_sample['STNAME'] == 'Georgia']
# Extract the FIPS codes
fips = df_sample_r['FIPS'].tolist()

data = pd.DataFrame(code.main(90, "init_state.csv"), columns=['S', 'I', 'R'])
Rvalues = data["R"].tolist()
validation_values = pd.read_csv("GeorgiaCOVIDCases.csv")["20230311"].tolist()

# Create model recovered values and validation values DataFrames for Plotly
Rchoropleth_data = pd.DataFrame({'FIPS': fips, 'Values': Rvalues})
validation_data = pd.DataFrame({'FIPS': fips, 'Values': validation_values})

# Create the choropleth map
Rfig = px.choropleth(
    Rchoropleth_data,
    geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
    locations='FIPS',
    color='Values',
    color_continuous_scale="Viridis",  # Built-in color scale
    title="Recovered Population in Georgia after 90 days",
    labels={'Values': 'Recovered Population'}
)
validation_fig = px.choropleth(
    validation_data,
    geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
    locations='FIPS',
    color='Values',
    color_continuous_scale="Viridis",  # Built-in color scale
    title="COVID-19 Cases in Georgia after 3 years",
    labels={'Values': 'COVID-19 Cases'}
)

# Update layout for better visualization
Rfig.update_geos(fitbounds="locations", visible=False)
validation_fig.update_geos(fitbounds="locations", visible=False)

#Create a subplot with 1 rows and 2 columns
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Model Recovered Population after 90 days", "Actual Infected Population after 3 years"),
    specs=[[{"type": "choropleth"}, {"type": "choropleth"}]]
)
# Add the choropleth maps to the subplots  
fig.add_trace(Rfig.data[0], row=1, col=1)
fig.add_trace(validation_fig.data[0], row=1, col=2)

# Update layout for each subplot to zoom into Georgia
fig.update_geos(fitbounds="locations", visible=False, row=1, col=1)
fig.update_geos(fitbounds="locations", visible=False, row=1, col=2)

# Update layout for the subplot
fig.update_layout(
    title_text="Disease Simulation in Georgia measured at end of spread",
    height=900,
    showlegend=False,
    geo=dict(bgcolor='rgb(229,229,229)'),
    paper_bgcolor='rgb(229,229,229)',
    title_font_size=20
)
# Show the subplot
fig.show()