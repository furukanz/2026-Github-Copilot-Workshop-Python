let workSeconds = 25 * 60;
let breakSeconds = 5 * 60;
let state = 'work';
let remaining = workSeconds;
let timerInterval = null;

function updateDisplay() {
    const minutes = Math.floor(remaining / 60);
    const seconds = remaining % 60;
    document.getElementById('minutes').textContent = String(minutes).padStart(2, '0');
    document.getElementById('seconds').textContent = String(seconds).padStart(2, '0');
    document.getElementById('state').textContent = state === 'work' ? '作業中' : '休憩中';
}

function tick() {
    if (remaining > 0) {
        remaining--;
        updateDisplay();
    } else {
        clearInterval(timerInterval);
        if (state === 'work') {
            state = 'break';
            remaining = breakSeconds;
            alert('作業終了！休憩しましょう');
        } else {
            state = 'work';
            remaining = workSeconds;
            alert('休憩終了！作業を再開しましょう');
        }
        updateDisplay();
    }
}

document.getElementById('start').addEventListener('click', function() {
    if (!timerInterval) {
        timerInterval = setInterval(tick, 1000);
    }
});

document.getElementById('reset').addEventListener('click', function() {
    clearInterval(timerInterval);
    timerInterval = null;
    state = 'work';
    remaining = workSeconds;
    updateDisplay();
});

updateDisplay();
