import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import json

# Load data
df = pd.read_csv('data/results.csv')
with open('model/feature_importance.json') as f:
    feature_importance = json.load(f)

app = Dash(__name__)

# Colors
COLORS = {
    'background': '#0f172a',
    'card': '#1e293b',
    'accent': '#6366f1',
    'bot': '#ef4444',
    'organic': '#22c55e',
    'suspicious': '#f59e0b',
    'text': '#f1f5f9'
}

app.layout = html.Div(style={'backgroundColor': COLORS['background'], 'minHeight': '100vh', 'padding': '20px', 'fontFamily': 'Arial'}, children=[

    # Title
    html.H1("🤖 Fake Engagement Detection Dashboard",
            style={'textAlign': 'center', 'color': COLORS['text'], 'marginBottom': '5px'}),
    html.P("Behavioural Analytics Hackathon — PS3",
           style={'textAlign': 'center', 'color': '#94a3b8', 'marginBottom': '30px'}),

    # Summary Cards
    html.Div(style={'display': 'flex', 'justifyContent': 'center', 'gap': '20px', 'marginBottom': '30px'}, children=[
        html.Div(style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '12px', 'width': '180px', 'textAlign': 'center', 'borderTop': f'4px solid {COLORS["accent"]}'}, children=[
            html.H2(f"{len(df)}", style={'color': COLORS['text'], 'margin': '0'}),
            html.P("Total Users", style={'color': '#94a3b8', 'margin': '5px 0 0 0'})
        ]),
        html.Div(style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '12px', 'width': '180px', 'textAlign': 'center', 'borderTop': f'4px solid {COLORS["bot"]}'}, children=[
            html.H2(f"{len(df[df['risk_label']=='Bot'])}", style={'color': COLORS['bot'], 'margin': '0'}),
            html.P("Bots Detected", style={'color': '#94a3b8', 'margin': '5px 0 0 0'})
        ]),
        html.Div(style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '12px', 'width': '180px', 'textAlign': 'center', 'borderTop': f'4px solid {COLORS["suspicious"]}'}, children=[
            html.H2(f"{len(df[df['risk_label']=='Suspicious'])}", style={'color': COLORS['suspicious'], 'margin': '0'}),
            html.P("Suspicious", style={'color': '#94a3b8', 'margin': '5px 0 0 0'})
        ]),
        html.Div(style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '12px', 'width': '180px', 'textAlign': 'center', 'borderTop': f'4px solid {COLORS["organic"]}'}, children=[
            html.H2(f"{len(df[df['risk_label']=='Organic'])}", style={'color': COLORS['organic'], 'margin': '0'}),
            html.P("Organic Users", style={'color': '#94a3b8', 'margin': '5px 0 0 0'})
        ]),
    ]),

    # Row 1: Pie Chart + Feature Importance
    html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}, children=[

        # Pie Chart
        html.Div(style={'backgroundColor': COLORS['card'], 'borderRadius': '12px', 'padding': '20px', 'flex': '1'}, children=[
            html.H3("User Distribution", style={'color': COLORS['text'], 'marginTop': '0'}),
            dcc.Graph(figure=px.pie(
                df, names='risk_label',
                color='risk_label',
                color_discrete_map={'Bot': COLORS['bot'], 'Organic': COLORS['organic'], 'Suspicious': COLORS['suspicious']},
                hole=0.4
            ).update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color=COLORS['text'],
                margin=dict(t=20, b=20)
            ))
        ]),

        # Feature Importance
        html.Div(style={'backgroundColor': COLORS['card'], 'borderRadius': '12px', 'padding': '20px', 'flex': '1'}, children=[
            html.H3("Feature Importance", style={'color': COLORS['text'], 'marginTop': '0'}),
            dcc.Graph(figure=go.Figure(go.Bar(
                x=list(feature_importance.values()),
                y=list(feature_importance.keys()),
                orientation='h',
                marker_color=COLORS['accent']
            )).update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color=COLORS['text'],
                margin=dict(t=20, b=20),
                yaxis=dict(autorange='reversed')
            ))
        ]),
    ]),

    # Row 2: Authenticity Score Distribution + Scatter
    html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}, children=[

        # Histogram
        html.Div(style={'backgroundColor': COLORS['card'], 'borderRadius': '12px', 'padding': '20px', 'flex': '1'}, children=[
            html.H3("Authenticity Score Distribution", style={'color': COLORS['text'], 'marginTop': '0'}),
            dcc.Graph(figure=px.histogram(
                df, x='authenticity_score', color='risk_label',
                color_discrete_map={'Bot': COLORS['bot'], 'Organic': COLORS['organic'], 'Suspicious': COLORS['suspicious']},
                nbins=40, barmode='overlay', opacity=0.7
            ).update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color=COLORS['text'],
                margin=dict(t=20, b=20)
            ))
        ]),

        # Scatter Plot
        html.Div(style={'backgroundColor': COLORS['card'], 'borderRadius': '12px', 'padding': '20px', 'flex': '1'}, children=[
            html.H3("Posts/Day vs Night Activity", style={'color': COLORS['text'], 'marginTop': '0'}),
            dcc.Graph(figure=px.scatter(
                df, x='avg_posts_per_day', y='night_activity_ratio',
                color='risk_label',
                color_discrete_map={'Bot': COLORS['bot'], 'Organic': COLORS['organic'], 'Suspicious': COLORS['suspicious']},
                opacity=0.6
            ).update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color=COLORS['text'],
                margin=dict(t=20, b=20)
            ))
        ]),
    ]),

    # Row 3: Interactive Filter
    html.Div(style={'backgroundColor': COLORS['card'], 'borderRadius': '12px', 'padding': '20px'}, children=[
        html.H3("Explore by Risk Label", style={'color': COLORS['text'], 'marginTop': '0'}),
        dcc.Dropdown(
            id='filter-dropdown',
            options=[{'label': i, 'value': i} for i in ['All', 'Bot', 'Organic', 'Suspicious']],
            value='All',
            style={'width': '200px', 'marginBottom': '15px'}
        ),
        dcc.Graph(id='filtered-chart')
    ])
])

@app.callback(
    Output('filtered-chart', 'figure'),
    Input('filter-dropdown', 'value')
)
def update_chart(selected):
    filtered = df if selected == 'All' else df[df['risk_label'] == selected]
    fig = px.scatter(
        filtered,
        x='engagement_burst_score',
        y='authenticity_score',
        color='risk_label',
        size='avg_posts_per_day',
        color_discrete_map={'Bot': COLORS['bot'], 'Organic': COLORS['organic'], 'Suspicious': COLORS['suspicious']},
        hover_data=['user_id', 'bot_probability']
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color=COLORS['text'],
        margin=dict(t=20, b=20)
    )
    return fig

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
