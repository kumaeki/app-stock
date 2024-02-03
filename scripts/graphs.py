import json

import plotly
from plotly.graph_objs import Scatter


def generate_graphs_json(df_historic, df_forecast, df_cv_1, df_cv_2, df_p):
    """generate the graph id list and graph json used by result.html


    Args:
        df_historic: the historic stock price
        df_forecast: the predicted stock price
        df_cv_1: test date in test horizon#1
        df_cv_2: test date in test horizon#2
        df_p: performance metrics

    Returns:
        ids: graph id list
        graphJSON: graph setting json
    """
    graphs = [
        {
            "data": [
                Scatter(
                    x=df_forecast["ds"],
                    y=df_forecast["yhat"],
                    name="Predicted",
                    marker=dict(color="blue"),
                ),
                Scatter(
                    x=df_historic["ds"],
                    y=df_historic["y"],
                    name="Actual",
                    marker=dict(color="red"),
                ),
            ],
            "layout": {
                "title": "stock price",
                "xaxis": {"title": "date"},
                "yaxis": {"title": "stock prick"},
            },
        },
        {
            "data": [
                Scatter(x=df_p["horizon"], y=df_p["mape"]),
            ],
            "layout": {
                "title": "mean absolute percent error(mape) vs forecast horizon(days)",
                "xaxis": {"title": "forecast horizon(days)"},
                "yaxis": {"title": "mape"},
            },
        },
        {
            "data": [
                Scatter(
                    x=df_cv_1["ds"],
                    y=df_cv_1["yhat"],
                    name="Predicted",
                    marker=dict(color="blue"),
                ),
                Scatter(
                    x=df_cv_1["ds"],
                    y=df_cv_1["y"],
                    name="Actual",
                    marker=dict(color="red"),
                ),
            ],
            "layout": {
                "title": "Predicted/Actual stock price # 1",
                "xaxis": {"title": "date"},
                "yaxis": {"title": "stock prick"},
            },
        },
        {
            "data": [
                Scatter(
                    x=df_cv_2["ds"],
                    y=df_cv_2["yhat"],
                    name="Predicted",
                    marker=dict(color="blue"),
                ),
                Scatter(
                    x=df_cv_2["ds"],
                    y=df_cv_2["y"],
                    name="Actual",
                    marker=dict(color="red"),
                ),
            ],
            "layout": {
                "title": "Predicted/Actual stock price # 2",
                "xaxis": {"title": "date"},
                "yaxis": {"title": "stock prick"},
            },
        },
    ]
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return ids, graphJSON
