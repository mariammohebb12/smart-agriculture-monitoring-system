
class SensorReading:
    def __init__(self, moisture, temperature, humidity, nutrients):
        self.moisture = moisture
        self.temperature = temperature
        self.humidity = humidity
        self.nutrients = nutrients


class Node:
    def __init__(self, reading):
        self.reading = reading
        self.next = None


class SensorLinkedList:
    def __init__(self):
        self.head = None

    def add_reading(self, reading):
        new_node = Node(reading)
        new_node.next = self.head
        self.head = new_node

    def get_latest_reading(self):
        return self.head.reading if self.head else None


class SensorSystem:
    def __init__(self):
        self.fields_data = {}


        self.crop_types = {}


        self.moisture_threshold = 20
        self.temperature_threshold = 35
        self.humidity_threshold = 30
        self.nutrient_threshold = 40


    def add_sensor_data(self, field_name, crop_type,
                        moisture, temperature, humidity, nutrients):

        reading = SensorReading(
            moisture,
            temperature,
            humidity,
            nutrients
        )


        if field_name not in self.crop_types:
            self.crop_types[field_name] = crop_type

        if field_name not in self.fields_data:
            self.fields_data[field_name] = SensorLinkedList()

        self.fields_data[field_name].add_reading(reading)


    def get_field(self, field_name):
        return self.fields_data.get(field_name, None)


    def get_field_status(self, field_name):
        field_data = self.get_field(field_name)

        if not field_data:
            return None

        reading = field_data.get_latest_reading()
        alerts = []

        if reading.moisture < self.moisture_threshold:
            alerts.append("Low moisture")

        if reading.temperature > self.temperature_threshold:
            alerts.append("High temperature")

        if reading.humidity < self.humidity_threshold:
            alerts.append("Low humidity")

        if reading.nutrients < self.nutrient_threshold:
            alerts.append("Low nutrients")

        return {
            "Field": field_name,
            "Crop Type": self.crop_types.get(field_name, "Unknown"),
            "Soil Moisture": reading.moisture,
            "Temperature": reading.temperature,
            "Humidity": reading.humidity,
            "Nutrients": reading.nutrients,
            "Alerts": alerts
        }


    def get_all_fields(self):
        result = []
        for field_name in self.fields_data:
            status = self.get_field_status(field_name)
            if status:
                result.append(status)
        return result

    