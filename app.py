# importing stuff

# Dash

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# Div.

import pandas as pd
import numpy as np
import calendar

# Plotly

import plotly.express as px
import plotly.graph_objects as go

# Datamodel

import datamodel

# actually getting the data

order = datamodel.get_data()
order2 = datamodel.get_data()

df_year = datamodel.get_year()
df_month = datamodel.get_month()

# create figures

# sales by employee

fig_employee = px.bar(order, 
    x='emp_name', y='total', 
    color='type', text='total', title='Sales by Employee',
    hover_data=[],
    labels={'total':'Total sales', 'emp_name':'Employee', 'type':'Product Type'})
fig_employee.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_employee.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=45)

# sales by product

fig_product = px.bar(order2, 
    x='productname', y='total', 
    color='type', text='total', title='Sales by Product',
    hover_data=[],
    labels={'total':'Total sales', 'productname':'Product', 'type':'Product Type'})
fig_product.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_product.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=45)

# dash init

dash_app = dash.Dash(__name__)
app = dash_app.server


# layout

dash_app.layout = html.Div(
    children=[
# sales by employee
        html.Div(className='row',
                children=[
                    html.Div(className='four columns div-user-controls',
                            children=[
                                html.H2('Employee Sales dashboard'),
                                html.P('Select filters from dropdown'),

                    html.Div(children="Month", className="menu-title"),
                            dcc.Dropdown(
                                id='drop_month',
                                options=[{'label':selectmonth, 'value':selectmonth} for selectmonth in df_month['monthnames']],
                            ),
                    html.Div(children="Year", className="menu-title"),
                            dcc.Dropdown(
                                id='drop_year',
                                options=[{'label':selectyear, 'value':selectyear} for selectyear in df_year]
                            ),
                            ]
                    ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                            children=[
                                dcc.Graph(id="sales_employee", figure=fig_employee)
                            ]
                    ),
                ]
            ),

# sales by product

        html.Div(className='row',
                children=[
                    html.Div(className='four columns div-user-controls',
                            children=[
                                html.H2('Product Sales dashboard'),
                                html.P('Select filters from dropdown'),

                    html.Div(children="Month", className="menu-title"),
                            dcc.Dropdown(
                                id='drop_month1',
                                
                                options=[{'label':selectmonth, 'value':selectmonth} for selectmonth in df_month['monthnames']],
                            ),
                    html.Div(children="Year", className="menu-title"),
                            dcc.Dropdown(
                                id='drop_year1',
                                options=[{'label':selectyear, 'value':selectyear} for selectyear in df_year]
                            ),
                            ]
                    ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                            children=[
                                dcc.Graph(id="sales_product", figure=fig_product)
                            ]
                    ),
                ]
            )
        ]
)

# Callbacks

# sales by employee

@dash_app.callback(
    Output('sales_employee', 'figure'),
    [Input('drop_month', 'value'),
    Input('drop_year', 'value')],
    
)

def update_graph(drop_month, drop_year):

    if drop_year:
        if drop_month:
            order_fig1 = order.loc[(order['orderyear'] == drop_year) & (order['ordermonth'] == drop_month)]
            
        else:
            order_fig1 = order.loc[order['orderyear'] == drop_year]
            
    else:
        if drop_month:
            order_fig1 = order.loc[order['ordermonth'] == drop_month]
            
        else:
            order_fig1 = order
        
    return {'data':[go.Bar(
        x = order_fig1['emp_name'],
        y = order_fig1['total']
            )
        ]
    }

# sales by product

@dash_app.callback(
    Output('sales_product', 'figure'),  
    [Input('drop_month1', 'value'),
    Input('drop_year1', 'value')]
)
def update_graph1(drop_month1, drop_year1):

    if drop_year1:
        if drop_month1:
            order_fig2 = order2.loc[(order2['orderyear'] == drop_year1) & (order2['ordermonth'] == drop_month1)]
            
        else:
            order_fig2 = order2.loc[order2['orderyear'] == drop_year1]
            
    else:
        if drop_month1:
            order_fig2 = order2.loc[order2['ordermonth'] == drop_month1]
            
        else:
            order_fig2 = order2
        
    return {'data':[go.Bar(
        x = order_fig2['productname'],
        y = order_fig2['total']
            )
        ]
    }

# app init
if __name__ == '__main__':
    dash_app.run_server(debug=True)
