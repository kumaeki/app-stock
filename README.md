# Forecast the Stock Price

This is a app which try to forecast the stock price in future

## Data

Fetch the stock data from <https://finance.yahoo.com>, by using [yfinance](https://pypi.org/project/yfinance/)

## Model

Forecast the future price by using [Prophet](https://facebook.github.io/prophet/)

## Code

```text
.vscode
    settings.json  (setting file for vscode)
scripts (python files)
    fetch_data.py (fetch data from yahoo)
    forecast.py (forecast the price)
    graphs.py (generate json for user interface)
static (bootstrap css/js files and image files)
templates
    index.html (input the stock information)
    result.html (show the result)
.deployment (used by azure)
.gitignore
app.py (the main python file)
README.md
requirements.txt
```

## Run in local

```zsh
# create a new virtual environment
python -m venv .venv

# activate the virtual environment
source .venv/bin/activate

# install the necessary packages
pip install -r requirements.txt

# run the flask app
flask run
```

## Run in Azure

This app is created based on the Azure Quick start [Deploy a Python (Django or Flask) web app to Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python).

For instructions on how to create the Azure resources and deploy the application to Azure, refer to the Quick start article.

you could find my sample app here <https://app-stock-price.azurewebsites.net/>
