import matplotlib.pyplot as plt

from home_energy_flow.plot.datamodels import MonthlyData


def plot_data_per_month_as_lines(monthly_datas: list[MonthlyData]):
    months = range(1, 13)

    # Create the plot
    plt.figure(figsize=(10, 6))

    # Plot each data series
    for montly_data in monthly_datas:
        label = montly_data.name
        data = montly_data.data
        plt.plot(months, data, label=f"{label}: {sum(data):.0f} kWh", marker="o")

    # Add labels and title
    plt.xlabel("Month")
    plt.ylabel("Energy (kWh)")
    plt.title(f"Monthly Energy Production and Consumption {monthly_datas[0].year}")

    # Add grid and legend
    plt.grid(True)
    # location is outside
    plt.legend(loc="upper center")

    # Show the plot
    month_names = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    plt.xticks(months, month_names)
    plt.show()
