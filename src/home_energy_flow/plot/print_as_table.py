from tabulate import tabulate

from home_energy_flow.plot.datamodels import MonthlyData


def pprint_data_per_month_as_table(monthly_datas: list[MonthlyData]):
    # Create a list of months (1 to 12)
    months = range(1, 13)

    # Create the table with each row corresponding to a month
    table = []
    for month in months:
        row = [month]
        for data in monthly_datas:
            row.append(f"{data.data[month-1]:06.1f}")
        table.append(row)

    # Define headers
    headers = ["Month"] + [data.name for data in monthly_datas]

    # Print the table using tabulate
    print(tabulate(table, headers, tablefmt="pretty"))
