class Battery:
    def __init__(self, capacity_kwh=1.5, initial_soc=1.0, voltage=24):
        self.capacity = capacity_kwh * 1000  # Convert kWh to Wh
        self.soc = initial_soc  # 0 to 1 scale
        self.voltage = voltage  # volts, affects Peukert calc

    def charge(self, charger_power_watts, time_min):
        """
        Simulate charging for a given number of minutes.
        Applies tapering above 90% SoC.
        """
        if self.soc >= 1.0:
            print("Battery is already fully charged.")
            return

        energy_added = charger_power_watts * time_min / 60  # Wh
        charge_ratio = energy_added / self.capacity

        old_soc = self.soc

        if self.soc < 0.9:
            self.soc += charge_ratio
        else:
            taper_factor = (1 - self.soc) * 5  # Slow tapering near full
            self.soc += charge_ratio * taper_factor

        # Clamp to 1.0
        self.soc = min(1.0, self.soc)

        if energy_added < 1:
            print(f"Charging: <1Wh (SOC unchanged at {old_soc:.3f})")
        else:
            print(f"Charging: {energy_added:.2f}Wh (SOC before: {old_soc:.3f}, SOC after: {self.soc:.3f})")

    def discharge(self, power_draw_w, time_min, temperature_c):
        """
        Simulate discharging over time with Peukert's law and temperature effects.
        """
        base_energy = power_draw_w * time_min / 60  # Wh
        peukert_k = 1.05  # For small Li-ion systems

        # Approximate current in Amps
        current = power_draw_w / self.voltage
        effective_energy = base_energy * (current ** (peukert_k - 1))

        # Optional: exponential derating based on temp
        if temperature_c < 5:
            effective_energy *= 1 + (5 - temperature_c) * 0.02  # ~2% per °C
        elif temperature_c > 35:
            effective_energy *= 1 + (temperature_c - 35) * 0.01  # ~1% per °C

        old_soc = self.soc
        self.soc = max(0.0, self.soc - effective_energy / self.capacity)

        print(f"Discharging: {effective_energy:.2f}Wh (SOC before: {old_soc:.3f}, SOC after: {self.soc:.3f})")

    def get_current_kwh(self):
        return self.soc * self.capacity / 1000

    def get_current_soc(self):
        return self.soc
    
    def get_current_soc_percent(self):
        return self.soc * 100

    def estimate_runtime_min(self, power_draw_w):
        """
        Estimate how long (in minutes) the battery can continue at current draw.
        """
        if power_draw_w == 0:
            return float('inf')
        return (self.get_current_kwh() * 1000) / power_draw_w * 60
