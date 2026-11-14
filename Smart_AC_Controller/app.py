
from flask import Flask, request, jsonify, render_template
from fuzzy_controller import calculate_fan_speed, get_fan_category
from datetime import datetime
import csv
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/control", methods=["POST"])
def auto_control():
    try:
        data = request.get_json()

        temp = float(data["temperature"])
        humidity = float(data["humidity"])
        target = float(data["target"])

        if not 16 <= temp <= 45:
            return jsonify({"error": "Temperature must be 16-45°C"}), 400

        if not 20 <= humidity <= 100:
            return jsonify({"error": "Humidity must be 20-100%"}), 400

        if not 16 <= target <= 30:
            return jsonify({"error": "Target must be 16-30°C"}), 400

        # Fuzzy Logic Calculation
        speed = calculate_fan_speed(temp, humidity)
        category = get_fan_category(speed)
 
# Cooling Status
        if temp <= target:
            cooling = "Target temperature reached"
            comfort = "Comfortable"
        elif temp > target + 2:
            cooling = "Strong cooling required"
            comfort = "Room is too warm"
        else:
            cooling = "Normal cooling"
            comfort = "Slightly warmer than target"

# Save History
        file_exists = os.path.exists("ac_history.csv")

        with open("ac_history.csv", "a", newline="") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    "Time", "Temperature", "Humidity",
                    "Target", "Fan Speed", "Mode"
                ])

            writer.writerow([
                datetime.now().strftime("%H:%M:%S"),
                temp, humidity, target, round(speed, 2), category
            ])

        return jsonify({
            "temperature": temp,
            "humidity": humidity,
            "target": target,
            "fan_speed": round(speed, 2),
            "category": category,
            "cooling": cooling,
            "comfort": comfort
        })

    except (ValueError, TypeError, KeyError):
        return jsonify({"error": "Invalid input data"}), 400

    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(debug=True)
