import requests
import json


def fetch_weather_data():
    """
    Fetch the maximum temperature forecast for Tokyo using the Open-Meteo API.

    Returns:
        dict: A dictionary containing the date and the maximum temperature.
    """
    lat = 35.6895
    lon = 139.6917
    params = {"latitude": lat, "longitude": lon,
              "daily": "temperature_2m_max",
              "timezone": "Asia/Tokyo"
              }
    headers = {
        "User-Agent": "DataScienceLearningNotebook/1.0"
    }
    response = requests.get("https://api.open-meteo.com/v1/forecast", params=params, headers=headers, timeout=3)
    response = response.json()["daily"]
    max_i = response["temperature_2m_max"].index(max(response["temperature_2m_max"]))
    return {
        "date": response["time"][max_i],
        "max_temperature": response["temperature_2m_max"][max_i]}


def save_to_json(data, filename):
    """
    Save the extracted weather data to a JSON file.

    Args:
        data (dict): The data to be saved.
        filename (str): The name of the JSON file.
    """
    ...
    with open(filename, "w") as file:
        json.dump(data, file)

if __name__ == "__main__":
    # Fetch the weather data
    weather_data = fetch_weather_data()
    print(weather_data)
    # Save the data to a JSON file
    save_to_json(weather_data, "tokyo_weather.json")

    print("Data successfully saved to tokyo_weather.json")
