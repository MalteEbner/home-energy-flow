from solar_production.datamodel.pv_data import Module, PVSystem
from solar_production.datamodel.solar_data import (
    SolarRadiationData,
    Time,
    TimeSeriesEntry,
)


def solar_data_for_module(
    module: Module, available_data: list[SolarRadiationData]
) -> SolarRadiationData:
    # Find the solar radiation data that matches the module's slope and azimuth
    for data in available_data:
        if (
            data.inputs.mounting_system.fixed.slope.value == module.slope.value
            and data.inputs.mounting_system.fixed.azimuth.value == module.azimuth.value
        ):
            return data
    raise ValueError("No matching solar radiation data found")


def compute_production_single_module(module: Module, solar_data: list[TimeSeriesEntry]):
    """
    Compute the total energy production of a module using the given solar radiation data.
    """
    energy_kWh: list[float] = []
    for entry in solar_data:
        energy_Wh = module.kWP * entry.G_i * module.n
        energy_kWh.append(energy_Wh / 1000)
    return energy_kWh


def compute_production(system: PVSystem, all_solar_data: list[SolarRadiationData]):
    """
    Compute the total energy production of a PV system using the given solar radiation data.
    """
    # Assert that the times of all solar data sets are the same
    times: list[Time] = [data.time for data in all_solar_data[0].outputs.hourly]
    for data in all_solar_data[1:]:
        data = data.outputs.hourly
        assert len(data) == len(times), "Length of solar data sets do not match"
        assert data[0].time == times[0], "Times of solar data sets do not match"
        assert data[-1].time == times[-1], "Times of solar data sets do not match"

    production_per_module = []
    for i, module in enumerate(system.modules):
        # Find the solar radiation data that matches the module's slope and azimuth
        solar_data = solar_data_for_module(module, all_solar_data)

        production = compute_production_single_module(module, solar_data.outputs.hourly)
        production_per_module.append(production)

    # Sum the energy production of all modules for each time step
    total_production: list[float] = [
        sum(production[i] for production in production_per_module)
        for i in range(len(times))
    ]

    # Limit the total production to the maximum power of the PV system
    if system.maximum_power_kW is not None:
        total_production = [
            min(production, system.maximum_power_kW) for production in total_production
        ]

    return times, total_production
