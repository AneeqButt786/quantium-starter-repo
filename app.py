import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

CSV_FILE = "./combined_sales_data.csv"
PRICE_INCREASE_DATE = "2021-01-15"

# load and process the sales data
df = pd.read_csv(CSV_FILE)
df.columns = df.columns.str.lower()
df['date'] = pd.to_datetime(df['date'])

# initialize the Dash app
app = Dash(__name__)

# custom CSS styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Pink Morsel Sales Analysis</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            }
            .main-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 30px 20px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-top: 20px;
                margin-bottom: 20px;
            }
            .header-title {
                text-align: center;
                color: #1a1a1a;
                margin-top: 20px;
                margin-bottom: 10px;
                font-size: 38px;
                font-weight: 700;
                letter-spacing: -1px;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            .header-subtitle {
                text-align: center;
                color: #6b7280;
                font-size: 17px;
                margin-bottom: 40px;
                font-style: italic;
                line-height: 1.6;
            }
            .filter-container {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: 35px;
                padding: 20px;
                background: #f9fafb;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
            }
            .filter-label {
                font-size: 16px;
                font-weight: 600;
                color: #374151;
                margin-right: 20px;
            }
            .radio-items-container {
                display: flex;
                gap: 25px;
                flex-wrap: wrap;
            }
            .chart-container {
                margin: 0 auto;
                max-width: 1100px;
                padding: 20px;
                background: #ffffff;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# define the app layout
app.layout = html.Div([
    html.Div([
        html.H1(
            'Pink Morsel Sales Analysis',
            className='header-title'
        ),
        html.P(
            'Were Pink Morsel sales higher before or after the price increase on January 15, 2021?',
            className='header-subtitle'
        ),
        html.Div([
            html.Span('Filter by Region: ', className='filter-label'),
            dcc.RadioItems(
                id='region-filter',
                options=[
                    {'label': 'All', 'value': 'All'},
                    {'label': 'North', 'value': 'North'},
                    {'label': 'East', 'value': 'East'},
                    {'label': 'South', 'value': 'South'},
                    {'label': 'West', 'value': 'West'}
                ],
                value='All',
                inline=True,
                style={
                    'display': 'flex',
                    'gap': '25px',
                    'fontSize': '15px',
                    'fontFamily': 'Segoe UI, Arial, sans-serif'
                },
                inputStyle={
                    'marginRight': '8px',
                    'cursor': 'pointer',
                    'accentColor': '#3b82f6'
                },
                labelStyle={
                    'cursor': 'pointer',
                    'padding': '8px 12px',
                    'borderRadius': '6px',
                    'transition': 'all 0.2s ease',
                    'color': '#4b5563'
                }
            )
        ], className='filter-container'),
        html.Div([
            dcc.Graph(
                id='sales-chart',
                style={'width': '100%', 'height': '100%'}
            )
        ], className='chart-container')
    ], className='main-container')
])

# callback to update chart based on region selection
@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(selected_region):
    # filter data by selected region
    if selected_region == 'All':
        filtered_df = df.copy()
        region_title = 'All Regions'
    else:
        filtered_df = df[df['region'].str.lower() == selected_region.lower()]
        region_title = selected_region
    
    # group by date and sum all sales for each date
    daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
    daily_sales = daily_sales.sort_values('date')
    
    # create the line chart
    fig = go.Figure()
    
    # add background shading for before and after price increase
    price_date = pd.to_datetime(PRICE_INCREASE_DATE)
    if len(daily_sales) > 0:
        min_date = daily_sales['date'].min()
        max_date = daily_sales['date'].max()
        max_sales = daily_sales['sales'].max()
    else:
        min_date = price_date
        max_date = price_date
        max_sales = 0
    
    # before price increase (subtle green background)
    fig.add_shape(
        type="rect",
        x0=min_date,
        x1=price_date,
        y0=0,
        y1=max_sales if max_sales > 0 else 1000,
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
        y1=max_sales if max_sales > 0 else 1000,
        fillcolor="rgba(255, 182, 193, 0.1)",
        line=dict(width=0),
        layer="below"
    )
    
    # add the sales line
    if len(daily_sales) > 0:
        fig.add_trace(go.Scatter(
            x=daily_sales['date'],
            y=daily_sales['sales'],
            mode='lines',
            name='Pink Morsel Sales',
            line=dict(color='#2C3E50', width=2.5),
            hovertemplate='<b>Date:</b> %{x|%B %d, %Y}<br><b>Sales:</b> $%{y:,.0f}<extra></extra>'
        ))
    
    # add vertical line to mark the price increase date
    if max_sales > 0:
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
            text=f'Pink Morsel Sales Over Time - {region_title}',
            font=dict(size=22, color='#2C3E50', family='Segoe UI, Arial, sans-serif'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Date',
            titlefont=dict(size=14, color='#4A4A4A', family='Segoe UI, Arial, sans-serif'),
            tickfont=dict(size=12, color='#6A6A6A'),
            gridcolor='#E8E8E8',
            showgrid=True
        ),
        yaxis=dict(
            title='Sales ($)',
            titlefont=dict(size=14, color='#4A4A4A', family='Segoe UI, Arial, sans-serif'),
            tickfont=dict(size=12, color='#6A6A6A'),
            gridcolor='#E8E8E8',
            showgrid=True,
            tickformat=',.0f'
        ),
        hovermode='x unified',
        template='plotly_white',
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=70, r=40, t=80, b=50),
        height=550,
        showlegend=False
    )
    
    return fig

# run the app
if __name__ == '__main__':
    app.run_server(debug=True)
