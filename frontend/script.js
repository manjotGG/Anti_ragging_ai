
const API = "http://127.0.0.1:8000";

async function submitComplaint() {
    const description = document.getElementById("description").value;

    const res = await fetch(`${API}/report`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ description })
    });

    const data = await res.json();

    document.getElementById("response").innerText =
        "Tracking ID: " + data.tracking_id +
        "\nSeverity: " + data.severity;
}

async function checkStatus() {
    const id = document.getElementById("trackId").value;

    const res = await fetch(`${API}/status/${id}`);
    const data = await res.json();

    document.getElementById("statusResult").innerText =
        "Status: " + data.status;
}