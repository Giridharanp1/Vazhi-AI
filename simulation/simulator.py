import random
from typing import Dict, List
from .vehicle import Vehicle, VehicleType
from .road import Road
from .intersection import Intersection

class Simulator:
    def __init__(self):
        self.intersections: Dict[str, Intersection] = {}
        self.roads: Dict[str, Road] = {}
        self.vehicles: Dict[str, Vehicle] = {}
        self.running = False
        
        self.simulation_time = 0.0
        self.dt = 1.0 # 1 second per step
        
        self.metrics = {
            "avg_wait": 0.0,
            "max_queue": 0,
            "throughput": 0,
            "spillback_events": 0,
            "signal_switches": 0
        }
        
    def add_intersection(self, intersection: Intersection):
        self.intersections[intersection.id] = intersection

    def add_road(self, road: Road):
        self.roads[road.id] = road

    def generate_vehicle(self, road_id: str, destination_id: str, is_emergency=False):
        road = self.roads.get(road_id)
        if road and len(road.vehicles) < road.capacity:
            v_type = VehicleType.AMBULANCE if is_emergency else random.choice([VehicleType.CAR, VehicleType.BIKE])
            vehicle = Vehicle(v_type, road_id, destination_id, is_emergency)
            road.add_vehicle(vehicle)
            self.vehicles[vehicle.id] = vehicle
            return vehicle
        return None

    def step(self):
        """Advances the simulation by one time step (dt)"""
        if not self.running:
            return
            
        self.simulation_time += self.dt
        
        # 1. Update vehicles (waiting time, basic movement logic)
        for road in self.roads.values():
            for vehicle in road.vehicles:
                # If vehicle is waiting at signal (simplified)
                # In a real simulation, we'd check distance to intersection and signal state.
                # For this MVP, we assume vehicles at the end of the road are waiting if signal is red.
                vehicle.wait(self.dt)
                
        # 2. Update metrics
        total_wait = 0
        total_vehicles = 0
        max_q = 0
        
        for road in self.roads.values():
            q = road.get_queue_length()
            if q > max_q: max_q = q
            for v in road.vehicles:
                total_wait += v.waiting_time
                total_vehicles += 1
                
        if total_vehicles > 0:
            self.metrics["avg_wait"] = total_wait / total_vehicles
        self.metrics["max_queue"] = max_q
        
    def get_state(self):
        return {
            "time": self.simulation_time,
            "running": self.running,
            "intersections": [i.to_dict() for i in self.intersections.values()],
            "roads": [r.to_dict() for r in self.roads.values()],
            "metrics": self.metrics
        }
