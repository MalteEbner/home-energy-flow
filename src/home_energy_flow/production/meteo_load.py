# Define paths to your JSON files
import json
from pathlib import Path
from home_energy_flow.production.meteo_datamodels import SolarRadiationData, Time


def preprocess_hourly_data(hourly_data: list) -> list:
    """Preprocess hourly data to convert time strings into Time instances."""
    preprocessed_data = []
    for entry in hourly_data:
        # Convert the 'time' field to a Time instance
        entry["time"] = Time.from_string(entry["time"])
        preprocessed_data.append(entry)
    return preprocessed_data


def load_solar_radiation_data(file_path: Path) -> SolarRadiationData:
    # Read the JSON data from the file
    with open(file_path, "r") as file:
        data = json.load(file)

    # Preprocess the 'hourly' data to handle the 'time' conversion
    data["outputs"]["hourly"] = preprocess_hourly_data(data["outputs"]["hourly"])

    # Convert the data into a SolarRadiationData instance using Pydantic
    return SolarRadiationData(**data)


def get_meteo_data_per_orientation() -> list[SolarRadiationData]:
    json_files = [
        Path("meteo_data_source/Timeseries_47.754_8.939_SA3_90deg_-90deg_2020_2023.json"),
        Path("meteo_data_source/Timeseries_47.754_8.939_SA3_90deg_90deg_2020_2023.json"),
        Path("meteo_data_source/Timeseries_47.753_8.939_SA3_45deg_-90deg_2020_2023.json"),
        Path("meteo_data_source/Timeseries_47.753_8.939_SA3_45deg_90deg_2020_2023.json"),
    ]

    # Load the solar radiation data from both files
    return [load_solar_radiation_data(file) for file in json_files]
