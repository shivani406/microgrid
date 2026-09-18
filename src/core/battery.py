class BatteryModel:
    def __init__(self, capacity_kwh=200.0, initial_soc=50.0, min_soc=20.0, max_soc=90.0, efficiency=0.95):
        self.capacity_kwh = capacity_kwh
        self.soc = initial_soc
        self.min_soc = min_soc
        self.max_soc = max_soc
        self.efficiency = efficiency

    def get_soc(self):
        return round(self.soc, 2)

    def charge(self, power_kw, duration_hours=1.0):
        energy_added_kwh = power_kw * duration_hours * self.efficiency
        soc_increase = (energy_added_kwh / self.capacity_kwh) * 100.0
        self.soc = min(self.max_soc, self.soc + soc_increase)
        return self.get_soc()

    def discharge(self, power_kw, duration_hours=1.0):
        energy_drawn_kwh = (power_kw * duration_hours) / self.efficiency
        soc_decrease = (energy_drawn_kwh / self.capacity_kwh) * 100.0
        self.soc = max(self.min_soc, self.soc - soc_decrease)
        return self.get_soc()