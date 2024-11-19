# Home Energy Flow

This repository allows you to simulate the electric energy flow in a building with a PV system, a battery, and a specific electric consumption profile, including temperature-dependent heating by a heat pump.

The simulation is based on hourly meteorological data for a specific location. This includes the solar radiation for the PV system and the outside temperature for the heat pump.

## Example Usage

See also the `example.py` file.
```python
year = 2023

# Define the PV system as 4 bifacial modules with 500 Wp each.
# They are bifacial and thus equivalent to 8 monofacial modules.
# They are vertically mounted (slope=90) and oriented to the east and west.
# For legal reasons, the maximum power is limited to 0.8 kW.
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
```
## Example Output

![Energy Flow Graph](docs/example_graph.png)

## Next Steps

There are many next steps to improve this project:

### Easier usage
- Add documentation.
- Add docstrings to all functions.
- Instead of requiring manual download of the meteorological data, directly get it from the PVGIS API.
- Publish the package on PyPI.

### Development Workflow

To improve the development workflow, the following steps should be taken:
- Add unit tests.
- Add end-to-end tests.
- Add CI for ensuring that the formatting and type checking are always correct.
- Add CI for the unit tests and end-to-end tests.

### Missing Features

New features that could be added are:
- Cost calculations, not only with fixed-price electricity but also with dynamic prices.
- Dynamic consumers, e.g., electric cars that can be charged or discharged or a washing machine that can be delayed.
- Automatic optimization to decide when to charge and discharge the battery and when to use dynamic consumers.
- Recommendations to determine the best battery size, PV system size, etc.
- More detailed regular consumption model, e.g., use the "Standardlastprofile Strom H0" from BDEW.
- More detailed heat pump model, e.g., with a COP (coefficient of performance) that depends on the outside temperature.
- More detailed PV model, e.g., with a temperature-dependent efficiency.


## Installation

Create a virtual environment, then install the package as specified in the `pyproject.toml`.

We recommend using [uv](https://github.com/astral-sh/uv) as a virtual environment, project, and package manager.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv .venv
source .venv/bin/activate
make install-dev
```

## Development

The code is formatted using `ruff` and type-checked using `mypy`. To use them, call `make format && make static-checks`.