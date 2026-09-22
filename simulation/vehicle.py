import uuid
import time

class VehicleType:
    CAR = "CAR"
    BIKE = "BIKE"
    BUS = "BUS"
    TRUCK = "TRUCK"
    AMBULANCE = "AMBULANCE"

class Vehicle:
    def __init__(self, vehicle_type: str, current_road_id: str, destination_id: str, is_emergency: bool = False):
        self.id = str(uuid.uuid4())
        self.vehicle_type = vehicle_type
        self.current_road_id = current_road_id
        self.destination_id = destination_id
        self.is_emergency = is_emergency
        
        self.speed = 40.0 if not is_emergency else 60.0
        self.waiting_time = 0.0
        self.creation_time = time.time()
        
    def wait(self, dt: float):
        self.waiting_time += dt

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.vehicle_type,
            "road": self.current_road_id,
            "destination": self.destination_id,
            "emergency": self.is_emergency,
            "waiting_time": self.waiting_time,
        }
