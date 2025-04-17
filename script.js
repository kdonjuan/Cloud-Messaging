const API_BASE_URL = "http://localhost:5001"; // Update if deployed elsewhere

// Function to publish a message (if needed)
function publishMessage() {
    const message = document.getElementById("messageInput").value;
    if (!message.trim()) {
        alert("Message cannot be empty!");
        return;
    }

    fetch(`${API_BASE_URL}/publish`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    })
    .then(response => response.json())
    .then(data => {
        alert("Message sent!");
        document.getElementById("messageInput").value = "";
        fetchMessages(); // Refresh message list
    })
    .catch(error => console.error("Error publishing message:", error));
}

// Function to fetch messages
function fetchMessages() {
    fetch(`${API_BASE_URL}/messages`)
        .then(response => response.json())
        .then(messages => displayMessages(messages))
        .catch(error => console.error("Error fetching messages:", error));
}

// Function to display messages in the table
function displayMessages(messages) {
    const tableBody = document.getElementById("messagesTable");
    tableBody.innerHTML = "";

    messages.forEach(msg => {
        const row = document.createElement("tr");
        if (msg.isDuplicate) {
            row.classList.add("highlight");
        }

        row.innerHTML = `
            <td>${msg.ItemID}</td>
            <td>${msg.Location}</td>
            <td>${msg.Quantity}</td>
            <td>${msg.TransactionDateTime}</td>
            <td>${msg.message_id}</td>
        `;

        tableBody.appendChild(row);
    });
}

// Function to filter messages by Item ID
function filterMessages() {
    const filter = document.getElementById("filterInput").value.toLowerCase();
    const rows = document.getElementById("messagesTable").rows;

    for (let row of rows) {
        const itemID = row.cells[0].innerText.toLowerCase();
        row.style.display = itemID.includes(filter) ? "" : "none";
    }
}

// Fetch messages on page load
window.onload = fetchMessages;
