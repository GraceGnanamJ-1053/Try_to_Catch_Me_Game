from flask import Flask, render_template_string

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Python Game | Try to Catch Me!</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', sans-serif;
            transition: background-color 0.3s ease;
        }
        header {
            background-color: #222;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .lights {
            display: flex;
            justify-content: space-between;
            padding: 0 40px;
            margin: 10px 0;
        }
        .light {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: yellow;
            box-shadow: 0 0 10px yellow;
            animation: blink 1s infinite alternate;
        }
        @keyframes blink {
            0% { opacity: 0.3; }
            100% { opacity: 1; }
        }
        #container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 30px;
        }
        #status-bar {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            margin-top: 15px;
            flex-wrap: wrap;
        }
        .status-box {
            font-size: 1.2em;
            padding: 10px 20px;
            background-color: #eee;
            border-radius: 8px;
            font-weight: bold;
            transition: color 0.3s ease;
        }
        .game-btn {
            padding: 8px 16px;
            font-size: 1em;
            border: none;
            border-radius: 6px;
            background-color: #444;
            color: white;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .game-btn:hover {
            background-color: #666;
        }
        #game-area {
            position: relative;
            width: 80vw;
            height: 60vh;
            border: 2px solid #ccc;
            border-radius: 10px;
            background: repeating-linear-gradient(
                45deg,
                #ffffff,
                #ffffff 10px,
                #f0f0f0 10px,
                #f0f0f0 20px
            );
            overflow: hidden;
            margin-top: 20px;
        }
        #game-box {
            width: 50px;
            height: 50px;
            background-color: red;
            position: absolute;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
    </style>
</head>
<body>
    <header>
        <div class="lights">
            <div class="light"></div><div class="light"></div><div class="light"></div>
            <div class="light"></div><div class="light"></div><div class="light"></div>
            <div class="light"></div><div class="light"></div><div class="light"></div>
            <div class="light"></div><div class="light"></div><div class="light"></div>
        </div>
        <h1>Try to Catch Me!</h1>
        <h3>A Python game by Grace Gnanam J</h3>
        <div class="lights">
            <div class="light"></div><div class="light"></div><div class="light"></div>
            <div class="light"></div><div class="light"></div><div class="light"></div>
            <div class="light"></div><div class="light"></div><div class="light"></div>
            <div class="light"></div><div class="light"></div><div class="light"></div>
        </div>
    </header>
    <div id="container">
        <div id="status-bar">
            <div id="score-display" class="status-box">Score: <span id="score">0</span></div>
            <div id="timer-display" class="status-box">Time: <span id="timer">0</span> sec</div>
            <button id="start-btn" class="game-btn">Start Game</button>
            <button id="stop-btn" class="game-btn">Stop Game</button>
            <button id="reset-btn" class="game-btn">Reset Game</button>
        </div>
        <div id="game-area">
            <div id="game-box" style="display: none;"></div>
        </div>
    </div>

    <script>
        let score = 0;
        let time = 0;
        let timerInterval;
        let gameRunning = false;

        const box = document.getElementById("game-box");
        const scoreDisplay = document.getElementById("score");
        const scoreContainer = document.getElementById("score-display");
        const timerDisplay = document.getElementById("timer");
        const startBtn = document.getElementById("start-btn");
        const stopBtn = document.getElementById("stop-btn");
        const resetBtn = document.getElementById("reset-btn");
        const gameArea = document.getElementById("game-area");

        function getRandomColor() {
            const r = Math.floor(Math.random() * 200);
            const g = Math.floor(Math.random() * 200);
            const b = Math.floor(Math.random() * 200);
            return `rgb(${r}, ${g}, ${b})`;
        }

        function moveBox() {
            const areaWidth = gameArea.clientWidth;
            const areaHeight = gameArea.clientHeight;
            const boxSize = 50;
            const margin = 20;

            const x = Math.random() * (areaWidth - boxSize - margin * 2) + margin;
            const y = Math.random() * (areaHeight - boxSize - margin * 2) + margin;

            box.style.left = x + "px";
            box.style.top = y + "px";
        }

        function startTimer() {
            timerInterval = setInterval(() => {
                time++;
                timerDisplay.textContent = time;
            }, 1000);
        }

        function stopGame() {
            clearInterval(timerInterval);
            gameRunning = false;
            box.style.display = "none";
        }

        function resetGame() {
            stopGame();
            score = 0;
            time = 0;
            scoreDisplay.textContent = score;
            timerDisplay.textContent = time;
            scoreContainer.style.color = "#000";
            document.body.style.backgroundColor = "#fff";
        }

        function startGame() {
            resetGame();
            gameRunning = true;
            box.style.display = "block";
            moveBox();
            startTimer();
        }

        box.addEventListener("click", () => {
            if (!gameRunning) return;
            score++;
            scoreDisplay.textContent = score;
            box.style.backgroundColor = getRandomColor();
            document.body.style.backgroundColor = getRandomColor();
            scoreContainer.style.color = getRandomColor();
            moveBox();
        });

        startBtn.addEventListener("click", () => {
            if (!gameRunning) startGame();
        });

        stopBtn.addEventListener("click", () => {
            if (gameRunning) stopGame();
        });

        resetBtn.addEventListener("click", () => {
            startGame();
        });
    </script>
</body>
</html>
"""

@app.route("/")
def game():
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
