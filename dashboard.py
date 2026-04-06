import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sensor_data import SensorSystem
from resource_allocation import ResourceAllocator
from crop_analytics import CropAnalytics
from weather_prediction import WeatherYieldPredictor
from enhanced_features import EnhancedFeatures


st.set_page_config(
    page_title="Smart Agriculture Monitoring System",
    layout="wide"
)

st.title("Smart Agriculture Monitoring System")
st.caption(
    "Multi-Field Simulation, Resource Allocation & Crop Analytics "
    "(Data Structures & Algorithms Project)"
)


if "sensor" not in st.session_state:
    st.session_state.sensor = SensorSystem()

if "allocator" not in st.session_state:
    st.session_state.allocator = ResourceAllocator()

if "analytics" not in st.session_state:
    st.session_state.analytics = CropAnalytics()

if "weather" not in st.session_state:
    st.session_state.weather = WeatherYieldPredictor()

if "enhanced" not in st.session_state:
    st.session_state.enhanced = EnhancedFeatures()

sensor = st.session_state.sensor
allocator = st.session_state.allocator
analytics = st.session_state.analytics
weather = st.session_state.weather
enhanced = st.session_state.enhanced


st.header("1️⃣ Sensor Data Management")

col1, col2, col3 = st.columns(3)

with col1:
    soil_moisture = st.number_input("Soil Moisture (%)", 0.0, 100.0, 50.0)
    st.caption("Normal range: 40% – 70%")

    nutrients = st.number_input("Soil Nutrients (%)", 0.0, 100.0, 50.0)
    st.caption("Normal range: 50% – 80%")

with col2:
    temperature = st.number_input("Temperature (°C)", -5.0, 50.0, 25.0)
    st.caption("Optimal range: 15°C – 30°C")

    humidity = st.number_input("Humidity (%)", 0.0, 100.0, 60.0)
    st.caption("Normal range: 40% – 70%")

with col3:
    rainfall = st.number_input("Rainfall (mm)", 0.0, 100.0, 20.0)
    st.caption("Low < 20 mm | Medium 20–50 mm")

    pests = st.number_input("Pest Severity", 0.0, 100.0, 10.0)
    st.caption("Safe < 40 | High risk > 40")


field_name = st.text_input("Field Name")
crop_type = st.text_input("Crop Type (e.g. Wheat, Corn, Rice)")


if st.button("Add Field"):
    if field_name.strip() == "" or crop_type.strip() == "":
        st.warning("Please enter both Field Name and Crop Type.")
    else:
        sensor.add_sensor_data(
            field_name,
            crop_type,
            soil_moisture,
            temperature,
            humidity,
            nutrients
        )

        allocator.add_field_requirements(
            field_name,
            water=max(0, 50 - soil_moisture),
            fertilizer=max(0, 60 - nutrients),
            pesticide=max(0, pests - 40),
            priority=1
        )

        analytics.add_yield_data(field_name, 3.0)

        weather.add_crop_sensitivity(
            field_name,
            rainfall_level="high" if rainfall < 20 else "medium",
            temperature_level="high" if temperature < 10 or temperature > 35 else "medium"
        )

        weather.add_weather_data(rainfall, temperature, 8)

        st.success(f"Field '{field_name}' with crop '{crop_type}' added successfully!")


st.header("2️⃣ Real-Time Sensor Status")

sensor_data = sensor.get_all_fields()

if sensor_data:
    st.dataframe(pd.DataFrame(sensor_data), use_container_width=True)
else:
    st.info("No sensor data available yet.")


st.header("3️⃣ Crop Analytics")

health_scores = analytics.calculate_health_scores(sensor_data)
risk_ranking = analytics.rank_fields_by_risk(health_scores)

st.subheader("Field Health Scores")
st.dataframe(
    pd.DataFrame(health_scores.items(), columns=["Field", "Health Score"]),
    use_container_width=True
)

st.subheader("Field Risk Ranking")
st.dataframe(pd.DataFrame(risk_ranking), use_container_width=True)


st.header("4️⃣ Resource Allocation")

water_inv = st.number_input("Available Water (liters)", 0, 2000, 500)
fert_inv = st.number_input("Available Fertilizer (kg)", 0, 1000, 300)
pest_inv = st.number_input("Available Pesticide (liters)", 0, 500, 150)

if st.button("Allocate Resources"):
    allocation_result = allocator.allocate_resources(
        water_inv, fert_inv, pest_inv
    )

    st.subheader("Resource Allocation Results")
    st.dataframe(
        pd.DataFrame.from_dict(
            allocation_result["Allocations"], orient="index"
        ),
        use_container_width=True
    )

    if allocation_result["Alerts"]:
        st.subheader("⚠️ Resource Alerts")
        for alert in allocation_result["Alerts"]:
            st.error(alert)
    else:
        st.success("No resource issues detected.")


st.header("5️⃣ Weather & Yield Prediction")

predicted_yield, yield_status = weather.predict_yield(health_scores)
adjustments = weather.generate_adjustments(predicted_yield, health_scores)

st.dataframe(
    pd.DataFrame({
        "Field": list(predicted_yield.keys()),
        "Expected Yield (tons)": list(predicted_yield.values()),
        "Status": list(yield_status.values())
    }),
    use_container_width=True
)

st.subheader("Adjustment Recommendations")
st.dataframe(
    pd.DataFrame(adjustments.items(), columns=["Field", "Action"]),
    use_container_width=True
)


st.header("6️⃣ Enhanced Decision Support")

resource_usage = {
    field: allocator.crop_requirements[field]["water"]
    for field in allocator.crop_requirements
}

weather_risk = {
    field: "high" if temperature < 10 or temperature > 35 else "medium"
    for field in resource_usage
}

recommendations = enhanced.generate_recommendations(
    health_scores,
    weather_risk,
    resource_usage
)

st.dataframe(pd.DataFrame(recommendations), use_container_width=True)


if sensor_data:
    st.header("7️⃣ Field Input Visualization")

    selected_field = st.selectbox(
        "Select field",
        [f["Field"] for f in sensor_data]
    )

    field = next(f for f in sensor_data if f["Field"] == selected_field)

    fig, ax = plt.subplots()
    ax.bar(
        ["Moisture", "Temperature", "Humidity", "Nutrients"],
        [
            field["Soil Moisture"],
            field["Temperature"],
            field["Humidity"],
            field["Nutrients"]
        ]
    )
    ax.set_title(f"Inputs for Field: {selected_field}")
    st.pyplot(fig)






















