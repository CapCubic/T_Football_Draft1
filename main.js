let authToken = "";

function authenticateUser() {
    fetch("/login", { method: "POST" })
    .then(response => response.json())
    .then(data => {
        authToken = data.token;
        fetchPlayers();
    })
    .catch(error => console.error("Login failed:", error));
}

function fetchPlayers() {
    fetch("/players", {
        headers: { "Authorization": `Bearer ${authToken}` }
    })
    .then(response => response.json())
    .then(players => {
        const table = document.getElementById("playerTable");
        players.forEach(player => {
            let row = table.insertRow();
            row.insertCell(0).textContent = player.name;
            row.insertCell(1).textContent = player.position;
            row.insertCell(2).textContent = player.goals_scored;
        });
    })
    .catch(error => console.error("Error fetching player data:", error));
}
