let image1 = "", image2 = "";

navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    document.getElementById("cam1").srcObject = stream;
    document.getElementById("cam2").srcObject = stream;
});

function capture(player) {
    const video = document.getElementById(`cam${player}`);
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);
    const dataURL = canvas.toDataURL("image/jpeg");

    if (player === 1) image1 = dataURL;
    else image2 = dataURL;

    alert(`Captured Player ${player}`);
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
    });
}
