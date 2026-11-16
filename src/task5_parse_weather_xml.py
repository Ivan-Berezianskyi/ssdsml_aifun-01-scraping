import xml.etree.ElementTree as ET
import csv


def parse_weather_xml(xml_file):
    """
    Parse weather data from an XML file.

    Args:
        xml_file (str): Path to the XML file.

    Returns:
        list of dict: A list of dictionaries with parsed weather data.
    """
    with open(xml_file, "r") as f:
        raw = ET.parse(f).getroot()

    cooked = []

    for child in raw:
        day_data = {}
        for elem in child:
            if elem.tag in ("temperature", "precipitation"):
                day_data[elem.tag] = float(elem.text)
            elif elem.tag == "humidity":
                day_data[elem.tag] = int(elem.text)
            else:
                day_data[elem.tag] = elem.text
        cooked.append(day_data)

    return cooked


def save_to_csv(data, filename="parsed_weather_data.csv"):
    """
    Save parsed weather data to a CSV file.

    Args:
        data (list of dict): Parsed weather data.
        filename (str): Name of the CSV file.
    """
    fieldnames = ["Date", "Temperature", "Humidity", "Precipitation"]

    rows = [
        {
            "Date": row["date"],
            "Temperature": row["temperature"],
            "Humidity": row["humidity"],
            "Precipitation": row["precipitation"],
        }
        for row in data
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(rows)


if __name__ == "__main__":
    # Parse the XML file
    weather_data = parse_weather_xml("weather_data.xml")

    # Save the parsed data to a CSV file
    save_to_csv(weather_data)
    print(
        "Data has been successfully parsed and saved to parsed_weather_data.csv."
    )