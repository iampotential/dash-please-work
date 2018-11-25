import os
from random import randint

import plotly.plotly as py
import plotly.graph_objs as go

import flask
import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd

# Setup the app
# Make sure not to change this file name or the variable names below,
# the template is configured to execute 'server' on 'app.py'
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server)

df = pd.read_csv('nfl929.csv')
home_dogs = pd.read_csv('nfl_home_dogs_929.csv')
home_favs = pd.read_csv('home_favs929.csv')
df['over_base'] = np.where(df['total']>df['over_under_line'],100,-110)
df['under_base'] = np.where(df['total']<df['over_under_line'],100,-110)
df['oucredit'] = np.where(df['total']==df['over_under_line'],110,0)
df['over_result']=df['over_base']+df['oucredit']
df['under_result']=df['under_base']+df['oucredit']
ou = ['over_result','under_result']
color = '#ffffff'
colors = {
    'background': '	#ffffff',
    'text': '#7FDBFF'
}
css1 = 'https://codepen.io/tonkotsuboy/pen/xaMVpo.css'

wind = []
for i in range(0,42,2):
    wind.append({'label':i,'value':i})
home_fav_options = [{'label':'home underdog','value': 0},
                     {'label':'home favorite','value': 1}]

home_dog_spread_options = []

for i in range(0,24,1):
    home_dog_spread_options.append({'label':i,'value':i})
temp = []
for i in range(-20,100,5):
    temp.append({'label':i,'value':i})
#    html.Div([
#        html.Div(dcc.Graph(animate=True, id='graph1'), className="six columns"),
 #       html.Div(dcc.Graph(animate=True, id='graph2'), className="six columns")
 #   ], className="row"),
over_under_options = []
for i in ou:
    over_under_options.append({'label':i,'value':i})
team_options = []
for i in df.team_favorite_id.unique():
    team_options.append({'label':i,'value':i})
week_options = []
for i in df.schedule_week.unique():
    week_options.append({'label':i,'value':i})
away_team_options = []
for i in df.team_away.unique():
    away_team_options.append({'label': i,'value':i})
home_team_options = []
for i in df.team_away.unique():
    home_team_options.append({'label':i,'value':i})
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '10px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '16px'
}
text_style = dict(family='Courier New, monospace', size=18, color='#7f7f7f')
app.layout = html.Div([
        html.H1('American Football Data'),
        dcc.Tabs(id="tabs", 
                 children=[
        dcc.Tab(label='Over under Data',
                style=tab_style, 
                selected_style=tab_selected_style, 
                children=[
html.Div([
                                   html.Div(
                                   html.H2('The charts below show weekly results of taking the over or the under when the over under line is greater than the selected amount. Each bar represents a specific week. After week 17, they are playoff games so the sample size diminishes quickly',
                                             style=text_style),
                                           className='twelve columns'),
                                   ],
    className='row'),
                


                                                                                        
       html.Div([
               html.Div(
                       dcc.Graph(id='new_graph12'),
                           className="six columns"),
    html.Div(
            dcc.Graph(id='new_graph13'),
             className="six columns")],
    className="row"),

                                            html.Div([

                                       

        html.Div(
                dcc.Graph(id='new_graph222'),
                 className="eight columns"),
                html.Div(id='OU_Data_output',
                         style={'color': '#119DFF', 'fontSize': 22,'fontWeight': 'bold'},
                className='four columns')],
                 className='row'),
                                        html.Div([
                html.Div(dcc.Slider(id='over_under_line',
                                    min=df['over_under_line'].min(),
                                    max=df['over_under_line'].max(),
                                    step=0.5,vertical=False,
                                    dots=True,included=True,
                                    updatemode='drag',value=40),
    className='three')],
    className="popover-list"),]), 
             ############################################################################
                     dcc.Tab(
                             label='Spread data',
                             style=tab_style, 
                selected_style=tab_selected_style,
            children=[
                    html.Div([
                                   html.Div(
                                   html.H2('Use the slider under the first graph to update charts. Data is for all games since 1999',
                                             style=text_style),
                                           className='twelve columns'),
                                   ],
    className='row'),
                    html.Div([
                            html.Div(
                                    dcc.Graph( id='graph6'),
                                         className="six columns"),
                                html.Div(
                                        dcc.Graph(id='spread_data_graph'), 
                                      className="six columns")],           
             className="row"),

                     html.Div([
                             html.Div(dcc.Slider(
                                     id='home_dog_spread_options',
                                     min=0,max=18,
                                  step=0.5,
                                  vertical=False,
                                  dots=True,
                                  included=True,
                                  updatemode='drag',
                                  value=1,
                                  ),
    style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '10px',
    'fontWeight': 'bold',
    'color': 'green',
},
                                      className="four columns")], 
             className="row"),
            html.Div([
                    html.Div(
                            id='line_slider_output',
                            style=text_style),
                            
    html.Div(
            id='week_dropdown_output',
             
             className='seven columns'),
             ],
             className="row"),
                       html.Div([
                               html.Div(
                                       dcc.Graph(id='graph5'), 
                                      className="six columns"),
    html.Div(
            dcc.Graph(id='spread_data_graph3'), 
                                      className="six columns"),
             ],
             className="row")]), 
############################################################################################
    
    
                  dcc.Tab(
                          label='Team data',
                          style=tab_style, 
                          selected_style=tab_selected_style,
                          children=[
                   
                           html.Div([
                                   html.Div(
                                   html.H2('Select Teams from dropdowns to see home and away performance against the spread',
                                             style=text_style),
                                           className='twelve columns'),
                                   ],
    className='row'),
                                
                           
                                                     html.Div([
                                                             html.Div(
                                 dcc.Dropdown(id='team_options',
                                                            style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '10px',
    'fontWeight': 'bold',
    'verticalAlign' : 'middle'
},
                              options=team_options,
                              value='NE',
                              multi=False),
    className="six columns"), 
                           html.Div(
                                   dcc.Dropdown(id='2nd_team_options',
                                                             style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '10px',
    'fontWeight': 'bold',
    'verticalAlign' : 'middle'
},
                              options=team_options,
                              value='DAL',
                              multi=False),
    className="six columns")],
    className='row'),                            
    html.Div([
    html.Div(
            dcc.Graph(id='team1_2'),
            className="six columns"),
    html.Div(
            dcc.Graph( id='team2_2'),
            className="six columns"),],
             className="row"),

                   html.Div([
                           html.Div(
                                   dcc.Graph(id='team1_1'),
                                      className="six columns"),
    html.Div(
            dcc.Graph( id='team2_1'),
             className="six columns")],
             className="row"),  
       ]),
###########################################################################################################
             dcc.Tab(
                     label='Prediction Center',
                     style=tab_style, 
                     selected_style=tab_selected_style,
                     children=[
                             html.Div([
                                   html.Div(
                                   html.H2('This page is currently under construction. It will be finished once I know what I am doing',
                                             style=text_style),
                                           className='twelve columns'),
                                   ],
    className='row'),
                             html.Div([
                                     html.Label('Opening spread',
                                                className='two columns'),
                                         html.Div(
                                                 dcc.Dropdown(id='Spread_line_ml',
                                                             style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '10px',
    'fontWeight': 'bold',
    'verticalAlign' : 'middle'
},
                              options=home_dog_spread_options,
                              value=0,
                              placeholder='Select your spread',
                              multi=False),
    className="four columns"),
            html.Label('Temprature to start game',
                       className='two columns'),
            html.Div(
                    dcc.Dropdown(id='temp_ml',
                                                             style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '10px',
    'fontWeight': 'bold',
    'verticalAlign' : 'middle'
},
                              options=temp,
                              value=35,
                              multi=False),
    className="four columns")],
    className='row'),
            html.Div([
                    html.Label('Wind speed at game start',
                               className='two columns'),
                      html.Div(
                              dcc.Dropdown(id='wind_ml',
                                                             style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '10px',
    'fontWeight': 'bold',
    'verticalAlign' : 'middle'
},
                              options=wind,
                              value=0,
                              multi=False),
    className="four columns"),
            html.Label('home underdog or home fav',
                       className='two columns'),
            html.Div(
                    dcc.Dropdown(id='home_underdog_ml',
                                                             style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '10px',
    'fontWeight': 'bold',
    'verticalAlign' : 'middle'
},
                              options=home_fav_options,
                              value=0,
                              multi=False),
            
    className="four columns"),
            
            html.Label('Over under line selector',
                       className='one columns'),
                            html.Div(dcc.Slider(id='ou_line_ml',
                                    min=df['over_under_line'].min(),
                                    max=df['over_under_line'].max(),
                                    step=0.5,
                                    vertical=False,
                                    dots=True,
                                    included=True,
                                    updatemode='drag',
                                    value=40),
    className='four columns'),
    ],
    className='row'),
            html.Div([
                    html.Div(id='ml_output',
                             className='four columns'),
                      ],
                                 className='row'),
                     ]),
             
             ]),
                   ],
                    style={'padding': '20px 20px 20px 20px'})
####callbacks#######
                    ###teams 
@app.callback(Output('team1_1', 'figure'),
              [Input('team_options', 'value')])
def update_figure(selected_team):
    filtered_df = home_dogs[home_dogs['team_home'] == selected_team]
    traces = []
    for i in filtered_df['team_home'].unique():
        df_by_team = filtered_df[filtered_df['team_home'] == i]
    traces.append(go.Scatter(
            x=df_by_team['schedule_date'],
            y=df_by_team['result'].cumsum(),
            text=df_by_team['team_away']+'@'+df_by_team['team_home'],
            opacity=0.7,
            mode='lines+markers',
         marker = dict(
        color = df_by_team['schedule_week'],
        colorscale='Viridis',
        size = 5+(df_by_team['spread_favorite']*-1))
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            yaxis={'title': 'USD'},
            autosize=True,
            xaxis=dict(tickfont=dict(family="Times New Roman",size=14)),
            title='{} as a home underdogs ATS'.format(selected_team),
            plot_bgcolor=color,
            hovermode='closest',
            
        )
    }
@app.callback(Output('team2_1', 'figure'),
              [Input('2nd_team_options', 'value')])
def update_figure55(selected_team):
    filtered_df = home_dogs[home_dogs['team_away'] == selected_team]
    traces = []
    for i in filtered_df['team_away'].unique():
        df_by_team = filtered_df[filtered_df['team_away'] == i]
    traces.append(go.Scatter(
            x=df_by_team['schedule_date'],
            y=df_by_team['away_Favs'].cumsum(),
            text=df_by_team['team_away']+'@'+df_by_team['team_home'],
            opacity=0.7,
            mode='lines+markers',
         marker = dict(
        color = df_by_team['schedule_week'],
        colorscale='Viridis',
        size = 5+(df_by_team['spread_favorite']*-1))
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            yaxis={'title': 'USD'},
            autosize=True,
            xaxis=dict(tickfont=dict(family="Times New Roman",size=14)),
            title='{} as a visiting favorite ATS'.format(selected_team),
            plot_bgcolor=color,
            hovermode='closest',
            
        )
    }
@app.callback(Output('team1_2', 'figure'),
              [Input('team_options', 'value')])
def update_figure2(selected_team):
     filtered_df = home_favs[home_favs['team_home'] == selected_team]
     traces2 = []
     for i in filtered_df['team_home'].unique():
        df_by_team = filtered_df[filtered_df['team_home'] == i]
     traces2.append(go.Scatter(
            x=df_by_team['schedule_date'],
            y=df_by_team['result'].cumsum(),
            text=df_by_team['team_away']+'@'+df_by_team['team_home'],
            opacity=0.7,
            mode='lines+markers',
         marker = dict(
        color = df_by_team['schedule_week'],
        colorscale='Viridis',
        size = 5+(df_by_team['spread_favorite']*-1))
        ))

     return {
        'data': traces2,
        'layout': go.Layout(
            yaxis={'title': 'rolling result of taking team as a home favorite'},
            title='{} as a home favorite ATS'.format(selected_team),
            xaxis=dict(tickfont=dict(family="Times New Roman",size=14)),
            plot_bgcolor=color,
            autosize=True,
            hovermode='closest',
        )
    }

@app.callback(Output('team2_2', 'figure'),
              [Input('2nd_team_options', 'value')])
def update_figur2e2(selected_team):
     filtered_df = home_favs[home_favs['team_away'] == selected_team]
     traces2 = []
     for i in filtered_df['team_away'].unique():
        df_by_team = filtered_df[filtered_df['team_away'] == i]
     traces2.append(go.Scatter(
            x=df_by_team['schedule_date'],
            y=df_by_team['away_dogs'].cumsum(),
            text=df_by_team['team_away']+'@'+df_by_team['team_home'],
            opacity=0.7,
            mode='lines+markers',
         marker = dict(
        color = df_by_team['schedule_week'],
        colorscale='Viridis',
        size = 5+(df_by_team['spread_favorite']*-1))
        ))

     return {
        'data': traces2,
        'layout': go.Layout(
            yaxis={'title': 'rolling result of taking team as a home favorite'},
            title='{} as an away underdog ATS'.format(selected_team),
            xaxis=dict(tickfont=dict(family="Times New Roman",size=14)),
            plot_bgcolor=color,
            autosize=True,
            hovermode='closest',
        )
    }


@app.callback(Output('graph5','figure'),
              [Input('home_dog_spread_options', 'value')])
def update_figure3(spread):
    filtered_df = home_dogs[home_dogs['spread_favorite']<spread*-1]
    traces3 = []
    traces3.append(go.Scatter(
            x=filtered_df['schedule_date'],
            y=filtered_df['result'].cumsum(),
            text=filtered_df['team_away']+'@'+filtered_df['team_home'],
            opacity=0.7,
            mode='markers',
            marker = dict(
                    color = filtered_df['result'].cumsum(),
                colorscale='Viridis',


        )))
    return {
        'data': traces3,
        'layout': go.Layout(
            yaxis={'title': 'diffrence from spead'},
            autosize=True,
            title='Home underdogs when the spread is greater than {}'.format(spread),
            xaxis=dict(tickfont=dict(family="Times New Roman",size=14)),
            plot_bgcolor=color,
            hovermode='closest'
        )
    }


@app.callback(Output('ml_output', 'children'),
                      [Input('Spread_line_ml', 'value'),
                      Input('wind_ml', 'value'),
                      Input('temp_ml', 'value'),
                      Input('ou_line_ml', 'value')])
def ml_result(spread,wind,temp,ou_line):
    x00 = float(spread)*-1
    x01 = float(wind)
    x02 = float(temp)
    x03 = float(ou_line)

    #array = [x00,x01,x02,1.00,x03,x04]
    array = [x00, 6, x01,x02,1,x03]
    return array



def update_figure4(selected_week):
    filtered_df = df[df['schedule_week'] == selected_week]
    traces5 = []
    for i in filtered_df['schedule_week'].unique():
        df_by_team = filtered_df[filtered_df['schedule_week']==i]
    traces5.append(go.Scatter(
            x=df_by_team['schedule_date'],
            y=df_by_team['result_total_plus_minus_two'].cumsum(),
            opacity=0.7,
            text=df_by_team['team_away']+'@'+df_by_team['team_home'],
            mode='lines+markers',
            marker = dict(color = 'reds',size = 5+(df_by_team['spread_favorite']*-1),
        )))
    

    return {
        'data': traces5,
        'layout': go.Layout(
            title=df_by_team['schedule_week'],
            xaxis=dict(tickfont=dict(family="Times New Roman",size=14)),
            plot_bgcolor=color,
            hovermode='closest'
        )
    }


@app.callback(Output('OU_Data_output', 'children'),
              [Input('over_under_line', 'value')])
def ou_output(ou):
    filtered_df = df[df['over_under_line'] >ou]
    filtered_df2 = df[df['over_under_line'] <ou]
    over_len = len(filtered_df)
    o_diff = filtered_df['oudiff'].mean()
    u_diff = filtered_df2['oudiff'].mean()
    o_diff_sd = filtered_df['oudiff'].std()
    u_diff_sd = filtered_df2['oudiff'].std()
    over_df = len(df[df['oudiff']>0])
    under_df = len(df[df['oudiff']<0])
    ties = len(df[df['oudiff']==0])
    under_len = len(filtered_df2)
    total_len = over_len + under_len
    line1 =  '{} total games over {} and {} games under'.format(over_len,ou,under_len)
    line2 = 'Of the {} games over {} the average was {} points from the total and a standard deviation from the line of {}'.format(over_len,ou,round(o_diff,3),round(o_diff_sd,3))
    line3 = 'Of the {} games under {} the average was {} points from the total and had a standard deviation of {}'.format(under_len,ou,round(u_diff,3),round(u_diff_sd,3))
    line4 = 'Of the {} total games, {} went over and {} went under. {} hit exactly on the over under line'.format(total_len,over_df,under_df,ties)
    return '{}. {}. {}. {}.'.format(line1,line2,line3,line4)
@app.callback(Output('new_graph222', 'figure'),
              [Input('over_under_line', 'value')])
def update_figure_new_222(line):
    filtered_df = df[df['over_under_line'] >line]
    traces35 = []
    traces35.append(go.Scatter(
            x=filtered_df['dates'],
            y=filtered_df['over_result'].cumsum(),
            text=filtered_df['team_away']+'@'+filtered_df['team_home'],
            opacity=0.7,
            name='over result > {}'.format(line),
            mode='lines',

        ))
    traces35.append(go.Scatter(
            x=filtered_df['dates'],
            y=filtered_df['under_result'].cumsum(),
            text=filtered_df['team_away']+'@'+filtered_df['team_home'],
            opacity=0.7,
            name='under result > {}'.format(line),
            mode='lines',

        ))
    filtered_df2 = df[df['over_under_line'] <line]

    traces35.append(go.Scatter(
            x=filtered_df2['dates'],
            y=filtered_df2['under_result'].cumsum(),
            text=filtered_df2['team_away']+'@'+filtered_df2['team_home'],
            opacity=0.7,
            name='under result < {}'.format(line),
            mode='lines',

        ))
    traces35.append(go.Scatter(
            x=filtered_df2['dates'],
            y=filtered_df2['over_result'].cumsum(),
            text=filtered_df2['team_away']+'@'+filtered_df2['team_home'],
            opacity=0.7,
            name='over result < {}'.format(line),
            mode='lines',

        ))

    return {
        'data': traces35,
        'layout': go.Layout(
            yaxis={'title': 'USD'},
            title='Over/under results for all games since 1999'.format(line),
            xaxis=dict(title='Use slider below',
                       tickfont=dict(family="Times New Roman",size=14)),
            plot_bgcolor=color,
            hovermode='closest',

        )}


   
        

     
@app.callback(Output('graph6', 'figure'),
              [Input('home_dog_spread_options', 'value')])

    
def update_figure303(spread):
    filtered_df = home_dogs[home_dogs['spread_favorite']>spread*-1]
    traces3 = []
    traces3.append(go.Scatter(
            x=filtered_df['schedule_date'],
            y=filtered_df['away_Favs'].cumsum(),
            text=filtered_df['team_away']+'@'+filtered_df['team_home'],
            opacity=0.7,
            mode='markers',
            marker = dict(
                    color = filtered_df['away_Favs'].cumsum(),

        colorscale='Viridis',

        )))
    return {
        'data': traces3,
        'layout': go.Layout(
            yaxis={'title': 'diffrence from spead'},
            autosize=True,
            title='Away favorites when the spread is less than {}'.format(spread),
            xaxis=dict(tickfont=dict(family="Times New Roman",size=14)),
            plot_bgcolor=color,
            hovermode='closest'
        )
    }
        


@app.callback(Output('spread_data_graph3','figure'),
              [Input('home_dog_spread_options', 'value')])
def update_figure33(spread):
    filtered_df = home_dogs[home_dogs['spread_favorite']>spread*-1]
    traces3 = []
    traces3.append(go.Scatter(
            x=filtered_df['schedule_date'],
            y=filtered_df['result'].cumsum(),
            text=filtered_df['team_away']+'@'+filtered_df['team_home'],
            opacity=0.7,
            mode='markers',
            marker = dict(
                    color = filtered_df['result'].cumsum(),

        colorscale='Viridis',

        )))
    return {
        'data': traces3,
        'layout': go.Layout(
            yaxis={'title': 'diffrence from spead'},
            autosize=True,
            title='Home underdogs when the spread is less than {}'.format(spread),
            xaxis=dict(tickfont=dict(family="Times New Roman",size=14)),
            plot_bgcolor=color,
            hovermode='closest'
        )
    }
@app.callback(Output('spread_data_graph','figure'),
              [Input('home_dog_spread_options', 'value')])
def update_figure31312(spread):
    filtered_df = home_dogs[home_dogs['spread_favorite']<spread*-1]
    traces3 = []
    traces3.append(go.Scatter(
            x=filtered_df['schedule_date'],
            y=filtered_df['away_Favs'].cumsum(),
            text=filtered_df['team_away']+'@'+filtered_df['team_home'],
            opacity=0.7,
            mode='markers',
            marker = dict(
                    color = filtered_df['away_Favs'].cumsum(),

        colorscale='Viridis',

        )))
    return {
        'data': traces3,
        'layout': go.Layout(
            
            autosize=True,
            title='Away favorites when the spread is greater than {}'.format(spread),
            xaxis=dict(tickfont=dict(family="Times New Roman",size=14)),
            plot_bgcolor=color,
            hovermode='closest'
        )
    }
        


 
@app.callback(Output('new_graph12', 'figure'),
              [Input('over_under_line', 'value')])
def update_figure_new_6(line):
    filtered_df = df[df['over_under_line'] <line]
    #filtered_df = filtered_df_1[filtered_df_1['schedule_week']==week]
    
    traces36 = []
    for i in filtered_df['schedule_week'].unique():
        filtered_df2 = filtered_df[filtered_df['schedule_week']==i]
        traces36.append(go.Bar(
            x=filtered_df2['schedule_week'],
            y=filtered_df2['over_result'].cumsum(),
            text=filtered_df2['over_result'].sum(),
            name="week number {}".format(i),
            opacity=0.7,
            width=1,
            marker=dict(colorscale='Viridis',)

        ))

    return {
        'data': traces36,
        'layout': go.Layout(
            yaxis={'title': 'USD'},
            title='Taking the over when the line is less than {}'.format(line),
            hovermode='closest',
            plot_bgcolor=color,
            xaxis=dict(tickfont=dict(family="Times New Roman",size=14)),
             )}   
@app.callback(Output('new_graph13', 'figure'),
              [Input('over_under_line', 'value')])
def update_figure_new_7(line):
    filtered_df = df[df['over_under_line'] >line]
    #filtered_df = filtered_df_1[filtered_df_1['schedule_week']==week]
    
    traces36 = []
    for i in filtered_df['schedule_week'].unique():
        filtered_df2 = filtered_df[filtered_df['schedule_week']==i]
        traces36.append(go.Bar(
            x=filtered_df2['schedule_week'],
            y=filtered_df2['under_result'].cumsum(),
            text=filtered_df2['under_result'].sum(),
            name="week number {}".format(i),
            opacity=0.7,
            width=1,
            marker=dict(colorscale='Viridis',)

        ))

    return {
        'data': traces36,
        'layout': go.Layout(
            yaxis={'title': 'USD'},
            title='Taking the under when the line is greater than {}'.format(line),
            hovermode='closest',
            width=500,
            plot_bgcolor=color,
            xaxis=dict(tickfont=dict(family="Times New Roman",size=14)),
             )}   
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.scripts.config.serve_locally = False


# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
