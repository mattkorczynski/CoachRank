import plotly.graph_objects as go
from plotly.subplots import make_subplots

def draw_plot_wins(wins, draws, losses, COLORS):
    figure_wins = make_subplots(
        rows=1,
        cols=1,
        vertical_spacing=0.05,
    )
    labels = ['Wins', 'Draws', ' Losses']
    values = [wins, draws, losses]
    figure_wins.add_trace(go.Pie(labels=labels, values=values, pull=[0.2, 0, 0],
                                 marker_colors=[COLORS[1], COLORS[2], COLORS[4]],
                                 showlegend=False, name='W/D/L')
                          )

    figure_wins.update_layout(paper_bgcolor='#2E2E2E', plot_bgcolor='#2E2E2E', font_color='white', width=1700,
                              title='W/D/L', title_font_family="Signika-Regular")
    return figure_wins