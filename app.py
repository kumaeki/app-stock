import json
import os
from datetime import datetime, timedelta

import pandas as pd
import plotly
import yfinance as yf
from flask import Flask, render_template, request, send_from_directory
from plotly.graph_objs import Scatter
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    name = request.form.get("name")
    if name == None:
        name = ""

    horizon = request.form.get("horizon")
    if horizon == None:
        horizon = 30

    date_pre_1m = (datetime.now() - timedelta(days=300)).strftime("%Y-%m-%d")
    date_pre_1d = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    start_date = request.form.get("start_date")
    if start_date == None:
        start_date = date_pre_1m

    end_date = request.form.get("end_date")
    if end_date == None:
        end_date = date_pre_1d

    print(f"name = {name}, start_date = {start_date}, end_date = {end_date}")
    return render_template(
        "index.html",
        name=name,
        horizon=horizon,
        start_date=start_date,
        end_date=end_date,
        previous_day=date_pre_1d,
    )


@app.route("/result", methods=["POST"])
def result():
    name = request.form.get("name")
    horizon = request.form.get("horizon")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    if name:
        data = yf.download(name, start=start_date, end=end_date)
        print("Request for hello page received with name=%s" % name)
        df_new = data.reset_index()
        df_new = df_new[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"})
        m = Prophet()
        m.fit(df_new)
        future = m.make_future_dataframe(periods=int(horizon), include_history=False)
        forecast = m.predict(future)[["ds", "yhat"]]

        period = (
            abs(
                datetime.strptime(start_date, "%Y-%m-%d")
                - datetime.strptime(end_date, "%Y-%m-%d")
            )
            // 5
        )
        df_cv = cross_validation(m, horizon=f"{period} days")
        cutoff_list = df_cv["cutoff"].unique().tolist()

        df_cv_1 = df_cv[df_cv["cutoff"] == cutoff_list[0]]

        df_cv_2 = df_cv[df_cv["cutoff"] == cutoff_list[1]]
        df_p = performance_metrics(df_cv)

        df_p["horizon"] = df_p["horizon"].dt.days

        graphs = [
            {
                "data": [
                    Scatter(
                        x=forecast["ds"],
                        y=forecast["yhat"],
                        name="Predicted",
                        marker=dict(color="blue"),
                    ),
                    Scatter(
                        x=df_new["ds"],
                        y=df_new["y"],
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

        return render_template(
            "result.html",
            ids=ids,
            graphJSON=graphJSON,
            horizon=horizon,
            name=name,
            start_date=start_date,
            end_date=end_date,
        )
    else:
        return render_template(
            "result.html", name=name, start_date=start_date, end_date=end_date
        )


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    app.run()
