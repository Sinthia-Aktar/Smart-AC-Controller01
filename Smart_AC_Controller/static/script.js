
async function autoControl() {

    const temperature = document.getElementById("temperature").value;
    const humidity = document.getElementById("humidity").value;
    const target = document.getElementById("target").value;

    try {
        const response = await fetch("/api/control", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                temperature: temperature,
                humidity: humidity,
                target: target
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error);
            return;
        }

        document.getElementById("fanSpeed").innerText =
            data.fan_speed + "%";

        document.getElementById("fanMode").innerText =
            data.category;

        document.getElementById("cooling").innerText =
            data.cooling;

        document.getElementById("comfort").innerText =
            data.comfort;

        document.getElementById("roomTemp").innerText =
            data.temperature + " °C";

        document.getElementById("roomHumidity").innerText =
            data.humidity + " %";

        document.getElementById("targetTemp").innerText =
            data.target + " °C";

        document.getElementById("progress").style.width =
            data.fan_speed + "%";

    } catch (error) {
        alert("Backend connection failed! Check Flask server.");
        console.error(error);
    }
}
