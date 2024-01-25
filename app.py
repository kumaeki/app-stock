import json
import os
from datetime import datetime, timedelta

import plotly
import yfinance as yf
from flask import Flask, render_template, request, send_from_directory
from plotly.graph_objs import Scatter
from prophet import Prophet

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    name = request.form.get("name")
    if name == None:
        name = ""

    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    print(f"name = {name}, start_date = {start_date}, end_date = {end_date}")

    return render_template("index.html", name=name, start_date=start_date, end_date=end_date)


@app.route("/result", methods=["POST"])
def result():
    name = request.form.get("name")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    print(f"from {start_date} to {end_date}")
    if name:
        data = yf.download(name, start=start_date, end=end_date)
        print("Request for hello page received with name=%s" % name)
        df_new = data.reset_index()
        df_new = df_new[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"})
        m = Prophet()
        m.fit(df_new)
        future = m.make_future_dataframe(periods=30)
        forecast = m.predict(future)[["ds", "yhat"]]
        print(forecast.head())
        print(forecast.tail())
        graphs = (
            {
                "data": [Scatter(x=forecast["ds"], y=forecast["yhat"])],
                "layout": {
                    "title": "Predicted stock price",
                    "yaxis": {"title": "date"},
                    "xaxis": {"title": "stock prick"},
                },
            },
        )
        graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template("result.html", graphJSON=graphJSON, name=name, start_date=start_date, end_date=end_date)
    else:
        return render_template("result.html", name=name, start_date=start_date, end_date=end_date)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    app.run()
