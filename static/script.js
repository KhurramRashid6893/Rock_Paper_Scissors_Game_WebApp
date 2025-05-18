let image = "";
let playerScore = 0;
let computerScore = 0;
let playerName = "";
let gameActive = false;

// Setup camera only when game starts
let streamInitialized = false;

function startGame() {
    const name = document.getElementById("playerName").value.trim();
    if (!name) {
        alert("Please enter your name!");
        return;
    }

    playerName = name;
    playerScore = 0;
    computerScore = 0;
    gameActive = true;

    document.getElementById("nameLabel").innerText = playerName;
    document.querySelector(".input-group").style.display = "none";
    document.getElementById("gameArea").style.display = "block";
    document.getElementById("playerScore").innerText = "0";
    document.getElementById("computerScore").innerText = "0";
    document.getElementById("result").innerText = "🎯 First to 5 wins!";

    if (!streamInitialized) {
        navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
            document.getElementById("cam").srcObject = stream;
            streamInitialized = true;
        });
    }

    // Begin first countdown
    startCountdown();
}

function startCountdown() {
    if (!gameActive) return;

    const countdownEl = document.getElementById("countdown");
    let counter = 3;
    countdownEl.innerText = counter;

    const interval = setInterval(() => {
        counter--;
        if (counter > 0) {
            countdownEl.innerText = counter;
        } else {
            clearInterval(interval);
            countdownEl.innerText = "✊✋✌️";
            captureAndSend();
        }
    }, 1000);
}

function captureAndSend() {
    const video = document.getElementById("cam");
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);
    image = canvas.toDataURL("image/jpeg");

    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player: image })
    })
    .then(res => res.json())
    .then(data => {
        const playerGesture = data.player;
        const computerGesture = data.computer;
        const winner = data.winner;

        document.getElementById("playerGestureImg").src = `/static/assets/${playerGesture.toLowerCase()}.png`;
        document.getElementById("computerGestureImg").src = `/static/assets/${computerGesture.toLowerCase()}.png`;

        // Show result with name
        let message = `${playerName}: ${playerGesture}, Computer: ${computerGesture}.`;
        if (winner === "Player") {
            playerScore++;
            message += ` ${playerName} wins this round!`;
        } else if (winner === "Computer") {
            computerScore++;
            message += ` Computer wins this round!`;
        } else {
            message += ` It's a draw!`;
        }

        document.getElementById("result").innerText = message;

        // Update scoreboard
        document.getElementById("playerScore").innerText = playerScore;
        document.getElementById("computerScore").innerText = computerScore;

        // Check if someone reached 5 points
        if (playerScore === 5 || computerScore === 5) {
            gameActive = false;
            const finalWinner = playerScore === 5 ? playerName : "Computer";
            document.getElementById("result").innerText = `🏆 ${finalWinner} wins the game with 5 points!`;
        } else {
            // Start next round after 2s
            setTimeout(startCountdown, 2000);
        }
    });
}
