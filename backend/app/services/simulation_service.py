import asyncio
from simulation.simulator import Simulator
from simulation.scenarios import setup_demo_scenario
from intelligence.signal_optimizer import SignalDecisionEngine

simulator = Simulator()
setup_demo_scenario(simulator)
decision_engine = SignalDecisionEngine()

simulation_task = None
broadcast_callback = None

async def run_simulation():
    while True:
        if simulator.running:
            simulator.step()
            
            # Run Intelligence Engine periodically (every 5 simulation seconds)
            if int(simulator.simulation_time) % 5 == 0:
                decisions = []
                for _, intersection in simulator.intersections.items():
                    intersection_dict = intersection.to_dict()
                    decision = decision_engine.decide_next_phase(intersection_dict)
                    intersection.update_phase(decision["selected_phase"], decision["duration"])
                    decisions.append(decision)
                
                # Append decisions to state
                state = simulator.get_state()
                state["decisions"] = decisions
            else:
                state = simulator.get_state()
                
            if broadcast_callback:
                await broadcast_callback(state)
                
        await asyncio.sleep(1.0) # 1 sec realtime = 1 sec sim time

def start_simulation(callback):
    global simulation_task, broadcast_callback
    broadcast_callback = callback
    if not simulation_task:
        simulation_task = asyncio.create_task(run_simulation())
        
def pause_simulation():
    simulator.running = False
    
def resume_simulation():
    simulator.running = True
    
def trigger_emergency():
    # Inject ambulance on East approach of J2
    simulator.generate_vehicle("E_J2", "HOSPITAL", is_emergency=True)
