

class EnhancedFeatures:
    def __init__(self):
        self.farms = {}  # farm -> list of fields

    def add_farm(self, farm_name, fields):
        self.farms[farm_name] = fields

    def predict_pest_risk(self, health, weather_risk):
        if health < 40 and weather_risk == "high":
            return " High pest risk – immediate pesticide required"
        elif health < 65:
            return " Medium pest risk – monitor field closely"
        else:
            return " Low pest risk – field conditions are safe"

    def optimize_resources(self, usage, health):
        if health < 40:
            return "Immediate action required: increase water and fertilizer"
        elif health < 65:
            return "Monitor closely: adjust resources if needed"
        else:
            return "Conditions are healthy – maintain routine care"

    def get_health_heatmap_data(self, crop_health):
        heatmap = []
        for field, health in crop_health.items():
            heatmap.append({
                "Field": field,
                "Health": health
            })
        return heatmap


    def generate_recommendations(self, crop_health, weather_risk, resource_usage):
        recommendations = []

        for field in crop_health:
            pest = self.predict_pest_risk(
                crop_health[field],
                weather_risk.get(field, "medium")
            )

            resource = self.optimize_resources(
                resource_usage.get(field, 0),
                crop_health[field]
            )

            recommendations.append({
                "Field": field,
                "Pest Recommendation": pest,
                "Resource Recommendation": resource
            })

        return recommendations


