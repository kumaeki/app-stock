import os
from datetime import datetime, timedelta

from flask import Flask, render_template, request, send_from_directory

from scripts.fetch_data import fetch_data
from scripts.forecast import forecast
from scripts.graphs import generate_graphs_json

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    code = request.form.get("code")
    if code == None:
        code = ""

    horizon = request.form.get("horizon")
    if horizon == None:
        horizon = 30

    date_pre_1y = (datetime.now() - timedelta(days=300)).strftime("%Y-%m-%d")
    start_date = request.form.get("start_date")
    if start_date == None:
        start_date = date_pre_1y

    date_pre_1d = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = request.form.get("end_date")
    if end_date == None:
        end_date = date_pre_1d

    return render_template(
        "index.html",
        code=code,
        horizon=horizon,
        start_date=start_date,
        end_date=end_date,
        previous_day=date_pre_1d,
    )


@app.route("/result", methods=["POST"])
def result():

    code = request.form.get("code")
    horizon = request.form.get("horizon")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    if code:
        # fetch data
        data = fetch_data(code, start_date, end_date)

        # if there is no data for the stock code,back to index.html
        if data.empty:
            return render_template(
                "index.html",
                code=code,
                horizon=horizon,
                start_date=start_date,
                end_date=end_date,
                previous_day=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
                error=True,
            )

        # preprocess the stock price data
        data = data.reset_index()
        df_new = data[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"})

        # forecast the future price
        df_forecast, df_cv_1, df_cv_2, df_p = forecast(df_new, horizon, start_date, end_date)

        # generate the ids and graphJSON show in result.html
        ids, graphJSON = generate_graphs_json(df_new, df_forecast, df_cv_1, df_cv_2, df_p)

        return render_template(
            "result.html",
            ids=ids,
            graphJSON=graphJSON,
            horizon=horizon,
            code=code,
            start_date=start_date,
            end_date=end_date,
        )
    else:
        return render_template("index.html", code=code, start_date=start_date, end_date=end_date)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    app.run()
