from datetime import datetime, timedelta

from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics


def forecast(df, horizon, start_date, end_date):
    """forecast the stock price and get the metrics of performance, by using the lib prophet

    # https://facebook.github.io/prophet/

      Args:
          df: the data frame used by fit the model
          horizon: the forecast horizon (days)
          start_date: history date from
          end_date: history date to

      Returns:
          df_forecast: data frame that contains predicted stock price
          df_cv_1: data frame that contains test date in test horizon#1
          df_cv_2: data frame that contains test date in test horizon#2
          df_p: data frame that contains performance metrics

    """
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=int(horizon), include_history=False)
    # get the predicted stock price
    df_forecast = m.predict(future)[["ds", "yhat"]]

    # get the test period
    period = abs(datetime.strptime(start_date, "%Y-%m-%d") - datetime.strptime(end_date, "%Y-%m-%d")) // 5
    # get the test result, and split to two data frame
    df_cv = cross_validation(m, horizon=f"{period} days")
    cutoff_list = df_cv["cutoff"].unique().tolist()
    df_cv_1 = df_cv[df_cv["cutoff"] == cutoff_list[0]]
    df_cv_2 = df_cv[df_cv["cutoff"] == cutoff_list[1]]

    # get the performance metrics
    df_p = performance_metrics(df_cv)
    df_p["horizon"] = df_p["horizon"].dt.days

    return df_forecast, df_cv_1, df_cv_2, df_p
