# Python Weather Forecasting Tool

This is a command line tool accepts a list of cities and returns the weather forecast.

## Usage

```
usage: app.py [-h] [--version] [--api-key API_KEY] [--date DATE] [--days DAYS] [--format {table,json,csv}] [--unit {metric,imperial,kelvin}] locations [locations ...]

positional arguments:
locations - Location names separated by spaces

optional arguments:
-h, --help Show the help message and exit
--version Show program's version number and exit

--api-key API_KEY - OpenWeatherMap API Key, if not provided default key is used.
--date DATE - Date for which the weather forecast is required. Format: YYYY-MM-DD (Optional, default is today)
--days DAYS - Number of days for which the weather forecast is required (Optional, default is 1)
--format {table,json,csv} - Output format (Optional, default is table)
--unit {metric,imperial,kelvin} - Temperature unit (Optional, default is metric)
```

# Tools

* VSCode with Python extension
* GitHub Copilot
* OpenWeatherMap API