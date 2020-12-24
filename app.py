import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

data = pd.read_csv(r'player_data.csv')
data.set_index(['id'])

########### Modify dataset
data['Total Cards'] = data['yellow_cards'] + data['red_cards']
data['GW Transfers'] = data['transfers_in_event'] - data['transfers_out_event']
data['Points per mil'] = data['total_points']*10.0 / data['now_cost']
data['now_cost'] = data['now_cost']/10.0

# Getting Team Names
team_dt = pd.DataFrame ({'team_code':[3, 7, 36, 90, 8, 31, 11, 54, 2, 13, 14, 43, 4, 49, 20, 6, 35, 21, 39, 1],
                         'team_name':['Arsenal', 'Aston Villa', 'Brighton & Howe Albion', 'Burnley', 'Chelsea', 
                                      'Crystal Palace', 'Everton', 'Fulham', 'Leeds United', 'Leicester City', 
                                      'Liverpool', 'Manchester City', 'Newcastle United', 'Sheffield United', 
                                      'Southampton', 'Spurs', 'West Brom', 'West Ham United', 'Wolves', 'Manchester United']})
df1 = data.merge(team_dt, on='team_code', how='left')
# df1.columns

# Getting player positions
pos_dt = pd.DataFrame ({'element_type':[1,2,3,4],
                         'position':['Goalkeepers', 'Defenders', 'Midfielders', 'Forwards']})
df = df1.merge(pos_dt, on='element_type', how='left')
# df.head()

df = df[['assists', 'bonus', 'bps', 'clean_sheets', 'code', 'cost_change_event', 'cost_change_start', 'creativity',
         'dreamteam_count', 'element_type', 'ep_next', 'ep_this', 'event_points', 'first_name', 'form', 'goals_conceded',
         'goals_scored', 'ict_index', 'id', 'influence', 'minutes', 'now_cost', 'own_goals', 'penalties_missed',
         'penalties_saved', 'photo', 'points_per_game', 'red_cards', 'saves', 'second_name', 'selected_by_percent',
         'threat', 'total_points', 'transfers_in', 'transfers_in_event', 'transfers_out', 'transfers_out_event',
         'web_name', 'yellow_cards', 'Total Cards', 'team_name', 'position', 'Points per mil', 'GW Transfers']]
df = df.set_axis(['Assists', 'Bonus', 'BPS', 'Clean sheets', 'Code','Cost change event', 'Cost change start',
                  'Creativity', 'No. of times in Dreamteam', 'Element Type', 'EP next', 'EP this', 'GW Points',
                  'First Name', 'Form', 'Goals Conceded', 'Goals Scored', 'ICT Index', 'ID', 'Influence', 'Minutes',
                  'Cost', 'Own Goals', 'Penalties Missed', 'Penalties saved', 'Photo', 'Points per Game', 'Red Cards',
                  'Saves', 'Second Name', 'Selected by Percent', 'Threat', 'Total Points', 'Transfers In',
                  'Transfers in GW', 'Transfers out', 'Transfers out GW', 'Web Name', 'Yellow cards', 'Total Cards',
                  'Team Name', 'Position', 'Points per mil', 'GW Transfers'],
            axis=1, inplace=False)

drop_downs = []

for i in ['Assists', 'Bonus', 'BPS', 'Clean sheets', 'Creativity', 'Form', 'Goals Conceded', 'Goals Scored', 'ICT Index', 'Influence',
           'Minutes', 'Cost', 'Own Goals', 'Penalties Missed', 'Penalties saved', 'Points per Game', 'Red Cards', 'Saves', 
           'Selected by Percent', 'Threat', 'Total Points', 'Yellow cards', 'Total Cards', 'GW Transfers', 'Points per mil']:
           j = i.replace(" ","")
           drop_downs.append(
            html.Div([
              html.Label(f'{i}', style={'display':'inline', 'fontSize':16, 'padding': '5px', 'vertical-align': 'middle'}),
              dcc.Dropdown(id=f'min_{j}', multi=False,
                            options = [{'label': i, 'value': i} for i in sorted(df[i].unique())]
                            ,value=df[i].min()
                            ,style={'display': 'inline-block', 'width': '60px', 'padding': '0', 'margin': '0'}
                            ),
              dcc.Dropdown(id=f'max_{j}', multi=False,
                            options = [{'label': i, 'value': i} for i in sorted(df[i].unique())]
                            ,value=df[i].max()
                            ,style={'display': 'inline-block', 'width': '60px', 'padding': '0', 'margin': '0'}
                            ),
              ], style={'textAlign':'start'}
              ))

input_list = []
for i in ['Assists', 'Bonus', 'BPS', 'Clean sheets', 'Creativity', 'Form', 'Goals Conceded', 'Goals Scored', 'ICT Index', 'Influence',
           'Minutes', 'Cost', 'Own Goals', 'Penalties Missed', 'Penalties saved', 'Points per Game', 'Red Cards', 'Saves', 
           'Selected by Percent', 'Threat', 'Total Points', 'Yellow cards', 'Total Cards', 'GW Transfers', 'Points per mil']:
  j = i.replace(" ","")

  input_list.append(
    Input(f'min_{j}','value')
  )
  input_list.append(
    Input(f'max_{j}','value')
  )

tbl_col=[
        {'name': 'First Name', 'id': 'First Name', 'deletable': False, 'selectable': False}, 
        {'name': 'Second Name', 'id': 'Second Name', 'deletable': False, 'selectable': False},
        {'name': 'Team Name', 'id': 'Team Name', 'deletable': False, 'selectable': False}, 
        {'name': 'Position', 'id': 'Position', 'deletable': False, 'selectable': False},
        {'name': 'Cost', 'id': 'Cost', 'deletable': False, 'selectable': False}, 
        {'name': 'Total Points', 'id': 'Total Points', 'deletable': False, 'selectable': False}, 
        {'name': 'Minutes', 'id': 'Minutes', 'deletable': False, 'selectable': False}, 
        {'name': 'Selected by Percent', 'id': 'Selected by Percent', 'deletable': False, 'selectable': False}, 
        {'name': 'Points per Game', 'id': 'Points per Game', 'deletable': False, 'selectable': False}, 
        {'name': 'Points per mil', 'id': 'Points per mil', 'deletable': False, 'selectable': False}, 
        {'name': 'GW Transfers', 'id': 'GW Transfers', 'deletable': False, 'selectable': False},
        {'name': 'Goals Scored', 'id': 'Goals Scored', 'deletable': False, 'selectable': False}, 
        {'name': 'Assists', 'id': 'Assists', 'deletable': False, 'selectable': False}, 
        {'name': 'Goals Conceded', 'id': 'Goals Conceded', 'deletable': False, 'selectable': False}, 
        {'name': 'Saves', 'id': 'Saves', 'deletable': False, 'selectable': False}, 
        {'name': 'Bonus', 'id': 'Bonus', 'deletable': False, 'selectable': False}, 
        {'name': 'BPS', 'id': 'BPS', 'deletable': False, 'selectable': False},
        {'name': 'ICT Index', 'id': 'ICT Index', 'deletable': False, 'selectable': False}, 
        {'name': 'Influence', 'id': 'Influence', 'deletable': False, 'selectable': False}, 
        {'name': 'Creativity', 'id': 'Creativity', 'deletable': False, 'selectable': False}, 
        {'name': 'Threat', 'id': 'Threat', 'deletable': False, 'selectable': False}, 
        {'name': 'Form', 'id': 'Form', 'deletable': False, 'selectable': False}, 
        {'name': 'Clean sheets', 'id': 'Clean sheets', 'deletable': False, 'selectable': False}, 
        {'name': 'Total Cards', 'id': 'Total Cards', 'deletable': False, 'selectable': False},
        {'name': 'Red Cards', 'id': 'Red Cards', 'deletable': False, 'selectable': False}, 
        {'name': 'Yellow cards', 'id': 'Yellow cards', 'deletable': False, 'selectable': False}, 
        {'name': 'Cost change event', 'id': 'Cost change event', 'deletable': False, 'selectable': False},
        {'name': 'Penalties Missed', 'id': 'Penalties Missed', 'deletable': False, 'selectable': False},
        {'name': 'Penalties saved', 'id': 'Penalties saved', 'deletable': False, 'selectable': False}, 
        {'name': 'EP next', 'id': 'EP next', 'deletable': False, 'selectable': False},
        {'name': 'EP this', 'id': 'EP this', 'deletable': False, 'selectable': False},
        {'name': 'Own Goals', 'id': 'Own Goals', 'deletable': False, 'selectable': False}, 
        {'name': 'No. of times in Dreamteam', 'id': 'No. of times in Dreamteam', 'deletable': False, 'selectable': False}
    ]

# the style arguments for the sidebar. We use position:fixed and a fixed width
TOPBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "100rem",
    # "padding": "10px 10px",
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": '100px',
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "10px 10px",
    "background-color": "#f8f9fa",
    'overflowY': 'scroll',
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "position": "fixed",
    "top": '100px',
    "bottom": 0,
    "margin-left": "18rem",
    "margin-right": "2rem",
    "width": "75rem",
    # "padding": "2rem 1rem",
    'overflowX': 'scroll',
    # 'overflowY': 'scroll',
}

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

topbar = html.Div(
    [
        html.H2("FPL Player Screener", className="display-4", 
                style={'backgroundColor': '#02894E', 'padding': '10px', 'textAlign': 'center', 'color': 'white', 'font-family': 'Snell Roundhand'},
                ),
        html.Hr(),
    ],
    style=TOPBAR_STYLE,
)

sidebar = html.Div(
    [
        html.P(
            "Filter for Players:", className="lead"
        ),
        dbc.Row([
            
            dbc.Col([
                dbc.Col([html.Label(f'Team Names:', style={'display':'inline', 'fontSize':16, 'padding': '5px', 'vertical-align': 'middle'}),]),
                dbc.Col([
                    html.Div(f'Arsenal, Aston Villa, Brighton & Howe Albion, Burnley, Chelsea, Crystal Palace, Everton, Fulham, Leeds United, Leicester City, Liverpool, Manchester City, Newcastle United, Sheffield United, Southampton, Spurs, West Brom, West Ham United, Wolves, Manchester United', 
                            id=f'TNameTxt', 
                            style={'display':'inline', 'fontSize':8, 'padding': '5px', 'vertical-align': 'middle', 'color': '9f91aa'}),
                    dcc.Dropdown(id=f'TeamName', multi=True,
                                options = [{'label': i, 'value': i} for i in sorted(df['Team Name'].unique())]
                                ,value=['Arsenal', 'Aston Villa', 'Brighton & Howe Albion', 'Burnley', 'Chelsea', 
                                      'Crystal Palace', 'Everton', 'Fulham', 'Leeds United', 'Leicester City', 
                                      'Liverpool', 'Manchester City', 'Newcastle United', 'Sheffield United', 
                                      'Southampton', 'Spurs', 'West Brom', 'West Ham United', 'Wolves', 'Manchester United']
                                ,style={'display': 'inline-block', 'width': '200px', 'padding': '0px', 'margin': '0'}
                                )])]
                , width=500, 
            ),

            dbc.Col([
                dbc.Col([html.Label(f'Position', style={'display':'inline', 'fontSize':16, 'padding': '5px', 'vertical-align': 'middle'}),]),
                dbc.Col([
                    html.Div(f'Goalkeepers, Defenders, Midfielders, Forwards', 
                            id=f'PosTxt', 
                            style={'display':'inline', 'fontSize':8, 'padding': '5px', 'vertical-align': 'middle', 'color': '9f91aa'}),
                    dcc.Dropdown(id=f'Position', multi=True,
                            options = [{'label': i, 'value': i} for i in sorted(df['Position'].unique())]
                            ,value=['Goalkeepers', 'Defenders', 'Midfielders', 'Forwards']
                            ,style={'display': 'inline-block', 'width': '200px', 'padding': '0px', 'margin': '0'}
                            )])]
                , width=500, 
            ),

            dbc.Col(drop_downs, width=500),

            dbc.Col(id='op', width=500),
        ])
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div([
            dash_table.DataTable(
                id='player_tbl',
                columns=tbl_col,
                data=df.to_dict('records'),
                editable=False,
                filter_action="custom",
                filter_query="",
                sort_action="native",
                sort_mode='multi',
                # row_selectable='multi',
                row_deletable=False,
                selected_rows=[],
                page_action='native',
                page_current= 0,
                style_header={
                    'backgroundColor': '#37003C',
                    'color': 'white',
                    'fontWeight': 'bold'
                },
                style_cell_conditional=[
                        {'textAlign': 'center',
                        'backgroundColor':'#EFEFEF'}
                ],
                page_size= 20,
            ),
            ],
            style=CONTENT_STYLE,
        )

app.layout = html.Div([dcc.Location(id="url"), topbar, sidebar, content])

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output('player_tbl', 'data'), Output('player_tbl', 'columns'), Output('TNameTxt', 'children'), Output('PosTxt', 'children')],
    [Input('player_tbl', "filter_query"), Input(f'TeamName','value'), Input(f'Position','value')] + input_list,
)
def update_op(filter, TeamName, Position, min_Assists, max_Assists, min_Bonus, max_Bonus, min_BPS, max_BPS, min_Cleansheets, max_Cleansheets, min_Creativity, max_Creativity, min_Form, max_Form, min_GoalsConceded, max_GoalsConceded, min_GoalsScored, max_GoalsScored, min_ICTIndex, max_ICTIndex, min_Influence, max_Influence, min_Minutes, max_Minutes, min_Cost, max_Cost, min_OwnGoals, max_OwnGoals, min_PenaltiesMissed, max_PenaltiesMissed, min_Penaltiessaved, max_Penaltiessaved, min_PointsperGame, max_PointsperGame, min_RedCards, max_RedCards, min_Saves, max_Saves, min_SelectedbyPercent, max_SelectedbyPercent, min_Threat, max_Threat, min_TotalPoints, max_TotalPoints, min_Yellowcards, max_Yellowcards, min_TotalCards, max_TotalCards, min_GWTransfers, max_GWTransfers, min_Pointspermil, max_Pointspermil):
    filtering_expressions = filter.split(' && ')

    data1 = df[df["Team Name"].isin(TeamName) & 
            df["Position"].isin(Position) & 
            (df['Assists']>=int(min_Assists)) & (df['Assists']<=int(max_Assists)) & 
            (df['Bonus']>=int(min_Bonus)) & (df['Bonus']<=int(max_Bonus)) & 
            (df['BPS']>=int(min_BPS)) & (df['BPS']<=int(max_BPS)) & 
            (df['Clean sheets']>=int(min_Cleansheets)) & (df['Clean sheets']<=int(max_Cleansheets)) & 
            (df['Creativity']>=int(min_Creativity)) & (df['Creativity']<=int(max_Creativity)) & 
            (df['Form']>=int(min_Form)) & (df['Form']<=int(max_Form)) & 
            (df['Goals Conceded']>=int(min_GoalsConceded)) & (df['Goals Conceded']<=int(max_GoalsConceded)) & 
            (df['Goals Scored']>=int(min_GoalsScored)) & (df['Goals Scored']<=int(max_GoalsScored)) & 
            (df['ICT Index']>=int(min_ICTIndex)) & (df['ICT Index']<=int(max_ICTIndex)) & 
            (df['Influence']>=int(min_Influence)) & (df['Influence']<=int(max_Influence)) & 
            (df['Minutes']>=int(min_Minutes)) & (df['Minutes']<=int(max_Minutes)) & 
            (df['Cost']>=int(min_Cost)) & (df['Cost']<=int(max_Cost)) & 
            (df['Own Goals']>=int(min_OwnGoals)) & (df['Own Goals']<=int(max_OwnGoals)) & 
            (df['Penalties Missed']>=int(min_PenaltiesMissed)) & (df['Penalties Missed']<=int(max_PenaltiesMissed)) & 
            (df['Penalties saved']>=int(min_Penaltiessaved)) & (df['Penalties saved']<=int(max_Penaltiessaved)) & 
            (df['Points per Game']>=int(min_PointsperGame)) & (df['Points per Game']<=int(max_PointsperGame)) & 
            (df['Red Cards']>=int(min_RedCards)) & (df['Red Cards']<=int(max_RedCards)) & 
            (df['Saves']>=int(min_Saves)) & (df['Saves']<=int(max_Saves)) & 
            (df['Selected by Percent']>=int(min_SelectedbyPercent)) & (df['Selected by Percent']<=int(max_SelectedbyPercent)) & 
            (df['Threat']>=int(min_Threat)) & (df['Threat']<=int(max_Threat)) & 
            (df['Total Points']>=int(min_TotalPoints)) & (df['Total Points']<=int(max_TotalPoints)) & 
            (df['Yellow cards']>=int(min_Yellowcards)) & (df['Yellow cards']<=int(max_Yellowcards)) & 
            (df['Total Cards']>=int(min_TotalCards)) & (df['Total Cards']<=int(max_TotalCards)) & 
            (df['GW Transfers']>=int(min_GWTransfers)) & (df['GW Transfers']<=int(max_GWTransfers)) & 
            (df['Points per mil']>=int(min_Pointspermil)) & (df['Points per mil']<=int(max_Pointspermil))]

    dff = data1
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    # return cntnt, TeamName, Position
    return dff.to_dict('records'), tbl_col, 'Selected Teams: ' + ', '.join(TeamName), 'Selected Positions: ' + ', '.join(Position)

if __name__ == "__main__":
    app.run_server(debug=False)
