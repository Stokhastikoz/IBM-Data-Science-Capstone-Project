# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

dropdown_options=[{"label": site, "value": site} for site in spacex_df["Launch Site"].unique()]
dropdown_options=[{"label": "All Sites", "value": "ALL"}] + dropdown_options

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=dropdown_options,
                                             value="ALL",
                                             placeholder="Select a Launch Site",
                                             searchable=True,
                                             #style={"width": "80%", "padding": "3px", "font-size": "20px", "textAlign": "center"}
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={i: i for i in range(0, 10001, 1000)},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df.groupby("Launch Site")["class"].sum().reset_index()
        fig = px.pie(filtered_df,
        values='class', 
        names='Launch Site', 
        title='Total Successful Launches by Site'
        )
        return fig
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"]==entered_site]["class"]
        fig = px.pie(filtered_df,
        values=filtered_df.value_counts().values, 
        names=filtered_df.value_counts().index, 
        title="Total Successful Launches at Site {}".format(entered_site)
        )
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, entered_payload):
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df["Payload Mass (kg)"].between(entered_payload[0], entered_payload[1])]
        fig = px.scatter(filtered_df,
        x="Payload Mass (kg)", 
        y="class", 
        color="Booster Version Category",
        hover_data=["Launch Site"],
        title="Correlation Between Payload and Success for all Sites"
        )
        return fig
    else:
        filtered_df = spacex_df[spacex_df["Payload Mass (kg)"].between(entered_payload[0], entered_payload[1])]
        pl_df = filtered_df[filtered_df["Launch Site"]==entered_site]
        fig = px.scatter(pl_df,
        x="Payload Mass (kg)", 
        y="class", 
        color="Booster Version Category",
        hover_data=["Launch Site"],
        title="Correlation Between Payload and Success at Site {}".format(entered_site)
        )
        return fig

# Run the app 
if __name__ == '__main__':
    app.run_server()
 