from Battery import Battery

class DeliveryRobot:
    def __init__(self, name, start_location=[50,50]):
        self.name = name
        self.location = start_location  # (x, y) or (lat, lon)
        self.battery = Battery()  
        self.status = 'IDLE'  # idle, en_route, charging, waiting, etc.
        self.current_task = None
        self.pending_task = None
        self.task_history = []
        self.available_at = 0  # simulation time step when robot becomes available again

    # task assignment methods
    def assign_task(self, task, current_time):
        self.pending_task = task
        self.task_history.append((current_time, task))
    
    def get_task_history(self):
        return self.task_history
    
    def get_available_at(self):
        return self.available_at
    
    def set_available_at(self, time):
        self.available_at = time
    
    # where am I methods
    def get_location(self):
        return self.location
    
    def get_current_location(self):
        return self.location
    
    def update_location(self, new_location):
        self.location = new_location
    
    # battery charge/discharge methods
    def get_battery(self):
        return self.battery
    
    def discharge(self, power_draw_w, time_min, temperature_c):
        self.battery.discharge(power_draw_w, time_min, temperature_c)
        if self.battery.get_current_soc() <= 0:
            self.status = 'MISSION_FAILED - OUT OF BATTERY - PLEASE COME GET ME!'

    def charge(self, power_w, duration_min):
        self.battery.charge(power_w, duration_min)
        if self.battery.get_current_soc() >= 1.0:
            self.status = 'IDLE'

    def get_battery_capacity(self):
        return self.battery.capacity
    
    def get_battery_soc(self):
        return self.battery.soc
    
    # robot status methods
    def get_status(self):
        return self.status
    
    def waiting_to_charge(self):
        self.status = 'WAITING_TO_CHARGE'

    def start_charging(self):
        self.status = 'CHARGING'
    
    def stop_charging(self):
        self.status = 'IDLE'

    def on_task_outbound(self):
        self.status = 'ON_TASK_OUTBOUND'

    def on_task_returning(self):
        self.status = 'ON_TASK_RETURNING'

    def on_task_at_customer_location(self):
        self.status = 'ON_TASK_AT_CUSTOMER_LOCATION'

    # display methods
    def display_status(self):
        print(f"Robot {self.name} is currently at {self.location} with battery SoC: {self.battery.get_current_soc():.1f}% and status: {self.status}")

    def __repr__(self):
        return f"{self.name} - SoC: {self.get_battery_soc():.1f}, Status: {self.status}"