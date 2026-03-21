function checkFatigue() {

    const resultElement = document.getElementById("result");
    const scoreElement = document.getElementById("score");
    const bar = document.getElementById("bar");

    // Loading UI
    resultElement.innerHTML = "🔄 Checking fatigue...";
    resultElement.style.color = "black";

    if (scoreElement) scoreElement.innerHTML = "";
    if (bar) bar.style.width = "0%";

    fetch("http://127.0.0.1:5000/check-fatigue")

        .then(response => {
            if (!response.ok) {
                throw new Error("Server error");
            }
            return response.json();
        })

        .then(data => {

            console.log("API Response:", data);

            const status = data["Fatigue Status"];
            const score = data["Fatigue Score (%)"];

            // 🎯 RESULT HANDLING
            if (status === "Fatigued") {

                resultElement.innerHTML =
                    "⚠️ Fatigue Detected! Please take some rest.";
                resultElement.style.color = "red";

                // 🔔 Alert
                alert("⚠️ You are fatigued! Take a break!");

                // 🔊 Sound alert
                const audio = new Audio("https://www.soundjay.com/buttons/beep-01a.mp3");
                audio.play();

            } else if (status === "Normal") {

                resultElement.innerHTML =
                    "✅ You look Normal and Active.";
                resultElement.style.color = "green";

            } else {

                resultElement.innerHTML = "⚠️ Unknown result received.";
                resultElement.style.color = "orange";
            }

            // 📊 SCORE DISPLAY
            if (score !== undefined && scoreElement) {

                scoreElement.innerHTML = "Fatigue Score: " + score + "%";
                scoreElement.style.color = "#333";

                // 🔥 Animate progress bar
                if (bar) {
                    setTimeout(() => {
                        bar.style.width = score + "%";
                    }, 200);
                }
            }

        })

        .catch(error => {

            resultElement.innerHTML =
                "❌ Cannot connect to AI server";
            resultElement.style.color = "orange";

            console.error("Error:", error);

        });
}