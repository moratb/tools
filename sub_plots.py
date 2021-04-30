from plotly.subplots import make_subplots
## Plotly subplots very cool
fig1 = px.imshow(kek)
fig2 = px.imshow(kek2)
trace1 = fig1['data'][0]
trace2 = fig2['data'][0]

fig = make_subplots(rows=1, cols=2, shared_xaxes=False)
fig.add_trace(trace1, row=1, col=1)
fig.add_trace(trace2, row=1, col=2)
plot(fig,show_link = False)
HTML(filename="./temp-plot.html")
