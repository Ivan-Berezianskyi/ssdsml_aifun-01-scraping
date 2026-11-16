import json
import csv


def load_json(filename):
    """
    Load JSON data from a file.

    Args:
        filename (str): The name of the JSON file to load.

    Returns:
        dict: The loaded JSON data.
    """

    with open(filename, "r") as f:
        return json.load(f)


def summarize_weather_data(data):
    """
    Summarize the weather data across all datas.

    Args:
        data (list of dict): The daily weather data.

    Returns:
        dict: A summary of the key metrics across all datas.
    """
    num_days = len(data)
    summary = {
        "average_max_temp": sum(day["max_temperature"] for day in data) / num_days if num_days else 0,
        "average_min_temp": sum(day["min_temperature"] for day in data) / num_days if num_days else 0,
        "total_precipitation": sum(day["precipitation"] for day in data),
        "average_wind_speed": sum(day["wind_speed"] for day in data) / num_days if num_days else 0,
        "average_humidity": sum(day["humidity"] for day in data) / num_days if num_days else 0,
        "hot_days": sum(1 for day in data if day["max_temperature"] > 30),
        "windy_days": sum(1 for day in data if day["wind_speed"] > 15),
        "rainy_days": sum(1 for day in data if day["precipitation"] > 0),
    }

    return summary


def export_to_csv(data, file):
    """
    Export the summarized weather data to a CSV file or file-like object.

    Args:
        data (list of dict): The daily weather data to export.
        file (str or file-like object): The name of the CSV file to save the data in, or a file-like object.
    """
    fieldnames = [
        "Date",
        "Max Temperature",
        "Min Temperature",
        "Precipitation",
        "Wind Speed",
        "Humidity",
        "Weather Description",
        "Is Hot Day",
        "Is Windy Day",
        "Is Rainy Day",
    ]

    rows = []
    for day in data:
        rows.append({
            "Date": day["date"],
            "Max Temperature": day["max_temperature"],
            "Min Temperature": day["min_temperature"],
            "Precipitation": day["precipitation"],
            "Wind Speed": day["wind_speed"],
            "Humidity": day["humidity"],
            "Weather Description": day["weather_description"],
            "Is Hot Day": day["max_temperature"] > 30,
            "Is Windy Day": day["wind_speed"] > 15,
            "Is Rainy Day": day["precipitation"] > 0,
        })

    if isinstance(file, str):
        with open(file, "w", newline="", encoding="utf-8") as f:
            csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(rows)
    else:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(rows)


if __name__ == "__main__":
    # Load the JSON data
    weather_data = load_json("tokyo_weather_complex.json")

    # Summarize the weather data
    summary = summarize_weather_data(weather_data['daily'])

    # Print the summary for verification
    print("Weather Data Summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")

    # Export the summarized data to a CSV file
    export_to_csv(weather_data['daily'], "tokyo_weather_summary.csv")

    print("Data successfully exported to tokyo_weather_summary.csv")