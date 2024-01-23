import json
import os

import plotly
import yfinance as yf
from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from plotly.graph_objs import Scatter
from prophet import Prophet

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    name = request.form.get("name")

    if name:
        data = yf.download(name, start="2023-01-01", end="2024-01-01")
        print("Request for hello page received with name=%s" % name)
        df_new = data.reset_index()
        df_new = df_new[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"})
        m = Prophet()
        m.fit(df_new)
        future = m.make_future_dataframe(periods=30)
        forecast = m.predict(future)[["ds", "yhat"]]
        print(forecast)
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
        return render_template("index.html", graphJSON=graphJSON)
    else:
        print("Request for hello page received with no name or blank name -- redirecting")
        return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"), "favicon.ico", mimetype="image/vnd.microsoft.icon"
    )


if __name__ == "__main__":
    app.run()
