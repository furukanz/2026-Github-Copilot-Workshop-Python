let workSeconds = 25 * 60;
let breakSeconds = 5 * 60;
let state = 'work';
let remaining = workSeconds;
let timerInterval = null;

const progressEl = document.getElementById('progress');
const minutesEl = document.getElementById('minutes');
const secondsEl = document.getElementById('seconds');
const statusEl = document.querySelector('.status');

const radius = progressEl.r.baseVal.value;
const circumference = 2 * Math.PI * radius;
progressEl.style.strokeDasharray = `${circumference} ${circumference}`;
progressEl.style.strokeDashoffset = circumference;

function setProgress(remainingSec, totalSec){
    const offset = circumference * (remainingSec / totalSec);
    progressEl.style.strokeDashoffset = offset;
}

function updateDisplay(){
    const minutes = Math.floor(remaining / 60);
    const seconds = remaining % 60;
    minutesEl.textContent = String(minutes).padStart(2,'0');
    secondsEl.textContent = String(seconds).padStart(2,'0');
    statusEl.textContent = state === 'work' ? '作業中' : '休憩中';
    const total = state === 'work' ? workSeconds : breakSeconds;
    setProgress(remaining, total);
}

function tick(){
    if (remaining > 0){
        remaining--;
        updateDisplay();
    } else {
        clearInterval(timerInterval);
        timerInterval = null;
        if (state === 'work'){
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

document.getElementById('start').addEventListener('click', function(){
    if (!timerInterval){
        timerInterval = setInterval(tick, 1000);
    }
});

document.getElementById('reset').addEventListener('click', function(){
    clearInterval(timerInterval);
    timerInterval = null;
    state = 'work';
    remaining = workSeconds;
    updateDisplay();
});

updateDisplay();
