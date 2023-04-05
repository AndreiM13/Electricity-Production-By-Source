import dash
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output
import requests
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import plotly.express as px



#Datasets
url = 'https://raw.githubusercontent.com/AndreiM13/Electricity_Production_By_Source/main/Electricity_Production_By_Source_Clean.csv'
response = requests.get(url)
data = response.content
df = pd.read_csv(url)

url2 = 'https://raw.githubusercontent.com/AndreiM13/Electricity_Production_By_Source/main/Electricity_Production_By_Source_Continet_Clean.csv'
response2 = requests.get(url2)
data2 = response2.content
df2 = pd.read_csv(url2)


#Interactive Components


resources_energy = ['Coal', 'Gas', 'Hydro', 'Renewables', 'Solar', 'Oil', 'Wind', 'Nuclear']

electricity_options = [
    {'label': 'Coal', 'value': 'Coal'},
    {'label': 'Gas', 'value': 'Gas'},
    {'label': 'Hydro', 'value': 'Hydro'},
    {'label': 'Renewables', 'value': 'Renewables'},
    {'label': 'Solar', 'value': 'Solar'},
    {'label': 'Oil', 'value': 'Oil'},
    {'label': 'Wind', 'value': 'Wind'},
    {'label': 'Nuclear', 'value': 'Nuclear'},
]


country_options = [
    dict(label='' + country, value=country)
    for country in df['Country'].unique()]


dropdown_country=dcc.Dropdown(
                        id='country_drop', 
                        options=country_options, 
                        value=['Portugal'], 
                        multi=True
                    )
slider_year = dcc.RangeSlider(
                id='year_slider',
                min=2000,
                max=2020,
                value=[2010, 2020],  
                marks={
                    '2000': '2000',
                    '2005': '2005',
                    '2010': '2010',
                    '2015': '2015',
                    '2020': '2020'
                },
                step=1,
            )


radio_items = dcc.RadioItems(
    id='electricity_options_radio',
    options=electricity_options,
    value='Coal',
    labelStyle={'display': 'block', 'margin': '10px 0'},
    inputStyle={'marginRight': '5px'},
    style={'fontFamily': 'Arial', 'fontSize': '20px', 'color': '#333'}
)

continent_options = [    'Europe',    'Africa',    'North America',    'Other Asia & Pacific',    'South & Central America',    'Middle East',]

continet_dropdown = dcc.Dropdown(
    id='continent_drop',
    options=[{'label': c, 'value': c} for c in continent_options],
    value='Europe'
)

years = [year for year in range(2000, 2021)]  

year_dropdown_graph3 = dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in years],
            value=2000
        )


dropdown_graph3 = dcc.Dropdown(
            id='resource-dropdown',
            options=[   {'label': 'Coal', 'value': 'Coal'},
                        {'label': 'Gas', 'value': 'Gas'},
                        {'label': 'Hydro', 'value': 'Hydro'},
                        {'label': 'Renewables', 'value': 'Renewables'},
                        {'label': 'Solar', 'value': 'Solar'},
                        {'label': 'Oil', 'value': 'Oil'},
                        {'label': 'Wind', 'value': 'Wind'},
                        {'label': 'Nuclear', 'value': 'Nuclear'}],
            value='Coal'
        )

#Layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, 'styles.css'])



server = app.server

app.layout = html.Div(
    [
        html.Div(
            html.H1('Electricity Production By Source'),
            className='H1'
        ),
        html.Div(
            html.P('This dashboard was created to show the evolution in time of electricity production by source, country, and also for continents'),
            className='first-paragraph'
        ),
        html.Div(
            [
                html.Div(
                    dcc.Graph(id='graph1'),
                    className='graph-container'
                ),
                html.Div(
                    [
                        dropdown_country,
                        radio_items,
                        slider_year
                    ],
                    className='tab-container'
                ),
            ],
            className='app-container'
        ),
        html.Div([
            html.H2('Resources Consumption by Continent', className='H2'),
            html.Div(
                [continet_dropdown, dcc.Graph(id='graph2')],
                className='graph2-container'
            )
        ]),
        html.Div([
            html.H3("Map of Electricity Production by Country", className='H3'),
            html.Div([
                html.Label("Select Year"),
                year_dropdown_graph3,
            ], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([
                html.Label("Select Electricity Resource"),
                dropdown_graph3,
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
            dcc.Graph(id='graph3'),
        ], className='graph3-container'),
        
       html.Div([html.Footer([
        html.P('Copyright © 2023'),
        html.P('This dashboard was created by our group as project'),
        html.P('As dataset we used: https://www.kaggle.com/datasets/prateekmaj21/electricity-production-by-source-world/code?select=Electricity_Production_By_Source.csv')
    ], className='footer')])

    ]
)


#first callback for first graph
@app.callback(
    Output('graph1', 'figure'),
    [Input('country_drop', 'value'),
      Input('electricity_options_radio', 'value'),
      Input('year_slider', 'value')]
)

#first graph
def update_graph(countries, electricity_options, year):
    filtered_by_year_df = df[(df['Year'] >= year[0]) & (df['Year'] <= year[1])]

    scatter_data = []

    for country in countries:
        filtered_by_year_and_country_df = filtered_by_year_df.loc[filtered_by_year_df['Country'] == country]

        temp_data = dict(
            type='scatter',  # change to 'line' for a line chart
            mode='lines+markers',  # specify that you want markers on the line
            y=filtered_by_year_and_country_df[electricity_options],
            x=filtered_by_year_and_country_df['Year'],
            name=country
        )

        scatter_data.append(temp_data)

    scatter_layout = dict(
        xaxis=dict(title='Year',
                   tickfont=dict(color='#4292C6')),
        yaxis=dict(title=electricity_options,
                   tickfont=dict(color='#4292C6')),  
        plot_bgcolor='rgba(0, 0, 0, 0.7)', # set the plot background color to a semi-transparent black
        paper_bgcolor='rgba(0, 0, 0, 0)', # set the paper background color to transparent
        height=650,
        width = 800,
        font=dict(color='#4292C6'), 
        legend=dict(orientation="h", y=1.05) # set the legend orientation and position
    )



    fig = go.Figure(data=scatter_data, layout=scatter_layout)

    return fig


#callback for second graph
@app.callback(
    Output('graph2', 'figure'),
    [Input('continent_drop', 'value')]
)

#second graph
def update_graph2(continent):
    # Create the bar chart
    fig2 = px.bar(
        df2[df2['Continent'] == continent],
        x="Year",
        y=resources_energy,
        color_discrete_sequence=['#084594', '#2171B5', '#4292C6', '#6BAED6', '#9ECAE1', '#C6DBEF', '#DEEBF7', '#F7FBFF'],
        category_orders={"resources_energy": resources_energy},
        barmode='stack'
    )

      # Update the figure layout
    fig2.update_layout(
        title='',
        xaxis_title='Year',
        yaxis_title='Resources Consumption',
        margin=dict(l=30, r=30, t=30, b=30),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            title_font=dict(color='#4292C6'),
            tickfont=dict(color='#4292C6')
        ),
        xaxis=dict(
            title_font=dict(color='#4292C6'),
            tickfont=dict(color='#4292C6')
        ),
        legend=dict(
            title_font=dict(color='#4292C6'),
            font=dict(color='#4292C6')
        )
    )




    return fig2


#callback for third graph


@app.callback(
    Output('graph3', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('resource-dropdown', 'value')]
)
def update_graph3(year_value, resource_value):
    df_filtered = df[df['Year'] == year_value]
    fig3 = update_figure4(df_filtered, resource_value)
    return fig3

def update_figure4(df, resource_value):
    if resource_value == 'Coal':
        z = df['Coal']
        colorbar_title = 'TW'
        title_text = 'Electricity Production by Country (Coal)'
    elif resource_value == 'Gas':
        z = df['Gas']
        colorbar_title = 'TW'
        title_text = 'Electricity Production by Country (Gas)'
    elif resource_value == 'Hydro':
        z = df['Hydro']
        colorbar_title = 'TW'
        title_text = 'Electricity Production by Country (Hydro)'
    elif resource_value == 'Oil':
         z = df['Oil']
         colorbar_title = 'TW'
         title_text = 'Electricity Production by Country (Oil)'
    elif resource_value == 'Renewables':
         z = df['Renewables']
         colorbar_title = 'TW'
         title_text = 'Electricity Production by Country (Renewables)'
    elif resource_value == 'Solar':
          z = df['Solar']
          colorbar_title = 'TW'
          title_text = 'Electricity Production by Country (Solar)'
    elif resource_value == 'Wind':
          z = df['Wind']
          colorbar_title = 'TW'
          title_text = 'Electricity Production by Country (Wind)'
    elif resource_value == 'Nuclear':
          z = df['Nuclear']
          colorbar_title = 'TW'
          title_text = 'Electricity Production by Country (Nuclear)'
        
    else :
        z = df['Year']
        colorbar_title = 'Electricity Production by Country'
        title_text = 'Electricity Production by Country'
        

    fig4 = go.Figure(data=go.Choropleth(
        locations=df['Code'],
        z=z,
        text=df['Country'],
        colorscale='Blues',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix='',
        colorbar_title=colorbar_title,
    ))

    fig4.update_layout(
        title_text=title_text,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
            bgcolor='rgba(0,0,0,0)'
        ),
        annotations=[dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            showarrow=False
        )],
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )



    return fig4



if __name__ == '__main__':
    app.run_server(debug=True)






