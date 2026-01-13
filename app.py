import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go

CSV_FILE = "./combined_sales_data.csv"
PRICE_INCREASE_DATE = "2021-01-15"

# load and process the sales data
df = pd.read_csv(CSV_FILE)
df.columns = df.columns.str.lower()
df['date'] = pd.to_datetime(df['date'])

# group by date and sum all sales for each date
daily_sales = df.groupby('date')['sales'].sum().reset_index()
daily_sales = daily_sales.sort_values('date')

# create the line chart
fig = go.Figure()

# add background shading for before and after price increase
price_date = pd.to_datetime(PRICE_INCREASE_DATE)
min_date = daily_sales['date'].min()
max_date = daily_sales['date'].max()
max_sales = daily_sales['sales'].max()

# before price increase (subtle green background)
fig.add_shape(
    type="rect",
    x0=min_date,
    x1=price_date,
    y0=0,
    y1=max_sales,
    fillcolor="rgba(144, 238, 144, 0.1)",
    line=dict(width=0),
    layer="below"
)

# after price increase (subtle red background)
fig.add_shape(
    type="rect",
    x0=price_date,
    x1=max_date,
    y0=0,
    y1=max_sales,
    fillcolor="rgba(255, 182, 193, 0.1)",
    line=dict(width=0),
    layer="below"
)

# add the sales line
fig.add_trace(go.Scatter(
    x=daily_sales['date'],
    y=daily_sales['sales'],
    mode='lines',
    name='Pink Morsel Sales',
    line=dict(color='#2C3E50', width=2.5),
    hovertemplate='<b>Date:</b> %{x|%B %d, %Y}<br><b>Sales:</b> $%{y:,.0f}<extra></extra>'
))

# add vertical line to mark the price increase date
fig.add_shape(
    type="line",
    x0=price_date,
    x1=price_date,
    y0=0,
    y1=max_sales,
    line=dict(color="#E74C3C", width=2, dash="dash"),
    layer="above"
)

# add annotation for price increase date
fig.add_annotation(
    x=price_date,
    y=max_sales * 0.9,
    text="Price Increase<br>Jan 15, 2021",
    showarrow=True,
    arrowhead=2,
    arrowcolor="#E74C3C",
    ax=0,
    ay=-40,
    bgcolor="white",
    bordercolor="#E74C3C",
    borderwidth=1.5,
    font=dict(size=11, color="#E74C3C")
)

# update layout - simple and clean
fig.update_layout(
    title=dict(
        text='Pink Morsel Sales Over Time',
        font=dict(size=20, color='#2C3E50'),
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title='Date',
        titlefont=dict(size=13),
        tickfont=dict(size=11),
        gridcolor='#E8E8E8',
        showgrid=True
    ),
    yaxis=dict(
        title='Sales ($)',
        titlefont=dict(size=13),
        tickfont=dict(size=11),
        gridcolor='#E8E8E8',
        showgrid=True,
        tickformat=',.0f'
    ),
    hovermode='x unified',
    template='plotly_white',
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=70, r=40, t=60, b=50),
    height=500,
    showlegend=False
)

# initialize the Dash app
app = Dash(__name__)

# define the app layout
app.layout = html.Div([
    html.Div([
        html.H1(
            'Pink Morsel Sales Analysis',
            style={
                'textAlign': 'center',
                'color': '#2C3E50',
                'marginTop': '30px',
                'marginBottom': '10px',
                'fontSize': '32px',
                'fontWeight': '600'
            }
        ),
        html.P(
            'Were Pink Morsel sales higher before or after the price increase on January 15, 2021?',
            style={
                'textAlign': 'center',
                'color': '#7F8C8D',
                'fontSize': '16px',
                'marginBottom': '30px',
                'fontStyle': 'italic'
            }
        ),
        dcc.Graph(
            id='sales-chart',
            figure=fig,
            style={'margin': '0 auto', 'maxWidth': '1100px'}
        )
    ], style={
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '20px',
        'backgroundColor': '#FFFFFF'
    })
])

# run the app
if __name__ == '__main__':
    app.run_server(debug=True)
