
## Meteo data source
This directory contains the hourly meteo data for a specific location and orientation.
There is one file for each location and orientation.
They were downloaded from the PVGIS website:

https://re.jrc.ec.europa.eu/pvg_tools/en/

Choose "hourly data", your location and the orientaion of PV panels.
Then download the data as `.json` and save it in this directory.
Last, add it under `src/home_energy_flow/production/meteo_load.py`

## TODO

Directly get the data from the PVGIS API.
