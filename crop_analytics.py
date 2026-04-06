import heapq



class CropAnalytics:
    def __init__(self):
        
        self.historical_yield_data = {}

        
        self.field_graph = {}


    def add_yield_data(self, field, yield_value):
        if field not in self.historical_yield_data:
            self.historical_yield_data[field] = []
        self.historical_yield_data[field].append(yield_value)


    def add_field_connections(self, field, connected_fields):
        self.field_graph[field] = connected_fields


    def analyze_yield_trends(self):
        average_yield = {}

        for field, yields in self.historical_yield_data.items():
            if yields:
                average_yield[field] = sum(yields) / len(yields)


        return sorted(
            average_yield.items(),
            key=lambda x: x[1],
            reverse=True
        )


    def calculate_health_scores(self, sensor_data):
        """
        Calculates health score (0–100) for each field
        based on sensor values.
        """

        health_scores = {}

        for field in sensor_data:
            score = 100

            moisture = field["Soil Moisture"]
            temperature = field["Temperature"]
            humidity = field["Humidity"]
            nutrients = field["Nutrients"]

  
            if moisture < 20:
                score -= 30
            elif moisture < 40:
                score -= 15

            if temperature < 10 or temperature > 35:
                score -= 25
            elif temperature < 18 or temperature > 30:
                score -= 10

 
            if humidity < 30:
                score -= 20
            elif humidity < 40:
                score -= 10

  
            if nutrients < 30:
                score -= 25
            elif nutrients < 50:
                score -= 10

            health_scores[field["Field"]] = max(0, score)

        return health_scores


    def rank_fields_by_risk(self, health_scores):
        """
        Uses a min-heap to rank fields by risk
        (lower health = higher risk)
        """

        risk_heap = []

        for field, health in health_scores.items():
            heapq.heappush(risk_heap, (health, field))

        ranked = []
        while risk_heap:
            health, field = heapq.heappop(risk_heap)
            ranked.append({
                "Field": field,
                "Health Score": health
            })

        return ranked


    def get_related_fields(self, field):
        return self.field_graph.get(field, [])
