import yfinance as yf


def fetch_data(stock_code, start_date, end_date):
    """Fetch Stock info from yahoo fiance using yfinance lib

    # yahoo fiance : https://finance.yahoo.com/
    # yfinance : https://pypi.org/project/yfinance/

      Args:
          stock_code: stock code
          start_date: history date from
          end_date: history date to

      Returns:
          data: DataFrame download from https://finance.yahoo.com/

    """
    data = yf.download(stock_code, start_date, end_date)
    return data
