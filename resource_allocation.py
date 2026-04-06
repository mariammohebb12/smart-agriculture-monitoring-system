import heapq


class ResourceAllocator:
    def __init__(self):
        self.crop_requirements = {}
        self.resource_graph = {}

    def add_field_requirements(self, field, water, fertilizer, pesticide, priority):
        self.crop_requirements[field] = {
            "water": water,
            "fertilizer": fertilizer,
            "pesticide": pesticide,
            "priority": priority
        }

    def add_connections(self, field, connected_fields):
        self.resource_graph[field] = connected_fields

    def allocate_resources(self, water_inventory, fertilizer_inventory, pesticide_inventory):

        priority_queue = []
        for field, data in self.crop_requirements.items():
            heapq.heappush(priority_queue, (data["priority"], field))

 
        demand_heap = []
        for field, data in self.crop_requirements.items():
            total_demand = data["water"] + data["fertilizer"] + data["pesticide"]
            heapq.heappush(demand_heap, (-total_demand, field))

        allocations = {}
        used_water = used_fertilizer = used_pesticide = 0

        while priority_queue:
            _, field = heapq.heappop(priority_queue)
            req = self.crop_requirements[field]

            water = min(req["water"], water_inventory)
            fertilizer = min(req["fertilizer"], fertilizer_inventory)
            pesticide = min(req["pesticide"], pesticide_inventory)

            allocations[field] = {
                "Water Allocated": water,
                "Fertilizer Allocated": fertilizer,
                "Pesticide Allocated": pesticide
            }

            water_inventory -= water
            fertilizer_inventory -= fertilizer
            pesticide_inventory -= pesticide

            used_water += water
            used_fertilizer += fertilizer
            used_pesticide += pesticide

        alerts = []

        if water_inventory <= 0:
            alerts.append("Water shortage")

        if fertilizer_inventory <= 0:
            alerts.append("Fertilizer shortage")

        if pesticide_inventory <= 0:
            alerts.append("Pesticide shortage")

        if used_water > 500:
            alerts.append("Water overuse detected")

        if used_fertilizer > 250:
            alerts.append("Fertilizer overuse detected")

        if used_pesticide > 120:
            alerts.append("Pesticide overuse detected")

        return {
            "Allocations": allocations,
            "Usage": {
                "Water Used": used_water,
                "Fertilizer Used": used_fertilizer,
                "Pesticide Used": used_pesticide
            },
            "Remaining": {
                "Water Remaining": water_inventory,
                "Fertilizer Remaining": fertilizer_inventory,
                "Pesticide Remaining": pesticide_inventory
            },
            "Alerts": alerts
        }


