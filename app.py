from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# Equipment data with additional appliances
equipment_data = {
    "Refrigerator": {"power": 150, "usage_hours": 24},
    "Air Conditioner": {"power": 2000, "usage_hours": 8},
    "Washing Machine": {"power": 500, "usage_hours": 1},
    "Lighting": {"power": 10, "usage_hours": 5},
    "TV": {"power": 120, "usage_hours": 4},
    "Microwave": {"power": 800, "usage_hours": 0.5},
    "Fan": {"power": 75, "usage_hours": 12},
    "Computer": {"power": 300, "usage_hours": 6},
    # Additional appliances
    "Heater": {"power": 1500, "usage_hours": 3},
    "Dishwasher": {"power": 1200, "usage_hours": 1.5},
    "Water Heater": {"power": 3000, "usage_hours": 2},
    "Rice Cooker": {"power": 600, "usage_hours": 1},
    "Vacuum Cleaner": {"power": 800, "usage_hours": 1},
    "Juicer": {"power": 300, "usage_hours": 0.5},
    "Grinder": {"power": 500, "usage_hours": 0.75},
    "Oven": {"power": 1200, "usage_hours": 2},
    "Toaster": {"power": 800, "usage_hours": 0.5},
    "Blender": {"power": 300, "usage_hours": 0.5},
}

# Solar irradiance data by city (in kWh/m²/day) - Sample data
location_irradiance = {
    "mumbai": 4.5,     # kWh/m²/day
    "delhi": 5.5,
    "bangalore": 5.0,
    "hyderabad": 5.2,
    "kolkata": 4.5,
    "chennai": 5.0,
    "pune": 5.1,
    "bhopal": 4.9,
    "indore": 5.0,
    "tokyo": 4.0,
    "osaka": 4.2,
    "kyoto": 4.1,
    "seoul": 3.8,
    "jakarta": 4.5,
    "bangkok": 5.0,
    "singapore": 4.5,
    "manila": 5.2,
    "ho chi minh city": 5.0,
    "hanoi": 4.8,
    "dubai": 5.8,
    "abu dhabi": 5.7,
    "riyadh": 6.0,
    "karachi": 5.3,
    "lahore": 5.1,
    "dhaka": 4.7,
    "kathmandu": 5.0,
    "new york city": 4.5,
    "los angeles": 5.5,
    "chicago": 4.2,
    "houston": 5.2,
    "phoenix": 6.0,
    "san francisco": 4.6,
    "miami": 5.0,
    "toronto": 4.0,
    "vancouver": 3.5,
    "montreal": 3.8,
    "mexico city": 5.3,
    "guadalajara": 5.4,
    "cancun": 5.6,
    "ottawa": 3.5,
    "calgary": 4.0,
    "london": 3.7,
    "paris": 3.9,
    "berlin": 4.0,
    "madrid": 5.3,
    "rome": 5.2,
    "barcelona": 5.4,
    "milan": 4.9,
    "amsterdam": 3.5,
    "brussels": 3.6,
    "zurich": 3.9,
    "vienna": 4.1,
    "athens": 5.5,
    "lisbon": 5.6,
    "warsaw": 3.9,
    "prague": 4.0,
    "budapest": 4.2,
    "stockholm": 3.4,
    "oslo": 3.2,
    "copenhagen": 3.6,
    "moscow": 3.5,
    "st. petersburg": 3.3,
    "sao paulo": 5.1,
    "rio de janeiro": 5.3,
    "buenos aires": 5.2,
    "lima": 5.0,
    "santiago": 5.6,
    "bogotá": 4.6,
    "quito": 5.0,
    "caracas": 5.2,
    "montevideo": 5.1,
    "la paz": 5.3,
    "cairo": 6.0,
    "lagos": 5.4,
    "nairobi": 5.1,
    "addis ababa": 5.0,
    "cape town": 5.2,
    "johannesburg": 5.1,
    "accra": 5.3,
    "dakar": 5.2,
    "casablanca": 5.5,
    "tunis": 5.4,
    "sydney": 5.0,
    "melbourne": 4.8,
    "brisbane": 5.3,
    "auckland": 4.2,
    "wellington": 4.0,
    "christchurch": 4.1
}


def calculate_solar_capacity(appliances, city):
    """
    Calculates the required solar panel capacity for a list of appliances in a given city.

    Parameters:
        appliances (list of dicts): List where each dict has 'name' (appliance), 'quantity', 'power', 'usage_hours'.
        city (str): City name to use the appropriate solar irradiance value.

    Returns:
        float: Required solar panel capacity in kW.
    """
    # Normalize city name to lowercase to handle case-insensitivity
    city = city.lower()

    # Validate city
    if city not in location_irradiance:
        raise ValueError(
            f"City '{city}' is not available. Choose from: {', '.join(location_irradiance.keys())}")

    # Get the solar irradiance for the specified city
    irradiance = location_irradiance[city]

    # Calculate total daily energy requirement in kWh
    total_energy_kwh = 0
    for appliance in appliances:
        name = appliance["appliance"]
        quantity = appliance["quantity"]

        # Retrieve power and usage hours from default data if not provided
        power = appliance.get("power", equipment_data.get(name, {}).get("power"))
        usage_hours = appliance.get("usageHours", equipment_data.get(name, {}).get("usage_hours"))

        if power is None or usage_hours is None:
            raise ValueError(f"Details for appliance '{name}' are missing or not found.")

        # Calculate energy for this appliance and add to total
        daily_energy = (power * usage_hours * quantity) / 1000  # Convert W-hours to kWh
        total_energy_kwh += daily_energy

    # Calculate required solar capacity (kW) based on irradiance
    required_solar_kw = total_energy_kwh / irradiance
    return round(required_solar_kw, 2)


@app.route('/calculate-solar', methods=['POST'])
def calculate_solar():
    try:
        data = request.json  # Parse JSON from request body
        city = str(data.get('city'))
        appliances = data.get('appliances', [])

        solar_requirement_kw = calculate_solar_capacity(city=city, appliances=appliances)

        return jsonify({
            'city': city,
            'solar_requirement': solar_requirement_kw
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/')
def solarbill():
    # Pass the list of cities to the template
    return render_template('solarbill.html', equipment_data=equipment_data, cities=list(location_irradiance.keys()))


if __name__ == '__main__':
    app.run(debug=False)

