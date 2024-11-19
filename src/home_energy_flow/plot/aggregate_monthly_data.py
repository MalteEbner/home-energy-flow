from home_energy_flow.plot.datamodels import MonthlyData
from home_energy_flow.production.meteo_datamodels import Time


def aggregate_monthly_data(
    times: list[Time],
    solar_production: list[float],
    regular_consumption: list[float],
    heatpump_consumption: list[float],
    total_consumption: list[float],
    energy_buy: list[float],
    energy_sell: list[float],
    self_usage: list[float],
) -> list[MonthlyData]:
    monthly_datas = []
    for name, values in [
        ("Solar Production", solar_production),
        ("Regular Consumption", regular_consumption),
        ("Heatpump Consumption", heatpump_consumption),
        ("Total Consumption", total_consumption),
        ("Energy Buy", energy_buy),
        ("Energy Sell", energy_sell),
        ("Self Usage", self_usage),
    ]:
        data_per_month = [0.0] * 12
        for time, d in zip(times, values):
            month = time.month
            data_per_month[month - 1] += d

        monthly_data = MonthlyData(name=name, data=data_per_month, year=times[0].year)
        monthly_datas.append(monthly_data)
    return monthly_datas
