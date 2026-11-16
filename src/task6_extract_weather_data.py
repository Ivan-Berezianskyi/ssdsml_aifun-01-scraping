import csv
import re


def clean_text(line):
    """
    Clean the text line by removing non-ASCII characters and fixing known issues.

    Args:
        line (str): The line of text to clean.

    Returns:
        str: The cleaned line of text.
    """



def extract_weather_data(text_file):
    """
    Extract weather data from a text file using regular expressions.

    Args:
        text_file (str): Path to the text file.

    Returns:
        list of dict: A list of dictionaries with extracted weather data.
    """
    with open(text_file, "r", encoding="utf-8", errors="ignore") as f:
        raw_text = f.read()

    cleaned_text = re.sub(r"[^\x00-\x7F]+", "", raw_text)

    pattern = r"Date: ([\d-]+), Max Temp: ([\d.-]+)C, Min Temp: ([\d.-]+)C, Humidity: (\d+)%, Precipitation: ([\d.]+)mm"

    extracted_data = []
    for date, max_t, min_t, hum, prec in re.findall(pattern, cleaned_text):
        extracted_data.append({
            "date": date,
            "max_temperature": float(max_t),
            "min_temperature": float(min_t),
            "humidity": int(hum),
            "precipitation": float(prec),
        })

    return extracted_data

def save_to_csv(data, filename="extracted_weather_data.csv"):
    """
    Save extracted weather data to a CSV file.

    Args:
        data (list of dict): Extracted weather data.
        filename (str): Name of the CSV file.
    """
    extracted_data = []
    for day in data:
        date, max_t, min_t, hum, prec = day.values()
        print(data)
        extracted_data.append({
            "Date": date,
            "Max Temperature": float(max_t),
            "Min Temperature": float(min_t),
            "Humidity": int(hum),
            "Precipitation": float(prec),
        })

    with open(filename, "w", newline="", encoding="utf-8") as f:
        csv_writer = csv.DictWriter(f, fieldnames=extracted_data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(extracted_data)

if __name__ == "__main__":
    # Extract data from the text file
    weather_data = extract_weather_data("weather_report.txt")

    # Save the extracted data to a CSV file
    save_to_csv(weather_data)
    print(
        "Data has been successfully extracted and saved to extracted_weather_data.csv."
    )
