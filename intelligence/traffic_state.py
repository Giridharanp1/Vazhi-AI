class TrafficStateEngine:
    def __init__(self, config: dict = None):
        self.config = config or {
            "weights": {
                "demand": 0.30,
                "queue": 0.20,
                "waiting": 0.15,
                "emergency": 0.25,
                "downstream_congestion": 0.10
            }
        }

    def calculate_approach_score(self, stats: dict, downstream_occupancy: float) -> dict:
        """
        Calculates priority score for a single approach.
        stats format: {"vehicles": int, "queue": int, "wait": float, "emergency": bool, "capacity": int}
        """
        
        # Normalize (assuming some max bounds for MVP: max 50 vehicles, max 50 queue, max 120s wait)
        demand_score = min(stats["vehicles"] / 50.0, 1.0)
        queue_score = min(stats["queue"] / 50.0, 1.0)
        waiting_score = min(stats["wait"] / 120.0, 1.0)
        emergency_score = 1.0 if stats["emergency"] else 0.0
        
        w = self.config["weights"]
        
        score = (
            w["demand"] * demand_score +
            w["queue"] * queue_score +
            w["waiting"] * waiting_score +
            w["emergency"] * emergency_score -
            w["downstream_congestion"] * downstream_occupancy
        )
        
        return {
            "score": max(0.0, score), # Keep non-negative
            "components": {
                "demand": demand_score,
                "queue": queue_score,
                "waiting": waiting_score,
                "emergency": emergency_score,
                "downstream": downstream_occupancy
            }
        }
