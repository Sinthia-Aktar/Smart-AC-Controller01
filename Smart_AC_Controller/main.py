
import csv

from Membership_functions import plot_membership_functions

from fuzzy_controller import (
    calculate_fan_speed,
    get_fan_category,
    plot_control_surface
)


#User Input

print("\nSMART AC CONTROLLER")
print("---------------------------")

try:

    temp = float(input("Enter Room Temperature (16-45°C): "))
    humid = float(input("Enter Humidity (20-100%): "))

    # Validate Temperature

    if not 16 <= temp <= 45:
        raise ValueError("Temperature must be between 16 and 45.")

    # Validate Humidity

    if not 20 <= humid <= 100:
        raise ValueError("Humidity must be between 20 and 100.")

 # Fuzzy Calculation

    result = calculate_fan_speed(temp, humid)

    category = get_fan_category(result)

# Display Result

    print("\n----- AC CONTROLLER RESULT -----")

    print("Temperature:", temp, "°C")
    print("Humidity:", humid, "%")
    print("Fan Speed:", round(result, 2), "%")
    print("Fan Category:", category)

# Test Cases

    test_cases = [
        (18, 25),
        (22, 40),
        (25, 55),
        (28, 45),
        (30, 60),
        (32, 75),
        (35, 40),
        (40, 65),
        (44, 95)
    ]

    results = []

    print("\n----- TEST CASE RESULTS -----")

    for t, h in test_cases:

        speed = calculate_fan_speed(t, h)

        fan = get_fan_category(speed)

        results.append([
            t,
            h,
            round(speed, 2),
            fan
        ])

        print(
            f"Temperature: {t}°C | "
            f"Humidity: {h}% | "
            f"Fan Speed: {speed:.2f}% | "
            f"Category: {fan}"
        )

# Save Results to CSV

    with open("test_results.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Temperature",
            "Humidity",
            "Fan Speed",
            "Fan Category"
        ])

        writer.writerows(results)

    print("\nTest results saved successfully!")

# Generate Graphs

    print("\nGenerating Membership Function Graph...")

    plot_membership_functions()

    print("\nGenerating Control Surface Graph...")

    plot_control_surface()

    print("\nPROJECT EXECUTION COMPLETED!")


except ValueError as error:

    print("\nInput Error:", error)


except Exception as error:

    print("\nAn error occurred:", error)
