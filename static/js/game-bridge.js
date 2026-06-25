let currentScore = 0;
let bestScore = 0;

const playerStorageKey = "wcg_player";

const currentScoreEl = document.getElementById("current-score");
const scoreResultEl = document.getElementById("score-result");
const shareScoreBtn = document.getElementById("share-score-btn");

function getStoredPlayer() {
    const player = localStorage.getItem(playerStorageKey);

    if (!player) {
        return null;
    }

    try {
        return JSON.parse(player);
    } catch {
        return null;
    }
}

function savePlayer(player) {
    localStorage.setItem(playerStorageKey, JSON.stringify(player));
}

async function registerPlayer() {
    let player = getStoredPlayer();

    if (player && player.id && player.nickname) {
        return player;
    }

    let nickname = prompt("Digite seu nickname para entrar no ranking:");

    if (!nickname || !nickname.trim()) {
        nickname = "Player";
    }

    nickname = nickname.trim().slice(0, 40);

    const response = await fetch("/api/player/register/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            nickname: nickname,
        }),
    });

    const data = await response.json();

    if (!data.success) {
        throw new Error(data.error || "Erro ao registrar jogador.");
    }

    player = {
        id: data.player_id,
        nickname: data.nickname,
    };

    savePlayer(player);

    return player;
}

function updateScoreView(score) {
    currentScore = score;
    currentScoreEl.textContent = currentScore;
}

async function submitScore(score) {
    const player = await registerPlayer();

    const response = await fetch("/api/score/submit/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            player_id: player.id,
            game_slug: window.WCG_GAME_SLUG,
            score: score,
        }),
    });

    const data = await response.json();

    if (!data.success) {
        throw new Error(data.error || "Erro ao enviar pontuação.");
    }

    bestScore = data.best_score;

    if (data.is_new_record) {
        scoreResultEl.innerHTML = `
            <strong>Novo recorde!</strong><br>
            ${player.nickname}, sua melhor pontuação agora é ${data.best_score}.
        `;
    } else {
        scoreResultEl.innerHTML = `
            Pontuação enviada.<br>
            Seu recorde continua ${data.best_score}.
        `;
    }

    shareScoreBtn.style.display = "inline-block";
}

window.addEventListener("message", async function(event) {
    if (!event.data || event.data.type !== "WCG_GAME_OVER") {
        return;
    }

    const score = Number(event.data.score || 0);

    updateScoreView(score);

    scoreResultEl.innerHTML = "Enviando pontuação...";

    try {
        await submitScore(score);
    } catch (error) {
        scoreResultEl.innerHTML = `<strong>Erro:</strong> ${error.message}`;
    }
});

shareScoreBtn.addEventListener("click", async () => {
    const url = `${window.location.origin}${window.location.pathname}?challenge=${bestScore}`;

    const text = `Eu fiz ${bestScore} pontos em ${window.WCG_GAME_TITLE} no World Cup Games 2026. Consegue bater?`;

    if (navigator.share) {
        await navigator.share({
            title: "World Cup Games 2026",
            text: text,
            url: url,
        });
    } else {
        await navigator.clipboard.writeText(`${text} ${url}`);
        alert("Link do desafio copiado!");
    }
});

function checkChallenge() {
    const params = new URLSearchParams(window.location.search);
    const challengeScore = params.get("challenge");

    if (challengeScore) {
        scoreResultEl.innerHTML = `
            <strong>Desafio recebido!</strong><br>
            Bata ${challengeScore} pontos neste game.
        `;
    }
}

checkChallenge();