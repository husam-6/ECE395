""" Husam Almanakly and Michael Bentivegna

Script to create a Gantt Chart for Senior Projects
"""

# %% Libraries
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd


# %%
df = pd.DataFrame([
    dict(Task="Rules Engine", Start='2022-10-11', Finish='2022-10-25'),
    dict(Task="Voice Recognition", Start='2022-10-18', Finish='2022-11-08'),
    dict(Task="Gantry System", Start='2022-11-06', Finish='2022-11-22'),
    dict(Task="Integration", Start='2022-11-08', Finish='2022-11-29'),
    dict(Task="Custom Chess Board", Start='2022-11-29', Finish='2022-12-20'),
    dict(Task="Format Input", Start='2022-11-29', Finish='2022-12-06'),
    dict(Task="WINTER BREAK / BUFFER", Start='2022-12-20', Finish='2023-01-16'),
    dict(Task="Magnets and Z-axis", Start='2023-01-17', Finish='2023-02-14'),
    dict(Task="Controller Setup", Start='2023-01-31', Finish='2023-03-21'),
    dict(Task="Board and Piece Movement", Start='2023-03-21', Finish='2023-04-18'),
    dict(Task="Test & Troubleshoot", Start='2023-04-18', Finish='2023-05-09')
])

# fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
# fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
fig = ff.create_gantt(df)
fig.show()