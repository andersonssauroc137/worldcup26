let score = 0;

const scoreElement = document.getElementById("score");
const addButton = document.getElementById("btn");
const gameOverButton = document.getElementById("game-over-btn");

addButton.addEventListener("click", () => {
    score += 100;
    scoreElement.innerHTML = `Score: ${score}`;
});

gameOverButton.addEventListener("click", () => {
    window.parent.postMessage({
        type: "WCG_GAME_OVER",
        gameSlug: "maple-rush",
        score: score
    }, "*");
});