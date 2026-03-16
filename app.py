from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = px.data.gapminder()

all_countries = sorted(df['country'].unique())
all_years = sorted(df['year'].unique())
numeric_measures = ['pop', 'gdpPercap', 'lifeExp']
measure_names = {
    'pop': 'Население',
    'gdpPercap': 'ВВП на душу',
    'lifeExp': 'Продолжительность жизни'
}

app = Dash(__name__)
server = app.server

CONTROL_STYLE = {'marginBottom': '5px', 'fontSize': '12px'}
LABEL_STYLE = {'fontWeight': 'bold', 'marginTop': '5px', 'marginBottom': '2px', 'fontSize': '12px'}

app.layout = html.Div([
    html.H1('Глобальная статистика стран (Gapminder)', 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginTop': '5px', 
                   'marginBottom': '5px', 'fontSize': '24px'}),
    
    html.Div([
        html.Div('Выберите год:', style={'fontWeight': 'bold', 'display': 'inline-block', 
                                         'marginRight': '10px', 'fontSize': '14px'}),
        dcc.Dropdown(
            id='year-selector',
            options=[{'label': str(year), 'value': year} for year in all_years],
            value=2007,
            clearable=False,
            style={'width': '200px', 'display': 'inline-block', 'verticalAlign': 'middle'}
        )
    ], style={'textAlign': 'center', 'marginBottom': '10px'}),
    
    html.Div([
        html.Div([
            html.H4('1. Сравнение стран', style={'marginTop': '0', 'marginBottom': '5px', 
                                                  'fontSize': '16px'}),
            html.Div([
                html.Div('Страны:', style=LABEL_STYLE),
                dcc.Dropdown(
                    id='country-selector',
                    options=[{'label': c, 'value': c} for c in all_countries],
                    value=['Canada', 'Germany', 'China'],
                    multi=True,
                    style=CONTROL_STYLE
                ),
                html.Div('Показатель:', style=LABEL_STYLE),
                dcc.RadioItems(
                    id='y-axis-selector',
                    options=[{'label': measure_names[m], 'value': m} for m in numeric_measures],
                    value='lifeExp',
                    inline=True,
                    labelStyle={'marginRight': '10px', 'fontSize': '12px'}
                ),
            ], style={'marginBottom': '5px'}),
            dcc.Graph(id='line-chart', style={'height': '220px'})
        ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top', 
                  'padding': '5px', 'boxSizing': 'border-box'}),
        
        html.Div([
            html.H4('2. Пузырьковая диаграмма', style={'marginTop': '0', 'marginBottom': '5px', 
                                                        'fontSize': '16px'}),
            html.Div([
                html.Div('Ось X:', style=LABEL_STYLE),
                dcc.Dropdown(
                    id='bubble-x',
                    options=[{'label': measure_names[m], 'value': m} for m in numeric_measures],
                    value='gdpPercap',
                    style=CONTROL_STYLE
                ),
                html.Div('Ось Y:', style=LABEL_STYLE),
                dcc.Dropdown(
                    id='bubble-y',
                    options=[{'label': measure_names[m], 'value': m} for m in numeric_measures],
                    value='lifeExp',
                    style=CONTROL_STYLE
                ),
                html.Div('Радиус:', style=LABEL_STYLE),
                dcc.Dropdown(
                    id='bubble-size',
                    options=[{'label': measure_names[m], 'value': m} for m in numeric_measures],
                    value='pop',
                    style=CONTROL_STYLE
                ),
            ], style={'marginBottom': '5px'}),
            dcc.Graph(id='bubble-chart', style={'height': '220px'})
        ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top', 
                  'padding': '5px', 'boxSizing': 'border-box'})
    ]),
    
    html.Div([
        html.Div([
            html.H4('3. Топ-15 стран по населению', style={'marginTop': '5px', 'marginBottom': '5px', 
                                                            'fontSize': '16px'}),
            dcc.Graph(id='top15-bar-chart', style={'height': '200px'})
        ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top', 
                  'padding': '5px', 'boxSizing': 'border-box'}),
        
        html.Div([
            html.H4('4. Население по континентам', style={'marginTop': '5px', 'marginBottom': '5px', 
                                                           'fontSize': '16px'}),
            dcc.Graph(id='continent-pie-chart', style={'height': '200px'})
        ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top', 
                  'padding': '5px', 'boxSizing': 'border-box'})
    ])
], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '5px', 
          'height': '95vh', 'overflow': 'hidden'})  

@callback(
    Output('line-chart', 'figure'),
    [Input('country-selector', 'value'),
     Input('y-axis-selector', 'value')]
)
def update_line_chart(selected_countries, y_axis):
    if not selected_countries:
        return px.line(title='Выберите страны')
    filtered_df = df[df['country'].isin(selected_countries)]
    fig = px.line(filtered_df, x='year', y=y_axis, color='country',
                  title=f'{measure_names[y_axis]} по годам',
                  labels={y_axis: measure_names[y_axis], 'year': 'Год'})
    fig.update_layout(margin=dict(l=40, r=20, t=40, b=20), height=200)
    return fig

@callback(
    Output('bubble-chart', 'figure'),
    [Input('bubble-x', 'value'),
     Input('bubble-y', 'value'),
     Input('bubble-size', 'value'),
     Input('year-selector', 'value')]
)
def update_bubble_chart(x_axis, y_axis, size_axis, selected_year):
    df_year = df[df['year'] == selected_year]
    fig = px.scatter(df_year, x=x_axis, y=y_axis, size=size_axis, 
                     hover_name='country', color='continent',
                     log_x=True, size_max=40,
                     title=f'{selected_year}: {measure_names[x_axis]} vs {measure_names[y_axis]}',
                     labels={x_axis: measure_names[x_axis], y_axis: measure_names[y_axis]})
    fig.update_layout(margin=dict(l=40, r=20, t=40, b=20), height=200)
    return fig

@callback(
    [Output('top15-bar-chart', 'figure'),
     Output('continent-pie-chart', 'figure')],
    [Input('year-selector', 'value')]
)
def update_year_charts(selected_year):
    df_year = df[df['year'] == selected_year]
    
    top15 = df_year.nlargest(15, 'pop')
    fig_bar = px.bar(top15, x='country', y='pop', color='continent',
                     title=f'Топ-15 стран ({selected_year})',
                     labels={'pop': 'Население', 'country': ''})
    fig_bar.update_layout(margin=dict(l=40, r=20, t=40, b=50), height=180, xaxis_tickangle=-45)
    
    continent_pop = df_year.groupby('continent', as_index=False)['pop'].sum()
    fig_pie = px.pie(continent_pop, values='pop', names='continent',
                     title=f'Население по континентам ({selected_year})',
                     hole=0.3)
    fig_pie.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=180)
    
    return fig_bar, fig_pie

if __name__ == '__main__':
    app.run(debug=True)