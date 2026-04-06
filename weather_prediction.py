

class WeatherYieldPredictor:
    def __init__(self):
        self.weather_data = {
            "rainfall": [],
            "temperature": [],
            "wind": []
        }


        self.crop_sensitivity = {}


        self.weather_crop_graph = {}


    def add_weather_data(self, rainfall, temperature, wind):
        self.weather_data["rainfall"].append(rainfall)
        self.weather_data["temperature"].append(temperature)
        self.weather_data["wind"].append(wind)


    def add_crop_sensitivity(self, field, rainfall_level, temperature_level):
        self.crop_sensitivity[field] = {
            "rainfall": rainfall_level,
            "temperature": temperature_level
        }


    def add_weather_relationship(self, weather_factor, affected_fields):
        self.weather_crop_graph[weather_factor] = affected_fields


    def analyze_weather_trends(self):
        return {
            "rainfall": sorted(self.weather_data["rainfall"]),
            "temperature": sorted(self.weather_data["temperature"]),
            "wind": sorted(self.weather_data["wind"])
        }


    def predict_yield(self, health_scores):
        trends = self.analyze_weather_trends()
        predicted_yield = {}
        yield_status = {}

        max_temp = max(trends["temperature"]) if trends["temperature"] else 0
        min_rain = min(trends["rainfall"]) if trends["rainfall"] else 0

        for field, sensitivity in self.crop_sensitivity.items():
            base_yield = 5.0  


            if sensitivity["temperature"] == "high":
                if max_temp > 38:
                    base_yield -= 2.0
                elif max_temp > 35:
                    base_yield -= 1.2

            if sensitivity["rainfall"] == "high":
                if min_rain < 15:
                    base_yield -= 1.5
                elif min_rain < 25:
                    base_yield -= 0.8


            health = health_scores.get(field, 100)

            if health < 20:
                base_yield -= 2.5
            elif health < 40:
                base_yield -= 1.5
            elif health < 60:
                base_yield -= 0.8


            base_yield = max(1.0, round(base_yield, 2))
            predicted_yield[field] = base_yield


            if base_yield < 2:
                yield_status[field] = " Critical – yield at risk"
            elif base_yield < 3:
                yield_status[field] = " Moderate – improvement needed"
            else:
                yield_status[field] = " Good – stable production"

        return predicted_yield, yield_status


    def generate_adjustments(self, predicted_yield, health_scores):
        adjustments = {}

        for field, y in predicted_yield.items():
            health = health_scores.get(field, 100)

            if health < 20 or y < 2:
                adjustments[field] = " Emergency intervention required"
            elif health < 40 or y < 2.5:
                adjustments[field] = " Increase irrigation, nutrients, and monitoring"
            elif health < 60 or y < 3:
                adjustments[field] = "Monitor closely and adjust resources"
            else:
                adjustments[field] = " Stable – no intervention needed"

        return adjustments


    def get_weather_alerts(self):
        alerts = []

        if self.weather_data["temperature"] and max(self.weather_data["temperature"]) > 35:
            alerts.append(" Extreme temperature detected")

        if self.weather_data["rainfall"] and min(self.weather_data["rainfall"]) < 20:
            alerts.append("Low rainfall risk")

        if self.weather_data["wind"] and max(self.weather_data["wind"]) > 10:
            alerts.append(" High wind conditions detected")

        return alerts



