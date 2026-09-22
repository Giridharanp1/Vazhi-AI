from .vehicle import Vehicle

class Road:
    def __init__(self, road_id: str, source_id: str, target_id: str, capacity: int, length: float):
        self.id = road_id
        self.source_id = source_id
        self.target_id = target_id
        self.capacity = capacity
        self.length = length
        
        # Vehicles currently on this road segment
        self.vehicles: list[Vehicle] = []
        
    def add_vehicle(self, vehicle: Vehicle):
        if len(self.vehicles) < self.capacity:
            self.vehicles.append(vehicle)
            return True
        return False

    def remove_vehicle(self, vehicle_id: str):
        self.vehicles = [v for v in self.vehicles if v.id != vehicle_id]

    def get_occupancy(self) -> float:
        """Returns a percentage from 0.0 to 1.0"""
        if self.capacity == 0:
            return 0.0
        return len(self.vehicles) / self.capacity

    def get_queue_length(self) -> int:
        # Simple heuristic: vehicles that have been waiting > 5 seconds are in queue
        return sum(1 for v in self.vehicles if v.waiting_time > 5)

    def to_dict(self):
        return {
            "id": self.id,
            "source": self.source_id,
            "target": self.target_id,
            "capacity": self.capacity,
            "occupancy": self.get_occupancy(),
            "queue_length": self.get_queue_length(),
            "vehicle_count": len(self.vehicles)
        }
