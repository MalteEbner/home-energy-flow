def compute_production_consumption(
    total_production_kWh: list[float],
    total_consumption_kWh: list[float],
    storage_kWh: float = 2.0,
    storage_efficiency: float = 0.9,
) -> tuple[list[float], list[float], list[float]]:
    """
    Compute energy buy, sell, and self-usage considering storage.

    Args:
        total_production_kWh (list[float]): List of production values in kWh.
        total_consumption_kWh (list[float]): List of consumption values in kWh.
        storage_kWh (float): Total storage capacity in kWh.
        storage_efficiency (float): Efficiency of storage (0 < efficiency <= 1).

    Returns:
        tuple[list[float], list[float], list[float]]: energy_buy, energy_sell, self_usage lists.
    """
    # Initialize the lists to store results
    energy_buy = []
    energy_sell = []
    self_usage = []

    # Ensure the lengths of both lists are the same
    assert len(total_production_kWh) == len(
        total_consumption_kWh
    ), "Production and consumption lists must be of the same length."

    # Initialize current storage state
    current_storage = 0.0  # Start with empty storage

    for prod, con in zip(total_production_kWh, total_consumption_kWh):
        if prod >= con:
            # Surplus energy available
            excess = prod - con

            # Calculate potential energy to charge storage
            charge_possible = min(
                excess * storage_efficiency, storage_kWh - current_storage
            )
            charge_energy = (
                charge_possible / storage_efficiency
            )  # Actual energy taken from surplus
            current_storage += charge_possible  # Update storage with charged energy

            # Remaining excess after charging storage
            remaining_excess = excess - charge_energy

            # Energy to sell is the remaining excess
            _energy_sell = remaining_excess
            _energy_buy = 0.0  # No need to buy energy
        else:
            # Deficit energy needed
            deficit = con - prod

            # Calculate potential energy to discharge from storage
            discharge_possible = min(deficit / storage_efficiency, current_storage)
            discharge_energy = (
                discharge_possible * storage_efficiency
            )  # Actual energy provided to cover deficit
            current_storage -= discharge_possible  # Update storage after discharging

            # Remaining deficit after discharging storage
            remaining_deficit = deficit - discharge_energy

            # Energy to buy is the remaining deficit
            _energy_buy = remaining_deficit
            _energy_sell = 0.0  # No excess to sell

        # Self-consumed energy is the minimum of production and consumption
        _self_usage = min(prod, con) + discharge_energy

        # Append the results to respective lists
        energy_buy.append(_energy_buy)
        energy_sell.append(_energy_sell)
        self_usage.append(_self_usage)

    # Return the results as a tuple of lists
    return energy_buy, energy_sell, self_usage
