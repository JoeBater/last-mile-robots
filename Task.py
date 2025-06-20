class Task:
    def __init__(self, order_id, robot_id, start_hour, start_minute):
        """
        Initializes a new task.
        """
        self.order_id = order_id
        self.robot_id = robot_id
        self.start_hour = start_hour
        self.start_minute = start_minute

    def __repr__(self):
        return f"Task(order_id={self.order_id}, robot_id={self.robot_id}, start_time={self.start_hour}:{self.start_minute})"
    
    def get_robot_id(self):
        return self.robot_id

    def get_start_time(self):
        return self.start_time
    
    def get_order_id(self):
        return self.order_id
    
    def get_start_time(self):
        return self.start_hour, self.start_minute
    