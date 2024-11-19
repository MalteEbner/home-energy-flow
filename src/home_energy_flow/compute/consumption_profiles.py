from collections import defaultdict
from typing import List
from home_energy_flow.production.meteo_data import TimeSeriesEntry


def generate_typical_consumption_profile(
    entries,
    total_consumption_kwh,
) -> List[float]:
    """
    Generate a typical electricity consumption profile for a household in Germany
    based on a list of TimeSeriesEntry, scaled to match a given total consumption in kWh per year.

    Args:
        entries:
            Timepoints for each hour of the year.
        total_consumption_kwh:
            Total desired consumption in kWh for the year.

    Returns:
         List of consumption values (in kWh) corresponding to each time entry.
         The sum of all values in the list will be equal to the total_consumption_kwh.
    """

    # Average consumption patterns, simplified example
    # Higher consumption in the morning and evening, lower consumption during the night.
    # TODO(Malte, 11/24): Replace this with a "Standardlastprofile Strom H0" from BDEW
    typical_daily_profile_first_half = [
        0.08,
        0.07,
        0.06,
        0.05,
        0.04,
        0.04,
        0.05,
        0.07,
        0.10,
        0.12,
        0.13,
        0.10,
    ]
    typical_daily_profile_second_half = [
        0.09,
        0.08,
        0.06,
        0.06,
        0.07,
        0.09,
        0.13,
        0.16,
        0.15,
        0.12,
        0.10,
        0.09,  # 12:00 - 23:00
    ]
    typical_daily_profile = (
        typical_daily_profile_first_half + typical_daily_profile_second_half
    )

    # Scale this daily profile so it adds up to 1 (this assumes 1 kWh total per day)
    profile_sum = sum(typical_daily_profile)
    scaled_daily_profile = [x / profile_sum for x in typical_daily_profile]

    # Generate hourly profile for the whole year (8760 hours in a non-leap year)
    hours_in_year = 8760
    if len(entries) != hours_in_year:
        raise ValueError(f"Expected {hours_in_year} entries, but got {len(entries)}")

    # Repeat the daily pattern across the whole year
    consumption_profile = []
    for i, entry in enumerate(entries):
        # Determine the hour of the day
        hour_of_day = entry.time.hour
        # Use the corresponding value from the daily profile
        scaled_value = scaled_daily_profile[hour_of_day]
        consumption_profile.append(scaled_value)

    # Calculate total hourly consumption factor to scale it up to match the yearly consumption
    total_profile_sum = sum(consumption_profile)
    scaling_factor = total_consumption_kwh / total_profile_sum

    # Apply the scaling factor to get the scaled consumption profile
    scaled_consumption_profile = [
        value * scaling_factor for value in consumption_profile
    ]

    return scaled_consumption_profile


def generate_heatpump_consumption_profile(
    entries: List[TimeSeriesEntry],
    total_electricity_consumption_kwh: float,
    inside_temp: float = 15.0,
    heating_times: list[tuple[int, int]] = [(8, 18)],
) -> List[float]:
    # Prepare a dictionary to accumulate daily consumption needs based on temperature difference
    daily_temp_diff = defaultdict(float)
    hourly_consumption_profile = []

    # Group entries by day and calculate the mean temperature difference for each day
    for entry in entries:
        day_key = (entry.time.year, entry.time.month, entry.time.day)
        temp_diff = max(
            inside_temp - entry.T2m, 0
        )  # Ensure consumption is positive (no heating when outside is warmer)
        daily_temp_diff[day_key] += temp_diff

    # Calculate total daily temp differences and scale to the total yearly consumption
    total_temp_diff = sum(daily_temp_diff.values())
    scaling_factor = (
        total_electricity_consumption_kwh / total_temp_diff
        if total_temp_diff > 0
        else 0
    )

    # Apply the scaling factor to get the daily consumption in kWh
    daily_consumption_kwh = {
        day: temp_diff * scaling_factor for day, temp_diff in daily_temp_diff.items()
    }

    # Create an hourly consumption profile based on heating times
    for entry in entries:
        day_key = (entry.time.year, entry.time.month, entry.time.day)
        consumption_for_day = daily_consumption_kwh.get(day_key, 0)

        # Calculate the number of active heating hours for the day
        heating_hours = sum(end - start for start, end in heating_times)

        # If the current hour is within the heating period, allocate consumption equally across those hours
        hour_of_day = entry.time.hour
        is_heating_hour = any(
            start <= hour_of_day < end for start, end in heating_times
        )

        if is_heating_hour and heating_hours > 0:
            # Distribute the daily consumption across the heating hours
            hourly_consumption_profile.append(consumption_for_day / heating_hours)
        else:
            hourly_consumption_profile.append(0.0)

    return hourly_consumption_profile
