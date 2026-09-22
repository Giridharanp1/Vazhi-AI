from .simulator import Simulator
from .intersection import Intersection
from .road import Road

def create_default_network(sim: Simulator):
    """
    Creates a 4-intersection topology + 1 Hospital.
    J1, J2, J3, J4
    Hospital is downstream of J3.
    """
    
    j1 = Intersection("J1", "Junction 1")
    j2 = Intersection("J2", "Junction 2")
    j3 = Intersection("J3", "Junction 3 (Hospital Route)")
    j4 = Intersection("J4", "Junction 4")
    
    sim.add_intersection(j1)
    sim.add_intersection(j2)
    sim.add_intersection(j3)
    sim.add_intersection(j4)
    
    # Create roads
    # Format: road_id, source, target, capacity, length
    roads = [
        # Incoming to J1
        Road("N_J1", "EXTERNAL", "J1", 50, 200.0),
        Road("S_J1", "EXTERNAL", "J1", 50, 200.0),
        Road("W_J1", "EXTERNAL", "J1", 50, 200.0),
        
        # J1 <-> J2
        Road("J1_J2", "J1", "J2", 30, 100.0),
        Road("J2_J1", "J2", "J1", 30, 100.0),
        
        # J1 <-> J4
        Road("J1_J4", "J1", "J4", 30, 100.0),
        Road("J4_J1", "J4", "J1", 30, 100.0),
        
        # J1 <-> J3
        Road("J1_J3", "J1", "J3", 40, 150.0),
        Road("J3_J1", "J3", "J1", 40, 150.0),
        
        # J2 External
        Road("N_J2", "EXTERNAL", "J2", 50, 200.0),
        Road("E_J2", "EXTERNAL", "J2", 50, 200.0),
        
        # J3 External
        Road("N_J3", "EXTERNAL", "J3", 50, 200.0),
        Road("E_J3", "EXTERNAL", "J3", 50, 200.0),
        
        # J3 -> Hospital
        Road("J3_HOSPITAL", "J3", "HOSPITAL", 100, 300.0),
        
        # J4 External
        Road("S_J4", "EXTERNAL", "J4", 50, 200.0),
        Road("E_J4", "EXTERNAL", "J4", 50, 200.0),
        Road("W_J4", "EXTERNAL", "J4", 50, 200.0),
    ]
    
    for r in roads:
        sim.add_road(r)
        
    # Wire approaches and departures
    j1.add_approach("NORTH", sim.roads["N_J1"])
    j1.add_approach("SOUTH", sim.roads["S_J1"])
    j1.add_approach("WEST", sim.roads["W_J1"])
    j1.add_approach("EAST", sim.roads["J3_J1"])
    j1.add_departure("NORTH", sim.roads["J1_J2"])
    j1.add_departure("SOUTH", sim.roads["J1_J4"])
    j1.add_departure("EAST", sim.roads["J1_J3"])
    
    j2.add_approach("NORTH", sim.roads["N_J2"])
    j2.add_approach("EAST", sim.roads["E_J2"])
    j2.add_approach("SOUTH", sim.roads["J1_J2"])
    j2.add_departure("SOUTH", sim.roads["J2_J1"])
    
    j3.add_approach("NORTH", sim.roads["N_J3"])
    j3.add_approach("EAST", sim.roads["E_J3"])
    j3.add_approach("WEST", sim.roads["J1_J3"])
    j3.add_departure("WEST", sim.roads["J3_J1"])
    j3.add_departure("EAST", sim.roads["J3_HOSPITAL"])
    
    j4.add_approach("SOUTH", sim.roads["S_J4"])
    j4.add_approach("EAST", sim.roads["E_J4"])
    j4.add_approach("WEST", sim.roads["W_J4"])
    j4.add_approach("NORTH", sim.roads["J1_J4"])
    j4.add_departure("NORTH", sim.roads["J4_J1"])

def setup_demo_scenario(sim: Simulator):
    """Initializes the demo scenario from the requirements"""
    create_default_network(sim)
    
    # Normal traffic baseline
    for _ in range(10):
        sim.generate_vehicle("N_J1", "J1")
        sim.generate_vehicle("S_J4", "J4")
        sim.generate_vehicle("E_J2", "J2")
        
    sim.running = True
