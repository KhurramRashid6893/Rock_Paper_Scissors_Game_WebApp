let image1 = "", image2 = "";

navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    document.getElementById("cam").srcObject = stream;
});

function capture(player) {
    const video = document.getElementById("cam");
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);
    const dataURL = canvas.toDataURL("image/jpeg");

    if (player === 1) {
        image1 = dataURL;
        alert("Player 1 captured!");
    } else {
        image2 = dataURL;
        alert("Player 2 captured!");
    }

    if (image1 && image2) {
        document.getElementById("play").disabled = false;
    }
}

function submitImages() {
    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player1: image1, player2: image2 })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText =
            `Player 1: ${data.player1}, Player 2: ${data.player2}, Winner: ${data.winner}`;
        image1 = "";
        image2 = "";
        document.getElementById("play").disabled = true;
    });
}
