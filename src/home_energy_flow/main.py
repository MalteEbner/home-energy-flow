from home_energy_flow.plot.aggregate_monthly_data import aggregate_monthly_data
import home_energy_flow.storage.compute_storage
from home_energy_flow.production.pv_system import PVSystem
from home_energy_flow.consumption import consumption_profiles
from home_energy_flow.production import compute_production, meteo_load
from home_energy_flow.plot import plot_graph, print_as_table
from home_energy_flow.consumption.consumption_profiles import HeatPumpSystem


def main(
    year: int,
    pv_system: PVSystem,
    regular_consumption_kWh: float,
    heatpump_system: HeatPumpSystem,
    storage_kWh: float,
) -> None:
    meteo_data_per_orientation = meteo_load.get_meteo_data_per_orientation()
    for meteo_data in meteo_data_per_orientation:
        meteo_data.outputs.hourly = [
            entry for entry in meteo_data.outputs.hourly if entry.time.year == year
        ]

    # Calculate the total energy production of the pv system
    times, total_production = compute_production.compute_production(
        pv_system, meteo_data_per_orientation
    )

    # Model the energy consumption of a household
    regular_consumption = consumption_profiles.generate_typical_consumption_profile(
        meteo_data_per_orientation[0].outputs.hourly,
        yearly_consumption_kWh=regular_consumption_kWh,
    )
    heatpump_consumption = consumption_profiles.generate_heatpump_consumption_profile(
        meteo_data_per_orientation[0].outputs.hourly,
        heatpump_system=heatpump_system,
    )
    total_consumption = [
        reg + heat for reg, heat in zip(regular_consumption, heatpump_consumption)
    ]

    # Calculate for each time the energy buy, energy sell and energy self usage
    energy_flow_data = (
        home_energy_flow.storage.compute_storage.compute_production_consumption(
            total_production, total_consumption, storage_kWh=storage_kWh
        )
    )

    # Visualize the data
    monthly_datas = aggregate_monthly_data(
        times,
        energy_flow_data.production,
        regular_consumption,
        heatpump_consumption,
        energy_flow_data.consumption,
        energy_flow_data.energy_buy,
        energy_flow_data.energy_sell,
        energy_flow_data.self_usage,
    )
    print_as_table.pprint_data_per_month_as_table(monthly_datas)
    plot_graph.plot_data_per_month_as_lines(monthly_datas)
