# Create a command line python application which accepts locations as command line arguments and prints the weather forecast details of those locations.
# Use argparse module to accept the locations as command line arguments.
# Use requests module to call the OpenWeatherMap API.
# Use prettytable module to display the results in tabular format.
# Use the following API key for calling OpenWeatherMap API - "012f92fc159de655d60e4ab2c4d7cad6"
# Use proper error handling techniques like if 404 error is coming, print "City Not Found" etc.
# Use proper naming conventions for variables, functions etc.
# Usage: python app.py location1 location2
# Example: python app.py Delhi Mumbai
# Should be able to accept any number of locations as command line arguments.
# Should be able to accept location names with spaces in between like "Los Angeles".
# Should be able to accept output formats like json, csv, table etc. as command line arguments.
# Example: python app.py Delhi Mumbai --format json
# Should be able to accept the unit as command line argument.
# Example: python app.py Delhi Mumbai --unit metric or imperial or kelvin
# Should be able to accept the API key as command line argument.
# Should be able to accept API key as command line argument, if not passed, use the default API key and show a warning message.
# Include an option to skip the API key warning message.
# Include an option to show the help message.
# Example: python app.py Delhi Mumbai --api-key 012f92fc159de655d60e4ab2c4d7cad6
# Error handling for invalid locations, invalid units, invalid output formats, invalid API key etc.
# Errors should be printed in red color with format "Error: <error message>".
# Output table should only show the following fields: "Location", "Weather", "Temperature", "Min Temp", "Max Temp", "Humidity", "Wind Speed", "Wind Degree", "Clouds", "Pressure", "Sunrise", "Sunset" and only one header row should be there.
# Don't use JSON object indexes directly, use the keys instead.
# Don't use the OpenWeatherMap API URL directly, use the API key and location name to call the API.
# Use the following API URL for calling OpenWeatherMap API forecast- "http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units={}&cnt={}&dt={}"
# Should be able to accept date and days as command line arguments and show the weather forecast for those days.
# If date is not passed, show the current weather forecast. If the days are not passed, show the weather forecast for the next 5 days.
# Example: python app.py Delhi Mumbai --date 2021-05-01 --days 3
# Use proper naming conventions for variables, functions etc.

# Path: app.py

import argparse
import requests
import json
from prettytable import PrettyTable
from colorama import Fore, Style
from datetime import datetime

# API key
API_KEY = "012f92fc159de655d60e4ab2c4d7cad6"

# API URL
API_URL = "http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units={}&cnt={}&dt={}"

# Define a function to get the weather forecast for the given locations
def get_weather_forecast(locations, date, days, api_key, units):
    weather_forecast_list = []
    for location in locations:
        response = requests.get(API_URL.format(location, api_key, units, days, date))
        if response.status_code == 200:
            weather_forecast_list.append(response.json())
        elif response.status_code == 401:
            print(
                Fore.RED
                + "Invalid API key. Please check the API key and try again."
                + Fore.RESET
            )
        elif response.status_code == 404:
            print(
                Fore.RED
                + "City not found " + location + ". Please check the city name and try again."
                + Fore.RESET
            )
        elif response.status_code == 429:
            print(
                Fore.RED
                + "Too many requests. Please wait for sometime and try again."
                + Fore.RESET
            )
        else:
            print(Fore.RED + "Some error occurred. Please try again." + Fore.RESET)
    # Return the weather forecast list
    return weather_forecast_list


def parse_arguments():
    # Create a parser object
    parser = argparse.ArgumentParser()
    parser.description = "Weather Forecast CLI Tool."
    # Add the arguments
    parser.add_argument(
        "locations", nargs="+", help="Location names separated by spaces"
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.1")
    parser.add_argument("--api-key", help="OpenWeatherMap API Key, if not provided default key is used")
    parser.add_argument(
        "--date",
        help="Date for which the weather forecast is required. Format: YYYY-MM-DD (Optional, default is today)",
        default=datetime.now().strftime("%Y-%m-%d"),
    )
    parser.add_argument(
        "--days",
        help="Number of days for which the weather forecast is required (Optional, default is 1)",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--format",
        help="Output format (Optional, default is table)",
        choices=["table", "json", "csv"],
        default="table",
    )
    parser.add_argument(
        "--unit",
        help="Temperature unit (Optional, default is metric)",
        choices=["metric", "imperial", "kelvin"],
        default="metric",
    )
    
    # Parse the arguments
    args = parser.parse_args()
    # Return the arguments
    return args


def print_weather_forecasts(weather_forecast_lists, format):
    if format == "json":
        # Parse the result and print the weather forecast in JSON format
        print(json.dumps(weather_forecast_lists, indent=4))
    elif format == "csv":
        # Parse the result and print the weather forecast in CSV format
        print(
            "Location,Date,Weather,Temperature,Min Temp,Max Temp,Humidity,Wind Speed,Wind Degree,Clouds,Pressure"
        )
        for weather_forecast_list in weather_forecast_lists:
            for weather_forecast in weather_forecast_list["list"]:
                print("{},".format(weather_forecast_list["city"]["name"]), end="")
                print(
                    "{},".format(
                        datetime.fromtimestamp(weather_forecast["dt"]).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    ),
                    end="",
                )
                print(
                    "{},".format(weather_forecast["weather"][0]["description"]), end=""
                )
                print("{},".format(weather_forecast["main"]["temp"]), end="")
                print("{},".format(weather_forecast["main"]["temp_min"]), end="")
                print("{},".format(weather_forecast["main"]["temp_max"]), end="")
                print("{},".format(weather_forecast["main"]["humidity"]), end="")
                print("{},".format(weather_forecast["wind"]["speed"]), end="")
                print("{},".format(weather_forecast["wind"]["deg"]), end="")
                print("{},".format(weather_forecast["clouds"]["all"]), end="")
                print("{}".format(weather_forecast["main"]["pressure"]))
    elif format == "table":
        # Parse the result and print the weather forecast in tabular format
        table = PrettyTable(
            [
                "Location",
                "Date",
                "Weather",
                "Temperature",
                "Min Temp",
                "Max Temp",
                "Humidity",
                "Wind Speed",
                "Wind Degree",
                "Clouds",
                "Pressure",
            ]
        )
        for weather_forecast_list in weather_forecast_lists:
            for weather_forecast in weather_forecast_list["list"]:
                table.add_row(
                    [
                        weather_forecast_list["city"]["name"],
                        datetime.fromtimestamp(weather_forecast["dt"]).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        weather_forecast["weather"][0]["description"],
                        weather_forecast["main"]["temp"],
                        weather_forecast["main"]["temp_min"],
                        weather_forecast["main"]["temp_max"],
                        weather_forecast["main"]["humidity"],
                        weather_forecast["wind"]["speed"],
                        weather_forecast["wind"]["deg"],
                        weather_forecast["clouds"]["all"],
                        weather_forecast["main"]["pressure"],
                    ]
                )
        print(table)


def main():
    # Parse the arguments
    args = parse_arguments()
    # Get the location
    locations = args.locations
    # Get the date, if not provided then use today's date
    date = args.date if args.date else datetime.now().strftime("%Y-%m-%d")
    # Get the number of days for which the weather forecast is required, if not provided then use 1
    days = args.days if args.days else 1
    # Get the API key, if not provided then use the default API key
    api_key = args.api_key if args.api_key else API_KEY
    # Get the units, if not provided then use the default units
    units = args.unit if args.unit else "metric"
    # Get the output format, if not provided then use the default format
    format = args.format if args.format else "table"

    # Get the weather forecast
    weather_forecasts = get_weather_forecast(locations, date, days, api_key, units)

    # Print the weather forecast
    print_weather_forecasts(weather_forecasts, format)
    print(Style.RESET_ALL, end="")

# Call the main function
if __name__ == "__main__":
    main()
