import numpy as np
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

from Membership_functions import (
    temperature,
    humidity,
    fan_speed
)

# Define Fuzzy Rules

rule1 = ctrl.Rule(temperature['low'] & humidity['low'], fan_speed['slow'])
rule2 = ctrl.Rule(temperature['low'] & humidity['medium'], fan_speed['slow'])
rule3 = ctrl.Rule(temperature['low'] & humidity['high'], fan_speed['moderate'])

rule4 = ctrl.Rule(temperature['medium'] & humidity['low'], fan_speed['moderate'])
rule5 = ctrl.Rule(temperature['medium'] & humidity['medium'], fan_speed['moderate'])
rule6 = ctrl.Rule(temperature['medium'] & humidity['high'], fan_speed['fast'])

rule7 = ctrl.Rule(temperature['high'] & humidity['low'], fan_speed['fast'])
rule8 = ctrl.Rule(temperature['high'] & humidity['medium'], fan_speed['fast'])
rule9 = ctrl.Rule(temperature['high'] & humidity['high'], fan_speed['fast'])

rules = [
    rule1, rule2, rule3,
    rule4, rule5, rule6,
    rule7, rule8, rule9
]

# Create Fuzzy Control System

control_system = ctrl.ControlSystem(rules)

simulation = ctrl.ControlSystemSimulation(
    control_system,
    cache=False
)

#  Calculate Fan Speed

def calculate_fan_speed(temp, humid):

    simulation.input['temperature'] = temp
    simulation.input['humidity'] = humid

    simulation.compute()

    return simulation.output['fan_speed']


# Classify Fan Speed

def get_fan_category(speed):

    if speed < 35:
        return "Slow"

    elif speed < 70:
        return "Moderate"

    else:
        return "Fast"


# Generate 3D Control Surface

def plot_control_surface():

    temp_values = np.arange(16, 46, 1)
    humidity_values = np.arange(20, 101, 2)

    X, Y = np.meshgrid(temp_values, humidity_values)
    Z = np.zeros(X.shape)

    for i in range(len(humidity_values)):
        for j in range(len(temp_values)):

            Z[i, j] = calculate_fan_speed(
                X[i, j],
                Y[i, j]
            )

    fig = plt.figure(figsize=(11, 8))

    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(X, Y, Z, cmap='viridis')

    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('Humidity (%)')
    ax.set_zlabel('Fan Speed (%)')

    ax.set_title('Fuzzy Logic Smart AC Control Surface')

    plt.savefig("control_surface.png", dpi=300)
    plt.show()