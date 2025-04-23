import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import code


# Load the datasets
df_sample = pd.read_csv('minoritymajority.csv')
df_sample_r = df_sample[df_sample['STNAME'] == 'Georgia']
# Extract the FIPS codes
fips = df_sample_r['FIPS'].tolist()

# Load the S, I, and R values from the CSV file
days = [5, 31, 90]

def create_figures(num_days):
    data = pd.DataFrame(code.main(num_days, "init_state.csv"), columns=['S', 'I', 'R'])
    Svalues = data["S"].tolist()
    Ivalues = data["I"].tolist()
    Rvalues = data["R"].tolist()

    # Create S,I, and R DataFrames for Plotly
    Schoropleth_data = pd.DataFrame({'FIPS': fips, 'Values': Svalues})
    Ichoropleth_data = pd.DataFrame({'FIPS': fips, 'Values': Ivalues})
    Rchoropleth_data = pd.DataFrame({'FIPS': fips, 'Values': Rvalues})

    # Create the choropleth map
    Sfig = px.choropleth(
        Schoropleth_data,
        geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
        locations='FIPS',
        color='Values',
        color_continuous_scale="Viridis",  # Built-in color scale
        title="Susceptible Population in Georgia",
        labels={'Values': 'Susceptible Population'}
    )
    Ifig = px.choropleth(
        Ichoropleth_data,
        geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
        locations='FIPS',
        color='Values',
        color_continuous_scale="Viridis",  # Built-in color scale
        title="Infected Population in Georgia",
        labels={'Values': 'Infected Population'}
    )
    Rfig = px.choropleth(
        Rchoropleth_data,
        geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
        locations='FIPS',
        color='Values',
        color_continuous_scale="Viridis",  # Built-in color scale
        title="Recovered Population in Georgia",
        labels={'Values': 'Recovered Population'}
    )

    # Update layout for better visualization
    Sfig.update_geos(fitbounds="locations", visible=False)
    Ifig.update_geos(fitbounds="locations", visible=False)
    Rfig.update_geos(fitbounds="locations", visible=False)

    return [Sfig, Ifig, Rfig]

figures5 = create_figures(5)
figures31 = create_figures(31)
figures90 = create_figures(90)

#Create a subplot with 3 rows and 1 column
fig = make_subplots(
    rows=3, cols=3,
    subplot_titles=("Susceptible Population - 5", "Susceptible Population - 31", "Susceptible Population - 90",
                     "Infected Population - 5", "Infected Population - 31", "Infected Population - 90",
                     "Recovered Population - 5", "Recovered Population - 31", "Recovered Population - 90"),
    specs=[[{"type": "choropleth"}, {"type": "choropleth"}, {"type": "choropleth"}],
           [{"type": "choropleth"}, {"type": "choropleth"}, {"type": "choropleth"}],
           [{"type": "choropleth"}, {"type": "choropleth"}, {"type": "choropleth"}]]
)
for i in range(0, 3):
    if i == 0:
        fig.add_trace(figures5[i].data[0], row=1, col=1)
        fig.add_trace(figures31[i].data[0], row=1, col=2)
        fig.add_trace(figures90[i].data[0], row=1, col=3)
        fig.update_geos(fitbounds="locations", visible=False, row=1, col=1)
        fig.update_geos(fitbounds="locations", visible=False, row=1, col=2)
        fig.update_geos(fitbounds="locations", visible=False, row=1, col=3)
    elif i == 1:
        fig.add_trace(figures5[i].data[0], row=2, col=1)
        fig.add_trace(figures31[i].data[0], row=2, col=2)
        fig.add_trace(figures90[i].data[0], row=2, col=3)
        fig.update_geos(fitbounds="locations", visible=False, row=2, col=1)
        fig.update_geos(fitbounds="locations", visible=False, row=2, col=2)
        fig.update_geos(fitbounds="locations", visible=False, row=2, col=3)
    else:
        fig.add_trace(figures5[i].data[0], row=3, col=1)
        fig.add_trace(figures31[i].data[0], row=3, col=2)
        fig.add_trace(figures90[i].data[0], row=3, col=3)
        fig.update_geos(fitbounds="locations", visible=False, row=3, col=1)
        fig.update_geos(fitbounds="locations", visible=False, row=3, col=2)
        fig.update_geos(fitbounds="locations", visible=False, row=3, col=3)


# Update layout for the subplot
fig.update_layout(
    title_text="Disease Simulation in Georgia",
    height=900,
    showlegend=False,
    geo=dict(bgcolor='rgb(229,229,229)'),
    paper_bgcolor='rgb(229,229,229)',
    title_font_size=20
)
# Show the subplot
fig.show()

# data = pd.DataFrame(code.main(90, "init_state.csv"), columns=['S', 'I', 'R'])
# Svalues = data["S"].tolist()
# Ivalues = data["I"].tolist()
# Rvalues = data["R"].tolist()

# # Create S,I, and R DataFrames for Plotly
# Schoropleth_data = pd.DataFrame({'FIPS': fips, 'Values': Svalues})
# Ichoropleth_data = pd.DataFrame({'FIPS': fips, 'Values': Ivalues})
# Rchoropleth_data = pd.DataFrame({'FIPS': fips, 'Values': Rvalues})

# # Create the choropleth map
# Sfig = px.choropleth(
#     Schoropleth_data,
#     geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
#     locations='FIPS',
#     color='Values',
#     color_continuous_scale="Viridis",  # Built-in color scale
#     title="Susceptible Population in Georgia",
#     labels={'Values': 'Susceptible Population'}
# )
# Ifig = px.choropleth(
#     Ichoropleth_data,
#     geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
#     locations='FIPS',
#     color='Values',
#     color_continuous_scale="Viridis",  # Built-in color scale
#     title="Infected Population in Georgia",
#     labels={'Values': 'Infected Population'}
# )
# Rfig = px.choropleth(
#     Rchoropleth_data,
#     geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
#     locations='FIPS',
#     color='Values',
#     color_continuous_scale="Viridis",  # Built-in color scale
#     title="Recovered Population in Georgia",
#     labels={'Values': 'Recovered Population'}
# )

# # Update layout for better visualization
# Sfig.update_geos(fitbounds="locations", visible=False)
# Ifig.update_geos(fitbounds="locations", visible=False)
# Rfig.update_geos(fitbounds="locations", visible=False)

# Create a subplot with 3 rows and 1 column
# fig = make_subplots(
#     rows=3, cols=1,
#     subplot_titles=("Susceptible Population", "Infected Population", "Recovered Population"),
#     specs=[[{"type": "choropleth"}], [{"type": "choropleth"}], [{"type": "choropleth"}]]
# )
# # Add the choropleth maps to the subplots  
# fig.add_trace(Sfig.data[0], row=1, col=1)
# fig.add_trace(Ifig.data[0], row=2, col=1)
# fig.add_trace(Rfig.data[0], row=3, col=1)

# # Update layout for each subplot to zoom into Georgia
# fig.update_geos(fitbounds="locations", visible=False, row=1, col=1)
# fig.update_geos(fitbounds="locations", visible=False, row=2, col=1)
# fig.update_geos(fitbounds="locations", visible=False, row=3, col=1)

# # Update layout for the subplot
# fig.update_layout(
#     title_text="Disease Simulation in Georgia",
#     height=900,
#     showlegend=False,
#     geo=dict(bgcolor='rgb(229,229,229)'),
#     paper_bgcolor='rgb(229,229,229)',
#     title_font_size=20
# )
# # Show the subplot
# fig.show()