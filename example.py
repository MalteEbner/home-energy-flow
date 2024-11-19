from home_energy_flow.consumption.consumption_profiles import HeatPumpSystem
from home_energy_flow.main import main
from home_energy_flow.production.datamodels import Azimuth, Slope
from home_energy_flow.production.pv_system import Modules, PVSystem


if __name__ == "__main__":
    year = 2023

    # Define the PV system as 4 bifacial modules with 500 Wp each.
    # They are bifacial and thus equivalent to 8 monofacial modules.
    # They are vertically mounted (slope=90) and oriented to the east and west.
    # For legal reasons, the maximum power is limited to 800W.
    pv_system_balkonkraftwerk = PVSystem(
        modules=[
            Modules(slope=Slope(value=90), azimuth=Azimuth.EAST(), kWP=0.5, n=4),
            Modules(slope=Slope(value=90), azimuth=Azimuth.WEST(), kWP=0.5, n=4),
        ],
        maximum_power_kW=0.8,
    )
    # The storage capacity of the battery is 2 kWh.
    storage_kWh = 2.0

    # The household has a regular consumption of 1000 kWh per year.
    # Additionally, the heat pump consumes 5000 kWh per year, but only between 8:00 and
    # 18:00 and proportional to the temperature difference between inside and outside.
    regular_consumption_kWh = 1000.0
    heatpump_system = HeatPumpSystem(
        yearly_electricity_consumption_kWh=5000.0,
        heating_turnoff_temp=13.0,
        heating_times=[(8, 18)],
    )

    # Run the simulation and visualize the results
    main(
        year=year,
        pv_system=pv_system_balkonkraftwerk,
        storage_kWh=storage_kWh,
        regular_consumption_kWh=regular_consumption_kWh,
        heatpump_system=heatpump_system,
    )