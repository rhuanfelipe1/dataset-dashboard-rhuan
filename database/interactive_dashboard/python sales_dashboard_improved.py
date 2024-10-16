import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('sales_uk.csv')

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Data Processing
total_sales = df['Total'].sum()
total_gross_income = df['gross income'].sum()
avg_rating = df['Rating'].mean()

# Aggregate sales by day
daily_sales = df.groupby(df['Date'].dt.date)['Total'].sum().reset_index()
daily_sales.columns = ['Date', 'Total']

# Area chart: Total sales over time with daily totals
area_sales_fig = px.area(
    daily_sales,
    x='Date',
    y='Total',
    title='Total Sales Over Time (Daily Totals)',
    template='plotly_dark',
    color_discrete_sequence=["#00CC96"],
    labels={'Total': 'Total Sales ($)', 'Date': 'Date'}
)

# Update the layout for better title spacing
area_sales_fig.update_layout(
    title=dict(
        text='Total Sales Over Time (Daily Totals)',
        font=dict(size=24, color='white'),
        pad=dict(t=20, b=20)
    ),
    xaxis_title=dict(
        text='Date',
        font=dict(size=18, color='white')
    ),
    yaxis_title=dict(
        text='Total Sales ($)',
        font=dict(size=18, color='white')
    ),
    margin=dict(l=40, r=40, t=60, b=40),
)

# Aggregate sales by product line
sales_by_product_line = df.groupby('Product line', as_index=False)['Total'].sum()

# Bar chart: Total sales by product line with specific color
bar_product_fig = px.bar(
    sales_by_product_line,
    x='Product line',
    y='Total',
    title='Total Sales by Product Line',
    color='Product line',
    color_discrete_sequence=px.colors.qualitative.Set2,
    template='plotly_dark'
)

bar_product_fig.update_layout(
    xaxis_title="Product Line",
    yaxis_title="Total Sales ($)",
    font=dict(family="Arial", size=12, color='white'),
    margin=dict(l=40, r=40, t=40, b=40),
    hovermode="x unified"
)

# Aggregate sales by city
sales_by_city = df.groupby('City', as_index=False)['Total'].sum()

# Bar chart: Total sales by city with specific color
bar_city_fig = px.bar(
    sales_by_city,
    x='City',
    y='Total',
    title='Total Sales by City',
    color='City',
    color_discrete_sequence=px.colors.qualitative.Plotly,
    template='plotly_dark'
)

bar_city_fig.update_layout(
    xaxis_title="City",
    yaxis_title="Total Sales ($)",
    font=dict(family="Arial", size=12, color='white'),
    margin=dict(l=40, r=40, t=40, b=40),
    hovermode="x unified"
)

# Pie chart: Customer type distribution
pie_customer_type = px.pie(df, names='Customer_type', title='Customer Type Distribution',
                           color_discrete_sequence=px.colors.sequential.RdBu, template='plotly_dark')

# Pie chart: Payment method distribution
pie_payment_method = px.pie(df, names='Payment', title='Payment Method Distribution',
                            color_discrete_sequence=px.colors.sequential.Emrld, template='plotly_dark')

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Define layout with a slider for date range
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H2("Sales Dashboard", className="text-center text-white mb-2"),
                html.H6("Analyze Your Sales Performance", className="text-center text-muted mb-4")
            ])
        ),
    ]),

    # KPI Cards Row
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4(f"${total_sales:,.2f}", className="card-title text-white"),
                html.P("Total Sales", className="card-text text-white"),
            ]),
        ], class_name="bg-primary shadow"), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4(f"${total_gross_income:,.2f}", className="card-title text-white"),
                html.P("Total Gross Income", className="card-text text-white"),
            ]),
        ], class_name="bg-success shadow"), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4(f"{avg_rating:.2f}", className="card-title text-white"),
                html.P("Average Rating", className="card-text text-white"),
            ]),
        ], class_name="bg-info shadow"), width=4),
    ], className="mb-4"),

    # Navigation Buttons
    html.Div([
        dbc.Button("All", id='show-all', n_clicks=0, className="mr-2 mb-2"),
        dbc.Button("Total Sales Over Time", id='tab1', n_clicks=0, className="mr-2 mb-2"),
        dbc.Button("Total Sales by Product Line", id='tab2', n_clicks=0, className="mr-2 mb-2"),
        dbc.Button("Total Sales by City", id='tab3', n_clicks=0, className="mr-2 mb-2"),
        dbc.Button("Customer Type Distribution", id='tab4', n_clicks=0, className="mr-2 mb-2"),
        dbc.Button("Payment Method Distribution", id='tab5', n_clicks=0, className="mr-2 mb-2"),
        dbc.Button("Instructions", id='instructions-button', n_clicks=0, className="mb-2"),
    ], className='mb-4 text-center',
        style={'display': 'flex', 'justify-content': 'center', 'flex-wrap': 'wrap', 'gap': '10px'}),

    # Content area for graphs (show all graphs by default)
    html.Div(id='graph-content', children=[
        dcc.Graph(id='sales-over-time', figure=area_sales_fig, config={'displayModeBar': False}),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=bar_product_fig, config={'displayModeBar': False}), width=6),
            dbc.Col(dcc.Graph(figure=bar_city_fig, config={'displayModeBar': False}), width=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=pie_customer_type, config={'displayModeBar': False}), width=6),
            dbc.Col(dcc.Graph(figure=pie_payment_method, config={'displayModeBar': False}), width=6),
        ]),
    ], style={'margin-bottom': '15px'}),

    # Footer
    html.Footer("© 2024 Sales Dashboard", className="text-center text-white mt-4"),

    # Instructions Modal
    dbc.Modal(
        [
            dbc.ModalHeader("Instructions"),
            dbc.ModalBody(
                html.Div([
                    html.P("Welcome to the Sales Dashboard! Here’s how to use it:", className="font-weight-bold"),
                    html.Hr(),  # Horizontal line for separation
                    html.Ul([
                        html.Li("View Total Sales Over Time: Click the 'Total Sales Over Time' button to see the daily total sales represented in an area chart."),
                        html.Li("Explore Sales by Product Line: Click 'Total Sales by Product Line' to view a bar chart of sales categorized by product line."),
                        html.Li("Sales by City: Click 'Total Sales by City' to see sales performance across different cities."),
                        html.Li("Customer Insights: Check out the 'Customer Type Distribution' and 'Payment Method Distribution' pie charts for insights into your customers."),
                        html.Li("Back to All Charts: Click 'All' to return to the full dashboard view."),
                    ]),
                    html.Hr(),  # Horizontal line for separation
                    html.P("Use the dashboard to analyze and make informed decisions based on your sales data!", className="font-weight-bold"),
                ])
            ),
            dbc.ModalFooter(
                dbc.Button("Close", id="close", className="ml-auto")
            ),
        ],
        id="instructions-modal",
        size="lg",
    )
], fluid=True)

# Callbacks to control the visibility of graphs
@app.callback(
    Output('graph-content', 'children'),
    [Input('show-all', 'n_clicks'),
     Input('tab1', 'n_clicks'),
     Input('tab2', 'n_clicks'),
     Input('tab3', 'n_clicks'),
     Input('tab4', 'n_clicks'),
     Input('tab5', 'n_clicks')]
)
def display_graphs(show_all, tab1, tab2, tab3, tab4, tab5):
    ctx = dash.callback_context

    if not ctx.triggered:
        return [
            dcc.Graph(id='sales-over-time', figure=area_sales_fig, config={'displayModeBar': False}),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=bar_product_fig, config={'displayModeBar': False}), width=6),
                dbc.Col(dcc.Graph(figure=bar_city_fig, config={'displayModeBar': False}), width=6),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=pie_customer_type, config={'displayModeBar': False}), width=6),
                dbc.Col(dcc.Graph(figure=pie_payment_method, config={'displayModeBar': False}), width=6),
            ])
        ]

    # Identify which button was pressed
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'show-all':
        return [
            dcc.Graph(id='sales-over-time', figure=area_sales_fig, config={'displayModeBar': False}),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=bar_product_fig, config={'displayModeBar': False}), width=6),
                dbc.Col(dcc.Graph(figure=bar_city_fig, config={'displayModeBar': False}), width=6),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=pie_customer_type, config={'displayModeBar': False}), width=6),
                dbc.Col(dcc.Graph(figure=pie_payment_method, config={'displayModeBar': False}), width=6),
            ])
        ]

    elif button_id == 'tab1':
        return [dcc.Graph(id='sales-over-time', figure=area_sales_fig, config={'displayModeBar': False})]

    elif button_id == 'tab2':
        return [dcc.Graph(figure=bar_product_fig, config={'displayModeBar': False})]

    elif button_id == 'tab3':
        return [dcc.Graph(figure=bar_city_fig, config={'displayModeBar': False})]

    elif button_id == 'tab4':
        return [dcc.Graph(figure=pie_customer_type, config={'displayModeBar': False})]

    elif button_id == 'tab5':
        return [dcc.Graph(figure=pie_payment_method, config={'displayModeBar': False})]


# Callback to control the instructions modal
@app.callback(
    Output("instructions-modal", "is_open"),
    [Input("instructions-button", "n_clicks"),
     Input("close", "n_clicks")],
    [dash.dependencies.State("instructions-modal", "is_open")],
)
def toggle_instructions(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
