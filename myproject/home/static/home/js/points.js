document.addEventListener("DOMContentLoaded", loadPoints);

async function loadPoints() {
    const pointsDisplay = document.getElementById("user-points");
    const pointsValue = document.getElementById("points-value");

    if (!pointsDisplay || !pointsValue) {
        return;
    }

    try {
        const response = await fetch("/api/points/", {
            credentials: "same-origin"
        });

        if (!response.ok || !response.headers.get("content-type")?.includes("application/json")) {
            return;
        }

        const data = await response.json();
        if (Number.isInteger(data.points) && data.points >= 0) {
            pointsValue.innerText = data.points;
        }
    } catch (error) {
        console.error("Cannot load points:", error);
    }
}
