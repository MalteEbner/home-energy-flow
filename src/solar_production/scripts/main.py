import copy
import json
from pathlib import Path
from pprint import pprint
import solar_production.compute.compute_storage
from solar_production.datamodel.common_data import Azimuth, MonthlyData, Slope
from solar_production.datamodel.pv_data import Module, PVSystem
from solar_production.datamodel.solar_data import SolarRadiationData, Time
from solar_production.compute import compute_consumption, compute_production
from solar_production.visualize import plot, print_as_table

# Define paths to your JSON files
json_files = [
    Path("solar_data/Timeseries_47.754_8.939_SA3_90deg_-90deg_2020_2023.json"),
    Path("solar_data/Timeseries_47.754_8.939_SA3_90deg_90deg_2020_2023.json"),
    Path("solar_data/Timeseries_47.753_8.939_SA3_45deg_-90deg_2020_2023.json"),
    Path("solar_data/Timeseries_47.753_8.939_SA3_45deg_90deg_2020_2023.json"),
]


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


def aggregate_per_month(times: list[Time], data: list[float], name: str) -> MonthlyData:
    data_per_month = [0.0] * 12
    for time, d in zip(times, data):
        month = time.month
        data_per_month[month - 1] += d

    return MonthlyData(name=name, data=data_per_month)


def pprint_data_per_month(data: MonthlyData):
    formatted_values = " ".join(f"{value:05.1f}" for value in data.data)
    print(f"{data.name}: {formatted_values}")


def main():
    # Load the solar radiation data from both files
    solar_datas = [load_solar_radiation_data(file) for file in json_files]

    # Filter the solar data to include include the year 2023
    for solar_data in solar_datas:
        solar_data.outputs.hourly = [
            entry for entry in solar_data.outputs.hourly if entry.time.year == 2023
        ]

    pv_system_balkonkraftwerk = PVSystem(
        modules=[
            Module(slope=Slope(value=90), azimuth=Azimuth(value=-90), kWP=0.5, n=4),
            Module(slope=Slope(value=90), azimuth=Azimuth(value=90), kWP=0.5, n=4),
        ],
        maximum_power_kW=0.8,
    )

    pv_system_full = PVSystem(
        modules=[
            Module(slope=Slope(value=45), azimuth=Azimuth(value=-90), kWP=0.5, n=4),
            Module(slope=Slope(value=45), azimuth=Azimuth(value=90), kWP=0.5, n=4),
        ],
        maximum_power_kW=10.0,
    )

    pv_system = pv_system_balkonkraftwerk
    # pv_system = pv_system_full

    # Calculate the total energy production of the module
    times, total_production = compute_production.compute_production(
        pv_system, solar_datas
    )
    print(f"Total_production: {sum(total_production):06.1f} kWh")

    # Model the energy consumption of a household
    regular_consumption = compute_consumption.generate_typical_consumption_profile(
        solar_datas[0].outputs.hourly, total_consumption_kwh=1000
    )
    heatpump_consumption = compute_consumption.generate_heatpump_consumption_profile(
        solar_datas[0].outputs.hourly,
        total_electricity_consumption_kwh=3000,
        inside_temp=15.0,
        heating_times=[(8, 18)],
    )
    total_consumption = [
        reg + heat for reg, heat in zip(regular_consumption, heatpump_consumption)
    ]

    # Calculate for each time the energy buy, energy sell and engergy self usage
    energy_buy, energy_sell, self_usage = (
        solar_production.compute.compute_storage.compute_production_consumption(
            total_production, total_consumption, storage_kWh=2.0
        )
    )

    monthly_datas = []
    for name, values in [
        ("Total Production", total_production),
        ("Regular Consumption", regular_consumption),
        ("Heatpump Consumption", heatpump_consumption),
        ("Total Consumption", total_consumption),
        ("Energy Buy", energy_buy),
        ("Energy Sell", energy_sell),
        ("Self Usage", self_usage),
    ]:
        monthly_data = aggregate_per_month(times, values, name)
        monthly_datas.append(monthly_data)

    print_as_table.pprint_data_per_month_as_table(monthly_datas)
    plot.plot_data_per_month_as_lines(monthly_datas)


if __name__ == "__main__":
    main()
