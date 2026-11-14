import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

#  Define variables
temperature = ctrl.Antecedent(np.arange(16, 46, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(20, 101, 1), 'humidity')
fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')

# Temperature membership functions
temperature['low'] = fuzz.trapmf(temperature.universe, [16, 16, 20, 26])
temperature['medium'] = fuzz.trimf(temperature.universe, [22, 30, 36])
temperature['high'] = fuzz.trapmf(temperature.universe, [32, 38, 45, 45])

# Humidity membership functions
humidity['low'] = fuzz.trapmf(humidity.universe, [20, 20, 35, 50])
humidity['medium'] = fuzz.trimf(humidity.universe, [40, 60, 80])
humidity['high'] = fuzz.trapmf(humidity.universe, [70, 85, 100, 100])

# Fan speed membership functions
fan_speed['slow'] = fuzz.trapmf(fan_speed.universe, [0, 0, 20, 40])
fan_speed['moderate'] = fuzz.trimf(fan_speed.universe, [25, 50, 75])
fan_speed['fast'] = fuzz.trapmf(fan_speed.universe, [60, 80, 100, 100])

# Plot membership functions
def plot_membership_functions():

    variables = [temperature, humidity, fan_speed]

    fig, axes = plt.subplots(3, 1, figsize=(9, 10))

    for ax, var in zip(axes, variables):
        for term in var.terms:
            ax.plot(var.universe, var[term].mf, label=term)

        ax.set_title(var.label.capitalize())
        ax.set_xlabel(var.label)
        ax.set_ylabel("Membership Degree")
        ax.legend()
        ax.grid()

    plt.tight_layout()
    plt.savefig("membership_functions.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    plot_membership_functions()