import plotly.graph_objects as go
from plotly.subplots import make_subplots


def draw_plot_wins(wins, draws, losses, colors):
    figure_wins = make_subplots(
        rows=1,
        cols=1,
        vertical_spacing=0.05,
    )
    labels = ['Wins', 'Draws', ' Losses']
    values = [wins, draws, losses]
    figure_wins.add_trace(go.Pie(labels=labels, values=values, pull=[0.2, 0, 0],
                                 marker_colors=[colors[1], colors[2], colors[4]],
                                 showlegend=False, name='W/D/L')
                          )

    figure_wins.update_layout(paper_bgcolor='#2E2E2E', plot_bgcolor='#2E2E2E', font_color='white', width=1700,
                              title='W/D/L', title_font_family="Signika-Regular")
    return figure_wins


def draw_plot_wins_sunburst(wins, draws, losses, wins_home,
                            wins_away, draws_home, draws_away,
                            losses_home, losses_away, colors):

    figure_wins = go.Figure(go.Sunburst(
        labels=['Games', 'Wins', 'Draws', 'Losses', 'Wins H', 'Wins A', 'Draws H', 'Draws A', 'Losses H', 'Losses A'],
        parents=['', 'Games', 'Games', 'Games', 'Wins', 'Wins', 'Draws', 'Draws', 'Losses', 'Losses'],
        values=[(wins+draws+losses), wins, draws, losses, wins_home,
                wins_away, draws_home, draws_away, losses_home, losses_away],
        branchvalues="total",
    ))

    figure_wins.update_layout(paper_bgcolor='#2E2E2E', plot_bgcolor='#2E2E2E', font_color='white', width=500,
                              title='W/D/L', title_font_family="Signika-Regular", colorway=colors,
                              margin=dict(t=0, l=0, r=0, b=0), showlegend=True)
    return figure_wins
