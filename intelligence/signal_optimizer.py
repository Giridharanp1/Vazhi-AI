from .traffic_state import TrafficStateEngine

class SignalDecisionEngine:
    def __init__(self):
        self.state_engine = TrafficStateEngine()
        
    def decide_next_phase(self, intersection_dict: dict) -> dict:
        """
        Takes in intersection dictionary from intersection.to_dict()
        Returns the decision containing selected_phase, duration, reason.
        """
        stats = intersection_dict["stats"]
        downstream = intersection_dict["downstream"]
        
        # Valid Phases mapped to Approaches + Departures
        # Simple Model: NS_GREEN vs EW_GREEN
        # We will calculate a score for North, South, East, West.
        
        scores = {}
        reasons = {}
        for direction, direction_stats in stats.items():
            ds_occupancy = downstream.get(direction, 0.0)
            score_data = self.state_engine.calculate_approach_score(direction_stats, ds_occupancy)
            scores[direction] = score_data["score"]
            
            # Generate explainable reason
            reason_parts = []
            if direction_stats["emergency"]:
                reason_parts.append(f"Emergency vehicle detected on {direction}.")
            if direction_stats["wait"] > 60:
                reason_parts.append(f"High accumulated wait time ({int(direction_stats['wait'])}s).")
            if ds_occupancy > 0.8:
                reason_parts.append(f"Downstream occupancy is high ({int(ds_occupancy*100)}%). Holding traffic.")
            elif direction_stats["vehicles"] > 10:
                reason_parts.append(f"High vehicle demand ({direction_stats['vehicles']} vehicles).")
                
            if not reason_parts:
                reason_parts.append(f"Standard rotation. Score: {score_data['score']:.2f}")
                
            reasons[direction] = " ".join(reason_parts)
            
        # Select best phase
        # For simplicity in MVP, we just take the approach with highest score.
        best_direction = max(scores, key=scores.get)
        best_score = scores[best_direction]
        
        if best_score == 0.0:
            return {
                "intersection": intersection_dict["id"],
                "selected_phase": "ALL_RED",
                "duration": 5,
                "reason": ["No demand."]
            }
            
        phase = f"{best_direction}_PRIORITY"
        duration = 15 # default adaptive green
        if "Emergency" in reasons[best_direction]:
            duration = 30
            phase = "EMERGENCY_CORRIDOR"
            
        return {
            "intersection": intersection_dict["id"],
            "selected_phase": phase,
            "duration": duration,
            "reason": [reasons[best_direction]],
            "score": best_score
        }
