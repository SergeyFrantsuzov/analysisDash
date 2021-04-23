import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import chart_studio.plotly as py
import os
# import petrofunc as pf
from data import create_dataframe
import layouts

# from statistic import statistic_by_zones

def permeability_kspp(por, *args):
    A, F, S = args
    if por.any() > 0:
        perm = np.exp(A * np.power(por, F) - S)
    return perm


def equation_from_text(equsText):
    if len(equsText) > 0:
        equsSplite = equsText.splitlines()
        equsNames = []
        equsForms = []
        for equ in range(len(equsSplite)):

            equ_Temp = equsSplite[equ].split('=')
            if len(equ_Temp) > 1:
                equsNames.append(equ_Temp[0])
                equsForms.append(equ_Temp[1])
        equations = dict(zip(equsNames, equsForms))

        return equations


def delta_between_perm(perm_orig, phi_orig, equation):

    phi = np.array([phi_orig[i] for i in range(len(perm_orig)) if perm_orig[i] is not None])
    perm = np.array([perm_orig[i] for i in range(len(perm_orig)) if perm_orig[i] is not None])
    calcPerm = eval(equation)
    delta = np.log10(perm) - np.log10(calcPerm)
    delta = delta[np.logical_not(np.isnan(delta))]
    return delta


# region Константы в основном это название столбцов
porosityColumnName = 'Porosity'
permeabilytyColumnName = 'Permeability_Kl'
wellColumnName = 'Wells'
irrWaterColumnName = 'Swirr'
fieldsColumnName = 'Fields'
zonesColumnName = 'Zones'
capillaryPressure = 'CP'
waterSaturationCP = 'SW'
sampleID = 'SampleID'
ri = 'RI'
ff = 'FF'
sw_ri = 'Sw'
# endregion

#  Объяснение данных строк пока опускается, будет объяснено далее
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
analysisDashApp = dash.Dash(__name__, title='Analysis')  # , external_stylesheets=external_stylesheets)
# Путь к результатам исследования керна
# os.chdir('D:\\!_Work_project\\!_Data\\Fields\\Zapadno-Zimnee\\Core\\NewData\\For_Python')
# server = appDashGI.server
# print(os.getcwd())
# fileList = os.listdir(path=".")
# Данные RCAL
pathData = os.getcwd() + "\\" + "data" + "\\"
# pathData = "E:\\Programming\\02042021\Programming\\PyCharmProjects\\PM\\DashBoards\\analysisDash\\data"
# print(pathData)
dfNames, df = create_dataframe(pathData)

figPorosityPermability = layouts.PorPermLayout()

figPermeabilityIrreducibleWater = layouts.PermSwirrLayout()

fig_PC_SW = layouts.PCSWLayout()

fig_Por_FF = layouts.FFPorLayout()

fig_SW_RI = layouts.RISwLayout()

fig_Dist_Perm = layouts.PermHistLayout()

analysisDashApp.layout = html.Div(children=[

    html.Div([

    ], id='header'),
    html.Div([
        html.A(
            title='RCAL',
            href = "#rcal_analysis",
        )

    ], id='menu', className='menu'),

    html.Div([

        html.Div([

            # region Color_filter
            html.Div([
                # html.Label('Color'),
                dcc.RadioItems(
                    id='visualization_data',

                    options=[
                        {'label': 'All Data', 'value': 'All_Data'},
                        {'label': 'Wells', 'value': wellColumnName},
                        {'label': 'Zones', 'value': zonesColumnName},
                        {'label': 'Researches', 'value': 'Research_type'},
                    ],
                    value='All_Data',
                    labelStyle={'display': 'inline-block'}
                ),
            ], className='color_filter'),
            # endregion
            # region ToggleSwitch
            html.Div([
                # html.Label('Por'),
                daq.ToggleSwitch(
                    id='toggleswitch',
                    # labelPosition='top',
                    # label='Por/Perm layout',

                    # style={'position': 'absolute', 'top': 0, 'right': 50, 'z-index': 9999},
                    value=True
                ),
                # html.Label('Perm'),

            ], id='por_perm_toggleswitch'),

            # endregion
            # region Graph
            dcc.Graph(
                id='por_perm',
                # config=dict(responsive=True),
                figure=figPorosityPermability,
                # figure=go.Figure(),
                config={'displayModeBar': False,
                        # 'queueLength': 0
                        }
            ),
            dcc.Graph(
                id='perm_swirr',
                # config=dict(responsive=True),
                figure=figPermeabilityIrreducibleWater,
                config={'displayModeBar': False,
                        # 'queueLength': 0
                        }
            ),
            dcc.Graph(
                id='perm_calc_dist',
                # config=dict(responsive=True),
                figure=fig_Dist_Perm,
                config={'displayModeBar': False,
                        # 'queueLength': 0
                        }
            ),

            html.Div([
                dcc.Textarea(
                    id='equationsText',
                    value='perm=np.exp(0.01*phi**2.2-4.5)\nswirr=53/(k+0.025)**0.17',
                    style={'width': '100%', 'height': 200},
                ),
                html.Button('Apply', id='applyEquations', n_clicks=0),
                html.Div(id='textarea-state-example-output', style={'whiteSpace': 'pre-line'})
            ], id='text_area')
        ], id='rcal_cp_plots'),

        # endregion
        
    ], id='main', className='container'),
    
    html.Div([
            # region Color_filter
            html.Div([
                # html.Label('Color'),
                dcc.RadioItems(
                    id='visualization_data2',

                    options=[
                        {'label': 'All Data', 'value': 'All_Data'},
                        {'label': 'Wells', 'value': wellColumnName},
                        {'label': 'Zones', 'value': zonesColumnName},
                        {'label': 'Researches', 'value': 'Research_type'},
                    ],
                    value='All_Data',
                    labelStyle={'display': 'inline-block'}
                ),
            ], className='color_filter'),
            # endregion
            dcc.Graph(
                id='por_ff',
                # config=dict(responsive=True),
                figure=fig_Por_FF

            ),
            dcc.Graph(
                id='sw_ri',
                # config=dict(responsive=True),
                figure=fig_SW_RI
            ),
        ], id='ff_ri_plots', className='container'),
    
    html.Div([
        dcc.Graph(
            id='sw_cp',
            # config=dict(responsive=True),
            figure=fig_PC_SW,
            config={'displayModeBar': False,
                    'responsive': False
                    # 'queueLength': 0
                    }
        ),

    ], id='capillary_model', className='container')

])


@analysisDashApp.callback(
    [Output('por_perm', 'figure'),
     Output('perm_swirr', 'figure')],
    [Input('visualization_data', 'value'),
     Input('applyEquations', 'n_clicks')],
    State('equationsText', 'value')
)
# # Input('point-mode', 'value')])
def update_rcal_graph(visual_data, n_clicks, equationsText):
    df_rcal = df[dfNames.index('RCAL')]
    if visual_data in [wellColumnName, zonesColumnName]:
        data_temp_por_perm = [go.Scatter(x=df_rcal[df_rcal[visual_data] == i][porosityColumnName].values,
                                         y=df_rcal[df_rcal[visual_data] == i][permeabilytyColumnName].values,
                                         mode='markers',
                                         name=i
                                         ) for i in df_rcal[visual_data].unique()]
        data_temp_perm_swirr = [
            go.Scatter(x=df_rcal[df_rcal[visual_data] == i][permeabilytyColumnName].values,
                       y=df_rcal[df_rcal[visual_data] == i][irrWaterColumnName].values,
                       mode='markers',
                       name=i
                       ) for i in df_rcal[visual_data].unique()]

    elif visual_data == 'All_Data':
        data_temp_por_perm = [go.Scatter(x=df_rcal[porosityColumnName].values,
                                         y=df_rcal[permeabilytyColumnName].values,
                                         mode='markers',
                                         name='All Data'
                                         )]
        data_temp_perm_swirr = [go.Scatter(x=df_rcal[permeabilytyColumnName].values,
                                           y=df_rcal[irrWaterColumnName].values,
                                           mode='markers',
                                           name='All Data'
                                           )]
    elif visual_data == 'Research_type':
        data_temp_por_perm = [
            go.Scatter(x=df[dfNames.index(i)].drop_duplicates(subset=['SampleID'])[porosityColumnName].values,
                       y=df[dfNames.index(i)].drop_duplicates(subset=['SampleID'])[permeabilytyColumnName].values,
                       mode='markers',
                       name=i
                       ) for i in dfNames]
        data_temp_perm_swirr = [go.Scatter(x=df_rcal[permeabilytyColumnName].values,
                                           y=df_rcal[irrWaterColumnName].values,
                                           mode='markers',
                                           name='All Data'
                                           )]

    if n_clicks > 0 and len(equationsText) > 0:
        equations = equation_from_text(equationsText)
        aPhi = np.linspace(1, 30, 100)
        aPerm = 10 ** np.linspace(-2, 3, 100)
        dataCategory = {'perm': 'data_temp_por_perm', 'swirr': 'data_temp_perm_swirr'}
        variableCategory = {'perm': 'phi', 'swirr': 'k'}
        varReplace = {'phi': 'aPhi', 'k': 'aPerm'}
        for equationName in equations.keys():
            # if
            try:
                for t in dataCategory.keys():
                    if t in equationName:
                        catKeys = t
                calcData = eval(equations[equationName].replace(variableCategory[catKeys],
                                                                varReplace[variableCategory[catKeys]]))

                eval(dataCategory[catKeys]).append(
                    go.Scatter(x=eval(varReplace[variableCategory[catKeys]]),
                               y=calcData,
                               mode='lines',
                               name=equationName
                               ))
            except:
                print('!!!')

    figPorosityPermabilityUpdate = go.Figure(
        data=data_temp_por_perm,
        layout=go.Layout(
            # title=dict(text='Porosity-Permeability_Kl'),
            xaxis=dict(title='Porosity, %',
                       range=[0, 30],
                       showline=True,
                       linewidth=2,
                       linecolor='black'),
            yaxis=dict(type='log',
                       title='Permeability, mD',
                       range=[-3, 4],
                       showline=True,
                       linewidth=2,
                       linecolor='black'
                       ),
            showlegend=True,
            legend_title_text=visual_data,
            margin={'l': 0, 'b': 0, 't': 40, 'r': 0},
            # margin=dict(l=20, b=20, t=40, r=20),
            template='plotly_white'
        )
    )
    figPermeabilityIrreducibleWaterUpdate = go.Figure(
        data=data_temp_perm_swirr,

        layout=go.Layout(
            # title=dict(text='Permeability-Irreducible_Water'),
            xaxis=dict(title='Permeability_Kl, mD',
                       type='log',
                       range=[-3, 4],
                       showline=True,
                       linewidth=2,
                       linecolor='black'),
            yaxis=dict(title='Swirr, %',
                       range=[0, 100],
                       showline=True,
                       linewidth=2,
                       linecolor='black'
                       ),
            showlegend=True,
            legend_title_text=visual_data,
            margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
            # margin={'l': 0, 'b': 0, 't': 40, 'r': 0},
            # margin=dict(l=20, b=20, t=40, r=20),
            template='plotly_white'
        )
    )
    return figPorosityPermabilityUpdate, figPermeabilityIrreducibleWaterUpdate


@analysisDashApp.callback(

    Output('perm_calc_dist', 'figure'),
    Input('applyEquations', 'n_clicks'),
    [State('por_perm', 'figure'),
     State('equationsText', 'value')]
)
def update_dist_graph(n_clicks, figData, textEquation):
    if n_clicks is None:
        raise PreventUpdate
    elif len(textEquation) > 0:
        equations = equation_from_text(textEquation)
        eqName = ''
        for eqNameTemp in list(equations.keys()):
            if eqNameTemp.find('perm') != -1:
                eqName = eqNameTemp
        distHist = go.Figure()
        fig_data = figData['data']
        dataHist = []
        for d in fig_data:
            if str(d['name']).find('perm') == -1 and len(eqName)>0:
                # print(d['name'])
                data_name = str(d['name'])
                temp_por = np.array(d['x'])
                temp_perm = np.array(d['y'])
                # calcPerm = eval(equation)
                # delta = np.log10(perm) - np.log10(calcPerm)
                # delta = delta[np.logical_not(np.isnan(delta))]
                temp_delta = delta_between_perm(temp_perm, temp_por, equations[eqName])
                dataHist.append(
                    go.Histogram(
                        x=temp_delta,
                        xbins=dict(start=-3, end=3, size=0.2),
                        opacity=0.5,
                        # marker_color='#9E0000',
                        name=data_name,
                    )
                )
            distHist = go.Figure(
                data=dataHist,
                layout=go.Layout(
                    # title=dict(text='Pc-Water Saturation'),
                    xaxis=dict(title='Permeability',
                               range=[-3, 3],
                               # type="log",
                               showline=True,
                               linewidth=2,
                               linecolor='black'),
                    yaxis=dict(
                        # type='log',
                        title='Count',
                        # range=[0, 100],
                        # type="log",
                        showline=True,
                        linewidth=2,
                        linecolor='black'
                    ),
                    margin={'l': 0, 'b': 0, 't': 0, 'r': 40},
                    # margin=dict(l=20, b=20, t=40, r=20),
                    template='plotly_white',
                    # height=400,
                    # width=500
                )
            )
        distHist.add_vline(x=0, line_width=3, line_dash="dash", line_color="green")
        distHist.update_layout(barmode='overlay')
        return distHist


if __name__ == '__main__':
    analysisDashApp.run_server(debug=True, port=1235)
