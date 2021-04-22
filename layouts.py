import plotly.graph_objects as go


def PorPermLayout(): 
    fig = go.Figure(
    data=[
        # go.Scatter(x=df_rcal[porosityColumnName].values,
        #              y=df_rcal[permeabilytyColumnName].values,
        #              mode='markers',
        #              name='All Data'
        #              )
    ],
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
        margin={'l': 0, 'b': 0, 't': 40, 'r': 0},
        # margin=dict(l=20, b=20, t=40, r=20),
        template='plotly_white'
    )
    )
    return fig

def PermSwirrLayout():
    fig = go.Figure(
    data=[
        # go.Scatter(x=df_rcal[permeabilytyColumnName].values,
        #              y=df_rcal[irrWaterColumnName].values,
        #              mode='markers',
        #              name='All Data'
        #              )
    ],

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
        legend_title_text='Trend',
        margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
        # margin={'l': 0, 'b': 0, 't': 40, 'r': 0},
        # margin=dict(l=20, b=20, t=40, r=20),
        template='plotly_white'
    )
    )
    return fig

def RiSwLayout():
    fig = go.Figure(
    data=[

    ],
    # region layout
    layout=go.Layout(
        # title=dict(text='Pc-Water Saturation'),
        xaxis=dict(title='Water Saturation, dec',
                   range=[-1, 0],
                   type="log",
                   showline=True,
                   linewidth=2,
                   linecolor='black'),
        yaxis=dict(
            # type='log',
            title='Resistivity Index',
            range=[0, 2],
            type="log",
            showline=True,
            linewidth=2,
            linecolor='black'
        ),
        margin={'l': 0, 'b': 0, 't': 0, 'r': 40},
        # margin=dict(l=20, b=20, t=40, r=20),
        template='plotly_white',
        # height=400,
        # width=500
    ))
    return fig

def FFPorLayout():
    fig_Por_FF = go.Figure(
    data=[

    ],
    # region layout
    layout=go.Layout(
        # title=dict(text='Pc-Water Saturation'),
        xaxis=dict(title='Porosity, dec',
                   range=[-2, -0.3],
                   type="log",
                   showline=True,
                   linewidth=2,
                   linecolor='black'),
        yaxis=dict(
            # type='log',
            title='Formation Factor',
            range=[0, 3],
            type="log",
            showline=True,
            linewidth=2,
            linecolor='black'
        ),
        margin={'l': 0, 'b': 0, 't': 0, 'r': 40},
        # margin=dict(l=20, b=20, t=40, r=20),
        template='plotly_white',
        # height=400,
        # width=500
    ))
    return fig
