import time
from typing import Dict, List, Optional
from .road import Road
from .vehicle import Vehicle

class Phase:
    NS_GREEN = "NS_GREEN"
    EW_GREEN = "EW_GREEN"
    NORTH_PRIORITY = "NORTH_PRIORITY"
    SOUTH_PRIORITY = "SOUTH_PRIORITY"
    EAST_PRIORITY = "EAST_PRIORITY"
    WEST_PRIORITY = "WEST_PRIORITY"
    EMERGENCY_CORRIDOR = "EMERGENCY_CORRIDOR"
    ALL_RED = "ALL_RED"

class Intersection:
    def __init__(self, intersection_id: str, name: str):
        self.id = intersection_id
        self.name = name
        
        # Approaches (incoming roads) mapped by direction (e.g., 'NORTH', 'SOUTH', 'EAST', 'WEST')
        self.approaches: Dict[str, Road] = {}
        
        # Outgoing roads mapped by direction
        self.departures: Dict[str, Road] = {}
        
        # State
        self.current_phase = Phase.ALL_RED
        self.phase_start_time = time.time()
        self.phase_duration = 0
        
        # Emergency state
        self.has_emergency = False
        self.prepared_for_emergency = False

    def add_approach(self, direction: str, road: Road):
        self.approaches[direction] = road

    def add_departure(self, direction: str, road: Road):
        self.departures[direction] = road

    def update_phase(self, new_phase: str, duration: int):
        self.current_phase = new_phase
        self.phase_start_time = time.time()
        self.phase_duration = duration

    def time_in_phase(self):
        return time.time() - self.phase_start_time

    def get_approach_stats(self, direction: str) -> dict:
        road = self.approaches.get(direction)
        if not road:
            return {"vehicles": 0, "queue": 0, "wait": 0.0, "emergency": False}
        
        avg_wait = sum(v.waiting_time for v in road.vehicles) / len(road.vehicles) if road.vehicles else 0.0
        has_emergency = any(v.is_emergency for v in road.vehicles)
        
        return {
            "vehicles": len(road.vehicles),
            "queue": road.get_queue_length(),
            "wait": avg_wait,
            "emergency": has_emergency,
            "capacity": road.capacity
        }

    def get_downstream_occupancy(self, direction: str) -> float:
        """Get downstream occupancy for a given departure direction"""
        road = self.departures.get(direction)
        if road:
            return road.get_occupancy()
        return 0.0

    def to_dict(self):
        stats = {d: self.get_approach_stats(d) for d in self.approaches.keys()}
        downstream = {d: self.get_downstream_occupancy(d) for d in self.departures.keys()}
        return {
            "id": self.id,
            "name": self.name,
            "current_phase": self.current_phase,
            "time_in_phase": self.time_in_phase(),
            "duration": self.phase_duration,
            "stats": stats,
            "downstream": downstream,
            "emergency": self.has_emergency
        }
