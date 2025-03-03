


from dataclasses import dataclass


@dataclass
class Prices:
    energy_buy_eur_per_kWh: float = 0.3
    energy_sell_eur_per_kWh: float = 0.08