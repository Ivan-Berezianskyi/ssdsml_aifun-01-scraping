import json


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


def analyze_daily_weather(day, temp_threshold=30, wind_threshold=15, humidity_threshold=70):
    """
    Analyze weather data for a single day.

    Args:
        day (dict): The weather data for the day.
        temp_threshold (float): The temperature threshold to determine a hot day.
        wind_threshold (float): The wind speed threshold to determine a windy day.
        humidity_threshold (float): The humidity threshold to determine uncomfortable weather.

    Returns:
        dict: A dictionary with analysis results for the day.
    """
    temp_swing = round(day["max_temperature"] - day["min_temperature"], 1)
    precipitation = day["precipitation"]

    if precipitation == 0:
        rain_severity = "none"
    elif precipitation < 2.5:
        rain_severity = "light"
    elif precipitation <= 7.6:
        rain_severity = "moderate"
    else:
        rain_severity = "heavy"

    info = {
        "date": day["date"],
        "max_temperature": day["max_temperature"],
        "min_temperature": day["min_temperature"],
        "precipitation": precipitation,
        "wind_speed": day["wind_speed"],
        "humidity": day["humidity"],
        "weather_description": day["weather_description"],
        "is_hot_day": day["max_temperature"] > temp_threshold,
        "temperature_swing": temp_swing,
        "is_significant_swing": temp_swing > 10,
        "is_windy_day": day["wind_speed"] > wind_threshold,
        "is_uncomfortable_day": day["humidity"] > humidity_threshold,
        "is_rainy_day": precipitation > 0,
        "rain_severity": rain_severity,
    }

    return info


def generate_daily_report(analysis):
    """
    Generate a detailed report based on the analysis results for a single day.

    Args:
        analysis (dict): The analysis results for the day.

    Returns:
        str: A detailed report as a string.
    """
    temp_value = analysis.get("max_temperature", analysis["temperature_swing"])

    lines = [
        f"Date: {analysis['date']}",
        f"Weather: {analysis['weather_description']}",
        f"Temperature: Max {temp_value}°C",
        "It was a hot day." if analysis["is_hot_day"] else "It was not a hot day.",
        "It was a windy day." if analysis["is_windy_day"] else "It was not a windy day.",
        "It was an uncomfortable day." if analysis["is_uncomfortable_day"] else "Humidity was comfortable.",
    ]

    if analysis["is_rainy_day"]:
        severity = analysis.get("rain_severity", "moderate")
        lines.append(f"It was a rainy day ({severity} rain).")
    else:
        lines.append("There was no precipitation.")

    report = "\n".join(lines)
    return report


def summarize_weather_analysis(analyses):
    """
    Summarize the weather analysis over multiple days.

    Args:
        analyses (list of dict): A list of daily analysis results.

    Returns:
        str: A summary report as a string.
    """
    hottest = max(analyses, key=lambda d: (d.get("max_temperature", 0), d["is_hot_day"]))
    windiest = max(analyses, key=lambda d: (d.get("wind_speed", 0), d["is_windy_day"]))
    most_humid = max(analyses, key=lambda d: (d.get("humidity", 0), d["is_uncomfortable_day"]))
    rainiest = max(analyses, key=lambda d: (d.get("precipitation", 0), d["is_rainy_day"]))

    report = (
        f"Hottest day: {hottest['date']}\n"
        f"Windiest day: {windiest['date']}\n"
        f"Most humid day: {most_humid['date']}\n"
        f"Rainiest day: {rainiest['date']}"
    )
    return report


if __name__ == "__main__":
    # Load the JSON data
    weather_data = load_json("tokyo_weather_complex.json")
    print(weather_data)
    # Analyze the weather data for each day
    analyses = [analyze_daily_weather(day) for day in weather_data['daily']]

    # Generate and print daily reports
    for analysis in analyses:
        report = generate_daily_report(analysis)
        print(report)

    # Generate and print a summary report
    summary_report = summarize_weather_analysis(analyses)
    print(summary_report)